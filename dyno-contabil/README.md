# Dyno Contábil / Finance

Nicho do ecossistema Dyno. Ainda sem código neste repositório.

- **Público e objetivo:** Contadores, escritórios contábeis, consultores e profissionais financeiros.
- **Situação:** Ideia em desenvolvimento

## O que já se sabe

- Decisão pendente: planos do Contábil.
- Documentos no projeto: pasta `dyno-contabil/`.

## Quando ganhar código

Seguir o desenho dos outros produtos: `docs/` para escopo e notas, `n8n/workflows/` para o backup dos workflows
(com um prefixo próprio no n8n, ex.: `Dyno Contábil | …`, e uma linha em `PRODUTOS` no
[`limpar_export.py`](../plataforma/n8n/limpar_export.py)). O que for comum a outros produtos vai para
[`../plataforma/`](../plataforma/) ou para o core do [Dyno Business](../dyno-business/).
