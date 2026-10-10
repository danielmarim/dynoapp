# Aba "Categorias" na área do cliente (10/10/2026)

Pedido do Daniel: "Libere a aba de categorias no site do dynoapp.com.br". Escolha: criar uma aba nova em /minhaconta.

## O que a cliente vê
- **Gastos por categoria**: Este mês, Mês passado ou 3 meses. Cada categoria mostra uma barra, a variação em % contra o período anterior e o limite (a barra fica amarela a partir de 80% e vermelha a partir de 100%).
- **Sem categoria**: até 30 gastos que ficaram em "outros". Ela escolhe a categoria e pode marcar "Usar sempre para [palavra]", que vira regra.
- **Regras que o Dyno aprendeu**: a lista (ex.: padaria → Alimentação), com Remover (2 cliques) e Adicionar.
- **Limites**: o orçamento do mês inteiro e um limite por categoria, com Salvar e Remover.
- Tudo é sincronizado com o WhatsApp, porque usa as mesmas tabelas.
- **Plano**: ver os gastos vale para todos. Regras e limites exigem o Completo (`dyno_plano_bloqueado`: `regra_categoria` e `definir_orcamento`). Quem não tem o plano vê um aviso e não vê os formulários.
- **Links diretos**: `dynoapp.com.br/minhaconta/categorias` e `#categorias`.

## Peças
| Onde | O quê |
|---|---|
| Supabase | `public.dyno_site_categorias(p_token, p jsonb)`, com as ops `ver`, `regra_salvar`, `regra_apagar`, `limite_salvar` (aceita "1.350,50"), `limite_apagar` e `transacao_categoria`. Acesso só por service_role. |
| n8n `nslhB7FRnKuAOPuf` (Dyno \| API do site) | Bloco `acao === 'categorias'` em "Ação agenda" (valida op, período, id, tamanhos; exige o cookie `dyno_sess`). `'categorias'` também foi incluída nas listas do "É avaliação?". Publicado em 10/10 como e08075c0. A versão anterior é 81d063a3. |
| Site | `site/www/assets/categorias.js` e a tag `<script src="/assets/categorias.js?v=1" defer>` em `conta.html`, depois do chat.js. |
| Backup | `public.dyno_site_files_bak_1010`: `conta.html#01` antes da mudança. |

**Para entrar no ar:** reiniciar o projeto Docker `dyno-site` na Hostinger (hPanel → VPS 1825327 → Docker → dyno-site → Restart). O container só aplica o overlay quando inicia.

## Como desfazer
1. Restaurar `conta.html#01` a partir de `dyno_site_files_bak_1010` (ou tirar a tag `categorias.js`).
2. Apagar a linha `assets/categorias.js#01` do overlay.
3. No n8n, restaurar a versão 81d063a3 do `nslhB7FRnKuAOPuf` e publicar.
4. Reiniciar `dyno-site`.

## Pendências
- Testar na conta real depois do restart (as 3 abas de período, salvar e remover regra e limite, reclassificar um gasto).
- Opcional: citar a aba em /funcionalidades.
- Opcional: apagar a tabela de backup depois de uns dias.
