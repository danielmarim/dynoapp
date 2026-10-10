# Dyno — Passagem de bastão (atualizado em 10/10/2026; base de 07/10 + `ATUALIZACAO-2026-10-10.md`)

Leia este arquivo primeiro. Ele resume o estado do projeto e diz onde está cada coisa. O detalhe completo está em `DOCUMENTACAO-TECNICA.md` (exportado do documento principal). **O que mudou depois de 07/10 está em `ATUALIZACAO-2026-10-10.md`**; quando houver contradição, vale o mais recente.

> **Para a IA que continuar o projeto:** responda em português, de forma concisa. Siga a seção "Regras que não podem ser quebradas". Nunca peça nem repita senhas ou chaves no chat: o Daniel cria as credenciais no n8n e passa só o nome delas.

---

## 1. O que é

- **Dyno**: assessor pessoal que funciona só pelo WhatsApp. Duas vozes no mesmo número:
  - **Dyno** (💰): dinheiro — gastos, receitas, contas, extrato, orçamentos, relatórios, conta/plano/LGPD.
  - **Dina** (⏰): agenda e rotina — lembretes, tarefas, listas, compromissos, check-ins.
- **Dono**: Daniel Ricardo Marim. Empresa: DM OBSERVAIT SOLUCOES EM TECNOLOGIA LTDA, CNPJ 65.176.391/0001-45.
- **Número do Dyno**: +55 11 93949-7178 (instância `dyno`). Site: https://dynoapp.com.br. Instagram: @dynoapp.ia.
- **Fase**: Beta fechado (20 vagas, 60 dias grátis). **Planos:** Essencial R$ 9,90/mês (99,90/ano), Completo R$ 19,90 (199,90), Premium R$ 39,90 (399,90). Gating dos planos desde 07/10: a trava vale só para assinatura ativa; teste grátis e família usam tudo. Lançamento previsto para 01/12/2026; meta de 150 clientes pagantes até 07/2027 (`dyno_config.meta_clientes_pagantes`).
- **Contatos:** suporte@dynoapp.com.br (caixa real, criada em 07/10; resposta em 24 h) e privacidade@dynoapp.com.br (DPO, só LGPD). `no-reply@` não é caixa.

## 2. Arquitetura em uma linha

WhatsApp → Evolution API (wa.dynoapp.com.br) → **n8n** (identifica o cliente no **Supabase**) → **OpenAI** (gpt-6-luna para todos desde 07/10; imagens em gpt-5.6-luna) interpreta e devolve resposta + ações → n8n grava e responde. Comprovantes no **Supabase Storage** (bucket privado `comprovantes`, desde 07/10). Cobrança no **Asaas**.

## Repositório

Código e documentação no GitHub (privado): https://github.com/danielmarim/dynoapp — branch `main`, primeiro push em 05/10/2026. Cópia local do Daniel: `H:\Claude\MVP - DynoApp\dynoapp-repo`. Em 10/10 o `site/` passou a espelhar a produção (pacote-base + overlay) e dois workflows foram reexportados; o resto do `n8n/` segue como em 08/10 (ver `ATUALIZACAO-2026-10-10.md`).

**Como o Daniel quer trabalhar (06/10):** a IA **não faz push** no GitHub. Ela entrega um **.zip com os arquivos alterados** e o Daniel sobe manualmente. Mudanças em **produção** (n8n, Supabase, site por overlay, Hostinger) a IA pode fazer direto na sessão, respeitando as regras abaixo.

## 3. Onde está cada coisa

