# Painel "ao vivo" na área do cliente (10/10/2026)

## Contexto
Uma cliente do Beta reclamou que o painel não atualizava quando ela mandava gastos novos pelo WhatsApp, nem recarregando a página.

O que foi verificado:
- Os gastos do dia estavam salvos com o `cliente` certo.
- A API (`nslhB7FRnKuAOPuf`, ação `painel`) lê `dyno_transacoes` direto do Supabase a cada chamada. Não existe cache no n8n nem no nginx: `/api` vai por proxy_pass com `Cache-Control: no-store`.
- Não houve execução com erro.

Causa mais provável: o print foi tirado antes dos gastos novos, ou o navegador do celular devolveu a página guardada em vez de recarregar (comum no navegador interno do WhatsApp ou ao trocar de app). De qualquer forma, o painel não se atualizava sozinho.

## O que mudou
- Arquivo novo `plataforma/site/www/assets/painel-vivo.js`, carregado por `conta.html` depois de `categorias.js`.
- Funcionamento:
  - Escuta a resposta do painel da carga inicial.
  - Com a página visível, consulta o painel de novo a cada 30 s, ao voltar para a aba do navegador e ao restaurar a página da memória (bfcache).
  - Compara gastos, receitas, número de lançamentos, o último lançamento e a quantidade de tarefas, lembretes, contas e agenda.
  - Se algo mudou e o Painel está aberto, recarrega a página sozinho. Não recarrega se a pessoa estiver digitando ou com uma janela aberta.
  - Se ela estiver em outra aba, recarrega quando voltar para o Painel.
  - Mostra embaixo do status: "Atualiza sozinho · conferido às HH:MM".
- Custo: 1 chamada `/api` a cada 30 s por página aberta e visível. O limite do nginx é 20 por minuto por IP.
- Testado em navegador headless com API simulada.

**Para entrar no ar:** reiniciar o `dyno-site` na Hostinger.

## Como desfazer
Tirar a tag `painel-vivo.js` de `conta.html`, apagar a linha `assets/painel-vivo.js#01` do overlay e reiniciar o `dyno-site`.
