#!/usr/bin/env bash
# Vigia do servidor RESERVA (outro provedor).
#  - A cada INTERVALO s: bate ponto no árbitro e testa o principal direto pelo IP.
#  - Assume sozinho só quando as duas coisas falham: o principal parou de bater ponto há SILENCIO_S s
#    e não responde direto há FALHAS_DIRETAS tentativas. O árbitro garante que só um lado ganha.
#  - Ao assumir: restaura a última cópia, sobe os projetos com a mesma versão do n8n e vira o DNS na Cloudflare.
#  Comandos: vigia.sh [rodar|verificar|voltar [--sim]]
# shellcheck source=comum.sh
. "$(dirname "$0")/comum.sh"

: "${PRINCIPAL_IP:?defina PRINCIPAL_IP}"
: "${RESERVA_IP:?defina RESERVA_IP (IP público deste servidor)}"
PROJETOS=${PROJETOS:-n8n evolution-dyno dyno-site dyno-n8n-dominio}
SONDA_HOST=${SONDA_HOST:-n8n.srv1825327.hstgr.cloud}
SONDA_CAMINHO=${SONDA_CAMINHO:-/healthz}
SILENCIO_S=${SILENCIO_S:-180}
FALHAS_DIRETAS=${FALHAS_DIRETAS:-4}
AUTO=${AUTO:-1}
CF_API=${CF_API:-https://api.cloudflare.com/client/v4}
CF_NOMES=${CF_NOMES:-dynoapp.com.br wa.dynoapp.com.br n8n.dynoapp.com.br}

compose() { local p=$1; shift; (cd "$DADOS/projetos/$p" && docker compose -p "$p" "$@"); }

# ---------- cópia recebida ----------

ultima_copia() { echo "$DADOS/copias/$(cat "$DADOS/copias/ULTIMA" 2>/dev/null)"; }

copia_completa() {
  [ -s "$1/info.json" ] && [ -s "$1/n8n/database.sqlite" ] && [ -s "$1/n8n/arquivos.tar" ] && [ -s "$1/evolution/banco.dump" ]
}

idade_copia() {
  jq -r '(now - (.criada_em | fromdateiso8601)) | floor' "$(ultima_copia)/info.json" 2>/dev/null || echo -1
}

# ---------- testes ----------

sondar_principal() {
  local c
  c=$(curl -sk -o /dev/null -m 10 -w '%{http_code}' --resolve "$SONDA_HOST:443:$PRINCIPAL_IP" "https://$SONDA_HOST$SONDA_CAMINHO" 2>/dev/null)
  [ "${c:-0}" -ge 200 ] 2>/dev/null && [ "$c" -lt 500 ]
}

# ---------- DNS (Cloudflare) ----------

cf() { curl -sS -m 20 -H "Authorization: Bearer ${CF_TOKEN:-}" -H "Content-Type: application/json" "$@"; }

dns_apontar() {
  local ip=$1 nome id r falhou=0
  if [ -z "${CF_TOKEN:-}" ] || [ -z "${CF_ZONA:-}" ]; then
    log "DNS: Cloudflare não configurada; aponte $CF_NOMES para $ip à mão"
    return 1
  fi
  for nome in $CF_NOMES; do
    id=$(cf "$CF_API/zones/$CF_ZONA/dns_records?type=A&name=$nome" | jq -r '.result[0].id // empty')
    if [ -z "$id" ]; then log "DNS: registro A de $nome não encontrado"; falhou=1; continue; fi
    r=$(cf -X PATCH "$CF_API/zones/$CF_ZONA/dns_records/$id" -d "$(jq -nc --arg ip "$ip" '{content: $ip}')")
    if jq -e .success <<<"$r" >/dev/null 2>&1; then log "DNS: $nome -> $ip"; else log "DNS: falhou em $nome: $r"; falhou=1; fi
  done
  return $falhou
}

# ---------- assumir ----------

# fixar_n8n INFO: deixa a imagem do n8n na mesma versão do principal (o banco não pode ir para uma versão mais antiga
# na volta). Usa a imagem já baixada pelo preparar(); só vai ao registro se ela não estiver aqui.
fixar_n8n() {
  local ref dig
  ref=$(jq -r '.n8n_imagem // empty' "$1")
  dig=$(jq -r '.n8n_digest // empty' "$1")
  if [ -z "$ref" ] || [ -z "$dig" ] || [[ "$ref" == *@* ]]; then log "aviso: versão do n8n não fixada (imagem '$ref')"; return 0; fi
  if docker image inspect "$dig" >/dev/null 2>&1 || docker pull -q "$dig" >/dev/null 2>&1; then
    docker tag "$dig" "$ref" && log "n8n fixado na versão do principal: $(jq -r '.n8n_versao // "?"' "$1")"
  else
    log "ERRO: não consegui a imagem do n8n do principal ($dig); vai a versão que estiver aqui"
    return 1
  fi
}

extrair_projetos() { # extrair_projetos COPIA DESTINO
  local t
  rm -rf "$2.novo" && mkdir -p "$2.novo"
  for t in "$1"/projetos/*.tar; do [ -e "$t" ] && tar -C "$2.novo" -xf "$t"; done
  rm -rf "$2" && mv "$2.novo" "$2"
}

# Enquanto o principal atende, deixa as imagens baixadas (as dos projetos e a versão exata do n8n), para a virada
# não depender do Docker Hub. Só refaz quando os projetos ou a versão do n8n mudam.
preparar() {
  local origem marca p
  origem=$(ultima_copia)
  copia_completa "$origem" || return 0
  marca=$( { cat "$origem"/projetos/*.tar 2>/dev/null; jq -r '.n8n_digest // ""' "$origem/info.json"; } | sha256sum | cut -c1-16)
  [ "$(cat "$DADOS/preparado" 2>/dev/null)" = "$marca" ] && return 0
  log "baixando as imagens dos projetos (preparo para uma virada)"
  extrair_projetos "$origem" "$DADOS/preparo"
  for p in $PROJETOS; do
    [ -d "$DADOS/preparo/$p" ] || continue
    (cd "$DADOS/preparo/$p" && docker compose -p "$p" pull -q --ignore-pull-failures >/dev/null 2>&1) || log "aviso: falha ao baixar imagens de $p"
  done
  if fixar_n8n "$origem/info.json"; then
    echo "$marca" > "$DADOS/preparado"
    log "imagens prontas para uma virada"
  fi
}

parar_servicos() {
  local c
  for c in "$N8N_CONTAINER" "$EVO_API_CONTAINER"; do
    rodando "$c" && docker stop -t 30 "$c" >/dev/null && log "parei $c"
  done
  return 0
}

# ativar MUDOU_EM: sobe tudo a partir da última cópia. Segue mesmo se uma parte falhar (o resto ainda ajuda).
ativar() {
  local mudou=$1 origem p n8n_feito=0 evo_feito=0
  origem=$(ultima_copia)
  copia_completa "$origem" || { log "ATIVAÇÃO: não há cópia completa em $origem"; return 1; }
  log "ATIVANDO o reserva com a cópia de $(jq -r .criada_em "$origem/info.json")"

  extrair_projetos "$origem" "$DADOS/projetos"
  fixar_n8n "$origem/info.json"

  for p in $PROJETOS; do
    [ -d "$DADOS/projetos/$p" ] || continue
    compose "$p" up --no-start --pull missing >/dev/null 2>&1 || { log "ERRO: não consegui criar os containers de $p"; continue; }
    if [ $n8n_feito = 0 ] && existe "$N8N_CONTAINER"; then
      rodando "$N8N_CONTAINER" && docker stop -t 30 "$N8N_CONTAINER" >/dev/null
      if restaurar_n8n "$origem/n8n"; then log "n8n restaurado"; else log "ERRO: restauração do n8n falhou"; fi
      n8n_feito=1
    fi
    if [ $evo_feito = 0 ] && existe "$EVO_PG_CONTAINER" && existe "$EVO_API_CONTAINER"; then
      rodando "$EVO_API_CONTAINER" && docker stop -t 30 "$EVO_API_CONTAINER" >/dev/null
      docker start "$EVO_PG_CONTAINER" >/dev/null
      if restaurar_evolution "$origem/evolution"; then log "Evolution restaurada"; else log "ERRO: restauração da Evolution falhou"; fi
      evo_feito=1
    fi
    if compose "$p" up -d --pull missing >/dev/null 2>&1; then log "projeto $p no ar"; else log "ERRO: projeto $p não subiu"; fi
  done

  if esperar_n8n 36; then log "n8n saudável"; else log "ERRO: o n8n não ficou saudável em 3 min"; fi
  dns_apontar "$RESERVA_IP" || log "ERRO: o DNS não foi virado por completo"
  echo "$mudou" > "$DADOS/ativado"
  log "reserva ATIVO. Se o WhatsApp pedir QR code, reconecte a instância no manager da Evolution."
}

# ---------- voltar ao principal (planejado) ----------

voltar() {
  local est ativo sil r id i
  if ! est=$(batimento) || ! jq -e .ok <<<"$est" >/dev/null; then echo "árbitro inacessível: $est"; return 1; fi
  ativo=$(jq -r .ativo <<<"$est")
  sil=$(jq -r '.principal_silencio_s // 999999' <<<"$est")
  if [ "$ativo" = principal ]; then echo "O principal já é o ativo."; return 0; fi
  if [ "$sil" -ge 120 ]; then
    echo "O agente do principal não bate ponto há ${sil}s. Ligue o principal e confira o container dyno-reserva-agente antes."
    return 1
  fi
  if [ "$ativo" = reserva ]; then
    if [ "${1:-}" != --sim ]; then
      read -r -p "Parar o atendimento no reserva e devolver ao principal? Leva alguns minutos fora do ar. (sim/não) " r
      [ "$r" = sim ] || { echo "Cancelado."; return 1; }
    fi
    log "volta: parando n8n e Evolution no reserva"
    parar_servicos
    rm -rf "$DADOS/saida.novo"
    if ! copiar_n8n "$DADOS/saida.novo/n8n" || ! copiar_evolution "$DADOS/saida.novo/evolution"; then
      log "volta: falha ao copiar os dados; religando o reserva"
      docker start "$N8N_CONTAINER" "$EVO_API_CONTAINER" >/dev/null
      return 1
    fi
    id="$(date +%s)-$RANDOM"
    echo "$id" > "$DADOS/saida.novo/PRONTA"
    rm -rf "$DADOS/saida" && mv "$DADOS/saida.novo" "$DADOS/saida"
    chown -R "$(stat -c %u:%g "$DADOS")" "$DADOS/saida"
    batimento "$(jq -nc --arg id "$id" '{saida_id: $id}')" >/dev/null
    r=$(mudar reserva devolvendo "volta planejada ($id)")
    if ! jq -e .ok <<<"$r" >/dev/null 2>&1; then
      log "volta: árbitro recusou ($r); religando o reserva"
      docker start "$N8N_CONTAINER" "$EVO_API_CONTAINER" >/dev/null
      return 1
    fi
    log "volta: dados prontos ($id); esperando o principal restaurar (até 15 min)"
  fi
  for i in $(seq 1 60); do
    est=$(batimento) && [ "$(jq -r .ativo <<<"$est")" = principal ] && break
    sleep 15
  done
  if [ "$(jq -r .ativo <<<"$est" 2>/dev/null)" = principal ]; then
    dns_apontar "$PRINCIPAL_IP" || log "ERRO: o DNS não voltou por completo para o principal"
    for p in $(echo "$PROJETOS" | tr ' ' '\n' | tac); do
      [ -d "$DADOS/projetos/$p" ] && compose "$p" down >/dev/null 2>&1
    done
    rm -f "$DADOS/ativado"
    log "volta concluída: o principal atende de novo e o reserva voltou a esperar"
  else
    log "volta: o principal não confirmou em 15 min; o reserva volta a atender"
    mudar devolvendo reserva "volta cancelada: o principal não confirmou" >/dev/null
    docker start "$N8N_CONTAINER" "$EVO_API_CONTAINER" >/dev/null
    return 1
  fi
}

# ---------- comandos ----------

info_vigia() {
  jq -nc --argjson i "$(idade_copia)" --arg a "$(cat "$DADOS/ativado" 2>/dev/null)" '{copia_idade_s: $i, ativado: $a}'
}

verificar() {
  echo "== cópia mais recente: $(ultima_copia)"
  if copia_completa "$(ultima_copia)"; then
    jq . "$(ultima_copia)/info.json"; echo "idade: $(idade_copia) s"
  else
    echo "NENHUMA CÓPIA COMPLETA (o agente do principal já rodou?)"
  fi
  echo "== principal direto ($SONDA_HOST em $PRINCIPAL_IP)"
  sondar_principal && echo "responde" || echo "NÃO RESPONDE"
  echo "== árbitro"
  batimento "$(info_vigia)" || true
  echo
  echo "== Cloudflare"
  if [ -n "${CF_TOKEN:-}" ]; then
    cf "$CF_API/user/tokens/verify" | jq -c '{success, status: .result.status}'
    for n in $CF_NOMES; do
      echo "$n: $(cf "$CF_API/zones/${CF_ZONA:-x}/dns_records?type=A&name=$n" | jq -r '.result[0] | "\(.content) proxied=\(.proxied)"' 2>/dev/null)"
    done
  else
    echo "CF_TOKEN vazio"
  fi
}

rodar() {
  log "vigia iniciado (principal $PRINCIPAL_IP, assume após ${SILENCIO_S}s sem batimento e $FALHAS_DIRETAS falhas diretas, automático=$AUTO)"
  local falhas=0 est ativo sil mudou r
  while true; do
    if est=$(batimento "$(info_vigia)") && jq -e .ok <<<"$est" >/dev/null; then
      ativo=$(jq -r .ativo <<<"$est")
      mudou=$(jq -r .mudou_em <<<"$est")
      sil=$(jq -r '.principal_silencio_s // -1' <<<"$est")
      case $ativo in
        principal)
          # Nunca atender junto com o principal.
          rm -f "$DADOS/ativado"
          if rodando "$N8N_CONTAINER" || rodando "$EVO_API_CONTAINER"; then log "o principal é o ativo: parando o que está ligado aqui"; parar_servicos; fi
          if sondar_principal; then
            [ $falhas -gt 0 ] && log "principal respondeu de novo"
            falhas=0
          else
            falhas=$((falhas + 1))
            log "principal sem resposta direta ($falhas/$FALHAS_DIRETAS), sem batimento há ${sil}s"
          fi
          # Principal batendo ponto: aproveita para deixar as imagens prontas.
          [ "$sil" -ge 0 ] && [ "$sil" -lt "$SILENCIO_S" ] && preparar
          if [ "$AUTO" = 1 ] && [ $falhas -ge "$FALHAS_DIRETAS" ] && [ "$sil" -ge "$SILENCIO_S" ]; then
            if copia_completa "$(ultima_copia)"; then
              r=$(mudar principal reserva "principal sem batimento há ${sil}s e sem resposta direta em $falhas tentativas")
              if jq -e .ok <<<"$r" >/dev/null 2>&1; then ativar "$(jq -r .mudou_em <<<"$r")"; else log "árbitro recusou: $r"; fi
            else
              log "não assumo: não há cópia completa do principal"
            fi
          fi
          ;;
        reserva)
          [ "$(cat "$DADOS/ativado" 2>/dev/null)" = "$mudou" ] || ativar "$mudou"
          ;;
        devolvendo) : ;;
      esac
    else
      log "árbitro inacessível (não assumo nada sem ele): ${est:-sem resposta}"
    fi
    sleep "$INTERVALO"
  done
}

case "${1:-rodar}" in
  rodar) rodar ;;
  verificar) verificar ;;
  voltar) shift; voltar "$@" ;;
  *) echo "uso: vigia.sh [rodar|verificar|voltar [--sim]]"; exit 2 ;;
esac