| Peça | Onde | Observação |
|---|---|---|
| Lógica (workflows) | n8n em https://n8n.srv1825327.hstgr.cloud | Projeto pessoal do Daniel. Lista na seção 5 |
| Banco | Supabase, projeto `xvekgnbneeokihtjpbts` (us-east-2), plano gratuito | Tabelas `dyno_*`, funções RPC `dyno_*`. Desde 07/10 `anon`/`authenticated` não têm acesso a nenhuma tabela |
| Dados do dia a dia do assistente | Supabase (`dyno_transacoes`, `dyno_contas`, `dyno_lembretes`, `dyno_tarefas`, `dyno_mensagens`, ...) | Data tables do n8n só para extras, veículos, manutenções e listas |
| Comprovantes | Supabase Storage, bucket privado `comprovantes`, `<cliente>/<AAAA>/<MM>/...`; índice em `dyno_comprovantes` | Cópias antigas ainda no Drive |
| Servidor | VPS Hostinger srv1825327 (KVM 4, IP 77.37.41.74), id da VM 1825327 | Conferir renovação (vencia em 09/10/2026) |
| WhatsApp do Dyno | Docker `evolution-dyno` (instância `dyno`) | Painel: wa.dynoapp.com.br/manager |
| Site | Docker `dyno-site` (nginx). Na inicialização baixa o site do Supabase (RPC `dyno_site_bundle`) e aplica o overlay `dyno_site_files` | Fonte do site: pasta `site/` deste repositório (espelha a produção desde 10/10; ver `site/NOTA-PRODUCAO.md`) |
| Imagens (cards) | Docker `dyno-render` (Gotenberg 8), só na rede interna `n8n_default` | `http://dyno-render:3000/forms/chromium/screenshot/html` |
| Backups | Google Drive (conta oficialdynamowear): "Dyno - Backups (privado)" | Backup diário 03:40, 14 dias |
| Cobrança | Asaas (credencial `asaas-prod`, webhook com token) | |
| E-mail | Hostinger Mail: caixas `suporte@` e `privacidade@`; credencial n8n `SMTP account` (suporte@, smtp.hostinger.com:465) | Usada pelo fluxo de avisos ao Daniel |
| Documentação viva | Docs do projeto no claude.ai (pastas `dyno/`, `plataforma/`, `dyno-business/` etc.; índice em `00-indice/LEIA-ME.md`) + Claude Doc "Dyno — Documentação técnica e Roadmap" | Os docs antigos ainda citam `claude/...` |

**Número antigo desligado (05/10/2026):** o Assessor não atende nem envia mais pelo número pessoal do Daniel (5511930851325). O cérebro descarta o que chega dessa instância, os alertas ao Daniel saem pelo número do Dyno. O número 5511930851325 segue cadastrado como o Daniel (usuário e administrador).

O mesmo VPS também roda a Dynamo Wear (Evolution `evolution`, Chatwoot) e um servidor de Project Zomboid. **Não mexer neles.**

## 4. Credenciais (só os nomes — os valores estão no n8n/Hostinger)

No n8n (Header Auth): `Supabase_Dyno`, `evolution-dyno`, `anthropic-dyno`, `jev-typesafe`, `asaas-prod`, `asaas-access-token`, `Google Places`, `dyno-site` (cabeçalho `X-Dyno-Site` do site). OpenAI: `openai-dyno` (projeto DynoApp, limite US$ 20/mês). Google Drive: OAuth2. SMTP: `SMTP account` (suporte@).

## 5. Workflows do Dyno (n8n)

Nomes atuais no n8n: "Dyno | …" para os do produto, "Dyno Plataforma | …" para os de infraestrutura e "Dyno Business | …" para o Business (renomeados em 10/10). Os IDs não mudaram.

