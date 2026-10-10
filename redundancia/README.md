# Servidor reserva

Se o VPS da Hostinger cair, vencer ou for bloqueado, um segundo servidor, em **outro provedor**, assume o Dyno
sozinho: n8n, WhatsApp (Evolution), site e o endereço do n8n. Quando o principal volta, ele não atende junto. A
volta para a Hostinger é um comando, na hora que for melhor.

O Supabase fica fora dos dois servidores, então os dados que estão nele não precisam ser copiados.

## Como funciona

```
                     Supabase (árbitro: tabela dyno_servidor)
                    /  bate ponto a cada 30 s            \  bate ponto a cada 30 s
 PRINCIPAL (Hostinger)                                    RESERVA (outro provedor)
 n8n, Evolution, site...                                  só o vigia ligado, esperando
 agente: a cada 5 min copia  ── rsync por SSH ─────────>  /srv/dyno-reserva/copias
 n8n + Evolution + projetos                               (imagens já baixadas)

 Cloudflare (DNS): dynoapp.com.br, wa. e n8n. apontam para quem está ativo
```

1. **No dia a dia** o agente do principal bate ponto no árbitro e, a cada 5 min, manda ao reserva uma cópia do n8n
   (banco SQLite, com workflows, credenciais e Data tables), da Evolution (banco e sessão do WhatsApp) e das pastas
   dos projetos do Docker Manager (compose e `.env`). O reserva deixa as imagens baixadas, na mesma versão do n8n do
   principal.
2. **O reserva assume** quando três coisas acontecem juntas: o principal está sem bater ponto há 3 min, não responde
   direto em 4 tentativas seguidas (cerca de 2 min) e há uma cópia completa. Quem decide é o árbitro: só um lado
   ganha a troca. O reserva restaura a última cópia, sobe os projetos, vira o DNS na Cloudflare e o Daniel recebe o
   aviso "🛟 Servidor reserva assumiu" no WhatsApp. São cerca de 5 a 7 min fora do ar.
3. **Quando o principal volta**, o agente lê no árbitro que o reserva está atendendo e para o n8n e a Evolution do
   principal (cerca). Nada volta sozinho, para não ter dois servidores atendendo ao mesmo tempo.
4. **A volta é planejada**: um comando no reserva para o atendimento lá, manda os dados para o principal, que
   restaura e sobe, e o DNS volta para a Hostinger. São alguns minutos fora; melhor de madrugada.

**O que se perde numa virada:** até 5 min de dados do n8n e da Evolution (o que mudou depois da última cópia). O
que está no Supabase não se perde. O WhatsApp vai com a sessão, mas pode pedir para ler o QR code de novo no
manager da Evolution.

**O que não vai junto:** a Evolution e o Chatwoot da Dynamo Wear (chat.dynamowear.com.br) e o Whisper. O n8n é o
mesmo para Dyno e Dynamo Wear: durante a virada os workflows da Dynamo Wear rodam no reserva, mas os webhooks que
chegam pelo endereço da Hostinger esperam a volta.

## Peças

| Peça | Onde | Arquivo |
| --- | --- | --- |
| Árbitro | Supabase | tabelas `dyno_servidor` e `dyno_servidor_eventos`, funções `dyno_servidor_batimento` e `dyno_servidor_mudar` |
| Agente | Principal, projeto `dyno-reserva-agente` no Docker Manager | `principal/dyno-reserva-agente.yml` |
| Endereço próprio do n8n | Principal, projeto `dyno-n8n-dominio` (vai junto para o reserva) | `principal/dyno-n8n-dominio.yml` |
| Vigia | Reserva, `/opt/dyno-reserva` | `reserva/docker-compose.yml` e `reserva/preparar-servidor.sh` |
| Scripts | dentro dos dois compose | `src/` (mude aqui e rode `python3 redundancia/gerar.py`) |
| Teste de ponta a ponta | qualquer máquina com dois Docker | `teste/simular.sh` |

## Instalação

Leva uma tarde. A ordem importa: o DNS na Cloudflare vem antes de tudo.

### 1. Domínio na Cloudflare (grátis)

1. Crie a conta e adicione `dynoapp.com.br` (plano Free). Ela copia os registros atuais.
2. Confira se vieram todos, principalmente os do e-mail da Hostinger (MX, SPF, DKIM).
3. Crie o registro `A` de `n8n` apontando para `77.37.41.74`.
4. Deixe `dynoapp.com.br`, `www`, `wa` e `n8n` com a nuvem **laranja** (proxy). É ela que faz a troca de servidor
   ser instantânea.
5. Em **SSL/TLS**, use o modo **Full** (não o *Full (strict)*: o reserva usa certificado próprio na origem).
6. Deixe o **Bot Fight Mode** desligado: o n8n chama a Evolution por `wa.dynoapp.com.br`.
7. Na Hostinger (hPanel → Domínios → DNS / Nameservers), troque os nameservers pelos dois que a Cloudflare mostrar.
   A troca leva de minutos a algumas horas.
8. Crie um token de API (My Profile → API Tokens → *Edit zone DNS*), só para a zona `dynoapp.com.br`, e anote o
   **Zone ID** (página Overview do domínio). Os dois vão para o `.env` do reserva.

### 2. Servidor reserva

Um VPS pequeno em **outro provedor** (se a conta da Hostinger for bloqueada, um segundo VPS dela cai junto). Algo
com 2 a 4 vCPU e 4 GB de RAM, Ubuntu 24.04. Exemplos: Hetzner CPX21 ou DigitalOcean de 4 GB, perto de US$ 8–10/mês.

