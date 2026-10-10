# Workflows do n8n

`workflows/` guarda o backup da lógica do Dyno, já limpo para o git.

## Como atualizar

1. No n8n, exporte os workflows do Dyno pela interface (selecionar todos → Download, ou ⋯ → Download em cada um).
   Use o download da interface: ele leva a referência das credenciais (só nome e ID). A leitura pela API/MCP não leva,
   e um workflow importado assim perde as credenciais de todos os nós HTTP.
2. Coloque os `.json` (ou o `.zip`) em `n8n/_download/`. Essa pasta fica fora do git.
3. Rode `python n8n/limpar_export.py`. O script:
   - troca o valor da constante `SEGREDO` (nó **Preparar** da "Dyno | API do site") por `__SEGREDO__`;
   - troca o `p_token` fixo enviado às RPCs do Supabase (hoje só no "Dyno | Asaas webhook") por `__P_TOKEN__`;
   - remove `pinData` e `staticData`, que podem trazer dados de clientes de execuções de teste;
   - procura valores com cara de chave ou token e não grava o arquivo suspeito (mostra onde está, nunca o valor);
   - avisa quando há telefones fixos no código.
4. Confira o `git diff` e faça o commit de `n8n/workflows/`. Depois apague o conteúdo de `n8n/_download/`.

As credenciais (valores) ficam só no n8n. Para restaurar num n8n novo, é preciso recriar as credenciais com os
mesmos nomes, ter a `N8N_ENCRYPTION_KEY` guardada num cofre de senhas e repor os valores de `__SEGREDO__` e
`__P_TOKEN__` depois de importar.

Os 4 workflows desligados (Setup Evolution, TEMP limpeza de testes, TESTE Google Places, TESTE IA em camadas)
não estão no backup: são de setup ou teste.

## Atualização de 10/10/2026

Só `dyno-api-do-site-area-do-cliente__nslhB7FRnKuAOPuf.json` (58 nós) e `dyno-whatsapp-cerebro__YFgP2bYqeHbQc5t1.json`
(164 nós) foram reexportados; os demais seguem como em 08/10. Faltam os renomeados "Dyno Plataforma | …",
"Dyno Business | …" e os 7 do WhatsApp oficial (Meta). O `limpar_export.py` agora aceita qualquer nome que comece com "Dyno".

**Atenção:** esses dois vieram da leitura pela API, **sem a referência das credenciais** dos nós. Antes de importar
num n8n novo, reexporte-os pela interface (passos acima) ou religue as credenciais à mão. A versão de 08/10, com as
credenciais, continua no histórico do git.
