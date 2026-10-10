# Dyno — Atualização de 10/10/2026

Complementa a `PASSAGEM-DE-BASTAO.md`. Quando houver contradição entre os dois, vale este arquivo.

> **Caminhos (mais tarde em 10/10):** o repositório foi dividido por produto. Onde este arquivo diz `site/`, leia `plataforma/site/`; `n8n/workflows/` virou `<produto>/n8n/workflows/` e o script está em `plataforma/n8n/`; `videos/`, `card-semanal/` e `docs/notas/` estão em `dyno-pessoal/`. A pendência 1 (exportar os workflows) foi resolvida: os 56 estão no repositório.

## O que mudou no código deste repositório

| Pasta | Mudança |
|---|---|
| `site/www/` e `site/templates/` | Agora **espelha a produção**: pacote-base (`dyno_site_bundle`, id 1) com o overlay (`dyno_site_files`) por cima. Entraram 33 arquivos novos (admin, Dyno Business, chat, agenda, listas, painel, categorias, avaliação, banco) e 14 alterados (páginas, `site.css`, `familia.js`, `planos.js`, nginx). `assets/site-base.css` é o CSS claro original, que o entrypoint do container copia de `site.css` na inicialização. |
| `n8n/workflows/` | Só **dois** workflows foram reexportados: `dyno-api-do-site-area-do-cliente.json` (aba Categorias, 58 nós) e `dyno-whatsapp-cerebro.json` (várias contas Google, 164 nós). Os outros 30 continuam na versão de 08/10. Ver "Pendências". |
| `videos/` | Projetos HyperFrames novos: reels de família, lembrar, novidades, planos, rastreio e **reunião (Google Agenda, 9:16)**, stories de novidades, tutorial da família e `arte-feed`. Sem renders, áudio nem snapshots. |
| `docs/notas/` | Notas de 10/10: aba Categorias e painel ao vivo. |

**Atenção:** o `site/build.py` está **atrás** do site em produção (as páginas foram editadas direto no overlay). **Não rode o `build.py` sobre `site/www/`**: ele apagaria as mudanças. Para publicar a partir deste repositório, empacote `site/www` e `site/templates` como no `README.md` (tar + base64 em `dyno_site_bundle`), depois apague as linhas de `dyno_site_files` e reinicie o `dyno-site`.

## Funções novas em produção (10/10)

1. **Várias contas Google por cliente** (pessoal e institucional, até 3).
   - Tabela `dyno_agenda_conexoes` com `id`, `rotulo`, `principal`; índice único `(usuario_id, lower(google_email))` e uma conta principal ativa por usuário. `dyno_reunioes.conta_email` guarda em qual conta a reunião foi criada.
   - O Dyno pergunta em qual agenda marcar compromissos, tarefas e lembretes quando há mais de uma conta, e sempre para reunião (Meet).
   - OAuth com `prompt=select_account consent`. LGPD exportar/eliminar tratam todas as contas.
   - Workflows: Google Agenda (`3iZpB1Sku6OVZUB1`), cérebro (`YFgP2bYqeHbQc5t1`), LGPD (`3jEnG5ZmIFf16JGS`). Doc no projeto: `dyno/agenda-varias-contas-google-10-10.md`.
2. **Aba "Categorias"** na área do cliente: gastos por categoria, gastos sem categoria, regras aprendidas e limites. Função `dyno_site_categorias`, ação `categorias` na API do site, script `assets/categorias.js`. Ver `docs/notas/aba-categorias-site-10-10.md`.
3. **Painel "ao vivo"**: confere novidades a cada 30 s e recarrega sozinho. Script `assets/painel-vivo.js`. Ver `docs/notas/painel-ao-vivo-10-10.md`.
4. **Reel da reunião** (Google Agenda): `videos/dyno-reel-reuniao`.

## Organização da família de produtos

- Nomes: **Dyno** (pessoal), **Dyno Business**, **Dyno Fit**, **Dyno Contábil** (escritório contábil e consultor), **Dyno Maker** (3D, vira nicho próprio). **Dyno Vendas** é candidato em validação (CRM B2B por WhatsApp); escopo em `dyno-vendas/escopo-dyno-vendas-10-10.md` no projeto.
- Documentos do projeto reorganizados por pasta: `dyno/`, `dyno-business/`, `dyno-maker/`, `dyno-contabil/`, `dyno-vendas/`, `plataforma/` e `00-indice/LEIA-ME.md`. Os docs antigos ainda citam caminhos `claude/...`; os nomes de arquivo não mudaram.
- n8n: 16 workflows renomeados para "Dyno Plataforma | …" e o do grupo dos negócios para "Dyno Business | WhatsApp (grupos dos negócios)". Tags: `dyno`, `dyno-business`, `dyno-maker`, `plataforma`, `teste`. Dynamo Wear e os demais fluxos não foram tocados.

## Para entrar no ar

O site só aplica o overlay quando o container inicia. **Reiniciar o projeto Docker `dyno-site` na Hostinger** (VPS 1825327) para ativar a aba Categorias e o painel ao vivo. A API (n8n) já está publicada.

## Pendências

1. **Exportar o restante dos workflows do n8n.** A sessão da IA não tem como baixar todos (não há credencial de API do n8n). Opções: no n8n, selecionar todos e *Download*, depois `python n8n/limpar_export.py` (o filtro já aceita "Dyno Plataforma |" e "Dyno Business |"); ou criar uma credencial de API do n8n e passar só o nome dela à IA. Faltam também os 7 workflows do WhatsApp oficial (Meta) e os renomeados.
2. Reiniciar o `dyno-site` e testar `/minhaconta/categorias` e o painel ao vivo com uma cliente real.
3. Testes reais: várias contas Google (conectar a segunda conta, perguntar a agenda, reunião), "aprova" entre aspas, código do Dyno Business.
4. O painel do site ainda mostra só a conta Google principal; o bom dia das 7h30 ainda não lê o Google.
5. SPF/DKIM/DMARC do domínio; aprovar a correção de LGPD pendente.
6. Decisões de nomes: Maker × "3D Felps Maker", planos do Contábil, escopo do Fit, subdomínios.
7. Validar o Dyno Vendas (conversa com 3 a 5 vendedores) antes de construir.

## Regras que continuam valendo

As da seção 9 da `PASSAGEM-DE-BASTAO.md`. Em especial: a IA não faz push no GitHub, não envia mensagem a clientes sem o Daniel aprovar texto e destinatários, e nunca escreve chaves ou senhas.
