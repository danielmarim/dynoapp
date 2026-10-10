#!/usr/bin/env bash
# Servidor reserva do Dyno: funções usadas pelo agente (principal) e pelo vigia (reserva).
# Quem decide qual servidor atende é o árbitro no Supabase (tabela dyno_servidor).
set -uo pipefail

: "${PAPEL:?defina PAPEL (principal ou reserva)}"
: "${SUPABASE_URL:?defina SUPABASE_URL}"
: "${SUPABASE_ANON:?defina SUPABASE_ANON (chave pública do Supabase)}"
: "${SERVIDOR_TOKEN:?defina SERVIDOR_TOKEN (o mesmo nos dois servidores)}"
: "${DADOS:?defina DADOS (pasta de trabalho)}"
: "${MONTAGEM:?defina MONTAGEM (como os containers auxiliares enxergam DADOS)}"

FERRAMENTAS=${FERRAMENTAS:-keinos/sqlite3:3.46.1@sha256:055d4be20d868f4077598cbbc33ce4ff39dbefbbe0b87e39ca7b70f9f51caf51}
N8N_CONTAINER=${N8N_CONTAINER:-n8n-n8n-1}
N8N_DIR=${N8N_DIR:-/home/node/.n8n}
EVO_PG_CONTAINER=${EVO_PG_CONTAINER:-dyno-evo-postgres}
EVO_API_CONTAINER=${EVO_API_CONTAINER:-dyno-evo-api}
INTERVALO=${INTERVALO:-30}

log() { echo "$(date '+%Y-%m-%d %H:%M:%S') [$PAPEL] $*"; }

# ---------- árbitro (Supabase) ----------

# arbitro FUNCAO JSON: chama a RPC acrescentando o token. Imprime a resposta; falha se a rede ou o HTTP falharem.
arbitro() {
  local corpo
  corpo=$(jq -c --arg t "$SERVIDOR_TOKEN" '. + {p_token: $t}' <<<"$2") || return 1
  curl -sS -m 15 --fail-with-body -X POST "$SUPABASE_URL/rest/v1/rpc/$1" \
    -H "apikey: $SUPABASE_ANON" -H "Content-Type: application/json" -d "$corpo"
}

# batimento [JSON_INFO]: avisa que este servidor está vivo e imprime o estado ({ok, ativo, mudou_em, ...}).
batimento() {
  local info=${1:-}
  [ -n "$info" ] || info='{}'
  arbitro dyno_servidor_batimento "$(jq -nc --arg s "$PAPEL" --argjson i "$info" '{p_servidor: $s, p_info: $i}')"
}

# mudar DE PARA MOTIVO: troca o servidor ativo (só acontece se o estado ainda for DE).
mudar() {
  arbitro dyno_servidor_mudar "$(jq -nc --arg de "$1" --arg para "$2" --arg m "$3" --argjson s "${SILENCIO_S:-180}" \
    '{p_de: $de, p_para: $para, p_motivo: $m, p_silencio_s: $s}')"
}

# ---------- containers ----------

rodando() { [ "$(docker inspect -f '{{.State.Running}}' "$1" 2>/dev/null)" = true ]; }
existe() { docker inspect "$1" >/dev/null 2>&1; }

# auxiliar ARGS...: roda um comando no container de ferramentas (sqlite3, tar), com DADOS visível no mesmo caminho.
# Sem rede: só mexe em arquivos.
auxiliar() { docker run --rm --network none --user 0 --entrypoint sh -v "$MONTAGEM" "$@"; }

