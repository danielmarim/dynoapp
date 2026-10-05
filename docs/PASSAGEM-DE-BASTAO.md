# Dyno — Passagem de bastão (05/10/2026)

Leia este arquivo primeiro. Ele resume o estado do projeto e diz onde está cada coisa. O detalhe completo está em `DOCUMENTACAO-TECNICA.md` (exportado do documento principal).

> **Para a IA que continuar o projeto:** responda em português, de forma concisa. Siga a seção "Regras que não podem ser quebradas". Nunca peça nem repita senhas ou chaves no chat: o Daniel cria as credenciais no n8n e passa só o nome delas.

---

## 1. O que é

- **Dyno**: assessor pessoal que funciona só pelo WhatsApp. Duas vozes no mesmo número:
  - **Dyno** (💰): dinheiro — gastos, receitas, contas, extrato, orçamentos, relatórios, conta/plano/LGPD.
  - **Dina** (⏰): agenda e rotina — lembretes, tarefas, listas, compromissos, check-ins.
- **Dono**: Daniel Ricardo Marim. Empresa: DM OBSERVAIT SOLUCOES EM TECNOLOGIA LTDA, CNPJ 65.176.391/0001-45.
- **Número do Dyno**: +55 11 93949-7178 (instância `dyno`). Site: https://dynoapp.com.br. Instagram: @dynoapp.ia.
- **Fase**: Beta fechado, 10 vagas, 60 dias grátis. Depois: **R$ 19,90/mês** ou **R$ 199,90/ano**. Lançamento previsto para 01/12/2026 (meta 50 clientes); meta de 300 clientes no 1º semestre de 2027.

## 2. Arquitetura em uma linha

WhatsApp → Evolution API (wa.dynoapp.com.br) → **n8n** (identifica o cliente no **Supabase**) → **OpenAI** interpreta e devolve resposta + ações → n8n grava e responde. Comprovantes no Google Drive. Cobrança no **Asaas**.

## Repositório

Código e documentação no GitHub (privado): https://github.com/danielmarim/dynoapp — branch `main`, primeiro push em 05/10/2026. Cópia local do Daniel: `H:\Claude\MVP - DynoApp\dynoapp-repo`. Os workflows do n8n ainda precisam ser exportados: baixar pela interface do n8n para `n8n/_download/` e rodar `python n8n/limpar_export.py` (ver `n8n/README.md`).

## 3. Onde está cada coisa

| Peça | Onde | Observação |
|---|---|---|
| Lógica (workflows) | n8n em https://n8n.srv1825327.hstgr.cloud | Projeto pessoal do Daniel. Lista na seção 5 |
| Banco | Supabase, projeto `xvekgnbneeokihtjpbts` (us-east-2), plano gratuito | Tabelas `dyno_*`, funções RPC `dyno_*` |
| Dados do dia a dia do assistente | Data tables do n8n (`assessor_transacoes`, `assessor_lembretes`, `assessor_tarefas`, `assessor_contas`, `assessor_orcamentos`, `assessor_mensagens`, ...) | Ainda não migradas para o Supabase |
| Servidor | VPS Hostinger srv1825327 (KVM 4, IP 77.37.41.74), id da VM 1825327 | **Vence em 09/10/2026 com renovação automática desligada** |
| WhatsApp do Dyno | Docker `evolution-dyno` (instância `dyno`) | Painel: wa.dynoapp.com.br/manager |
| Site | Docker `dyno-site` (nginx). Na inicialização baixa o site do Supabase (RPC `dyno_site_bundle`) | Fonte do site: pasta `site/` deste pacote |
| Imagens (cards) | Docker `dyno-render` (Gotenberg 8), só na rede interna `n8n_default` | `http://dyno-render:3000/forms/chromium/screenshot/html` |
| Arquivos | Google Drive (conta oficialdynamowear): "Meu Assessor - Comprovantes" e "Dyno - Backups (privado)" | Backup diário 03:40, 14 dias |
| Cobrança | Asaas (credencial `asaas-prod`, webhook com token) | |
| Documentação viva | Claude Doc "Dyno — Documentação técnica e Roadmap" + docs do projeto no claude.ai | Cópia em `DOCUMENTACAO-TECNICA.md` |

