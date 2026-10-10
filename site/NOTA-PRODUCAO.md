# site/ espelha a produção (10/10/2026)

`www/` e `templates/` foram refeitos a partir do que o container `dyno-site` serve: pacote-base (`dyno_site_bundle`, id 1) + overlay (`dyno_site_files`), com o overlay valendo.

- `www/assets/site-base.css` é o CSS claro original. Na inicialização o entrypoint copia `site.css` para `site-base.css` (só se `site.css` ainda não tiver `@import`) e troca `site.css?v=9` por `v=10` e `painel2.js?v=1` por `v=2` nos HTML. Por isso alguns HTML aqui ainda citam `v=9`.
- `build.py` e `func_page.py` estão **atrás** do site: não rode o `build.py` sobre `www/`, porque ele sobrescreve as páginas editadas direto no overlay.
- `www/business/` é o site do Dyno Business (business.dynoapp.com.br). Os `.png` do Business ficam no overlay como `.b64` e aqui já estão decodificados.
- Segredo: `X-Dyno-Site` usa a variável `SITE_SECRET` do container. Nada de segredo neste diretório.
