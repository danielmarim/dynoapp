# Workflows do n8n

O backup da lógica fica, já limpo para o git, na pasta de cada produto. O produto sai do nome do workflow no n8n:

| Nome no n8n | Pasta |
|---|---|
| `Dyno Plataforma \| …` | [`plataforma/n8n/workflows/`](workflows/) |
| `Dyno \| …` | [`dyno-pessoal/n8n/workflows/`](../../dyno-pessoal/n8n/workflows/) |
| `Dyno Business \| …` | [`dyno-business/n8n/workflows/`](../../dyno-business/n8n/workflows/) |

Um workflow novo de Maker, Fit, Contábil ou Vendas precisa de um prefixo próprio (ex.: `Dyno Maker | …`) e de uma linha
em `PRODUTOS` no `limpar_export.py`; até lá ele cai em `plataforma/` (só com `--todos`).

## Como atualizar

1. No n8n, exporte os workflows do Dyno pela interface (selecionar todos → Download, ou ⋯ → Download em cada um).
   Use o download da interface: ele leva a referência das credenciais (só nome e ID). A leitura pela API/MCP não leva,
   e um workflow importado assim perde as credenciais de todos os nós HTTP.
2. Coloque os `.json` (ou o `.zip`) em `plataforma/n8n/_download/`. Essa pasta fica fora do git.
3. Rode `python plataforma/n8n/limpar_export.py`. O script:
   - troca o valor da constante `SEGREDO` (nó **Preparar** da "Dyno | API do site") por `__SEGREDO__`;
   - troca o `p_token` fixo enviado às RPCs do Supabase (hoje só no "Dyno | Asaas webhook") por `__P_TOKEN__`;
   - remove `pinData` e `staticData`, que podem trazer dados de clientes de execuções de teste;
   - procura valores com cara de chave ou token e não grava o arquivo suspeito (mostra onde está, nunca o valor);
   - avisa quando há telefones fixos no código.
4. Confira o `git diff` e faça o commit das pastas `<produto>/n8n/workflows/`. Depois apague o conteúdo de `plataforma/n8n/_download/`.

As credenciais (valores) ficam só no n8n. Para restaurar num n8n novo, é preciso recriar as credenciais com os
mesmos nomes, ter a `N8N_ENCRYPTION_KEY` guardada num cofre de senhas e repor os valores de `__SEGREDO__` e
`__P_TOKEN__` depois de importar.

Os 5 workflows desligados de setup ou teste não estão no backup: Setup Evolution, TEMP limpeza de testes,
TEMP varrer preços do site, TESTE Google Places e "Dyno Plataforma | TESTE IA em camadas (manual)".

## Atualização de 10/10/2026

Exportados pela conexão MCP do n8n os **56 workflows** "Dyno …", "Dyno Plataforma | …" e "Dyno Business | …"
(versão publicada de cada um), passados pelo `limpar_export.py`. Entraram os 7 do WhatsApp oficial (Meta), os
agentes, o Dyno Business e os demais que faltavam; os 6 renomeados para "Dyno Plataforma | …" trocaram de nome de arquivo.
Ficaram de fora os 5 de setup/teste acima, a "Dyna 2.0" (não é Dyno) e os da Dynamo Wear.

O `limpar_export.py` agora aceita qualquer nome que comece com "Dyno" e troca o caminho secreto do webhook da
Pluggy por `pluggy-<SEGREDO-REMOVIDO>`.

**Atenção:** a leitura pela MCP/API **não traz a referência das credenciais** dos nós. Para guardar a lógica no git
serve; para restaurar num n8n novo, prefira o download pela interface (passos acima) ou religue as credenciais à mão.
As versões de 08/10, com as credenciais, continuam no histórico do git.
