# Dyno — Documentação técnica e Roadmap

Oct 5, 2026 · @DANIEL

## Visão geral

O Dyno é um assessor pessoal que funciona só pelo WhatsApp. Ele já está em produção para a família (Daniel, Quézia e Eliezer) e para os primeiros clientes do Beta fechado. O número do Dyno é o 5511939497178 e o site é [dynoapp.com.br](https://dynoapp.com.br).

O que ele faz hoje:

- **Finanças:** registra gastos e receitas por texto, áudio, foto ou PDF. Também cuida de orçamentos por categoria com alertas de 80% e 100%, contas a pagar, assinaturas, parcelados, recebíveis, importação de extrato e fatura, e dashboard em imagem.
- **Organização:** lembretes que insistem (a cada 30 min, até 6 vezes, apagando o aviso anterior sem resposta), tarefas, notas e listas, manutenção da casa e do carro, e busca de lugares perto.
- **Rotina automática:** resumo da manhã e relatórios das 12h, 18h e 21h, check-ins perguntando "esqueceu de registrar algo?", resumo semanal em imagem (domingo 20h) e mensagem das 6h para a família. A rotina fala com a voz da Dina, e o resumo das 21h, de gastos, com o Dyno.
- **Conta do cliente:** cadastro por convite, 60 dias grátis, cobrança no Asaas, área do cliente no site e pedidos de LGPD pelo próprio WhatsApp.

O caminho de uma mensagem: WhatsApp → Evolution API dedicada (wa.dynoapp.com.br) → n8n, que identifica o cliente no Supabase → OpenAI interpreta e devolve resposta + ações → o n8n grava as ações nas tabelas e responde pela Evolution. Comprovantes vão para o Google Drive.

&#91;embedded content: Arquitetura do Dyno · canal, orquestração e serviços\]

## Número do Dyno no WhatsApp

O Dyno atende por um número próprio, o **+55 11 93949-7178**, ligado à instância `dyno` da Evolution dedicada (wa.dynoapp.com.br). Ele foi conectado por QR Code em 04/10, por volta de 01:53.

| Item | Valor |
| --- | --- |
| Número | 5511939497178 (WhatsApp Business) |
| Link direto | [wa.me/5511939497178](https://wa.me/5511939497178) |
| Instância | `dyno` na Evolution `evolution-dyno` |
| Credencial no n8n | evolution-dyno |
| Webhook de entrada | /webhook/dyno-whatsapp, só evento MESSAGES\_UPSERT |
| Perfil | Foto com o "D" verde sobre azul-marinho; recado "Seu assistente pessoal no WhatsApp. Piloto por convite." |
| Onde atende | Privado de clientes atendidos e da família; grupo da família "DYNO Assessor Pessoal" |
| O que ignora | Outros grupos (inclusive os da Dynamo Wear) e quem não tem convite nem cadastro |
| Reconexão | Automática pelo workflow de Saúde a cada 5 min |

O **número pessoal do Daniel** (5511930851325, instância `pesquisa-aereo` na Evolution da Dynamo Wear) foi desligado do Assessor em 05/10: o cérebro ignora tudo o que chega pela instância pesquisa-aereo (acabou o "conversa comigo mesmo"), e os alertas para o Daniel (saúde, erros, painel, Asaas, falha de envio) saem pelo número do Dyno. Os nós antigos de envio por pesquisa-aereo ficaram desativados. O número continua sendo o do Daniel como usuário e administrador. A instância `dyno` antiga, que ficava no servidor da Dynamo, foi desconectada.

## Dyno e Dina

Desde 04/10 o atendimento tem duas vozes no mesmo número e na mesma conversa: o Dyno cuida do dinheiro e a Dina, da agenda e da rotina. É o mesmo cérebro; só mudam a voz e o cabeçalho de cada resposta, sem custo extra para o cliente.

| Assistente | Cabeçalho | Cuida de |
| --- | --- | --- |
| 05/10 | Lembretes menos insistentes | Insistência a cada 30 min; o aviso anterior sem resposta é apagado para todos (ids em `dyno_lembretes.msg_id` e `msg_jid`) |
| 05/10 | Dados no Supabase por número do cliente | Mensagens, memórias, transações, tarefas, lembretes, contas, orçamentos e assinaturas; leituras filtradas por cliente; LGPD e API do site usam o número |
| 05/10 | Extrato por print em PDF | PDF de uma página muito comprida (app salvo como PDF) é cortado em fatias e lido pelo Claude |
| 05/10 | Aba Funcionalidades e menu de quem está logado | 35 funções do Dyno e da Dina no site; "Minha área" no lugar de "Entrar" |
| Dyno (ele) | *💰 Dyno* | Gastos e receitas, contas a pagar, boletos e comprovantes, extrato, limites e alertas, parcelados, recebíveis, dashboards e relatórios |
| Dina (ela) | *⏰ Dina* | Lembretes que insistem, compromissos, tarefas e projetos, listas e notas, manutenções da casa e do carro, lugares perto |

- **Escolha da voz:** a IA devolve o campo `voz` (dyno ou dina) pelo assunto principal. Se a pessoa começa com "Dina, …" ou "Dyno, …", responde quem foi chamado. Cumprimentos, conta, plano, cobrança e LGPD ficam com o Dyno.
- **Cérebro (YFgP2bYqeHbQc5t1):** nó "Persona (Dyno e Dina)" entre "Complemento do prompt (extras)" e "OpenAI (cérebro)" acrescenta as regras da dupla; "Interpretar resposta" põe o cabeçalho e remove o que a IA tenha escrito. O antigo prefixo "*Dyno:*" saiu dos nós de envio.
- **Lembretes (Xbdnisj9AjKJFYAF):** lembretes comuns saem como Dina; lembretes de contas a pagar saem como Dyno. A busca de lugares também sai como Dina.
- **Ainda como Dyno:** alertas de orçamento e mensagens de cadastro e convite.
- **Apresentação:** em 04/10 o Dyno apresentou a Dina para as 3 contas ativas da família (Daniel, Quézia, Eliezer), em duas mensagens.
- O nome "Dina" substituiu a ideia "Woody", descartada pela associação com Toy Story.

## Infraestrutura

Tudo roda em um VPS da Hostinger, com exceção do banco (Supabase gerenciado) e dos arquivos (Google Drive). O servidor é compartilhado com a Dynamo Wear e com um servidor de Project Zomboid.

**Servidor:** srv1825327, plano KVM 4 (4 vCPU, 16 GB de RAM), IP 77.37.41.74. Uso medido em 04/10: CPU \~6%, RAM \~6 GB e disco \~40 GB. **Vence em 09/10/2026 com a renovação automática desligada.**

### Containers Docker

| Projeto | Containers (imagem) | Para que serve | Exposição |
| --- | --- | --- | --- |
| n8n | n8n-n8n-1 (n8nio/n8n, sem tag fixa); n8n-traefik-1 (traefik) | Toda a lógica do Dyno; Traefik faz o HTTPS de todos os domínios | Traefik publica 80/443; n8n só em 127.0.0.1:5678 |
| evolution-dyno | dyno-evo-api (evolution-api v2.3.7); dyno-evo-postgres (postgres 15); dyno-evo-redis (redis 7) | WhatsApp do Dyno, instância `dyno` | wa.dynoapp.com.br via Traefik |
| dyno-site | dyno-site (nginx 1.27-alpine) | Site e área do cliente; repassa /api ao n8n | dynoapp.com.br via Traefik |
| evolution | evolution-api v2.3.7 + postgres + redis | WhatsApp da Dynamo Wear e o número pessoal (instância pesquisa-aereo) | chat.dynamowear.com.br |
| chatwoot | chatwoot v4.16.1 (rails + sidekiq) + pgvector pg16 + redis | Atendimento da Dynamo Wear (não é do Dyno) | interno |
| dyno-whisper | dyno-whisper (whisper-asr-webservice v1.10.0, modelo `small`) | Whisper local em modo sombra ao lado da OpenAI. Compose e guia em `whisper/`. **Ainda não instalado** (10/10) | interno: só a rede n8n\_default (`http://dyno-whisper:9000`) |
| pzserver | Project Zomboid + 2 painéis | Servidor de jogo (não é do Dyno). Parado em 05/10; exclusão definitiva pendente (Daniel, no hPanel) | UDP 16261-16262, TCP 27015 |

O firewall da Hostinger (**dyno-vps-padrao**) libera só SSH 22, HTTP 80, HTTPS 443, ICMP e as portas do jogo. Há backups semanais da Hostinger fora do servidor e snapshot semanal do VPS.

**Cuidados:** a imagem do n8n não tem versão fixa, então reimplantar o projeto puxa a versão mais nova; faça isso só numa janela de manutenção. O n8n está com GENERIC\_TIMEZONE=Europe/Berlin, mas cada workflow do Dyno define America/Sao\_Paulo.

## Links, domínios e conectividade

O Dyno usa um domínio próprio (dynoapp.com.br) e o subdomínio da Hostinger do n8n. Todos apontam para o IP 77.37.41.74, e o Traefik emite os certificados HTTPS.

### Domínios e DNS

| Registro | Tipo | Destino | Uso |
| --- | --- | --- | --- |
| dynoapp.com.br | A | 77.37.41.74 | Site e área do cliente (container dyno-site) |
| www.dynoapp.com.br | redireciona | dynoapp.com.br | — |
| wa.dynoapp.com.br | A | 77.37.41.74 | Evolution do Dyno (container dyno-evo-api) |
| n8n.srv1825327.hstgr.cloud | subdomínio da Hostinger | 77.37.41.74 | Editor e webhooks do n8n |
| chat.dynamowear.com.br | A | mesmo VPS | Evolution da Dynamo Wear (número pessoal) |
| no-reply@dynoapp.com.br | e-mail Hostinger | — | Única caixa; faltam SPF, DKIM e DMARC |

O domínio está registrado na Hostinger.

### Links públicos

| Link | Para que serve |
| --- | --- |
| [dynoapp.com.br](https://dynoapp.com.br) | Site |
| [dynoapp.com.br/entrar](https://dynoapp.com.br/entrar) | Login por código |
| [dynoapp.com.br/conta](https://dynoapp.com.br/conta) | Área do cliente |
| [dynoapp.com.br/termos](https://dynoapp.com.br/termos) e [/privacidade](https://dynoapp.com.br/privacidade) | Termos de Uso e Política de Privacidade |
| [wa.me/5511939497178](https://wa.me/5511939497178) | Conversar com o Dyno |
| [ig.me/m/dynoapp.ia](https://ig.me/m/dynoapp.ia) | Pedir convite pelo direct do Instagram |
| [Vídeo "Como usar o Dyno"](https://resource2.heygen.ai/video/b22e72bd9dc442a8843e9d7663df7684/original.mp4) | Tutorial enviado nas boas-vindas |
| [dynoapp.com.br/beta](https://dynoapp.com.br/beta) | Pedido de vaga no Beta (substitui o direct do Instagram nos botões) |

### Endereços internos e endpoints

| Endereço | Quem chama | Proteção |
| --- | --- | --- |
| n8n.../webhook/dyno-whatsapp | Evolution do Dyno | URL do webhook global |
| n8n.../webhook/assessor-whatsapp | Workflow de cadastro (repasse ao cérebro) | interno |
| n8n.../webhook/dyno-site-api | nginx do site (`/api` e `/api/arquivo`) | Cabeçalho secreto X-Dyno-Site + limite por IP |
| n8n.../webhook/dyno-cadastro | Cadastro pelo site | Rate limit por IP |
| n8n.../webhook/dyno-asaas | Asaas | Token `asaas-access-token` |
| n8n.../webhook/dyno-painel | Daniel (painel de observabilidade) | Token do painel |
| n8n.../webhook/dyno-infra | Script de métricas do servidor | Token de infra |
| n8n.../webhook/dyno | Página de cadastro antiga | a desligar |
| n8n.../healthz | Monitor externo | público |
| wa.dynoapp.com.br/manager | Daniel (painel da Evolution) | Chave global |
| http://n8n:5678 | nginx do site, pela rede Docker n8n\_default | sem sair do servidor |

### Serviços externos

| Serviço | Endereço | Conexão |
| --- | --- | --- |
| Supabase | xvekgnbneeokihtjpbts.supabase.co (us-east-2) | REST/RPC com a chave de serviço (credencial Supabase\_Dyno) |
| OpenAI | api.openai.com | Credencial openai-dyno (projeto DynoApp, limite US$ 20/mês, alertas 80% e 100%) |
| Anthropic (Claude) | api.anthropic.com | Credencial anthropic-dyno |
| TypeSafe (Jev) | API da TypeSafe | Credencial jev-typesafe |
| Banco Central (PTAX) | API pública do BC | Público (cotação do alerta de câmbio) |
| Asaas | api.asaas.com/v3 | Credencial asaas-prod |
| Google Drive | API do Google, conta oficialdynamowear | OAuth2 (credencial Google Drive account) |
| Nominatim | nominatim.openstreetmap.org | Público |

Pastas no Drive: "Meu Assessor - Comprovantes" (comprovantes) e "Dyno - Backups (privado)" (backups diários).

## Fluxo do projeto: de onde vem, para onde vai

Toda mensagem entra pelo workflow de cadastro. Ele decide se a pessoa ainda está se cadastrando ou se já é atendida pelo cérebro, e a resposta volta pela mesma Evolution.

&#91;embedded content: Fluxo de uma mensagem · da chegada à resposta\]

No caminho do cérebro, áudio vira texto antes da OpenAI. Foto e PDF são lidos pela IA e salvos no Drive. Extratos vão para o workflow de importação, e LGPD e dashboard vão para os seus workflows.

### Todos os fluxos de dados

| # | Origem | Destino | Como | O que passa |
| --- | --- | --- | --- | --- |
| 1 | Cliente no WhatsApp | Evolution do Dyno | Protocolo do WhatsApp Web | Texto, áudio, foto, PDF, planilha, localização |
| 2 | Evolution do Dyno | n8n /dyno-whatsapp | HTTPS (webhook) | Evento da mensagem |
| 3 | Cadastro (n8n) | Supabase | RPC `dyno_whatsapp_passo` | Passo do cadastro, convite, aceite |
| 4 | Cadastro (n8n) | Asaas | API v3 | Nome, e-mail, CPF, celular (só o cliente) |
| 5 | Cadastro (n8n) | Cérebro /assessor-whatsapp | HTTPS interno | Mensagem de quem já é atendido |
| 6 | Cérebro | Supabase | RPC `dyno_assessor_identificar` | Número → autor, plano, situação da conta |
| 7 | Cérebro | Data tables | Nós do n8n | Lê contexto e grava gastos, tarefas, lembretes, memórias |
| 8 | Cérebro | OpenAI | API (chat e transcrição) | Texto, imagem, PDF → resposta + ações |
| 9 | Cérebro | Google Drive | API do Google | Comprovantes (foto e PDF) |
| 10 | n8n (todos) | Evolution do Dyno → cliente | HTTPS (sendText, sendMedia) | Respostas, lembretes, relatórios |
| 11 | Navegador | nginx do site → n8n /dyno-site-api | HTTPS + cabeçalho secreto | Login, painel, extrato, comprovantes, plano |
| 12 | API do site | Supabase, Data tables, Drive, Asaas | APIs | Sessão, dados do cliente, arquivos, faturas |
| 13 | Asaas | n8n /dyno-asaas | HTTPS + token | Pagamento confirmado, atrasado, cancelado |
| 14 | Agendados (n8n) | Data tables e Supabase → Evolution | Gatilho de horário | Lembretes, relatórios, avisos de fim do teste |
| 15 | Supabase (pg\_cron + pg\_net) | n8n /healthz, wa., site | HTTPS a cada 5 min | Teste de disponibilidade |
| 16 | Workflows com erro | Erros e alertas → Supabase + WhatsApp do Daniel | Error workflow | Falha, sem dados pessoais |
| 17 | Backup (n8n) | Google Drive | API do Google, 03:40 | JSON com Supabase + Data tables |

## Ferramentas e tecnologias

O Dyno é feito sem servidor de aplicação próprio: a lógica fica toda no n8n, e os dados e regras de negócio ficam em funções SQL no Supabase.

| Camada | Ferramenta | Uso no Dyno |
| --- | --- | --- |
| Orquestração | n8n self-hosted (Docker) | 29 workflows (25 ativos): cérebro, agendados, cadastro, cobrança, API do site, operação |
| Canal | Evolution API v2.3.7 (WhatsApp Web, não oficial) | Recebe e envia mensagens, baixa mídia, foto e recado do perfil |
| IA | OpenAI gpt-5.6-luna | Entende a mensagem e devolve JSON `{resposta, acoes[]}`; lê foto, PDF e extratos; pesquisa na web |
| IA (voz) | OpenAI gpt-4o-mini-transcribe | Transcreve áudios |
| Banco | Supabase gratuito (Postgres 17, projeto `projeto-dyno`, us-east-2) | Clientes, sessões, cobrança, logs, importações; funções RPC; pg\_cron |
| Banco legado | Data tables do n8n (SQLite, limite 200 MiB) | Dados do assistente: transações, tarefas, lembretes, memórias, contas |
| Arquivos | Google Drive (conta oficialdynamowear) | Comprovantes e backups diários |
| Cobrança | Asaas (produção, API v3) | Cliente, assinatura Pix ou cartão, webhook de pagamento |
| Site | nginx 1.27 + HTML/CSS/JS estático | Site, área do cliente, proxy /api para o n8n |
| HTTPS | Traefik + Let's Encrypt | Certificados de todos os domínios |
| Hospedagem | Hostinger VPS KVM 4 + Docker Manager | Servidor, firewall, snapshots, backups |
| Localização | Nominatim (OpenStreetMap) | Endereço a partir da localização enviada |
| Gráficos | Nó Edit Image do n8n | Dashboard financeiro em PNG |
| Vídeo | HyperFrames | Vídeo promo do Beta e tutorial de boas-vindas |

Credenciais do n8n usadas pelo Dyno, só por nome: **Supabase\_Dyno**, **evolution-dyno**, **openai-dyno**, **anthropic-dyno**, **jev-typesafe**, **asaas-prod**, **asaas-access-token**, **Google Places**, **Google Drive account**. Desde 05/10 a OpenAI usa a credencial openai-dyno; a variável `OPENAI_API_KEY` do n8n fica só para o DMChat da Dynamo Wear. Nenhum segredo fica em código ou neste documento.

## IA em camadas (OpenAI, Claude e Jev)

A camada de IA fica no workflow **Dyno | IA em camadas** (mOXAwF2cZ8zbYs2j), que qualquer workflow do Dyno chama do mesmo jeito. Quem decide qual IA responde é a configuração no Supabase, sem mexer em código. Desde 04/10 o **Claude Sonnet 5.5 lê os extratos** (o Importar extrato chama a camada) e o **Jev roda em modo sombra** no cérebro (workflow Dyno | Jev modo sombra, Yw7mI0ybOITBwJoQ), gravando a comparação em `dyno_ia_sombra` sem o texto da mensagem; relatório com `dyno_ia_sombra_relatorio(7)`. A conversa continua na OpenAI. Atenção: o Sonnet 5.5 recusa `tool_choice` forçado, então a camada usa `auto` e pede a ferramenta no sistema.

| Camada (tarefa) | Configuração | Hoje | Plano |
| --- | --- | --- | --- |
| conversa (cérebro) | `ia_conversa` | openai | Testar Claude Sonnet 5.5 (`claude-sonnet-5-5`) em A/B |
| documento (extrato, fatura, PDF, foto) | `ia_documento` | **claude** (desde 04/10), OpenAI de reserva | Claude Sonnet 5.5 |
| simples (categoria, check-ins, textos curtos) | `ia_simples` | openai | Claude Haiku 4.5 (`claude-haiku-4-5`) |
| decisão (intenção, "ok" de lembrete, duplicado) | `ia_decisao_modo` | **sombra** (desde 04/10) | sombra → ativo, com Jev (`jev-latest`) |
| áudio | — | OpenAI | Whisper local em **modo sombra** desde 10/10 (ver abaixo). A API do Claude não transcreve |

**Como funciona:**

1. O workflow recebe `{tarefa, sistema, mensagens, esquema}`, ou `{tarefa: 'decisao', decisao: {state, questions}}` para o Jev.
2. Ele lê a configuração pela função `dyno_ia_config()` (chaves `ia_*` em `dyno_config`).
3. Converte o pedido para o formato da IA escolhida. Imagem e PDF viram blocos do Claude, e o esquema JSON vira uma ferramenta obrigatória. O texto fixo do sistema usa o cache da Anthropic, que custa 10% do preço nas repetições.
4. Se o Claude falhar ou estiver sem chave, a OpenAI responde no lugar (`reserva: true`).
5. Devolve sempre o mesmo formato: `{ok, provedor, reserva, modelo, texto, json, decisao, uso, ms}`.

Teste de 04/10, no workflow **Dyno | TESTE IA em camadas (manual)** (0NTpUwVxsZFMm8Li):

- pedido pela OpenAI: categoria "Alimentação" em 1,6 s;
- pedido forçando o Claude ainda sem chave: a reserva respondeu "Combustível" em 1,3 s;
- pedido de decisão: voltou "desligado", como esperado.

Teste com a chave do Claude já publicada (04/10, credencial **anthropic-dyno**):

- Haiku 4.5 classificou "paguei 120 de gasolina" como "Combustível" em 0,7 s.
- Sonnet 5.5 respondeu uma conversa em 4,0 s, dos quais 273 tokens foram de raciocínio interno. Para o cérebro, vale testar o esforço reduzido e ver se fica mais rápido.
- O cache do texto do sistema só entra em prompts com mais de \~1.000 tokens, como o do cérebro, e não nos testes curtos.
- **Jev conectado com a credencial jev-typesafe (ver abaixo)**.

Teste do Jev (04/10, credencial **jev-typesafe**, modelo jev-1.13.0, \~0,3 s por pedido):

| Mensagem | Intenção escolhida | É confirmação? |
| --- | --- | --- |
| "ok, feito" | confirmar\_lembrete (confiança 1,0) | sim (0,97), certo |
| "gastei 45 no mercado" | registrar\_gasto (1,0) | sim (0,95), **errado** |
| "me lembra amanhã de levar o carro na revisão" | criar\_lembrete (1,0) | não (0,06), certo |

As três intenções vieram certas. A pergunta de sim/não errou em um caso com alta certeza, o que confirma a regra de usar o Jev primeiro só em modo sombra e com perguntas bem descritas.

**Formato das perguntas do Jev** (sem o campo `criteria`, a API responde 422):

- **choice:** `{type: 'choice', instructions: 'pergunta', criteria: {opcao: 'quando escolher'}}`
- **score:** `{type: 'score', instructions: '...', criteria: ['nível 0', 'nível 1', ...]}`
- **noul:** `{type: 'noul', instructions: '...', criteria: {'true': 'quando sim', 'false': 'quando não'}}`

O campo `state` pode ser um texto ou um objeto. A camada devolve também uma forma simplificada em `json`, por exemplo `{intencao: {valor, confianca}}`, além da resposta original em `decisao`.

Crédito comprado: US$ 10 na Anthropic e US$ 10 na TypeSafe (04/10).

### Whisper local em modo sombra

Desde 10/10 o cérebro manda cada áudio também ao **Whisper local** (container `dyno-whisper`, pasta `whisper/`), sem mudar a resposta: quem responde continua sendo a transcrição da OpenAI.

- No cérebro, o ramo **Montar sombra (Whisper)** → **Whisper (modo sombra)** sai do nó Transcrever áudio e roda por último, depois da resposta, sem esperar.
- O workflow **Dyno | Whisper modo sombra** (V08b0qgQ3qb0Q0vI) transcreve no container, compara palavra a palavra com a OpenAI e grava em `dyno_whisper_sombra`: latência dos dois, duração do áudio, número de palavras e similaridade (0 a 1). O texto só é guardado nos áudios do Daniel; de clientes ficam só as métricas.
- Enquanto o container não estiver instalado, o Whisper não responde e nada é gravado.
- Relatório: `select dyno_whisper_sombra_relatorio(7);`. Desligar: desativar o nó **Montar sombra (Whisper)** no cérebro.
- Ao trocar `ASR_MODEL` ou `ASR_ENGINE` no compose, troque também as constantes no nó **Comparar com a OpenAI**, para o relatório separar por modelo.

### Medição de custo de IA

Desde 04/10 (cerca de 20h), toda chamada de IA grava os tokens usados e o custo na tabela `dyno_ia_uso`, com autor e origem. As origens registradas são: cérebro, áudio, busca de lugares, extrato, reflexão das 6h e camada.

- **Preços:** ficam em `dyno_ia_precos`, em US$ por milhão de tokens. O da gpt-5.6-luna precisa ser conferido no painel da OpenAI.
- **Relatório:** `dyno_ia_custos(dias, dolar)` mostra o total, R$ por pessoa por mês e a divisão por origem, modelo e pessoa.
- **Retenção:** 180 dias. O pedido de apagar dados da LGPD também apaga esses registros.
- **Já medido:** cada mensagem do cérebro usa \~7.200 tokens de entrada, dos quais \~6.600 vêm do cache, e custa \~US$ 0,0018.

O relatório real de 7 dias está agendado para 11/10/2026.

### Passo a passo: chave do Claude (Anthropic)

1. Entre em [platform.claude.com](https://platform.claude.com) com a conta da empresa e ative a autenticação em dois fatores.
2. Em **Billing**, adicione crédito (sugestão: US$ 10 a US$ 20 para os testes) e defina um limite mensal de gasto.
3. Em **API Keys**, clique em **Create Key** e dê o nome `dyno-n8n`. Copie a chave, que começa com `sk-ant-` e só aparece uma vez.
4. No n8n: **Credentials → Add credential → Header Auth**. Use nome da credencial `anthropic-dyno`, Name `x-api-key` e, em Value, cole a chave. Salve.
5. Abra o workflow **Dyno | IA em camadas**, clique no nó **Claude**, escolha a credencial `anthropic-dyno` e publique.
6. Me avise só o nome da credencial. Eu rodo o teste e mudo `ia_documento` e `ia_simples` quando aprovado.

### Passo a passo: chave do Jev (TypeSafe)

1. Entre em [typesafe.ai](https://typesafe.ai). Se ainda houver lista de espera, inscreva-se e aguarde o convite do console.
2. No console (console.typesafe.ai), em **Settings → API Keys**, crie a chave `dyno-n8n`. Ela começa com `ts_`. Contas novas recebem cerca de US$ 5 de crédito.
3. No n8n: **Credentials → Add credential → Header Auth**. Use nome da credencial `jev-typesafe`, Name `Authorization` e Value ` Bearer  ` seguido da chave (com o espaço depois de Bearer). Salve.
4. No workflow **Dyno | IA em camadas**, clique no nó **Jev**, escolha `jev-typesafe` e publique.
5. Me avise. Eu ligo `ia_decisao_modo = sombra`: o Jev decide em paralelo sem agir, e comparo por 1 a 2 semanas antes de passá-lo para `ativo`.

**Regras:** a chave nunca vai para o chat, o WhatsApp ou o código, só para a credencial do n8n. Se uma chave vazar, apague-a no console e crie outra. Antes de ativar, Anthropic e TypeSafe entram no mapa de dados da LGPD e na Política de Privacidade.

## Alerta de câmbio (dólar e euro)

Função do Dyno lançada em 05/10. O cliente pede pelo WhatsApp ("me avisa quando o dólar ficar abaixo de R$ 4,90", "quanto tá o euro?", "cancela meus alertas de câmbio") e o Dyno avisa uma vez quando o valor é atingido. Só informa: nunca recomenda comprar ou vender nem prevê cotação.

- **Cotação:** workflow "Dyno | Alerta de câmbio" (asdiDsXdGoWC7Bip), a cada 15 min, seg–sex 9h–18h. Fonte em uso: PTAX do Banco Central (oficial, grátis). AwesomeAPI fica como fonte 1 quando houver chave grátis (credencial `awesomeapi`).
- **Banco:** `dyno_cambio_cotacoes` (120 dias) e `dyno_cambio_alertas` (RLS, até 5 por pessoa, entra na eliminação LGPD, inativos apagados após 180 dias). RPCs `dyno_cambio_registrar`, `dyno_cambio_contexto`, `dyno_cambio_acao`, `dyno_cambio_resumo`, só service\_role.
- **Cérebro:** "Câmbio (Supabase)" + "Complemento (câmbio)" colocam cotação e alertas no prompt; "Detectar câmbio" + "Câmbio: salvar alerta" gravam as ações.
- **Divulgação:** anúncio aos 10 cadastros; seção "O dólar caiu? O Dyno te avisa." na home do site + item na lista do Dyno + pergunta no FAQ; post 1080×1350 e reel de 22 s (com e sem música) para o Instagram.
- **Pendente:** chave da AwesomeAPI e teste real pelo WhatsApp (criar, consultar, cancelar).

## n8n: workflows

O Dyno tem 25 workflows ativos (inclui o Jev e o Whisper em modo sombra e o Alerta de câmbio) e 4 desligados (só de setup ou teste, incluindo o TESTE IA em camadas, 0NTpUwVxsZFMm8Li), todos no projeto pessoal do n8n. Editor: n8n.srv1825327.hstgr.cloud.

### Atendimento (tempo real)

| Workflow | ID | Gatilho | O que faz |
| --- | --- | --- | --- |
| WhatsApp (cérebro) | YFgP2bYqeHbQc5t1 | Webhook /assessor-whatsapp | Identifica o cliente, transcreve áudio, lê foto/PDF, chama a OpenAI, executa as ações (22 saídas) e responde |
| WhatsApp clientes (cadastro por convite) | XRsXyav6ICD921Q8 | Webhook /dyno-whatsapp (Evolution) | Recebe todos os eventos do número, conduz o cadastro, comandos de admin e repassa o resto ao cérebro |
| Extras | K4GH2JArrLnZbJAG | Chamado pelo cérebro | Notas e listas, parcelados, recebíveis, desfazer, convites, Excel, tarefas por projeto |
| Dashboard financeiro (imagem) | qHNQDuOeWVg7EyZq | Chamado pelo cérebro | Gera o PNG de gastos e envia |
| Importar extrato (conta e cartão) | yBCWxnd2N9d3uDxM | Chamado pelo cérebro | Lê PDF/CSV/OFX/Excel com IA, tira duplicados, pede IMPORTAR e grava |
| LGPD do titular | 3jEnG5ZmIFf16JGS | Chamado pelo cérebro | Envia cópia dos dados e apaga tudo com confirmação |
| Enviar convite pelo admin | WNefuC4RhAAfS3Vs | Chamado pelo cadastro | Daniel pede um convite no WhatsApp; cria e envia |

### Agendados

| Workflow | ID | Quando | O que faz |
| --- | --- | --- | --- |
| Lembretes e mensagem das 6h | Xbdnisj9AjKJFYAF | A cada minuto + 06:00 | Dispara lembretes com insistência; resumo da família no grupo |
| Relatórios do dia e check-ins | 9VTi7hePHvXOvYrW | 07:30, 10:00, 12:00, 14:12, 18:00, 21:00 | Relatórios por cliente e "esqueceu de registrar algo?" |
| Agentes diários | 2mEE5d9YWcgutRbD | 09:00 | Renovação de assinaturas, manutenções, pedido de km |
| Extras diários | 4sWI6Gs5o7AAR59R | 09:30 | Lança parcelas/recorrentes e avisa tarefas atrasadas |
| Resumo semanal individual | Z2heNCM6hmMq0PZ0 | Domingo 20:00 | Card em imagem da semana (Dina), pelo número do Dyno; por enquanto só a família |
| Alerta de câmbio | asdiDsXdGoWC7Bip | A cada 15 min, seg–sex 9h–18h | Cotação do dólar e do euro e aviso de quem pediu alerta |
| Lembrete de cadastro incompleto | BBRCGBQtIX8waiqL | A cada hora | Cadastros parados, convites não usados e avisos de fim do teste |

### Site, cobrança e operação

| Workflow | ID | Gatilho | O que faz |
| --- | --- | --- | --- |
| API do site (área do cliente) | nslhB7FRnKuAOPuf | Webhook /dyno-site-api (via nginx) | Login por código, conta, plano, cancelamento, painel, extrato, comprovantes, zip |
| Cadastro e cobrança | QwETMN0WuCbOmSRO | Webhook /dyno-cadastro | Cadastro pelo site, vaga e cliente no Asaas |
| Asaas webhook | FAxcJprGwlZAyKhw | Webhook /dyno-asaas | Valida o token e atualiza status e pagamentos |
| Saúde (health check) | v9JsD02YHFAgmLPE | A cada 5 min | Testa Supabase, Asaas e WhatsApp; reconecta; avisa só na mudança |
| Erros e alertas | 5UUmuzItIYDsd3AG | Error workflow | Registra falhas e avisa o Daniel (sem repetir por 15 min) |
| Painel e infraestrutura | j3WSfca0UXb06SeW | Webhook + agendado | Painel de observabilidade e métricas do servidor |
| Backup diário e monitor externo | ssmh5caNcmvqPBSD | 03:40 + a cada 10 min | Backup no Drive (14 dias) e aviso de quedas |
| Página de cadastro (temporária) | BFmfbtTei9fQCgCB | Webhook /dyno | Página antiga; pode ser desligada |
| IA em camadas (OpenAI, Claude, Jev) | mOXAwF2cZ8zbYs2j | Chamado por outros workflows | Escolhe a IA pela configuração, converte o pedido e usa a OpenAI como reserva |

Desligados: Setup Evolution (LsVMn71OPQmyc4Mz), TEMP limpeza de testes (uOt8WPfaI5lk6PT2) e TESTE Google Places (uodpCgu2VBUwqbO4).

**Regras de trabalho no n8n:** cada envio de mensagem usa a credencial evolution-dyno. Mensagens do bot começam com um caractere invisível para evitar loop. Workflows agendados guardam só execuções com erro. Para testar um workflow agendado, desligue antes os nós de envio, porque a execução manual dispara o gatilho de agenda.

## Banco de dados

Os dados ficam em dois lugares. O Supabase guarda clientes, cobrança, site e operação. As Data tables do n8n ainda guardam os dados do assistente (gastos, tarefas, lembretes e o resto). Unificar tudo no Supabase é o principal item técnico do roadmap.

### Supabase (projeto-dyno, Postgres 17, us-east-2)

Todas as tabelas têm RLS ligado. O n8n acessa só com a chave de serviço, e as funções são liberadas apenas para `service_role`.

| Tabela | Conteúdo |
| --- | --- |
| dyno\_usuarios | Clientes: nome, autor único, WhatsApp, e-mail, CPF, plano, ciclo, status, `gratis_ate`, ids do Asaas, forma de pagamento (11 linhas) |
| dyno\_convites | Convites do Beta (12) |
| dyno\_pagamentos / dyno\_eventos\_asaas | Pagamentos e eventos do webhook, sem repetir |
| dyno\_site\_sessoes / dyno\_site\_codigos / dyno\_sessoes | Login por código no WhatsApp e sessões (token com hash) |
| dyno\_importacoes | Extratos aguardando IMPORTAR (apagados após 7 dias) |
| dyno\_feedback | Respostas do feedback do piloto |
| dyno\_lembretes\_cadastro | Controle dos lembretes de cadastro e fim do teste |
| dyno\_admin\_pendente | Comandos de admin aguardando confirmação |
| dyno\_logs | Logs de saúde e erros (7 dias) |
| dyno\_monitor / dyno\_monitor\_quedas | Vigia externo e registro de quedas |
| dyno\_site\_bundle / dyno\_site\_stage | Pacote do site usado no deploy |
| dyno\_config | Configurações gerais |
| dyno\_servidor / dyno\_servidor\_eventos | Árbitro do servidor reserva: qual servidor atende, batimentos e histórico de viradas (ver `redundancia/`) |
| dyno\_whisper\_sombra | Comparação Whisper local × OpenAI nos áudios (texto só dos áudios do Daniel) |

Funções principais (RPC):

- **Identidade e atendimento:** `dyno_assessor_identificar`, `dyno_usuario_atendido`, `dyno_assessor_destinos`, `dyno_vagas`, trigger `dyno_usuario_autor_tg`.
- **Cadastro e cobrança:** `dyno_whatsapp_passo` (máquina de estados do cadastro), `dyno_cadastrar`, `dyno_convite_criar`, `dyno_convite_enviar`, `dyno_conversao_lembretes`, `dyno_conversao_resposta`, `dyno_evento_asaas`, `dyno_cadastro_lembretes`.
- **Site:** `dyno_site_codigo_pedir`, `dyno_site_codigo_validar`, `dyno_site_conta`, `dyno_site_plano`, `dyno_site_cancelar`, `dyno_site_sair`, `dyno_site_sessao_usuario`.
- **LGPD:** `dyno_lgpd_exportar`, `dyno_lgpd_eliminar`, `dyno_titular_exportar`, `dyno_titular_eliminar`.
- **Admin e operação:** `dyno_admin`, `dyno_admin_achar`, `dyno_metricas`, `dyno_painel`, `dyno_log`, `dyno_log_lote`, `dyno_backup_export`, `dyno_monitor_rodar`, `dyno_monitor_relatorio`, `dyno_infra_registrar`, `dyno_feedback_lembretes`.
- **Extrato:** `dyno_importacao_salvar`, `dyno_importacao_decidir`, `dyno_importacoes_limpar`.
- **Servidor reserva:** `dyno_servidor_batimento`, `dyno_servidor_mudar` (liberadas para a chave pública, mas só funcionam com o token dos servidores, guardado como resumo em `dyno_servidor.token_hash`).
- **Whisper em sombra:** `dyno_whisper_sombra_registrar`, `dyno_whisper_sombra_relatorio`.

Tarefas agendadas no banco (pg\_cron):

| Tarefa | Quando | O que faz |
| --- | --- | --- |
| dyno-monitor-externo | a cada 5 min | Testa o n8n e o site de fora do servidor |
| dyno\_purga\_logs | 03:15 | Apaga logs com mais de 7 dias |
| dyno-limpar-importacoes | 07:20 | Apaga importações com mais de 7 dias |

### Data tables do n8n (dados do assistente)

Todas têm a coluna `autor` (ou `pessoa`). Cada consulta filtra por ela, então um cliente nunca vê dados de outro.

| Tabela | Conteúdo |
| --- | --- |
| assessor\_transacoes | Gastos e receitas: tipo, valor, categoria, descrição, data, forma de pagamento, comprovante |
| assessor\_lembretes | Lembretes: quando, recorrência, status, insistências, conta ligada |
| assessor\_tarefas | Tarefas com prioridade, prazo, status e projeto |
| assessor\_contas | Contas a pagar: vencimento, beneficiário, linha digitável, status |
| assessor\_assinaturas | Assinaturas: valor, ciclo, próxima cobrança |
| assessor\_orcamentos | Limite mensal por categoria |
| assessor\_extras | Notas, listas, parcelados, recebíveis |
| assessor\_memorias | Memória do que o cliente contou (ex.: endereço) |
| assessor\_mensagens | Histórico curto da conversa |
| assessor\_manutencoes / assessor\_veiculos | Casa e carro |
| assessor\_rotina / assessor\_devocional | Mensagem das 6h da família (devocional licenciado, nunca enviado a clientes) |

O limite das Data tables é 200 MiB no total, e a decisão foi mantê-lo assim por enquanto.

## Site e área do cliente

O site [dynoapp.com.br](https://dynoapp.com.br) está no ar. É estático, servido por nginx, e não fala direto com o banco: toda chamada passa por `/api`, que o nginx repassa ao n8n com um cabeçalho secreto.

**Páginas:** Início, Como funciona, Preços, Dúvidas, Termos e Privacidade (preliminares, faltam razão social, CNPJ e revisão jurídica), Entrar e Minha área. "Quero participar" leva ao pedido de vaga em /beta (antes ia ao direct do Instagram @dynoapp.ia), e "Já tenho convite" leva ao WhatsApp do Dyno. As fontes são Inter Tight e Inter.

**Login:** sem senha, com um código de 6 dígitos enviado pelo WhatsApp do Dyno.

- O código vale 10 minutos e aceita até 5 tentativas.
- Limites de pedido: 3 códigos por número a cada 15 minutos e 10 por IP por hora.
- A sessão fica num cookie seguro de 30 dias, e o banco guarda só o hash do token.

**Área do cliente, em 4 abas:**

| Aba | O que mostra |
| --- | --- |
| Painel | Gastos, receitas e saldo do mês, categorias com barra de limite (só onde há orçamento), 6 meses, contas, lembretes, tarefas, assinaturas |
| Extrato | Lançamentos com filtro de período, categoria e tipo; exporta CSV |
| Comprovantes | Galeria por categoria e data, visualizador, download em ZIP |
| Minha conta | Status, plano, dias grátis, faturas, trocar plano, cancelar |

**Publicar uma mudança:** editar `build.py` e `www/assets`, gerar o pacote, gravar em `dyno_site_bundle` no Supabase e reiniciar o projeto Docker `dyno-site`. O container baixa o pacote ao iniciar e guarda a última cópia boa.

**Para vender (04/10):**

- **Conversa animada no topo:** as bolhas aparecem uma a uma, com "digitando…" antes das respostas (`home.js`); parada para quem desliga animações.
- **Dupla Dyno e Dina:** seção "Dois assessores. Uma conversa só." na home e em Como funciona, FAQ "Quem é a Dina?" e rodapé.
- **Selos honestos:** LGPD, não mexe no seu dinheiro, número exclusivo, empresa brasileira com CNPJ e sem fidelidade.
- **Vagas ao vivo:** `POST /api {acao:'vagas'}` chama `dyno_vagas()` e mostra "restam X vagas" no topo, no bloco do Beta e no /beta. No n8n, o nó "Ação pública (vagas)" só age depois da checagem do cabeçalho do site.
- **Comparativo de preço sem citar nome:** principal concorrente R$ 358,80/ano (12x R$ 29,90) e 7 dias de garantia contra R$ 199,90/ano (R$ 16,66/mês) e 60 dias grátis; economia de R$ 158,90/ano, com fonte e data no rodapé.
- **/beta simplificado:** pede só nome e WhatsApp; o pedido para seguir o @dynoapp.ia foi para o convite e para as boas-vindas no WhatsApp.

Versão publicada: site.css v7, bundle md5 c5d132e8771cc585e3e23e5fcfe06b45.

## LGPD

O titular já consegue baixar e apagar os próprios dados pelo WhatsApp, e o Dyno guarda o mínimo necessário. O que falta é a parte jurídica: CNPJ, encarregado (DPO) e revisão dos Termos e da Política de Privacidade. Os itens abaixo são informação técnica, não parecer jurídico.

### Mapa de dados

| Dado | Onde fica | Finalidade | Retenção |
| --- | --- | --- | --- |
| Nome, WhatsApp, e-mail | Supabase `dyno_usuarios` | Cadastro e atendimento | Enquanto for cliente |
| CPF | Só no Asaas | Cadastro de cliente para cobrança | Regras do Asaas |
| Aceite (data, versão, hash do IP) | Supabase | Prova do consentimento | Enquanto durar o cadastro |
| Pagamentos | Supabase + Asaas | Controle financeiro e fiscal | Em geral 5 anos (confirmar com jurídico) |
| Gastos, tarefas, lembretes, memórias, mensagens | Data tables do n8n | Prestar o serviço | Enquanto for cliente |
| Comprovantes (foto e PDF) | Google Drive | Prova do gasto | Enquanto for cliente |
| Extratos importados | Supabase `dyno_importacoes` | Confirmação antes de gravar | 7 dias |
| Logs técnicos | Supabase `dyno_logs` | Operação e segurança | 7 dias, sem dado pessoal |
| Backups | Google Drive (pasta privada) | Recuperação | 14 dias |

### Direitos do titular

- **Acesso e portabilidade:** a pessoa escreve "meus dados" no WhatsApp e recebe um arquivo JSON com tudo.
- **Eliminação:** a pessoa escreve "CONFIRMO APAGAR MEUS DADOS". O Dyno manda uma cópia antes, apaga as tabelas e os comprovantes, anonimiza o cadastro e remove o cliente no Asaas. Os pagamentos ficam por obrigação fiscal.
- **Cancelamento:** na área do cliente ou pelo WhatsApp, a qualquer momento e sem custo.
- **Consentimento:** o aceite cita os Termos de Uso e a Política de Privacidade antes do CPF.

### Pendências

- [ ] CNPJ, razão social, cidade/UF e encarregado (DPO) nos Termos e na Privacidade
- [ ] Revisão jurídica dos dois textos e da frase de aceite
- [ ] Caixa privacidade@dynoapp.com.br
- [ ] Contratos de operador e avaliação da transferência internacional (Supabase nos EUA, OpenAI)
- [ ] Procedimento de incidente: conter, avaliar risco e comunicar à ANPD e aos titulares no prazo legal

## Segurança da informação

As camadas de rede, banco e aplicação estão protegidas. Falta o endurecimento do sistema operacional, que só dá para fazer com terminal no servidor.

| Camada | O que está aplicado | Falta |
| --- | --- | --- |
| Rede | Firewall da Hostinger (dyno-vps-padrao): só 22, 80, 443, ICMP e portas do jogo. n8n só em 127.0.0.1; Evolution, Postgres e Redis sem porta pública | — |
| Transporte | HTTPS em todos os domínios (Traefik + Let's Encrypt) | — |
| Servidor | Snapshot semanal da Hostinger + backups semanais fora do servidor | SSH só com chave, fail2ban, atualizações automáticas, rotação de logs (script pronto) |
| Banco | RLS em todas as tabelas; funções `security definer` só para `service_role`; o site nunca fala direto com o banco | Supabase no plano gratuito, sem backup automático do banco |
| Segredos | Chaves só nas credenciais do n8n e no ambiente dos containers; nada em código ou chat | Revogar a chave exposta da Telnyx |
| Aplicação | Webhooks com token ou cabeçalho secreto; rate limit no cadastro e no login; código de login de 10 min; sessão com hash; CSP e cabeçalhos de segurança no site | CORS do /dyno-cadastro restrito ao domínio |
| Isolamento de clientes | Toda leitura e gravação filtra por `autor`; comprovante só é entregue ao dono | Migrar para o Supabase com `conta_id` e RLS por cliente |
| Execuções | Cadastro, Asaas e site não guardam execuções; agendados guardam só erros | Retenção de 7 dias no n8n (variáveis de ambiente) |
| Contas | — | 2FA em Hostinger, n8n, Supabase, Asaas, Google e e-mail |

**Backups e recuperação:**

- **Diário, 03:40:** JSON com Supabase e Data tables na pasta privada do Google Drive, guardando os 14 mais recentes.
- **Semanal, pela Hostinger:** snapshot do VPS e backup automático fora do servidor.
- **A cada 5 min, para o servidor reserva** (quando instalado): cópia do n8n, da Evolution e dos projetos, pronta para assumir. Ver `redundancia/README.md`.
- **Pendente:** a chave de criptografia do n8n (N8N\_ENCRYPTION\_KEY) deve ficar num cofre de senhas, porque sem ela as credenciais não abrem num restore. Também vale testar uma restauração completa uma vez.

## Observabilidade

O Daniel recebe no WhatsApp qualquer falha de workflow, mudança de saúde dos serviços e queda vista de fora. Cada alerta é enviado uma vez, sem repetição.

| Sinal | Quem mede | Frequência | Onde fica | Alerta |
| --- | --- | --- | --- | --- |
| Saúde de Supabase, Asaas e WhatsApp | Workflow Saúde (v9JsD02YHFAgmLPE) | 5 min | `dyno_logs` (7 dias) | Só quando muda de estado (2 falhas seguidas); reconecta o WhatsApp sozinho |
| Disponibilidade de n8n, wa. e site, vista de fora | Supabase pg\_cron + pg\_net | 5 min | `dyno_monitor`, `dyno_monitor_quedas` | Queda registrada é avisada em até 10 min |
| Falha de workflow | Erros e alertas (5UUmuzItIYDsd3AG) | A cada erro | `dyno_logs` | WhatsApp, no máximo 1 por erro a cada 15 min, sem telefone na mensagem |
| CPU, memória e disco | Script no servidor → /dyno-infra | 5 min | Supabase | Disco ≥ 85%, memória ≥ 90%, CPU ≥ 95% (1 por hora); script ainda não instalado |
| Negócio: vagas, cadastros, pagamentos | Painel /dyno-painel e `admin resumo` no WhatsApp | Sob demanda | Supabase | — |
| Execuções do n8n | n8n | Contínuo | Banco do n8n | Erros vão para o workflow de erros |

O **painel de observabilidade** fica em n8n.../webhook/dyno-painel e pede um token. Ele mostra:

- vagas e usuários por status;
- cadastros em 24 h e 7 dias, e bloqueios por limite;
- saúde dos serviços e erros recentes;
- CPU, memória e disco;
- pagamentos e situação da retenção.

**Ponto cego:** se o VPS inteiro cair, os alertas só chegam quando ele voltar, porque o WhatsApp sai dele. O UptimeRobot (gratuito, na conta do Daniel) fecharia esse buraco com aviso por e-mail ou aplicativo. Com o **servidor reserva** instalado (`redundancia/`), a queda do VPS faz o reserva assumir em 5 a 7 min, e o aviso "Servidor reserva assumiu" sai pelo WhatsApp do próprio reserva.

## Capacidade e objetivo

A estrutura de hoje aguenta com folga cerca de **300 clientes ativos**, e o teto sem mudanças fica perto de **500**. Os números são estimativas a partir do uso medido em 04/10. A conta considera \~15 mensagens por cliente por dia, mais \~6 mensagens automáticas (relatórios e check-ins). O primeiro gargalo não é o servidor: é o WhatsApp não oficial e o n8n rodando num processo só.

| Recurso | Uso hoje | Limite | Quando aperta |
| --- | --- | --- | --- |
| VPS (4 vCPU, 16 GB) | CPU \~6%, RAM \~6 GB, disco \~40 GB | Dividido com Dynamo Wear e jogo | Acima de \~1.000 clientes |
| n8n (processo único, SQLite) | Poucas execuções por minuto | \~20 a 30 mensagens por minuto no pico, cada uma esperando a OpenAI | \~500 clientes |
| Data tables do n8n | Pequeno | 200 MiB no total | Algumas centenas de clientes por 1 ano (o histórico de mensagens é o que mais cresce) |
| Supabase gratuito | 13 MB | 500 MB de banco | Folgado; o risco é não ter backup automático |
| WhatsApp (Evolution, 1 número) | Família + piloto | Sem limite fixo, mas volume automático alto aumenta o risco de bloqueio | \~300 clientes (\~1.800 mensagens automáticas por dia) |
| OpenAI | Baixo | Limites da conta (sobem com o uso) | Custo, não capacidade |

### Objetivo por fase

| Fase | Meta de clientes | O que a estrutura precisa |
| --- | --- | --- |
| Beta (até 03/12) | 10 vagas + família e cortesias | Nada além do que já existe |
| Lançamento (01/12/2026) | 50 clientes | Dados no Supabase, UptimeRobot, Supabase Pro, VPS renovado |
| 1º semestre de 2027 | 300 clientes | API oficial do WhatsApp, n8n em modo fila (workers + Redis + Postgres) e VPS só do Dyno, prontos antes de chegar a \~150 clientes |

Metas definidas pelo Daniel em 04/10: **50 clientes no lançamento** e **300 clientes no 1º semestre de 2027**. A estrutura de hoje já cobre a meta do lançamento. A de 300 cai exatamente no limite seguro do número não oficial, então a troca para a API oficial e o n8n em fila deve estar pronta no meio do caminho, por volta de 150 clientes, e não depois.

## Planos ofertados e cobrança

O Beta fechado tem 10 vagas, 60 dias grátis e nenhuma cobrança no cadastro. Depois dos 60 dias o plano custa **R$ 19,90/mês** ou **R$ 199,90/ano**, pago só por Pix ou cartão. Quem não quiser continuar sai sem custo.

| Plano | Preço | Para quem | Cobrança |
| --- | --- | --- | --- |
| Beta (teste) | Grátis por 60 dias | 10 vagas, só por convite | Nenhuma; no cadastro o Asaas recebe só o cliente |
| Mensal | R$ 19,90/mês | Quem continua depois do teste | Assinatura no Asaas, Pix ou cartão |
| Anual | R$ 199,90/ano (R$ 16,66/mês; economia de R$ 38,90) | Quem continua depois do teste | Assinatura anual no Asaas, Pix ou cartão |
| Família / cortesia | Sem custo | Daniel, Quézia, Eliezer; cortesias de 60 dias | Nenhuma; não ocupa vaga do Beta |

Todos os planos têm as mesmas funções. O cancelamento é livre, pela área do cliente ou pelo WhatsApp. Não há boleto.

**Jornada do cliente:**

1. Convite: pedido em dynoapp.com.br/beta aprovado pelo Daniel (APROVAR N), comando de admin ou direct do Instagram.
2. Cadastro pelo WhatsApp: nome, e-mail, aceite dos Termos e CPF.
3. O Asaas recebe só o cliente, sem cobrança.
4. Boas-vindas com o vídeo tutorial (40 s).
5. Feedback nos dias 7 e 30.
6. Avisos de fim do teste em D-5, D-1, D0 e D+3. O cliente escolhe mensal ou anual e Pix ou cartão, e aí a assinatura é criada no Asaas.
7. O pagamento confirmado pelo webhook ativa o cliente. Sem escolha, o assistente fica pausado.

**Base em 04/10:**

| Plano | Status | Pessoas |
| --- | --- | --- |
| família (grátis) | ativo | 5 (Daniel, Quézia, Eliezer, Márcia, Marcos) |
| piloto | em teste até 03/12 | 5 (Anderson, Marcelo, Paulo, Felipe, Victor Tavarez) |
| piloto | cancelado | 4 (testes) |

"Em teste" é o status `pendente` do banco: dentro dos 60 dias grátis, atendimento completo, sem pagamento confirmado. Vira `ativo` quando o Asaas confirma o pagamento. Só a exibição no modo admin mudou ("Em teste", e `admin clientes em teste` filtra). Só o Victor tem assinatura anual criada; Márcia e Marcos passaram a ativos sem cobrança; os nomes errados "Eu Quero" e "Sim." viraram Anderson e Marcelo.

Ainda não houve nenhuma cobrança real. O Tavarez mantém a assinatura antiga, com cobrança pendente para 03/12, por decisão do Daniel.

## Mercado: quem faz o mesmo e quanto cobra

Há pelo menos 15 assistentes no WhatsApp ativos no Brasil com proposta parecida com a do Dyno. A maioria cobra entre R$ 12 e R$ 40 por mês. Os que fazem só finanças são mais baratos; os assessores completos ficam perto de R$ 30 por mês.

| Serviço | Foco | Mensal | Anual (por mês) | Teste |
| --- | --- | --- | --- | --- |
| [Meu Assessor](https://meuassessor.com/) | Assessor completo + Open Finance | — | R$ 29,90 | 7 dias |
| [Meu Agente](https://otimizapro.com/meu-agente/) | Assessor completo | R$ 29,90 | R$ 20,93 | 7 dias de arrependimento |
| [Financinha](https://www.financinha.com.br/) | Finanças; Open Finance no plano maior | R$ 29,49 a R$ 39,90 | R$ 29,49 a R$ 39,90 | 7 dias |
| [Focca-Ai](https://focca-ai.com/) | Finanças + lembretes | R$ 24,90 a R$ 59,90 | 20% menos | 5 mensagens |
| [POQT](https://poqt.cloud/pt) | Finanças (diz ter 20 mil usuários) | R$ 20 | R$ 12 | 7 dias |
| [GranaZen](https://poqt.cloud/pt/blog/melhor-bot-financeiro-whatsapp) | Finanças | \~R$ 20 | — | sim |
| [Porquim](https://olhardigital.com.br/2025/09/03/dicas-e-tutoriais/o-que-e-e-como-funciona-o-porquim-ia-no-whatsapp/) | Só gastos (diz ter 3 mil usuários por dia) | R$ 29,90 por trimestre | R$ 5,58 | 7 dias |
| [Jota](https://jota.ai/blog/arquivo/assistente-ia-whatsapp-organizar-dinheiro) | Conta digital + assistente | Grátis | — | — |

Também existem ZapGastos, FalaZuki, FinanBot, Poupa.ai, Zap Mov, SecretárIA e SARA, sem preço público. Preços consultados em 04/10/2026 nos sites; Porquim e GranaZen vêm de artigos de set/2025 e mai/2026.

**Meu Assessor, visto em 04/10 (vídeo com Felipe Titto e telas do cadastro):** vende uma "equipe de assessores de IA" com personagens de nome e rosto (Sofi, Theo, Ítalo, fiscal), cadastro no site em 4 passos (nome, WhatsApp, e-mail, senha) e um plano só, Pro Anual em 12x de R$ 29,90 (cerca de R$ 358,80/ano), com usuários e lembretes ilimitados e garantia de 7 dias. Usa selos de API oficial do WhatsApp, Open Finance, LGPD, "somente leitura" e "+250 mil usuários". Resposta do Dyno: preço cerca de 44% menor, 60 dias grátis, selos só do que é verdade e a dupla Dyno e Dina.

## Planos depois do Beta (proposta)

A proposta são três planos: **Essencial a R$ 14,90**, **Completo a R$ 24,90** e **Premium com Open Finance a R$ 39,90** por mês. Cada um fica abaixo do concorrente direto da sua faixa. O plano anual sai por cerca de 10 meses (2 meses grátis).

|  | Essencial | Completo | Premium (Open Finance) |
| --- | --- | --- | --- |
| Mensal | R$ 14,90 | R$ 24,90 | R$ 39,90 |
| Anual | R$ 149 (R$ 12,42/mês) | R$ 249 (R$ 20,75/mês) | R$ 399 (R$ 33,25/mês) |
| Para quem | Quer só parar de perder o controle dos gastos | Quer um assessor que organiza a vida financeira e a rotina | Quer tudo automático, sem digitar gasto |
| Gastos por texto, áudio e foto | sim | sim | sim |
| Categorias e orçamento com alerta | sim | sim | sim |
| Lembretes que insistem | até 20 ativos | ilimitados | ilimitados |
| Tarefas e listas | sim | sim | sim |
| Resumo semanal e do mês | sim | sim | sim |
| Painel no site (painel e extrato) | sim | sim + comprovantes e ZIP | sim + comprovantes e ZIP |
| Contas a pagar (boleto, PDF) e assinaturas | — | sim | sim |
| Parcelados e recebíveis | — | sim | sim |
| Importar extrato e fatura | — | sim | sim |
| Relatórios do dia e check-ins | — | sim | sim |
| Dashboard em imagem | — | sim | sim |
| Casa e carro, busca de lugares | — | sim | sim |
| Google Agenda (quando lançar) | — | sim | sim |
| Open Finance (lançamentos automáticos) | — | — | até 3 contas ou cartões; R$ 5/mês por conta extra |
| Alertas de saldo baixo e cobrança estranha | — | — | sim |
| Pessoas na conta | 1 | 2 (casal) | até 4 (família) |
| Suporte | WhatsApp | WhatsApp | prioritário |
| Concorre com | POQT, GranaZen (\~R$ 20) | Meu Agente, Meu Assessor (R$ 29,90) | Financinha Open Finance (R$ 39,90), Meu Assessor |

**Por que esses preços**

- **Essencial (R$ 14,90):** porta de entrada abaixo dos bots só de finanças (\~R$ 20), mas sem as funções que custam mais IA (leitura de extrato, relatórios várias vezes por dia).
- **Completo (R$ 24,90):** é o Dyno de hoje, R$ 5 abaixo dos assessores completos. Deve ser o plano mais vendido e o destaque da página de preços.
- **Premium (R$ 39,90):** mesmo preço do Financinha com Open Finance, entregando bem mais funções.

**Cuidados**

- **Fundadores do Beta:** quem entrou no Beta recebeu a promessa de R$ 19,90/mês ou R$ 199,90/ano. A sugestão é dar a eles o plano Completo por esse preço para sempre ("preço de fundador"). Assim a promessa é cumprida e eles viram divulgadores.
- **Custo do Open Finance:** provedores como a Pluggy têm piso perto de R$ 2.500/mês, segundo relatos de desenvolvedores em mai–jun/2026. Isso exige cerca de 80 assinantes Premium só para pagar o provedor. Para começar, valem opções cobradas por conexão (relatos citam Polp, a partir de R$ 159/mês + \~R$ 5 por conexão, e Tecnospeed, R$ 540/mês). Confirmar com cada fornecedor antes de decidir. Fontes: [TabNews, mai/2026](https://www.tabnews.com.br/lucaslagrimante/4e9706bf-05bc-40f5-86f7-62acda248452) e [TabNews, jun/2026](https://tabnews.com.br/GuilhermeVieira/resolvi-o-problema-do-open-finance-caro-que-postei-aqui-achei-uma-alternativa-e-ja-esta-em-producao).
- **Teste grátis:** depois do Beta, 14 dias em vez de 60. O mercado usa 7, e 14 ainda é um diferencial.
- **Custo de IA por cliente:** medir no Beta antes de fechar os preços, para garantir margem no Essencial.
- **Família incluída (decisão do Daniel, 04/10):** o acesso da família vai junto com o plano, e não como pessoa extra paga, porque o cliente sente que está ganhando algo. O Completo inclui o casal, e o Premium até 4 pessoas. Um titular paga e convida os membros pelo WhatsApp; cada membro usa o próprio número e escolhe se os gastos entram na visão da família.

Os preços são uma proposta com base no mercado e precisam da decisão do Daniel e da conta de custos reais.

## Comparativo de funções: Dyno x mercado

O Dyno já cobre 11 das 13 funções comparadas; nenhum concorrente cita mais de 6. As duas que faltam ao Dyno (Google Agenda e Open Finance) são justamente as que os concorrentes mais caros usam para cobrar mais, e as duas estão no roadmap.

| Função | Dyno | Meu Assessor | Meu Agente | Financinha (Open Finance) | Focca+ | POQT | Porquim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Gastos por texto, áudio ou foto | sim | sim | sim | sim | sim | sim | sim |
| Lembretes que insistem até a confirmação | sim | — | — | — | — | — | — |
| Contas a pagar com aviso | sim | — | — | sim | sim | sim | — |
| Orçamento ou meta com alerta | sim | — | — | sim | sim | sim | sim |
| Tarefas e listas | sim | sim | sim | — | — | — | — |
| Google Agenda | planejado | sim | sim | — | sim | — | — |
| Open Finance | planejado (Premium) | sim | — | sim | não | — | não |
| Importar extrato e fatura | sim | — | — | — | — | — | — |
| Painel no site | sim | — | sim | sim | sim | — | — |
| Compartilhar com família ou sócio | sim | sim | sim | sim | sim | sim | — |
| Relatórios automáticos durante o dia | sim | — | — | — | — | — | — |
| Casa e carro (manutenções, km) | sim | — | — | — | — | — | — |
| Guardar comprovantes e documentos | sim | sim | sim | — | — | — | — |
| **Total de funções (de 13)** | **11** | **6** | **6** | **6** | **6** | **4** | **2** |
| Preço mensal comparado | R$ 24,90 (Completo proposto) | R$ 29,90 (anual) | R$ 29,90 | R$ 39,90 | R$ 39,90 | R$ 20 | \~R$ 9,97 (trimestral) |

"—" significa que o site ou o artigo consultado não cita a função; o serviço pode tê-la. "não" significa que o site diz que não tem. O Dyno foi avaliado pelo que existe hoje e os concorrentes pelo que publicam, então a comparação tende a favorecer o Dyno. Os concorrentes têm vantagens que a tabela não mostra: marca conhecida, milhares de usuários, app ou WhatsApp oficial e, no Meu Agente, emissão de contratos e ligações.

## Ranking comparativo

No ranking, o Dyno fica em 1º: tem quase o dobro de funções do segundo colocado e custa menos que os assessores completos. O critério é o número de funções; no empate, ganha quem tem Open Finance e depois o menor preço.

&#91;embedded content: sites dos serviços e artigos consultados em 04/10/2026 · 7 serviços, 13 funções\]

**Onde o Dyno perde hoje:**

- não tem Open Finance nem Google Agenda;
- usa WhatsApp não oficial;
- ainda não tem marca nem base de clientes;
- a operação depende de uma pessoa só.

O plano Premium e a fase 2 do roadmap atacam os três primeiros pontos.

## Roadmap: o que já foi feito

Em 3 dias o Dyno saiu de um assistente da família para um produto multi-cliente com site, cobrança, LGPD e operação monitorada. As entregas estão abaixo, da mais recente para a mais antiga.

| Data | Entrega | Detalhe |
| --- | --- | --- |
| 10/10 | Servidor reserva (pronto para instalar) | Árbitro no Supabase (`dyno_servidor`), agente no principal (batimento, cópia a cada 5 min, cerca), vigia no reserva (assume sozinho, vira o DNS na Cloudflare, volta planejada) e proxy n8n.dynoapp.com.br. Testado de ponta a ponta com dois Docker (`redundancia/teste/simular.sh`) |
| 10/10 | Whisper local em modo sombra | Compose do container `dyno-whisper` (pasta `whisper/`), workflow Dyno \| Whisper modo sombra e tabela `dyno_whisper_sombra`; compara com a OpenAI sem mudar a resposta. Falta instalar o container |
| 05/10 | Alerta de câmbio (dólar e euro) | Cotação PTAX do BC a cada 15 min, até 5 alertas por pessoa; anúncio aos 10 cadastros; seção no site, post e reel no Instagram |
| 04/10 | Dupla Dyno e Dina | Dina (agenda e rotina) e Dyno (dinheiro) no mesmo número, com cabeçalho por voz; apresentada às 3 contas da família |
| 04/10 | Site para vender | Conversa animada, selos, vagas ao vivo, comparativo de preço e seção da dupla |
| 04/10 | Base de clientes revisada | "Em teste" no modo admin; Márcia e Marcos ativos; nomes Anderson e Marcelo corrigidos |
| 04/10 | Conteúdo para o Instagram | Carrossel de 7 slides e 2 Reels (POV da luz e compra no mercado), com versões sem música para áudio do Instagram |
| 04/10 | Dina nos relatórios + card semanal | Bom dia 07:30, check-ins, 12h, 18h e resumo das 06h da família saem como Dina (21h segue Dyno). Domingo 20h: card em imagem da semana no privado, pelo número do Dyno, desenhado pelo serviço interno dyno-render (Gotenberg). Por enquanto só a família recebe. |
| 04/10 | Claude lendo extratos | ia\_documento = claude (Sonnet 5.5), OpenAI de reserva. O Importar extrato chama a IA em camadas. Corrigido: o Sonnet 5.5 não aceita tool\_choice forçado, agora usa auto. Falta teste com PDF real. |
| 04/10 | Jev em modo sombra | ia\_decisao\_modo = sombra. A cada mensagem o Jev classifica intenção, voz e se é simples, sem mudar a resposta; a comparação com o cérebro fica em dyno\_ia\_sombra (sem o texto). Relatório: dyno\_ia\_sombra\_relatorio(7). |
| 04/10 | Pedido do Beta pelo site com aprovação no WhatsApp | dynoapp.com.br/beta: só nome e WhatsApp; aviso ao Daniel; APROVAR N gera o convite e envia ao cliente; seguir @dynoapp.ia vai no convite e nas boas-vindas |
| 04/10 | IA em camadas e medição de custo | OpenAI, Claude e Jev conectados; custo por chamada em dyno\_ia\_uso |
| 04/10 | Importar extrato e fatura | PDF, CSV, OFX ou Excel pelo WhatsApp; IA lê, tira duplicados e grava após IMPORTAR |
| 04/10 | Painel: Extrato, Comprovantes e limites | Filtros, CSV, galeria, ZIP; barra de limite onde há orçamento |
| 04/10 | Relatórios do dia e check-ins | 07:30, 12h, 18h, 21h + check-ins 10h e 14h12 |
| 04/10 | Backup diário e monitor externo | Drive (14 dias) + vigia pelo Supabase a cada 5 min |
| 04/10 | Feedback do piloto e LGPD pelo WhatsApp | Perguntas nos dias 7 e 30; baixar e apagar meus dados |
| 04/10 | Cobrança sem boleto no cadastro | Escolha de plano e Pix/cartão só no fim do teste |
| 04/10 | Cortesia e vídeo tutorial | Plano família para Marcos e Márcia; vídeo de 40 s nas boas-vindas |
| 04/10 | Fase 2 multi-cliente | Identidade no Supabase, dados isolados por autor, agendados por destino |
| 04/10 | Site dynoapp.com.br e área do cliente | Login por código, painel, conta, plano, cancelamento |
| 04/10 | Modo administrador | Convites, resumo e consultas pelo WhatsApp do Daniel |
| 04/10 | Evolution dedicada | wa.dynoapp.com.br, separada da Dynamo Wear (fim das quedas) |
| 04/10 | Endurecimento do VPS | Firewall, snapshot, portas fechadas |
| 04/10 | Preços novos | R$ 19,90/mês ou R$ 199,90/ano |
| 03/10 | Cadastro, Asaas e webhook em produção | Convites, vagas, rate limit, idempotência |
| 03/10 | Segurança e observabilidade | RLS, logs de 7 dias, saúde a cada 5 min, alertas de erro, painel |
| 03/10 | Extras | Notas, listas, parcelados, recebíveis, desfazer, Excel, tarefas por projeto |
| 03/10 | Dashboard financeiro em imagem | PNG por período |
| 02/10 | Agentes de contas, assinaturas, casa e carro | Lembretes automáticos e baixa com despesa |
| 02/10 | Lembretes que insistem, orçamentos, resumo semanal, 6h | Insistência inicial de 10 em 10 min, alertas de 80% e 100% |
| 02/10 | MVP no ar | Cérebro com OpenAI, gastos por texto, áudio e foto, tarefas, memória |

## Roadmap: o que falta

O que falta está em 4 fases, com lançamento aberto em 01/12/2026. Cada fase só avança depois de passar pelo seu portão.

&#91;embedded content: Roadmap do Dyno · 4 fases e seus portões\]

### 1. Agora (5 a 9 de outubro)

- [ ] Renovar o VPS e ligar a renovação automática (vence 09/10)
- [ ] Teste real da importação de extrato: mandar um PDF com a legenda *extrato*
- [ ] Teste real do login do site com o Daniel e um piloto
- [ ] Teste real no Asaas: criar e cancelar uma assinatura anual
- [ ] Rodar o script de endurecimento no Terminal do hPanel e cadastrar a chave SSH
- [ ] Criar o UptimeRobot (n8n /healthz e wa.dynoapp.com.br)
- [ ] Revogar a chave da Telnyx
- [ ] Desligar a página de cadastro temporária (BFmfbtTei9fQCgCB) e sair dos grupos da Dynamo Wear no número do Dyno

### 2. Base sólida (10 a 31 de outubro)

- [ ] Migrar o que sobrou das Data tables para o Supabase: manutenções, veículos, rotina, extras e devocional (mensagens, memórias, transações, tarefas, lembretes, contas, orçamentos e assinaturas já migrados em 05/10)
- [ ] Ambiente de testes (cópia dos workflows principais com um número de teste)
- [ ] Fixar a versão do n8n e ligar a retenção de execuções de 7 dias numa janela de manutenção
- [ ] Abrir o CNPJ, preencher razão social e encarregado (DPO), e fazer a revisão jurídica de Termos e Privacidade
- [ ] Atualizar o site: Preços ("Pix ou cartão"), Termos e Privacidade
- [ ] E-mails suporte@ e privacidade@dynoapp.com.br, com SPF, DKIM e DMARC
- [ ] Restringir o CORS do `/webhook/dyno-cadastro` ao domínio
- [ ] Resumo semanal (card em imagem) para os clientes — já sai pelo número do Dyno, falta liberar para além da família
- [ ] IA em camadas: Jev (TypeSafe) para decisões rápidas como intenção, categoria e duplicado; Claude e OpenAI para conversa e documentos; OpenAI para áudio. Começar em modo sombra (só compara, não age) e incluir os novos fornecedores no mapa de dados da LGPD

### 3. Produto (novembro)

- [ ] Agente de agenda (Google Agenda; falta a credencial)
- [ ] Busca de lugares pelo Google Places (falta a chave)
- [ ] Open Finance com Pluggy, depois do Beta e com contrato
- [ ] Memória semântica com pgvector
- [ ] Instagram do Dyno conectado e teaser publicado
- [ ] Coletar e aplicar o feedback dos dias 7 e 30
- [ ] Preencher as 10 vagas do piloto (hoje 5 livres)
- [ ] Decidir os 3 planos pós-Beta (Essencial, Completo, Premium) e os preços, com o custo real de IA por cliente medido no Beta
- [ ] Cotar Open Finance por conexão (Polp, Tecnospeed, Pluggy) e escolher o provedor do Premium
- [ ] Plano no sistema: coluna de plano com limites (lembretes, pessoas, contas conectadas) e bloqueio das funções fora do plano no cérebro
- [ ] Asaas com os 3 valores (mensal e anual) e preço de fundador R$ 19,90 para quem veio do Beta
- [ ] Conta com membros: titular paga, convida a família pelo WhatsApp (até 2 no Completo e 4 no Premium), visão da família com gastos compartilhados ou privados

### 4. Lançamento (dezembro)

- [ ] Lançamento aberto em 01/12
- [ ] Conversão do Beta: os testes de Anderson, Marcelo, Paulo, Felipe e Victor Tavarez vencem em 03/12 (Márcia e Marcos já são família, sem cobrança)
- [ ] Decidir sobre a API oficial do WhatsApp (Meta) antes de crescer
- [ ] Mover o Dyno para um VPS próprio ou separar Dynamo Wear e o jogo
- [ ] Supabase Pro antes de ter clientes pagantes
- [ ] Ligações para lembretes importantes (Twilio), adiadas por decisão do Daniel
- [ ] Lançar com Essencial e Completo; liberar o Premium quando o Open Finance estiver pronto
- [ ] Página de preços do site com os 3 planos, Completo em destaque e teste de 14 dias
- [ ] Trocar de plano pela área do cliente e pelo WhatsApp

### Funções planejadas (ordem atualizada em 06/10)

Ver `docs/FUNCIONALIDADES-E-ROADMAP.md`: card semanal para todos, edição pelo WhatsApp, previsão do mês, cartão de crédito, categorias próprias, metas, agenda, boas-vindas guiadas, edição no painel, modo casal, pgvector, Google Agenda e áudio longo (adiado).

## Riscos e pendências imediatas

O maior risco agora é o VPS vencer em 09/10 com a renovação automática desligada: se ele cair, tudo para (WhatsApp, n8n e site).

| Risco | Impacto | O que fazer |
| --- | --- | --- |
| VPS vence em 09/10 sem renovação automática | Dyno inteiro fora do ar | Renovar no hPanel e ligar a renovação automática |
| Tudo num único servidor, dividido com Dynamo Wear e jogo | Uma falha derruba tudo | Servidor reserva em outro provedor com virada automática (`redundancia/`, pronto para instalar desde 10/10); separar a Dynamo Wear e o jogo antes de escalar |
| WhatsApp não oficial (Evolution) | Bloqueio do número pela Meta | Sem mensagens frias; avaliar a API oficial antes do lançamento |
| Dados do assistente nas Data tables do n8n | Limite de 200 MiB, sem backup próprio do banco, consultas lentas | Migrar para o Supabase |
| Imagem do n8n sem versão fixa | Atualização surpresa ao reimplantar | Fixar a versão numa janela de manutenção |
| Supabase no plano gratuito (confirmado) | Sem backup automático do banco; projeto pausa sem uso | Backup diário já cobre; Pro antes de clientes pagantes |
| Termos e Privacidade sem CNPJ e sem revisão | Risco jurídico na cobrança | Abrir CNPJ e fazer revisão jurídica |
| Chave da Telnyx exposta no chat | Uso indevido | Revogar ou apagar a conta |