**Número antigo desligado (05/10/2026):** o Assessor não atende nem envia mais pelo número pessoal do Daniel (5511930851325, instância `pesquisa-aereo` da Evolution da Dynamo Wear). O cérebro descarta o que chega dessa instância (nó "Identificar remetente"), os alertas ao Daniel saem pelo número do Dyno e os nós antigos de envio por `pesquisa-aereo` estão desativados. O número 5511930851325 segue cadastrado como o Daniel (usuário e administrador). O webhook da instância `pesquisa-aereo` na Evolution da Dynamo Wear ainda aponta para `/webhook/assessor-whatsapp`; pode ser apagado no painel dessa Evolution.

O mesmo VPS também roda a Dynamo Wear (Evolution `evolution`, Chatwoot) e um servidor de Project Zomboid (parado em 05/10; exclusão definitiva pendente, o Daniel faz no hPanel). **Não mexer neles.**

## 4. Credenciais (só os nomes — os valores estão no n8n/Hostinger)

No n8n (Header Auth): `Supabase_Dyno`, `evolution-dyno`, `anthropic-dyno`, `jev-typesafe`, `asaas-prod`, `asaas-access-token`, `Google Places`, `Evolution pesquisa-aereo`. OpenAI: credencial **`openai-dyno`** (projeto DynoApp na OpenAI, limite US$ 20/mês, alertas 80% e 100%) desde 05/10/2026 — usada no cérebro (conversa, áudio, busca), na reflexão das 6h e na camada de IA. A variável `OPENAI_API_KEY` do n8n continua existindo para o DMChat (Dynamo), mas o Dyno não a usa mais. Google Drive: OAuth2.

## 5. Workflows do Dyno (n8n)

| ID | Nome | O que faz |
|---|---|---|
| YFgP2bYqeHbQc5t1 | WhatsApp (cérebro) | Atendimento: áudio, foto, PDF, IA, ações, resposta Dyno/Dina |
| XRsXyav6ICD921Q8 | WhatsApp clientes (cadastro por convite) | Porta de entrada de toda mensagem; cadastro e repasse ao cérebro |
| Xbdnisj9AjKJFYAF | Lembretes e mensagem das 6h | Lembretes a cada minuto (insistem a cada 30 min, até 6x, apagando o aviso anterior; ver `docs/LEMBRETES-INSISTENCIA.md`) + resumo 06:00 da família |
| 9VTi7hePHvXOvYrW | Relatórios do dia e check-ins | 07:30, 10:00, 12:00, 14:12, 18:00 (Dina) e 21:00 (Dyno) |
| Z2heNCM6hmMq0PZ0 | Resumo semanal individual | Domingo 20h, card em imagem (Dina). **Hoje só a família** |
| qHNQDuOeWVg7EyZq | Dashboard financeiro (imagem) | Dashboard PNG sob pedido |
| yBCWxnd2N9d3uDxM | Importar extrato | Extrato/fatura (PDF, CSV, OFX, Excel) lido pelo **Claude**, confirma antes de gravar |
| mOXAwF2cZ8zbYs2j | IA em camadas | Escolhe OpenAI/Claude/Jev por `dyno_config` |
| Yw7mI0ybOITBwJoQ | Jev modo sombra | Jev classifica cada mensagem, grava em `dyno_ia_sombra` |
| K4GH2JArrLnZbJAG | Extras | Notas, parcelados, recebíveis, desfazer, Excel |
| 4sWI6Gs5o7AAR59R | Extras diários | 09:30 parcelas e tarefas atrasadas |
| 2mEE5d9YWcgutRbD | Agentes diários | 09:00 assinaturas, manutenções, km do carro |
| nslhB7FRnKuAOPuf | API do site | Login por código, área do cliente, contador de vagas |
| QwETMN0WuCbOmSRO | Cadastro e cobrança | Cadastro pelo site + Asaas |
| FAxcJprGwlZAyKhw | Asaas webhook | Pagamentos → status do cliente |
| WNefuC4RhAAfS3Vs | Enviar convite pelo admin | Comando do Daniel no WhatsApp |
| BBRCGBQtIX8waiqL | Lembrete de cadastro incompleto | A cada hora |
| 3jEnG5ZmIFf16JGS | LGPD do titular | Baixar e apagar dados |
| ssmh5caNcmvqPBSD | Backup diário e monitor externo | 03:40 backup no Drive |
| v9JsD02YHFAgmLPE | Saúde | Health check a cada 5 min, reconecta WhatsApp |
| 5UUmuzItIYDsd3AG | Erros e alertas | Workflow de erro de todos |
| j3WSfca0UXb06SeW | Painel e infraestrutura | Observabilidade |
| BFmfbtTei9fQCgCB | Página de cadastro (temporária) | **Pode ser desligada** |
| 0NTpUwVxsZFMm8Li | TESTE IA em camadas | Manual, desligado |
| asdiDsXdGoWC7Bip | Alerta de câmbio | A cada 15 min (seg–sex 9h–18h): dólar/euro (PTAX do BC; AwesomeAPI se tiver chave) e dispara alertas. Ver `ALERTA-DE-CAMBIO.md` |

