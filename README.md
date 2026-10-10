# Ecossistema Dyno

Assessores no WhatsApp para pessoas e negócios. O primeiro produto, o **Dyno Pessoal** — Dyno (💰 dinheiro) e Dina (⏰ agenda e rotina) — atende pelo WhatsApp **+55 11 93949-7178**. Site: https://dynoapp.com.br

**Comece por [`docs/PASSAGEM-DE-BASTAO.md`](docs/PASSAGEM-DE-BASTAO.md)** — estado do projeto, onde está cada peça, regras e pendências. As mudanças mais recentes estão em [`docs/ATUALIZACAO-2026-10-10.md`](docs/ATUALIZACAO-2026-10-10.md).
Detalhe completo em [`docs/DOCUMENTACAO-TECNICA.md`](docs/DOCUMENTACAO-TECNICA.md).

## Produtos

| Produto | Pasta | Papel | Público e objetivo | Situação |
|---|---|---|---|---|
| **Dyno Pessoal** | [`dyno-pessoal/`](dyno-pessoal/) | **Core** | Controle de finanças pessoais pelo WhatsApp e painel web | Disponível em beta |
| **Dyno Business** | [`dyno-business/`](dyno-business/) | Sistema core/híbrido, adaptável a qualquer nicho | Gestão financeira e operacional de negócios | Protótipo em desenvolvimento |
| **Dyno Maker** | [`dyno-maker/`](dyno-maker/) | Nicho | Microempreendedores e negócios de impressão 3D | Desenvolvimento mencionado |
| **Dyno Fit** | [`dyno-fit/`](dyno-fit/) | Nicho | Profissionais da área fitness e saúde | Em criação |
| **Dyno Contábil / Finance** | [`dyno-contabil/`](dyno-contabil/) | Nicho | Contadores e profissionais financeiros | Ideia em desenvolvimento |
| **Dyno Vendas** | [`dyno-vendas/`](dyno-vendas/) | Nicho | Equipes comerciais B2B e automação de CRM | Em desenvolvimento (validação) |
| Plataforma | [`plataforma/`](plataforma/) | Compartilhado | Site, n8n de infraestrutura, IA em camadas, WhatsApp oficial, observabilidade | Em produção |

## Estrutura

```
docs/                 documentos do ecossistema (passagem de bastão, atualizações, documentação técnica)
plataforma/           o que todos os produtos usam
  site/               site único (dynoapp.com.br e business.dynoapp.com.br), espelho da produção
  n8n/                workflows "Dyno Plataforma | …", limpar_export.py e o README do backup
dyno-pessoal/         core: n8n/workflows ("Dyno | …"), docs/, card-semanal/, videos/
dyno-business/        n8n/workflows ("Dyno Business | …")
dyno-maker/  dyno-fit/  dyno-contabil/  dyno-vendas/   escopo e situação de cada nicho
```

Cada produto segue o mesmo desenho quando ganha código: `docs/`, `n8n/workflows/` e, se tiver, `videos/`.
Os workflows vão para a pasta do produto pelo **nome no n8n** (`Dyno |`, `Dyno Business |`, `Dyno Plataforma |`);
ver [`plataforma/n8n/README.md`](plataforma/n8n/README.md).

## Arquitetura

WhatsApp → Evolution API (`wa.dynoapp.com.br`, instância `dyno`) ou API oficial da Meta → **n8n** → **Supabase** (`xvekgnbneeokihtjpbts`) + IA em camadas (OpenAI, Claude, Jev) → resposta. Cobrança no Asaas. Tudo num VPS Hostinger (Docker).

A lógica vive nos workflows do n8n. Este repositório guarda o backup deles e o que não fica no n8n nem no Supabase.

## Publicar o site

O site é um só para todos os produtos (o Business fica em `plataforma/site/www/business/`). Como `www/` espelha a
produção, **não rode o `build.py`** sobre ele (ver [`plataforma/site/NOTA-PRODUCAO.md`](plataforma/site/NOTA-PRODUCAO.md)).

```bash
cd plataforma/site
tar czf bundle.tgz www templates && base64 -w0 bundle.tgz > bundle.b64
# Supabase: update dyno_site_bundle set conteudo = '<conteúdo do bundle.b64>' where id = 1;
# apagar as linhas de dyno_site_files (overlay) e reiniciar o projeto Docker "dyno-site" na Hostinger
```

## Segurança

Nenhum segredo é versionado. Chaves ficam nas credenciais do n8n, nas variáveis dos containers e no painel da Hostinger.
Onde o código precisa de um segredo aparecem marcadores (`__SEGREDO__`, `__P_TOKEN__`, `<SEGREDO-REMOVIDO>`). **Mantenha este repositório privado**: a documentação cita nomes de clientes do Beta.
