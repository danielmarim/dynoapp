# Plataforma Dyno

O que é compartilhado por todos os produtos do ecossistema. Mudança aqui afeta o Pessoal, o Business e os nichos ao mesmo tempo.

| Pasta | Conteúdo |
|---|---|
| [`site/`](site/) | Site único servido pelo container `dyno-site` (nginx): `dynoapp.com.br` (Pessoal) e `business.dynoapp.com.br` (`www/business/`). `www/` e `templates/` espelham a produção; ver [`site/NOTA-PRODUCAO.md`](site/NOTA-PRODUCAO.md). `deploy/` (compose), `n8n/` (gerador do workflow da API do site) |
| [`n8n/workflows/`](n8n/workflows/) | Workflows `Dyno Plataforma \| …`: IA em camadas (OpenAI, Claude, Jev) e Jev modo sombra, saúde (health check), erros e alertas, backup diário, painel e infraestrutura, custos de IA, avisos ao Daniel e o WhatsApp oficial (Meta: webhook, ponte de envio, assinatura, diagnóstico, registro, perfil) |
| [`n8n/limpar_export.py`](n8n/limpar_export.py) | Limpa o export do n8n e grava cada workflow na pasta do produto. Ver [`n8n/README.md`](n8n/README.md) |

Infraestrutura (sem código aqui): VPS Hostinger srv1825327, Supabase `xvekgnbneeokihtjpbts`, Evolution API, Gotenberg (`dyno-render`), Asaas. Detalhes em [`../docs/DOCUMENTACAO-TECNICA.md`](../docs/DOCUMENTACAO-TECNICA.md).