Além desses, há 3 desligados de setup/teste: Setup Evolution (LsVMn71OPQmyc4Mz), TEMP limpeza de testes (uOt8WPfaI5lk6PT2) e TESTE Google Places (uodpCgu2VBUwqbO4). Total: 28 do Dyno, 24 ativos.

**Faça agora:** exporte os workflows pela interface do n8n para `n8n/_download/` e rode `python n8n/limpar_export.py`. O script só aceita os "Dyno |" (o n8n também tem os da Dynamo Wear e outros), troca o `SEGREDO`, tira `pinData` e barra arquivos com cara de chave. É o backup da lógica.

## 6. Configuração de IA (tabela `dyno_config`)

| Chave | Valor hoje |
|---|---|
| ia_conversa | openai (gpt-5.6-luna) |
| ia_documento | **claude** (claude-sonnet-5-5), OpenAI de reserva |
| ia_simples | openai |
| ia_decisao_modo | **sombra** (Jev observa, não decide) |

- Custos por chamada: tabela `dyno_ia_uso`; relatório `select dyno_ia_custos(7);`.
- Jev em sombra: `select dyno_ia_sombra_relatorio(7);`. Desligar: `update dyno_config set valor='desligado' where chave='ia_decisao_modo';`
- O Claude Sonnet 5.5 **recusa `tool_choice` forçado**; a camada usa `auto`.

## 7. Clientes (05/10/2026)

- **Família, grátis (ativos)**: Daniel, Quézia, Eliezer (grupo "DYNO Assessor Pessoal") + Márcia e Marcos (contas privadas).
- **Em teste até 03/12** (`status = 'pendente'` no banco = em teste, com acesso completo): Anderson, Marcelo, Paulo, Felipe, Victor Tavarez (único com assinatura anual no Asaas). Paulo e Victor ainda não usaram.
- Vagas do Beta: 5 livres de 10.
- Comandos de admin pelo WhatsApp do Daniel começam com `admin` (ex.: `admin resumo`, `admin clientes em teste`, convite). Detalhes em `DOCUMENTACAO-TECNICA.md`.

## 8. Como publicar o site

A fonte está em `site/`. O `build.py` gera `site/www/`. O container baixa o site do Supabase quando reinicia.

