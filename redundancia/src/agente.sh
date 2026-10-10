#!/usr/bin/env bash
# Agente do servidor PRINCIPAL (VPS Hostinger).
#  - A cada INTERVALO s: bate ponto no árbitro (Supabase).
#  - Se este servidor é o ativo: a cada INTERVALO_COPIA s copia n8n, Evolution e os projetos para o reserva.
#  - Se o reserva assumiu: para o n8n e a Evolution daqui (cerca), para não atender em dobro.
#  - Na volta planejada (estado "devolvendo"): busca os dados do reserva, restaura, sobe e retoma.
#  Comandos: agente.sh [rodar|verificar|copiar]
# shellcheck source=comum.sh
. "$(dirname "$0")/comum.sh"

: "${RESERVA_HOST:?defina RESERVA_HOST (IP do servidor reserva)}"
RESERVA_PORTA=${RESERVA_PORTA:-22}
RESERVA_USUARIO=${RESERVA_USUARIO:-dyno}
INTERVALO_COPIA=${INTERVALO_COPIA:-300}
PROJETOS=${PROJETOS:-n8n evolution-dyno dyno-site dyno-n8n-dominio}
CERCA=${CERCA:-$N8N_CONTAINER $EVO_API_CONTAINER}

CHAVE=$DADOS/ssh/id_ed25519
SSH="ssh -i $CHAVE -p $RESERVA_PORTA -o BatchMode=yes -o ConnectTimeout=15 -o ServerAliveInterval=15 -o StrictHostKeyChecking=accept-new -o UserKnownHostsFile=$DADOS/ssh/known_hosts"
DESTINO="$RESERVA_USUARIO@$RESERVA_HOST"

preparar_chave() {
  mkdir -p "$DADOS/ssh" && chmod 700 "$DADOS/ssh"
  if [ ! -f "$CHAVE" ]; then
    ssh-keygen -q -t ed25519 -N '' -C dyno-principal -f "$CHAVE"
  fi
  log "Chave deste servidor (vai no reserva, em /home/dyno/.ssh/authorized_keys):"
  log "command=\"rrsync /srv/dyno-reserva\",restrict $(cat "$CHAVE.pub")"
}

# ---------- cópia para o reserva ----------

# Pasta do projeto no servidor (onde está o docker-compose.yml e o .env), lida da etiqueta que o Compose grava.
pasta_projeto() {
  docker ps -a --filter "label=com.docker.compose.project=$1" --format '{{.Label "com.docker.compose.project.working_dir"}}' | head -n 1
}

# copiar_projeto NOME DESTINO: empacota os arquivos de configuração do projeto (compose, .env) como NOME/.
# Só o primeiro nível e arquivos pequenos: subpastas podem ter dados vivos (ex.: Postgres), que vão por cópia própria.
copiar_projeto() {
  local dir
  dir=$(pasta_projeto "$1")
  [ -n "$dir" ] || return 1
  auxiliar -v "$dir:/projeto/$1:ro" "$FERRAMENTAS" -euc \
    'cd /projeto && find "$2" -maxdepth 1 -type f -size -5120k | tar -cf "$1" -T -' _ "$2/$1.tar" "$1"
}

info_n8n() {
  local ref img dig ver
  ref=$(docker inspect -f '{{.Config.Image}}' "$N8N_CONTAINER")
  img=$(docker inspect -f '{{.Image}}' "$N8N_CONTAINER")
  dig=$(docker image inspect -f '{{range .RepoDigests}}{{.}} {{end}}' "$img" | awk '{print $1}')
  ver=$(docker exec "$N8N_CONTAINER" n8n --version 2>/dev/null | tail -n 1)
  jq -nc --arg r "$ref" --arg d "$dig" --arg v "$ver" '{n8n_imagem: $r, n8n_digest: $d, n8n_versao: $v}'
}