n8n_saudavel() { docker exec "$N8N_CONTAINER" wget -q -T 5 -O /dev/null http://127.0.0.1:5678/healthz 2>/dev/null; }

esperar_n8n() {
  local i
  for i in $(seq 1 "${1:-60}"); do
    n8n_saudavel && return 0
    sleep 5
  done
  return 1
}

esperar_postgres() {
  local i
  for i in $(seq 1 60); do
    docker exec "$EVO_PG_CONTAINER" sh -c 'pg_isready -q -U "$POSTGRES_USER"' 2>/dev/null && return 0
    sleep 2
  done
  return 1
}

# ---------- cópia e restauração ----------

# copiar_n8n DESTINO: cópia consistente do SQLite do n8n (mesmo com o n8n rodando) + demais arquivos da pasta .n8n.
copiar_n8n() {
  mkdir -p "$1"
  auxiliar --volumes-from "$N8N_CONTAINER" "$FERRAMENTAS" -euc '
    d="$1"; n="$2"
    rm -f "$d/database.sqlite"
    sqlite3 "$n/database.sqlite" ".backup $d/database.sqlite"
    test "$(sqlite3 "$d/database.sqlite" "pragma quick_check")" = ok
    tar -C "$n" -cf "$d/arquivos.tar" --exclude ./database.sqlite --exclude ./database.sqlite-wal \
      --exclude ./database.sqlite-shm --exclude ./database.sqlite-journal --exclude ./binaryData .' _ "$1" "$N8N_DIR"
}

# restaurar_n8n ORIGEM: com o container do n8n parado, troca o banco e os arquivos pelos da cópia.
restaurar_n8n() {
  auxiliar --volumes-from "$N8N_CONTAINER" "$FERRAMENTAS" -euc '
    s="$1"; n="$2"
    test "$(sqlite3 "$s/database.sqlite" "pragma quick_check")" = ok
    rm -f "$n/database.sqlite" "$n/database.sqlite-wal" "$n/database.sqlite-shm" "$n/database.sqlite-journal"
    tar -C "$n" -xf "$s/arquivos.tar"
    cp "$s/database.sqlite" "$n/database.sqlite"
    chown -R 1000:1000 "$n"' _ "$1" "$N8N_DIR"
}

# volumes nomeados montados no container (destinos), separados por espaço
volumes_de() { docker inspect -f '{{range .Mounts}}{{if eq .Type "volume"}}{{.Destination}} {{end}}{{end}}' "$1"; }

# copiar_evolution DESTINO: banco da Evolution (pg_dump) + volumes da API (sessão do WhatsApp).
copiar_evolution() {
  mkdir -p "$1"
  if ! docker exec "$EVO_PG_CONTAINER" sh -c 'pg_dump -U "$POSTGRES_USER" -d "${POSTGRES_DB:-$POSTGRES_USER}" -Fc' > "$1/banco.dump.tmp" ||
    [ ! -s "$1/banco.dump.tmp" ]; then
    rm -f "$1/banco.dump.tmp"
    return 1
  fi
  mv "$1/banco.dump.tmp" "$1/banco.dump"
  local vols
  vols=$(volumes_de "$EVO_API_CONTAINER")
  if [ -n "$vols" ]; then
    # shellcheck disable=SC2086
    auxiliar --volumes-from "$EVO_API_CONTAINER" "$FERRAMENTAS" -euc 'd="$1"; shift; tar -cf "$d/volumes.tar" "$@"' _ "$1" $vols
  else
    rm -f "$1/volumes.tar"
  fi
}

# restaurar_evolution ORIGEM: com a API parada e o Postgres rodando, troca o banco e os volumes da API.
restaurar_evolution() {
  esperar_postgres || { log "Postgres da Evolution não respondeu"; return 1; }
  docker exec -i "$EVO_PG_CONTAINER" sh -c \
    'pg_restore -U "$POSTGRES_USER" -d "${POSTGRES_DB:-$POSTGRES_USER}" --clean --if-exists --no-owner --single-transaction' \
    < "$1/banco.dump" || return 1
  if [ -s "$1/volumes.tar" ]; then
    local vols
    vols=$(volumes_de "$EVO_API_CONTAINER")
    # shellcheck disable=SC2086
    auxiliar --volumes-from "$EVO_API_CONTAINER" "$FERRAMENTAS" -euc '
      s="$1"; shift
      for v in "$@"; do find "$v" -mindepth 1 -delete; done
      tar -C / -xf "$s/volumes.tar"' _ "$1" $vols
  fi
}