1. `python3 build.py` (gera `www/`).
2. Montar o pacote: pasta com `www/` e `templates/` → `tar czf bundle.tgz www templates` → `base64 -w0 bundle.tgz`.
3. No Supabase: `update dyno_site_bundle set conteudo = '<base64>' where id = 1;` (a função RPC `dyno_site_bundle` devolve esse conteúdo).
4. Reiniciar o projeto Docker `dyno-site` no painel da Hostinger e esperar ~1 min.

O segredo do cabeçalho `X-Dyno-Site` fica só no ambiente do container (`SITE_SECRET`) e numa constante do nó "Preparar" do workflow API do site. Os scripts em `site/n8n/` usam o marcador `__SEGREDO__` no lugar dele — nunca coloque o valor real em arquivo.

## 9. Regras que não podem ser quebradas

1. Nunca escrever, pedir ou repetir chaves e senhas no chat ou em arquivos.
2. Não enviar mensagem para clientes, nem publicar nada, sem o Daniel aprovar o texto e os destinatários.
3. Nada de mensagem "fria" pelo número do Dyno (risco de bloqueio): só convites ou envios que o Daniel pedir.
4. O devocional (PDF) é licenciado: nunca enviar, citar ou narrar; a reflexão das 06:00 é original e só vai para o grupo da família.
5. No n8n, uma execução manual por API/MCP **envia de verdade**: desative os nós de envio antes de testar.
6. Não reimplantar o projeto Docker `n8n` (a imagem não tem versão fixa e o arquivo tem segredos). Só reiniciar quando necessário.
7. No Supabase, a palavra `DELETE` literal pode ser bloqueada por ferramentas; usar `'de'||'lete'` em `execute` quando preciso.
8. Não dar conselho jurídico ou financeiro como se fosse profissional.

## 10. Pendências (ordem sugerida)

1. **Renovar o VPS antes de 09/10** (se cair, para tudo).
2. Exportar os workflows do n8n (seção 5).
3. Decidir se o card semanal vai para os clientes em teste (mudar a constante `PESSOAS` em "Montar resumo de cada pessoa" ou usar `dyno_assessor_destinos()`).
4. Teste real: extrato em PDF pelo WhatsApp (Claude), login no site, assinatura anual no Asaas (criar e cancelar).
5. Conferir se o lembrete do café das 8:30 chega como Dina.
6. Revogar a chave antiga da Telnyx; script de endurecimento do VPS; UptimeRobot.
7. Validar nome no cadastro (recusar "sim", "eu quero", "ok").
8. Apresentar a Dina aos clientes em teste (texto precisa de aprovação).
9. LGPD: incluir Anthropic e TypeSafe no mapa de dados e na Política de Privacidade; SPF/DKIM/DMARC do e-mail.
10. Câmbio: chave grátis da AwesomeAPI (credencial `awesomeapi`) e teste real do alerta pelo WhatsApp. Site, post e reel do alerta já publicados/entregues em 05/10.
11. Site: grade "o que pedir", objeções no FAQ, botão flutuante.
12. Em ~11/10: ler o relatório de custos de IA e o relatório do Jev em sombra; se o Jev acertar >95% com confiança alta, usar ele para mandar mensagens simples a um modelo mais barato.

## 11. Conteúdo deste pacote

| Pasta | O quê |
|---|---|
| `PASSAGEM-DE-BASTAO.md` | Este arquivo |
| `DOCUMENTACAO-TECNICA.md` | Documento principal completo (arquitetura, banco, LGPD, segurança, roadmap, mercado) |
| `site/` | Fonte do site: `build.py`, `www/` gerado, `templates/` (nginx), `deploy/`, scripts do workflow da API (`n8n/`) |
| `card-semanal/` | Modelo HTML do card da semana (`tpl.js`) e o código do nó do n8n (`montar.js`) |
| `videos/` | Projetos HyperFrames dos vídeos (sem os MP4 renderizados): promo do Beta, vinheta, tutorial, reels "POV luz" e "mercado", destaques |
