# Dyno Pessoal (core)

Assessor pessoal no WhatsApp: **Dyno** (💰 dinheiro) e **Dina** (⏰ agenda e rotina), mais o painel do cliente em
https://dynoapp.com.br. É o produto core do ecossistema e está **disponível em beta**.

Público e objetivo: controle de finanças pessoais (e da rotina da família) pelo WhatsApp e painel web.

| Pasta | Conteúdo |
|---|---|
| [`n8n/workflows/`](n8n/workflows/) | Workflows `Dyno \| …`: o cérebro do WhatsApp, cadastro e cobrança, API do site, lembretes, relatórios, agentes, importação de extrato, Open Finance (Pluggy), Google Agenda, rastreio, LGPD e outros |
| [`docs/`](docs/) | Funcionalidades e roadmap, notas de funções (alerta de câmbio, lembretes que insistem) e `notas/` de 10/10 (aba Categorias, painel ao vivo) |
| [`card-semanal/`](card-semanal/) | Card "Sua semana" (HTML → PNG via Gotenberg `dyno-render`) e código do nó do n8n |
| [`videos/`](videos/) | Projetos HyperFrames dos vídeos de divulgação (sem áudio `.wav` e sem renders) |

O site do Pessoal fica em [`../plataforma/site/`](../plataforma/site/), junto com o do Business. A infraestrutura
compartilhada (IA em camadas, saúde, erros, WhatsApp oficial) está em [`../plataforma/`](../plataforma/).
