# Workflows do n8n

Exporte aqui os workflows do Dyno (no n8n: selecionar todos → Download) e faça commit dos `.json`.

Antes do commit, confira que nenhum arquivo traz valores secretos. Em especial, o nó **Preparar** do workflow
"Dyno | API do site" tem a constante `SEGREDO`: troque o valor por `__SEGREDO__` antes de subir.
As credenciais do n8n não vão no export (só o nome/ID), então o resto pode subir como está.
