#!/usr/bin/env bash
# Simulação de ponta a ponta da virada e da volta, com dois Docker na mesma máquina:
#   DOCKER_A = "principal" (projetos n8n, evolution-dyno, dyno-site, dyno-n8n-dominio)
#   DOCKER_B = "reserva"   (começa vazio)
# Usa um sshd local (porta 2222, usuário dyno com rrsync) e árbitro/Cloudflare falsos (falsos.py).
# Pré-requisitos: dois dockerd rodando, sshd, rsync, sqlite3, jq, python3; rodar como root.
# Uso: T=/tmp/sim bash simular.sh
set -uo pipefail
AQUI=$(cd "$(dirname "$0")" && pwd)
SRC=$AQUI/../src
T=${T:?defina T (pasta de trabalho)}
DOCKER_A=${DOCKER_A:-unix:///var/run/docker.sock}
DOCKER_B=${DOCKER_B:-unix:///var/run/docker-reserva.sock}
TOKEN=token-de-teste-0123456789abcdef0123456789
PORTA=8787
URL=http://127.0.0.1:$PORTA
BASE=${BASE:-/srv/sim-dyno-reserva}   # fora de /tmp: o dyno precisa atravessar o caminho

ok() { echo "  OK  $*"; }
falha() { echo "  FALHOU  $*"; FALHAS=$((FALHAS + 1)); }
FALHAS=0
A() { DOCKER_HOST=$DOCKER_A docker "$@"; }
B() { DOCKER_HOST=$DOCKER_B docker "$@"; }
estado() { curl -s "$URL/_estado"; }
esperar() { # esperar SEGUNDOS DESCRICAO COMANDO...
  local s=$1 d=$2 i; shift 2
  for i in $(seq 1 "$s"); do "$@" >/dev/null 2>&1 && { ok "$d (${i}s)"; return 0; }; sleep 1; done
  falha "$d (desisti após ${s}s)"; return 1
}

limpar() {
  pkill -f "agente.sh rodar" 2>/dev/null; pkill -f "vigia.sh rodar" 2>/dev/null; pkill -f "falsos.py $PORTA" 2>/dev/null
  for p in dyno-n8n-dominio dyno-site evolution-dyno n8n; do
    [ -d "$T/docker/$p" ] && (cd "$T/docker/$p" && DOCKER_HOST=$DOCKER_A docker compose -p "$p" down -v >/dev/null 2>&1)
    [ -d "$BASE/projetos/$p" ] && (cd "$BASE/projetos/$p" && DOCKER_HOST=$DOCKER_B docker compose -p "$p" down -v >/dev/null 2>&1)
  done
  rm -rf "$T/docker" "$T/agente" "$BASE"
}

env_comum() {
  export SUPABASE_URL=$URL SUPABASE_ANON=chave-publica SERVIDOR_TOKEN=$TOKEN INTERVALO=2
}
agente() { # agente COMANDO
  ( env_comum; export PAPEL=principal DADOS=$T/agente MONTAGEM=$T/agente:$T/agente DOCKER_HOST=$DOCKER_A \
      RESERVA_HOST=127.0.0.1 RESERVA_PORTA=2222 INTERVALO_COPIA=8
    exec bash "$SRC/agente.sh" "$@" )
}
vigia() { # vigia COMANDO
  ( env_comum; export PAPEL=reserva DADOS=$BASE MONTAGEM=$BASE:$BASE DOCKER_HOST=$DOCKER_B \
      PRINCIPAL_IP=127.0.0.2 RESERVA_IP=10.0.0.9 CF_TOKEN=x CF_ZONA=zona CF_API=$URL/client/v4 SILENCIO_S=6 FALHAS_DIRETAS=2
    exec bash "$SRC/vigia.sh" "$@" )
}

# ---------------------------------------------------------------- preparação
echo "== preparação"
limpar
mkdir -p "$T/docker"/{n8n,evolution-dyno,dyno-site,dyno-n8n-dominio} "$T/agente" "$BASE"/{copias,saida}
cat > "$T/docker/n8n/docker-compose.yml" <<'EOF'
services:
  n8n:
    image: n8nio/n8n
    restart: always
    environment:
      - N8N_DIAGNOSTICS_ENABLED=false
      - N8N_SECURE_COOKIE=false
      - N8N_LISTEN_ADDRESS=0.0.0.0
    volumes:
      - n8n_data:/home/node/.n8n
volumes:
  n8n_data:
EOF
cat > "$T/docker/evolution-dyno/docker-compose.yml" <<'EOF'
services:
  dyno-evo-postgres:
    image: postgres:15-alpine
    container_name: dyno-evo-postgres
    restart: always
    environment: {POSTGRES_USER: evo, POSTGRES_PASSWORD: segredo, POSTGRES_DB: evolution}
    volumes: [evo_pg:/var/lib/postgresql/data]
  dyno-evo-api:
    image: alpine:3.20
    container_name: dyno-evo-api
    restart: always
    command: ["sleep", "infinity"]
    environment: {SEGREDO: "${EVO_SEGREDO}"}
    volumes: [evo_inst:/evolution/instances]
    networks: [default, n8n_default]
volumes: {evo_pg: {}, evo_inst: {}}
networks: {n8n_default: {external: true}}
EOF
echo "EVO_SEGREDO=valor-do-env" > "$T/docker/evolution-dyno/.env"
cat > "$T/docker/dyno-site/docker-compose.yml" <<'EOF'
services:
  dyno-site:
    image: alpine:3.20
    container_name: dyno-site
    restart: unless-stopped
    command: ["sleep", "infinity"]
    networks: [n8n_default]
networks: {n8n_default: {external: true}}
EOF
cp "$AQUI/../principal/dyno-n8n-dominio.yml" "$T/docker/dyno-n8n-dominio/docker-compose.yml"

python3 "$AQUI/falsos.py" $PORTA $TOKEN 5 >/dev/null 2>&1 &
esperar 10 "árbitro falso no ar" curl -sf "$URL/_estado"

# usuário dyno + sshd com rrsync (como no preparar-servidor.sh do reserva)
id dyno >/dev/null 2>&1 || useradd -m -s /bin/sh dyno
usermod -p '*' dyno   # sem senha, mas não bloqueado (com a senha bloqueada o sshd recusa até chave)
chown -R dyno:dyno "$BASE" && chmod 750 "$BASE"
mkdir -p /run/sshd && ssh-keygen -A >/dev/null
pgrep -f "sshd -p 2222" >/dev/null || /usr/sbin/sshd -p 2222 -o PasswordAuthentication=no -o UsePAM=no
agente verificar >/dev/null 2>&1
mkdir -p /home/dyno/.ssh
echo "command=\"rrsync $BASE\",restrict $(cat "$T/agente/ssh/id_ed25519.pub")" > /home/dyno/.ssh/authorized_keys
chown -R dyno:dyno /home/dyno/.ssh && chmod 700 /home/dyno/.ssh && chmod 600 /home/dyno/.ssh/authorized_keys

echo "== principal no ar"
for p in n8n evolution-dyno dyno-site dyno-n8n-dominio; do
  (cd "$T/docker/$p" && DOCKER_HOST=$DOCKER_A docker compose -p "$p" up -d --quiet-pull >/dev/null 2>&1) || falha "subir $p"
done
esperar 180 "n8n do principal saudável" A exec n8n-n8n-1 wget -q -O /dev/null http://127.0.0.1:5678/healthz
esperar 60 "Postgres da Evolution pronto" A exec dyno-evo-postgres pg_isready -q -U evo
esperar 30 "proxy n8n.dynoapp.com.br repassa para o n8n" A exec dyno-n8n-dominio wget -q -O /dev/null http://127.0.0.1/healthz

importar() { # importar DOCKER NOME
  printf '[{"id":"%s","name":"%s","nodes":[],"connections":{},"active":false,"settings":{}}]' "$(echo "$2" | md5sum | cut -c1-16)" "$2" |
    DOCKER_HOST=$1 docker exec -i n8n-n8n-1 sh -c 'cat > /tmp/w.json && n8n import:workflow --input=/tmp/w.json' >/dev/null 2>&1
}
tem_workflow() { DOCKER_HOST=$1 docker exec n8n-n8n-1 n8n list:workflow 2>/dev/null | grep -q "$2"; }
marcador() { DOCKER_HOST=$1 docker exec dyno-evo-postgres psql -U evo -d evolution -tAc "select v from marcador"; }
sessao() { DOCKER_HOST=$1 docker exec dyno-evo-api cat /evolution/instances/sessao.json; }

importar "$DOCKER_A" marcador-v1 && ok "workflow marcador-v1 criado no principal" || falha "importar workflow"
A exec dyno-evo-postgres psql -U evo -d evolution -qc "create table marcador(v text); insert into marcador values('v1')" >/dev/null
A exec dyno-evo-api sh -c 'echo v1 > /evolution/instances/sessao.json'

# ---------------------------------------------------------------- cópias
echo "== agente e vigia rodando (principal vivo: o reserva não pode assumir)"
agente rodar > "$T/agente.log" 2>&1 &
vigia rodar > "$T/vigia.log" 2>&1 &
esperar 120 "primeira cópia chegou ao reserva" test -s "$BASE/copias/ULTIMA"
importar "$DOCKER_A" marcador-v2 && ok "workflow marcador-v2 criado depois da 1ª cópia"
A exec dyno-evo-postgres psql -U evo -d evolution -qc "update marcador set v='v2'" >/dev/null
A exec dyno-evo-api sh -c 'echo v2 > /evolution/instances/sessao.json'
U1=$(cat "$BASE/copias/ULTIMA")
esperar 120 "segunda cópia no outro espaço" sh -c "[ \"\$(cat $BASE/copias/ULTIMA)\" != \"$U1\" ]"
sleep 15
[ "$(estado | jq -r .estado.ativo)" = principal ] && ok "com o principal vivo o reserva não assumiu" || falha "o reserva assumiu com o principal vivo"
B ps -q | grep -q . && falha "há containers no reserva antes da virada" || ok "reserva sem nada ligado antes da virada"

# ---------------------------------------------------------------- queda do principal
echo "== principal cai (agente morre e containers param)"
pkill -f "agente.sh rodar"
A stop -t 5 n8n-n8n-1 dyno-evo-api dyno-evo-postgres dyno-site dyno-n8n-dominio >/dev/null
esperar 400 "reserva assumiu no árbitro" sh -c "curl -s $URL/_estado | jq -e '.estado.ativo == \"reserva\"'"
esperar 400 "ativação concluída" test -s "$BASE/ativado"
esperar 120 "n8n do reserva saudável" B exec n8n-n8n-1 wget -q -O /dev/null http://127.0.0.1:5678/healthz
tem_workflow "$DOCKER_B" marcador-v2 && ok "reserva tem o workflow da última cópia (v2)" || falha "workflow v2 não está no reserva"
[ "$(marcador "$DOCKER_B")" = v2 ] && ok "banco da Evolution restaurado (v2)" || falha "banco da Evolution: $(marcador "$DOCKER_B")"
[ "$(sessao "$DOCKER_B")" = v2 ] && ok "sessão do WhatsApp restaurada (v2)" || falha "sessão: $(sessao "$DOCKER_B")"
[ "$(B exec dyno-evo-api printenv SEGREDO)" = valor-do-env ] && ok ".env do projeto veio junto" || falha ".env do projeto"
[ "$(A image inspect -f '{{.Id}}' n8nio/n8n)" = "$(B image inspect -f '{{.Id}}' n8nio/n8n)" ] && ok "mesma versão do n8n nos dois" || falha "versão do n8n diferente"
estado | jq -e '.dns | to_entries | all(.value == "10.0.0.9")' >/dev/null && ok "DNS virado para o reserva" || falha "DNS: $(estado | jq -c .dns)"
B exec dyno-n8n-dominio wget -q -O /dev/null http://127.0.0.1/healthz && ok "n8n.dynoapp.com.br responde no reserva" || falha "proxy no reserva"

# ---------------------------------------------------------------- principal volta
echo "== principal volta (containers religam sozinhos) e o agente faz a cerca"
importar "$DOCKER_B" criado-no-reserva && ok "workflow criado durante a virada"
B exec dyno-evo-postgres psql -U evo -d evolution -qc "update marcador set v='v3'" >/dev/null
B exec dyno-evo-api sh -c 'echo v3 > /evolution/instances/sessao.json'
A start dyno-evo-postgres n8n-n8n-1 dyno-evo-api dyno-site dyno-n8n-dominio >/dev/null
agente rodar >> "$T/agente.log" 2>&1 &
esperar 60 "cerca: n8n do principal parado" sh -c "[ \"\$(DOCKER_HOST=$DOCKER_A docker inspect -f '{{.State.Running}}' n8n-n8n-1)\" = false ]"
esperar 30 "cerca: Evolution do principal parada" sh -c "[ \"\$(DOCKER_HOST=$DOCKER_A docker inspect -f '{{.State.Running}}' dyno-evo-api)\" = false ]"
[ "$(A inspect -f '{{.HostConfig.RestartPolicy.Name}}' n8n-n8n-1)" = no ] && ok "cerca: n8n do principal não religa sozinho" || falha "política de reinício"
[ "$(estado | jq -r .estado.ativo)" = reserva ] && ok "reserva continua ativo" || falha "estado mudou sozinho"

# ---------------------------------------------------------------- volta planejada
echo "== volta planejada (vigia.sh voltar --sim)"
vigia voltar --sim > "$T/volta.log" 2>&1
grep -q "volta concluída" "$T/volta.log" && ok "comando de volta terminou" || falha "volta: $(tail -3 "$T/volta.log")"
[ "$(estado | jq -r .estado.ativo)" = principal ] && ok "principal ativo de novo" || falha "estado: $(estado | jq -r .estado.ativo)"
esperar 60 "n8n do principal saudável" A exec n8n-n8n-1 wget -q -O /dev/null http://127.0.0.1:5678/healthz
tem_workflow "$DOCKER_A" criado-no-reserva && ok "principal recebeu o que foi criado no reserva" || falha "workflow do reserva não voltou"
[ "$(marcador "$DOCKER_A")" = v3 ] && ok "banco da Evolution voltou (v3)" || falha "banco da Evolution: $(marcador "$DOCKER_A")"
[ "$(sessao "$DOCKER_A")" = v3 ] && ok "sessão do WhatsApp voltou (v3)" || falha "sessão: $(sessao "$DOCKER_A")"
[ "$(A inspect -f '{{.HostConfig.RestartPolicy.Name}}' n8n-n8n-1)" = always ] && ok "política de reinício restaurada" || falha "política: $(A inspect -f '{{.HostConfig.RestartPolicy.Name}}' n8n-n8n-1)"
estado | jq -e '.dns | to_entries | all(.value == "127.0.0.2")' >/dev/null && ok "DNS de volta ao principal" || falha "DNS: $(estado | jq -c .dns)"
B ps -q | grep -q . && falha "ainda há containers ligados no reserva" || ok "reserva desligado e esperando"
esperar 60 "cópias recomeçaram depois da volta" sh -c "grep -c 'cópia enviada' $T/agente.log | awk '{exit !(\$1 >= 3)}'"
estado | jq -c '.eventos'

echo "== resultado: $FALHAS falha(s)"
[ "${MANTER:-0}" = 1 ] || limpar
exit $FALHAS
