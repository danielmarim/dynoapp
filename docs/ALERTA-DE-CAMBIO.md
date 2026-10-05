# Alerta de câmbio (função do Dyno) — 05/10/2026

Decisão do Daniel: não criar a "Zia"; o câmbio é função do **Dyno** (dinheiro). Só informa e avisa — nunca recomenda comprar/vender nem prevê (evita recomendação de investimento).

## Como o cliente usa
- "me avisa quando o dólar ficar abaixo de 5,20" / "me avisa se o euro passar de 6"
- "quanto tá o dólar?" (o Dyno responde com a cotação injetada no prompt)
- "cancela meus alertas de câmbio"
- Até 5 alertas por pessoa; cada alerta avisa **uma vez** (dias úteis, 9h–18h) e se encerra. Sem valor → o Dyno sugere um valor e confirma.

## Peças
- **Supabase:** `dyno_cambio_cotacoes` (histórico, 120 dias) e `dyno_cambio_alertas` (RLS; no `dyno_lgpd_eliminar`; inativos apagados após 180 dias — cron `dyno-limpar-cambio`).
  RPCs (só service_role): `dyno_cambio_registrar(p)` (grava e dispara; ignora cotação com mais de 3h), `dyno_cambio_contexto(p_autor)` (cotação + mín/máx 30 dias + alertas da pessoa), `dyno_cambio_acao(p)` (criar/cancelar), `dyno_cambio_resumo(moeda)`.
- **Workflow "Dyno | Alerta de câmbio"** (asdiDsXdGoWC7Bip): a cada 15 min, seg–sex 9h–18h.
  - Fonte 1 (em uso desde 05/10 14:15): **AwesomeAPI** com chave grátis — credencial n8n `Awesomeapi` (Header Auth `x-api-key`). Limite 100 mil req/mês; o alerta usa ~800.
  - Fonte 2 (reserva automática se a AwesomeAPI falhar): **PTAX do Banco Central** (oficial, grátis, sem chave; ~4 boletins por dia útil).
  - Envia pelo número do Dyno com `*💰 Dyno*` e grava no histórico da conversa.
  - O `pctChange` da AwesomeAPI veio −4,4% no primeiro teste (parece comparar com um fechamento antigo). O aviso só mostra "hoje: x%" quando a variação é de até 3%.
- **Cérebro:** nós "Câmbio (Supabase)" + "Complemento (câmbio)" (entre Persona e Modelo) injetam cotação e alertas no prompt; "Detectar câmbio" + "Câmbio: salvar alerta" (a partir de Interpretar resposta) gravam as ações.

## Lançamento (05/10)
- **Anúncio enviado** aos 10 cadastros pelo número do Dyno: dólar R$ 4,98 vs R$ 5,21 em 28/09 (−4,5%), euro R$ 5,58 (−5,8%) + exemplos de comandos.
- **Site dynoapp.com.br:** seção "O dólar caiu? O Dyno te avisa." na home, item "Alerta de dólar e euro" na lista do Dyno e pergunta no FAQ (fonte em `site/build.py`, CSS `.cambio` em `site/www/assets/site.css`).
- **Instagram:** post 1080×1350 e reel de 22 s (com e sem música). Projeto do reel em `videos/dyno-reel-dolar` (gen.py + sfx.py).
  - Legenda sugerida: "O dólar caiu? O Dyno te avisa. 💵 Agora é só pedir no WhatsApp: 'me avisa quando o dólar ficar abaixo de R$ 4,90' — e pronto, ele fica de olho por você. Funciona com dólar e euro, até 5 alertas, cotação atualizada a cada 15 minutos. Só informamos, não é recomendação de investimento. 👉 dynoapp.com.br #dyno #dolar #cambio #financaspessoais #whatsapp"
  - Valores do material são ilustrativos; sempre manter "só informo, não é recomendação".

## Pendências
- Testes 05/10: criação de alerta OK (Daniel, Anderson e Tavarez criaram pelo WhatsApp). Falta confirmar o **cancelamento** ("cancela meus alertas de câmbio" não apareceu no banco) e ver um aviso disparando de verdade.