| ID | Nome | O que faz |
|---|---|---|
| YFgP2bYqeHbQc5t1 | WhatsApp (cérebro) | Atendimento: áudio, foto, PDF, IA, ações, resposta Dyno/Dina. Várias contas Google (10/10) |
| XRsXyav6ICD921Q8 | WhatsApp clientes (cadastro por convite) | Porta de entrada; cadastro e repasse ao cérebro |
| Xbdnisj9AjKJFYAF | Lembretes e mensagem das 6h | Lembretes a cada minuto (1 aviso + 1 insistência após 1h) + resumo 06:00 da família |
| 9VTi7hePHvXOvYrW | Relatórios do dia e check-ins | Bom dia, meio-dia, tarde e noite; inclui "Agenda de hoje" (Dyno + Google) |
| Z2heNCM6hmMq0PZ0 | Resumo semanal individual | Domingo 20h, card em imagem (família e clientes) |
| qHNQDuOeWVg7EyZq | Dashboard financeiro (imagem) | Dashboard PNG sob pedido |
| yBCWxnd2N9d3uDxM | Importar extrato | Extrato/fatura lido pelo Claude, confirma antes de gravar |
| mOXAwF2cZ8zbYs2j | IA em camadas | Escolhe OpenAI/Claude/Jev por `dyno_config` |
| Yw7mI0ybOITBwJoQ | Jev modo sombra | Jev classifica cada mensagem, grava em `dyno_ia_sombra` |
| K4GH2JArrLnZbJAG | Extras | Notas, parcelados, recebíveis, desfazer, Excel |
| 4sWI6Gs5o7AAR59R | Extras diários | 09:30 parcelas e tarefas atrasadas |
| 2mEE5d9YWcgutRbD | Agentes diários | 09:00 assinaturas, manutenções, km do carro |
| nslhB7FRnKuAOPuf | API do site | Login por código, área do cliente, vagas, edição, comprovantes (Storage), avaliação em estrelas, aba Categorias (10/10) |
| g3LNovUOFKNt2IoC | Site: edição | Editar lançamentos/contas/lembretes pela área do cliente |
| 3iZpB1Sku6OVZUB1 | Google Agenda (sub-workflow) | listar/criar/editar/remover eventos; várias contas por cliente (10/10) |
| Jfu2kYsVxFkUjCzb | Cartões visuais (fluxo e parcelados) | Imagem 1080x1350 sob pedido |
| 8hZuNWjGcnjZV61O | Boas-vindas guiadas | Diário 10:30, 7 dicas nos 7 primeiros dias |
| FAxcJprGwlZAyKhw | Asaas webhook | Pagamentos → status do cliente |
| WNefuC4RhAAfS3Vs | Enviar convite pelo admin | Comando do Daniel no WhatsApp |
| BBRCGBQtIX8waiqL | Rotina horária | Cadastro incompleto, feedback dos dias 7 e 30, conversão do teste |
| 3jEnG5ZmIFf16JGS | LGPD do titular | Baixar e apagar dados (25 tabelas, Storage, Google, Asaas; todas as contas Google desde 10/10) |
| ssmh5caNcmvqPBSD | Backup diário e monitor externo | 03:40 backup no Drive; monitor a cada 10 min |
| v9JsD02YHFAgmLPE | Saúde | Health check a cada 5 min, reconecta WhatsApp |
| 5UUmuzItIYDsd3AG | Erros e alertas | Workflow de erro de todos |
| j3WSfca0UXb06SeW | Painel e infraestrutura | Observabilidade |
| asdiDsXdGoWC7Bip | Alerta de câmbio | Dólar/euro, seg–sex 9h–18h |
| 0c0ENHq0dDm8j81a | Agente: revisão diária das conversas | 07:00, relatório de qualidade ao Daniel |
| TdRC9l6KUJt63rB4 | Agente: custos de IA | 07:05, custo por cliente/modelo do dia anterior |
| jSWnrLfSeGaPrxvG | Agente: faxina financeira | Domingo 19:00, sugestões AJUSTAR/IGNORAR ao cliente |
| SxlvfszApKNjPMdn | Avisos ao Daniel | A cada 2 min: novo cliente, avaliações e feedback (WhatsApp + e-mail suporte@) |
| BFmfbtTei9fQCgCB, QwETMN0WuCbOmSRO | Página de cadastro temporária; cadastro e cobrança antigo | **Desativados em 07/10** |

Desde 08/10 há outros (rastreio de encomendas 17TRACK, agentes de assinaturas, documentos, promessas, pedidos de função e fábrica de conteúdo, bom dia personalizado, fila de envios, mensagens pós-cadastro, tempo e contatos, Dyno Business). A lista completa e atual está no n8n (tags `dyno`, `plataforma`, `dyno-business`).

**Backup da lógica:** `n8n/workflows/` neste repositório (ver `n8n/README.md` para o que está atualizado).

## 6. Configuração de IA (tabela `dyno_config`)

| Chave | Valor hoje |
|---|---|
| ia_conversa | openai (**gpt-6-luna** para todos desde 07/10) |
| ia_documento | claude (claude-sonnet-5-5), OpenAI de reserva |
| ia_simples | openai |
| ia_decisao_modo | sombra (Jev observa, não decide) |
| mensagens_retencao_dias | 90 (limpeza diária 03:22 UTC) |
| email_feedback | suporte@dynoapp.com.br |
| meta_clientes_pagantes / meta_clientes_prazo | 150 / 07/2027 |

- Custos por chamada: `dyno_ia_uso`; relatório diário pelo agente de custos (`dyno_custos_ia_relatorio()`).
- O Claude Sonnet 5.5 **recusa `tool_choice` forçado**; a camada usa `auto`.

