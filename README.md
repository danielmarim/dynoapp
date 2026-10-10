# Dyno — assessor pessoal no WhatsApp

Dyno (💰 dinheiro) e Dina (⏰ agenda e rotina) atendem pelo WhatsApp **+55 11 93949-7178**. Site: https://dynoapp.com.br

**Comece por [`docs/PASSAGEM-DE-BASTAO.md`](docs/PASSAGEM-DE-BASTAO.md)** — estado do projeto, onde está cada peça, regras e pendências.
Detalhe completo em [`docs/DOCUMENTACAO-TECNICA.md`](docs/DOCUMENTACAO-TECNICA.md).

## Arquitetura

WhatsApp → Evolution API (`wa.dynoapp.com.br`, instância `dyno`) → **n8n** → **Supabase** (`xvekgnbneeokihtjpbts`) + IA em camadas (OpenAI, Claude, Jev) → resposta. Cobrança no Asaas. Tudo num VPS Hostinger (Docker).

A lógica vive nos workflows do n8n (ver [`n8n/`](n8n/README.md)). Este repositório guarda o que não fica no n8n nem no Supabase.

## Estrutura

| Pasta | Conteúdo |
|---|---|
| `docs/` | Passagem de bastão, documentação técnica e notas de funções (ex.: `ALERTA-DE-CAMBIO.md`) |
| `site/` | Site estático: `build.py` gera `www/`; `templates/` (nginx), `deploy/` (compose), `n8n/` (gerador do workflow da API do site) |
| `card-semanal/` | Card "Sua semana" (HTML → PNG via Gotenberg `dyno-render`) e código do nó do n8n |
| `videos/` | Projetos HyperFrames dos vídeos de divulgação (sem áudio `.wav` e sem renders) |
| `n8n/` | Lugar para os exports dos workflows |
| `agentes/` | Instruções dos agentes de operação (ex.: Vigia de erros), reaproveitáveis em Rotinas, Paperclip ou Hermes |
| `redundancia/` | Servidor reserva: árbitro, agente do principal, vigia do reserva, guia e teste de ponta a ponta |
| `whisper/` | Compose e guia do Whisper (transcrição local) no VPS, só na rede interna do n8n |

## Publicar o site

```bash
cd site && python3 build.py
tar czf bundle.tgz www templates && base64 -w0 bundle.tgz > bundle.b64
# Supabase: update dyno_site_bundle set conteudo = '<conteúdo do bundle.b64>' where id = 1;
# Hostinger: reiniciar o projeto Docker "dyno-site"
```

## Segurança

Nenhum segredo é versionado. Chaves ficam nas credenciais do n8n, nas variáveis dos containers e no painel da Hostinger.
Onde o código precisa do segredo do site aparece o marcador `__SEGREDO__`. **Mantenha este repositório privado**: a documentação cita nomes de clientes do Beta.