```bash
# no reserva, como root (copie a pasta redundancia/reserva para lá)
bash preparar-servidor.sh
nano /opt/dyno-reserva/.env              # preencher CF_TOKEN e CF_ZONA
cp docker-compose.yml /opt/dyno-reserva/
```

O script instala o Docker, cria o usuário `dyno` (só consegue escrever em `/srv/dyno-reserva`), abre as portas 22,
80 e 443, gera o `SERVIDOR_TOKEN` e mostra o comando SQL com o resumo dele. **Ainda não suba o vigia.**

### 3. Token no árbitro

No SQL do Supabase, rode o `update dyno_servidor set token_hash = ...` que o script mostrou (ou me mande só esse
resumo, que eu cadastro). O token em si fica só nos dois servidores.

### 4. Principal (Docker Manager da Hostinger)

1. Projeto **`dyno-n8n-dominio`**: cole `principal/dyno-n8n-dominio.yml`. Teste: `https://n8n.dynoapp.com.br/healthz`.
2. Projeto **`dyno-reserva-agente`**: cole `principal/dyno-reserva-agente.yml` e, em Ambiente:
   ```
   SERVIDOR_TOKEN=<o mesmo do /opt/dyno-reserva/.env>
   RESERVA_HOST=<IP do reserva>
   ```
3. No log do agente aparece uma linha começando com `command="rrsync /srv/dyno-reserva",restrict ssh-ed25519`.
   Cole essa linha em `/home/dyno/.ssh/authorized_keys` no reserva.
4. Confira tudo:
   ```bash
   docker exec dyno-reserva-agente bash /app/agente.sh verificar
   ```
   Tem que mostrar os containers `n8n-n8n-1`, `dyno-evo-postgres` e `dyno-evo-api`, a pasta de cada projeto no
   servidor (o agente descobre sozinho), o árbitro com `"ok": true` e "acesso ao reserva: ok". Em poucos minutos
   chega a primeira cópia. Dos projetos vão só os arquivos do primeiro nível da pasta (compose e `.env`); se algum
   projeto depender de um arquivo numa subpasta, ele não vai junto.

### 5. Endereços que não podem depender da Hostinger

Durante uma virada, `n8n.srv1825327.hstgr.cloud` aponta para o principal parado. Por isso:

- **Webhook da Evolution do Dyno** (projeto `evolution-dyno`, variável `WEBHOOK_GLOBAL_URL`): trocar para
  `http://n8n:5678/webhook/dyno-whatsapp` se o `verificar` mostrar `dyno-evo-api` na rede `n8n_default`; senão,
  `https://n8n.dynoapp.com.br/webhook/dyno-whatsapp`.
- **Asaas** (Integrações → Webhooks): `https://n8n.dynoapp.com.br/webhook/dyno-asaas`.
- **Meta** (se a API oficial estiver ligada): o webhook do app para `n8n.dynoapp.com.br`.
- **Vigia externo do Supabase** (`dyno_monitor`): trocar o endereço do n8n para `https://n8n.dynoapp.com.br/healthz`.
- O repasse do cadastro para o cérebro já usa `http://localhost:5678` (feito em 10/10).

### 6. Ligar o vigia

```bash
cd /opt/dyno-reserva && docker compose up -d
docker exec dyno-vigia bash /app/vigia.sh verificar
```

Tem que mostrar a cópia mais recente, o principal "responde", o árbitro com `"ativo": "principal"` e os três nomes
na Cloudflare com o IP da Hostinger. No log (`docker logs -f dyno-vigia`) aparece "imagens prontas para uma virada".

### 7. Ensaio (de madrugada, uma vez)

1. No Docker Manager do principal, pare o projeto `dyno-reserva-agente` e depois o `n8n`.
2. Em 5 a 7 min chega o aviso no WhatsApp e `https://n8n.dynoapp.com.br/healthz` responde pelo reserva. Mande uma
   mensagem ao Dyno para ver o WhatsApp funcionando.
3. Ligue de novo o `n8n` e o `dyno-reserva-agente` no principal: o agente para o n8n e a Evolution de lá (cerca).
4. Volte: `docker exec -it dyno-vigia bash /app/vigia.sh voltar`.

## No dia a dia

- **Quem está atendendo:** `select ativo, mudou_em, motivo, principal_visto_em, reserva_visto_em from dyno_servidor;`
  e o histórico em `dyno_servidor_eventos`.
- **Voltar para a Hostinger depois de uma virada:** `docker exec -it dyno-vigia bash /app/vigia.sh voltar`.
  Antes, confira que o principal está ligado e que o agente bate ponto (`principal_visto_em` recente).
- **Manutenção no principal** (reiniciar o VPS, atualizar o n8n): se for passar de 3 min, ponha `AUTO=0` no `.env`
  do reserva e rode `docker compose up -d`; depois volte para `AUTO=1`. Com `AUTO=0` o vigia só registra a queda.
- **Atualizar o n8n no principal** não exige nada: a próxima cópia leva a versão nova e o reserva baixa a mesma.
- **Mudar os scripts:** edite `src/`, rode `python3 redundancia/gerar.py`, rode o teste e cole o compose novo.

## Teste

`teste/simular.sh` monta os dois servidores com dois Docker na mesma máquina (n8n e Postgres de verdade, árbitro e
Cloudflare falsos) e confere: o reserva não assume com o principal vivo; a queda faz o reserva assumir com os dados
da última cópia, a mesma versão do n8n, o `.env` dos projetos e o DNS virado; o principal que volta fica cercado;
a volta leva para o principal o que foi feito no reserva e devolve o DNS.
