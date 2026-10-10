# Dyno Business

Gestão financeira e operacional de negócios pelo WhatsApp. É um **sistema core/híbrido, adaptável a qualquer nicho**:
os nichos do ecossistema (Maker, Fit, Contábil, Vendas) podem partir dele.

Situação: **protótipo em desenvolvimento**, com um grupo piloto. Site: https://business.dynoapp.com.br

| Onde | Conteúdo |
|---|---|
| [`n8n/workflows/`](n8n/workflows/) | `Dyno Business \| WhatsApp (grupos dos negócios)`: entende venda e compra por texto ou áudio, gera orçamento em PDF (Gotenberg) e responde no grupo. `Avisos e acompanhamento de orçamentos`: fila `biz_avisos` e cobrança de orçamentos sem resposta. `Gerar imagem OG` (manual) |
| [`../plataforma/site/www/business/`](../plataforma/site/www/business/) | Site do Business. Scripts e estilo em `../plataforma/site/www/assets/biz*.js` e `biz.css` |

O workflow do grupo dos negócios também tem a tag `dyno-maker` no n8n, ligada ao nicho de impressão 3D ([Dyno Maker](../dyno-maker/)).

## Pendências

- Testar com cliente real o código do Dyno Business (ver [`../docs/ATUALIZACAO-2026-10-10.md`](../docs/ATUALIZACAO-2026-10-10.md)).
- Decidir subdomínios dos nichos.