## 7. Clientes

- Beta fechado: clientes em teste grátis com acesso completo, mais a família (Daniel, Quézia, Eliezer no grupo; Márcia e Marcos em contas privadas). Elieser pediu silêncio total.
- Comandos de admin pelo WhatsApp do Daniel começam com `admin`.
- Em 07/10 os clientes receberam a mensagem de novidades e o pedido de avaliação de 1 a 5 estrelas.

## 8. Como publicar o site

**Overlay (padrão hoje):** o container aplica `public.dyno_site_files(path#NN, conteudo)` por cima de `www/`; as peças `#NN` do mesmo caminho são concatenadas. Inserir/atualizar as linhas (inserir com aspas `$f$`, conferir `md5(conteudo)`), guardar um backup da linha anterior em tabela `dyno_site_files_bak_*` e reiniciar o projeto Docker `dyno-site` na Hostinger; o log mostra "overlay aplicado". Para conteúdo grande, o Supabase MCP dá timeout: usar um workflow temporário no n8n (Code + HTTP PATCH em `/rest/v1/dyno_site_files`). A peça `../templates/default.conf.template#01` alcança o nginx (rota `/minhaconta`).

**Bundle:** como `site/www` espelha a produção, dá para empacotar `www` e `templates` (`tar czf bundle.tgz www templates`, base64, `update dyno_site_bundle set conteudo=... where id=1`), apagar as linhas do overlay e reiniciar. **Não rode `build.py`** sobre `www/`: está atrás das páginas editadas no overlay.

O segredo `X-Dyno-Site` fica na env `SITE_SECRET` do container e na credencial n8n `dyno-site`. Nunca em arquivo.

## 9. Regras que não podem ser quebradas

1. Nunca escrever, pedir ou repetir chaves e senhas no chat ou em arquivos.
2. Não enviar mensagem para clientes, nem publicar nada, sem o Daniel aprovar o texto e os destinatários.
3. Nada de mensagem "fria" pelo número do Dyno (risco de bloqueio): só convites ou envios que o Daniel pedir.
4. O devocional (PDF) é licenciado: nunca enviar, citar ou narrar; a reflexão das 06:00 é original e só vai para o grupo da família.
5. No n8n, uma execução manual por API/MCP **envia de verdade**: desative os nós de envio antes de testar.
6. Não reimplantar o projeto Docker `n8n`. Só reiniciar quando necessário.
7. No Supabase, statements com `delete`/`drop` ou acima de ~3 KB dão timeout no MCP; preferir `rename`, `replace()` pequenos ou um workflow temporário.
8. Não dar conselho jurídico ou financeiro como se fosse profissional.
9. Não mexer nos serviços da Dynamo Wear nem do Project Zomboid, nem nos workflows de outros negócios.

## 10. Pendências

As de 10/10 estão em `ATUALIZACAO-2026-10-10.md`. As de 07/10 que seguem abertas: LGPD com o advogado (texto da Política), conferir o segredo `X-Dyno-Site` e a renovação do VPS, testes reais (comprovante, "apagar meus dados", faxina, qualidade do gpt-6-luna), verificação do app OAuth do Google, SPF/DKIM/DMARC e teste real de cobrança no Asaas antes de dezembro.

## 11. Histórico curto

- **05/10:** repositório no GitHub; número antigo desligado; alerta de câmbio.
- **06/10:** lembretes com 1 insistência; listas no site; tema escuro; previsão/metas/categorias/agenda; Google Agenda; Modo família; 3 planos.
- **07/10:** auditoria dos fluxos; LGPD eliminação completa; segurança do banco; retenção 90 dias; 3 agentes (revisão, custos, faxina); gpt-6-luna; comprovantes no Storage; links `/minhaconta`; avaliação em estrelas; avisos ao Daniel; gating dos planos; boas-vindas guiadas ligadas.
- **08–09/10:** rastreio de encomendas, agentes de assinaturas/documentos/promessas/pedidos, Dyno Business, site admin, WhatsApp oficial (Meta).
- **10/10:** várias contas Google por cliente, aba Categorias, painel ao vivo, reel da reunião, organização da família de produtos (Dyno, Business, Fit, Contábil, Maker; Vendas em validação), `site/` sincronizado com a produção.
