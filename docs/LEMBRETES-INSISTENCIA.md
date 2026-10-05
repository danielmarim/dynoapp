# Lembretes que insistem — 30 minutos e sem empilhar mensagens (05/10/2026)

Workflow n8n **Dyno | Lembretes e mensagem das 6h** (`Xbdnisj9AjKJFYAF`), ramo "A cada minuto".

## Por quê
O cliente (Daniel) percebeu que, sem responder, recebia um aviso atrás do outro e a conversa ficava cheia e "impositiva". Pedido: apagar o aviso anterior sem resposta e espaçar mais.

## Como funciona agora
1. Ao vencer, o lembrete é enviado e fica `aguardando`. A resposta do Evolution traz `key.id` e `key.remoteJid`, gravados em `dyno_lembretes.msg_id` e `msg_jid` (nó "Marcar como enviado").
2. Se não houver resposta, a cada **30 minutos** (`INTERVALO_MIN = 30`) o nó "Preparar envio" gera a insistência e devolve também `apagar_id` e `apagar_jid` do aviso anterior.
3. O nó "Tem aviso anterior?" (If) manda para "Apagar aviso anterior": `DELETE https://wa.dynoapp.com.br/chat/deleteMessageForEveryone/dyno` com `{ id, remoteJid, fromMe: true }` (credencial `evolution-dyno`). Em caso de erro (mensagem velha demais, já apagada) o fluxo segue e o novo aviso sai do mesmo jeito.
4. O novo aviso é enviado e seu id substitui o anterior.
5. Máximo de 6 envios (`MAX_ENVIOS = 6`, cerca de 2h30). Depois: "vou parar de insistir" e o lembrete expira (ou volta a `pendente` se for recorrente).

## O que o cliente vê
No lugar do aviso antigo o WhatsApp mostra "Mensagem apagada". Isso é do WhatsApp e não dá para esconder.

## Banco
`alter table dyno_lembretes add column msg_id text, add column msg_jid text;`

## Para ajustar
- Intervalo e máximo: constantes no topo do nó "Preparar envio".
- Texto do site (aba Funcionalidades, "Lembretes que insistem"): `site/func_page.py`.

## Pendente
- Teste real: pedir "me lembra daqui 2 minutos de testar", não responder por ~25 min e conferir que só o último aviso fica. A apagada depende do Evolution aceitar o `DELETE` com esse corpo; se falhar, o nó segue sem apagar (ver execuções).
- Atualizar o site publicado (o texto novo "a cada 30 minutos e apaga o aviso anterior" está só no repositório até o próximo deploy do pacote).
