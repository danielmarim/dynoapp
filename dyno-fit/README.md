# Dyno Fit

Nicho do ecossistema Dyno. Ainda sem código neste repositório.

- **Público e objetivo:** Profissionais da área fitness e saúde.
- **Situação:** Em criação

## O que já se sabe

- Escopo ainda a definir (pendência em [`../docs/ATUALIZACAO-2026-10-10.md`](../docs/ATUALIZACAO-2026-10-10.md)).
- Ainda não há workflow nem documento próprio.

## Quando ganhar código

Seguir o desenho dos outros produtos: `docs/` para escopo e notas, `n8n/workflows/` para o backup dos workflows
(com um prefixo próprio no n8n, ex.: `Dyno Fit | …`, e uma linha em `PRODUTOS` no
[`limpar_export.py`](../plataforma/n8n/limpar_export.py)). O que for comum a outros produtos vai para
[`../plataforma/`](../plataforma/) ou para o core do [Dyno Business](../dyno-business/).
