#!/usr/bin/env bash
# Prepara um VPS novo (Ubuntu 22.04 ou 24.04) para ser o servidor RESERVA do Dyno. Rodar uma vez, como root:
#   bash preparar-servidor.sh
# Depois: editar /opt/dyno-reserva/.env, copiar o docker-compose.yml desta pasta para /opt/dyno-reserva e subir.
# Pode rodar de novo sem estragar nada (não troca o token nem a chave já cadastrada).
set -euo pipefail
[ "$(id -u)" = 0 ] || { echo "rode como root"; exit 1; }

echo "== Docker"
if ! command -v docker >/dev/null; then
  curl -fsSL https://get.docker.com | sh
fi
systemctl enable --now docker >/dev/null

echo "== rsync e rrsync (o principal só consegue escrever em /srv/dyno-reserva)"
apt-get update -qq && apt-get install -y -qq rsync python3 openssl ufw >/dev/null
if ! command -v rrsync >/dev/null; then
  gunzip -c /usr/share/doc/rsync/scripts/rrsync.gz > /usr/local/bin/rrsync 2>/dev/null || cp /usr/share/doc/rsync/scripts/rrsync /usr/local/bin/rrsync
  chmod 755 /usr/local/bin/rrsync
fi

echo "== usuário dyno e pastas"
id dyno >/dev/null 2>&1 || useradd -m -s /bin/sh dyno
usermod -p '*' dyno   # sem senha, mas não bloqueado (com a senha bloqueada o sshd pode recusar até a chave)
mkdir -p /srv/dyno-reserva/copias /srv/dyno-reserva/saida
chown -R dyno:dyno /srv/dyno-reserva && chmod 750 /srv/dyno-reserva
install -d -m 700 -o dyno -g dyno /home/dyno/.ssh
touch /home/dyno/.ssh/authorized_keys && chown dyno:dyno /home/dyno/.ssh/authorized_keys && chmod 600 /home/dyno/.ssh/authorized_keys

echo "== firewall (SSH, HTTP e HTTPS)"
ufw allow 22/tcp >/dev/null && ufw allow 80/tcp >/dev/null && ufw allow 443/tcp >/dev/null
ufw --force enable >/dev/null

echo "== /opt/dyno-reserva/.env"
mkdir -p /opt/dyno-reserva
ENV=/opt/dyno-reserva/.env
if [ ! -f "$ENV" ]; then
  cat > "$ENV" <<EOF
# Token que o principal e o reserva usam para falar com o árbitro no Supabase. O MESMO vai no principal.
SERVIDOR_TOKEN=$(openssl rand -hex 32)
# IP público deste servidor e do principal (Hostinger)
RESERVA_IP=$(curl -fsS -4 https://api.ipify.org || echo PREENCHA)
PRINCIPAL_IP=77.37.41.74
# Cloudflare: token com permissão "Zone > DNS > Edit" só para dynoapp.com.br, e o Zone ID (Overview do domínio)
CF_TOKEN=
CF_ZONA=
# 1 = assume sozinho quando o principal cai; 0 = só avisa (a virada fica manual)
AUTO=1
EOF
  chmod 600 "$ENV"
fi
TOKEN=$(grep '^SERVIDOR_TOKEN=' "$ENV" | cut -d= -f2)

cat <<EOF

Pronto. Falta:
1. Preencher CF_TOKEN e CF_ZONA em $ENV
2. Copiar o docker-compose.yml (redundancia/reserva/) para /opt/dyno-reserva/ e rodar:
     cd /opt/dyno-reserva && docker compose up -d
3. No Supabase, cadastrar o token (só o resumo dele vai para o banco):
     update dyno_servidor set token_hash = '$(printf %s "$TOKEN" | sha256sum | cut -d' ' -f1)' where id = 1;
4. No principal, colar o agente com SERVIDOR_TOKEN igual ao de $ENV e RESERVA_HOST=$(grep '^RESERVA_IP=' "$ENV" | cut -d= -f2)
5. Pôr a linha da chave que o agente mostra no log em /home/dyno/.ssh/authorized_keys
EOF