copiar_e_enviar() {
  local t0 trab slot
  t0=$(date +%s)
  trab=$DADOS/trab
  rm -rf "$trab" && mkdir -p "$trab/projetos"
  copiar_n8n "$trab/n8n" || { log "cópia do n8n falhou"; return 1; }
  copiar_evolution "$trab/evolution" || { log "cópia da Evolution falhou"; return 1; }
  local p falta=""
  for p in $PROJETOS; do
    copiar_projeto "$p" "$trab/projetos" || falta="$falta $p"
  done
  [ -z "$falta" ] || log "aviso: projetos sem pasta encontrada (não vão para o reserva):$falta"
  info_n8n | jq --arg c "$(date -u +%FT%TZ)" --arg p "$PROJETOS" '. + {criada_em: $c, projetos: ($p | split(" "))}' > "$trab/info.json"

  # Dois espaços no reserva (a e b): escreve no que não é o atual e só depois aponta ULTIMA para ele.
  slot=a
  [ "$(cat "$DADOS/slot" 2>/dev/null)" = a ] && slot=b
  rsync -az --delete -e "$SSH" "$trab/" "$DESTINO:copias/$slot/" || { log "envio para o reserva falhou"; return 1; }
  echo "$slot" > "$DADOS/ULTIMA"
  rsync -a -e "$SSH" "$DADOS/ULTIMA" "$DESTINO:copias/ULTIMA" || { log "envio do marcador falhou"; return 1; }
  echo "$slot" > "$DADOS/slot"
  date +%s > "$DADOS/ultima_copia"
  log "cópia enviada ao reserva (espaço $slot, $(du -sh "$trab" | cut -f1), $(( $(date +%s) - t0 )) s)"
}

# ---------- cerca e volta ----------

cercar() {
  local c
  for c in $CERCA; do
    existe "$c" || continue
    [ -f "$DADOS/politica_$c" ] || docker inspect -f '{{.HostConfig.RestartPolicy.Name}}' "$c" > "$DADOS/politica_$c"
    docker update --restart=no "$c" >/dev/null
    if rodando "$c"; then docker stop -t 30 "$c" >/dev/null && log "cerca: parei $c (o reserva está atendendo)"; fi
  done
  touch "$DADOS/cercado"
}

descercar() {
  local c pol
  for c in $CERCA; do
    existe "$c" || continue
    pol=$(cat "$DADOS/politica_$c" 2>/dev/null || echo unless-stopped)
    [ "$pol" = no ] && pol=unless-stopped
    docker update --restart="$pol" "$c" >/dev/null
    rodando "$c" || docker start "$c" >/dev/null
    rm -f "$DADOS/politica_$c"
  done
  rm -f "$DADOS/cercado"
}

# Volta planejada: o reserva parou e deixou os dados em saida/. Busca, confere, restaura, sobe e devolve o comando.
receber_e_restaurar() {
  local id=$1 entrada=$DADOS/entrada
  [ -n "$id" ] || { log "volta: o reserva ainda não informou a saída"; return 1; }
  if [ "$(cat "$DADOS/restaurado" 2>/dev/null)" != "$id" ]; then
    cercar
    mkdir -p "$entrada"
    rsync -az --delete -e "$SSH" "$DESTINO:saida/" "$entrada/" || { log "volta: não consegui buscar os dados do reserva"; return 1; }
    [ "$(cat "$entrada/PRONTA" 2>/dev/null)" = "$id" ] || { log "volta: os dados no reserva não são os desta volta ($id)"; return 1; }
    restaurar_n8n "$entrada/n8n" || { log "volta: restauração do n8n falhou"; return 1; }
    restaurar_evolution "$entrada/evolution" || { log "volta: restauração da Evolution falhou"; return 1; }
    descercar
    esperar_n8n 60 || { log "volta: o n8n não ficou saudável; parando de novo"; cercar; return 1; }
    echo "$id" > "$DADOS/restaurado"
    log "volta: dados do reserva restaurados ($id)"
  fi
  local r
  r=$(mudar devolvendo principal "dados do reserva restaurados no principal ($id)") || return 1
  if jq -e .ok <<<"$r" >/dev/null; then
    log "volta concluída: o principal voltou a atender"
    rm -f "$DADOS/slot"   # próxima cópia recomeça no espaço a
  else
    log "volta: árbitro recusou ($r)"
  fi
}

# ---------- comandos ----------

