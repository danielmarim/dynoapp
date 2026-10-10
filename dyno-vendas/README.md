# Dyno Vendas

Nicho do ecossistema Dyno. Ainda sem código neste repositório.

- **Público e objetivo:** Equipes comerciais B2B: CRM e automação de vendas pelo WhatsApp.
- **Situação:** Em desenvolvimento — candidato em validação

## O que já se sabe

- Validar antes de construir: conversa com 3 a 5 vendedores.
- Escopo no projeto: `dyno-vendas/escopo-dyno-vendas-10-10.md`.
- Não confundir com o workflow `Dyno | Agentes de vendas: envio aprovado` (em `dyno-pessoal/`), que envia as mensagens de venda do próprio Dyno aprovadas pelo Daniel.

## Quando ganhar código

Seguir o desenho dos outros produtos: `docs/` para escopo e notas, `n8n/workflows/` para o backup dos workflows
(com um prefixo próprio no n8n, ex.: `Dyno Vendas | …`, e uma linha em `PRODUTOS` no
[`limpar_export.py`](../plataforma/n8n/limpar_export.py)). O que for comum a outros produtos vai para
[`../plataforma/`](../plataforma/) ou para o core do [Dyno Business](../dyno-business/).