verificar() {
  echo "== containers"
  local c
  for c in $N8N_CONTAINER $EVO_PG_CONTAINER $EVO_API_CONTAINER; do
    if existe "$c"; then
      echo "$c: $(docker inspect -f '{{.State.Status}} imagem={{.Config.Image}} reinicio={{.HostConfig.RestartPolicy.Name}} redes={{range $k, $v := .NetworkSettings.Networks}}{{$k}} {{end}}' "$c")"
      docker inspect -f '{{range .Mounts}}   {{.Type}} {{.Name}}{{.Source}} -> {{.Destination}}{{"\n"}}{{end}}' "$c"
    else
      echo "$c: NÃO ENCONTRADO"
    fi
  done
  echo "== projetos (pasta no servidor)"
  local p d
  for p in $PROJETOS; do d=$(pasta_projeto "$p"); echo "$p: ${d:-NÃO ENCONTRADO}"; done
  echo "== n8n"
  info_n8n
  echo "== árbitro"
  batimento || true
  echo
  echo "== reserva ($DESTINO)"
  rsync -e "$SSH" --list-only "$DESTINO:" && echo "acesso ao reserva: ok" || echo "acesso ao reserva: FALHOU"
}

# Batimento em processo separado: o ponto é batido a cada INTERVALO s mesmo durante uma cópia ou restauração
# demorada (senão o reserva poderia achar que o principal morreu). Grava o último estado em estado.json.
batedor() {
  local est info
  while true; do
    info=$(jq -nc --argjson u "$(cat "$DADOS/ultima_copia" 2>/dev/null || echo 0)" --arg s "$(cat "$DADOS/slot" 2>/dev/null)" \
      --argjson c "$([ -f "$DADOS/cercado" ] && echo true || echo false)" '{ultima_copia: $u, slot: $s, cercado: $c}')
    if est=$(batimento "$info") && jq -e .ok <<<"$est" >/dev/null 2>&1; then
      jq -c --argjson t "$(date +%s)" '. + {lido_em: $t}' <<<"$est" > "$DADOS/estado.json.tmp" && mv "$DADOS/estado.json.tmp" "$DADOS/estado.json"
    else
      log "árbitro inacessível: ${est:-sem resposta}"
    fi
    sleep "$INTERVALO"
  done
}

# Estado lido há pouco (até 3 batimentos); vazio se o árbitro não responde.
estado_recente() {
  jq -c --argjson agora "$(date +%s)" --argjson max $((INTERVALO * 3 + 5)) 'select(($agora - .lido_em) <= $max)' "$DADOS/estado.json" 2>/dev/null
}

rodar() {
  preparar_chave
  log "agente iniciado (reserva $DESTINO, cópia a cada ${INTERVALO_COPIA}s)"
  rm -f "$DADOS/estado.json"
  batedor &
  trap 'kill $! 2>/dev/null' EXIT
  local est ativo ultima
  while true; do
    ultima=$(cat "$DADOS/ultima_copia" 2>/dev/null || echo 0)
    est=$(estado_recente)
    if [ -n "$est" ]; then
      ativo=$(jq -r .ativo <<<"$est")
      case $ativo in
        principal)
          if [ -f "$DADOS/cercado" ]; then log "ativo de novo: religando n8n e Evolution"; descercar; fi
          if [ $(( $(date +%s) - ultima )) -ge "$INTERVALO_COPIA" ]; then copiar_e_enviar || true; fi
          ;;
        reserva)
          cercar
          ;;
        devolvendo)
          receber_e_restaurar "$(jq -r '.reserva_info.saida_id // empty' <<<"$est")" || true
          ;;
      esac
    else
      # Sem árbitro não muda nada: se já estava atendendo, continua (e continua copiando).
      if [ ! -f "$DADOS/cercado" ] && [ $(( $(date +%s) - ultima )) -ge "$INTERVALO_COPIA" ]; then copiar_e_enviar || true; fi
    fi
    sleep "$INTERVALO"
  done
}

case "${1:-rodar}" in
  rodar) rodar ;;
  verificar) preparar_chave; verificar ;;
  copiar) preparar_chave; copiar_e_enviar ;;
  *) echo "uso: agente.sh [rodar|verificar|copiar]"; exit 2 ;;
esac
