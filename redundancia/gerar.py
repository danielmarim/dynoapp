"""Gera os compose do agente (principal) e do vigia (reserva) com os scripts de src/ embutidos.

Os arquivos gerados são colados no Docker Manager (principal) ou ficam em /opt/dyno-reserva (reserva).
Não edite os .yml gerados: mude src/ e rode `python3 redundancia/gerar.py`.
"""
from pathlib import Path

AQUI = Path(__file__).parent
SRC = AQUI / "src"
IMAGEM = "docker:27.5.1-cli@sha256:851f91d241214e7c6db86513b270d58776379aacc5eb9c4a87e5b47115e3065c"
SUPABASE_URL = "https://xvekgnbneeokihtjpbts.supabase.co"
# Chave publishable (pública por desenho): só chama as funções liberadas para anon, e as do árbitro exigem o token.
SUPABASE_ANON = "sb_publishable_vHxckkjFp6vGKoTVXDVtlQ_xDnbSwwx"

# Antes de instalar pacotes: se o reserva já é o ativo, para o n8n e a Evolution na hora.
# Importa quando o principal volta de uma queda: os containers religam sozinhos no boot e não podem atender junto.
CERCA_RAPIDA = r"""r=$(wget -q -T 10 -O - --header "apikey: $SUPABASE_ANON" --header "Content-Type: application/json" \
  --post-data "{\"p_token\":\"$SERVIDOR_TOKEN\",\"p_servidor\":\"principal\"}" \
  "$SUPABASE_URL/rest/v1/rpc/dyno_servidor_batimento" 2>/dev/null || true)
case "$r" in
  *'"ok": true'*|*'"ok":true'*)
    case "$r" in
      *'"ativo": "principal"'*|*'"ativo":"principal"'*) ;;
      *)
        echo "cerca rápida: o reserva é o ativo; parando n8n e Evolution aqui"
        mkdir -p /dados
        for c in ${CERCA:-n8n-n8n-1 dyno-evo-api}; do
          [ -f "/dados/politica_$c" ] || docker inspect -f '{{.HostConfig.RestartPolicy.Name}}' "$c" > "/dados/politica_$c" 2>/dev/null
          docker update --restart=no "$c" >/dev/null 2>&1
          docker stop -t 10 "$c" >/dev/null 2>&1
        done
        touch /dados/cercado ;;
    esac ;;
esac
"""


def bloco(texto, recuo=8):
    """Texto para dentro do bloco `command: - |` do compose: recuado e com $ escapado ($$)."""
    linhas = texto.replace("$", "$$").splitlines()
    return "\n".join((" " * recuo + l) if l.strip() else "" for l in linhas)


def entrypoint(script, comando, pacotes, cerca=False):
    partes = []
    if cerca:
        partes.append(CERCA_RAPIDA)
    partes.append(f"apk add --no-cache -q {pacotes} >/dev/null || {{ echo 'falha ao instalar pacotes'; sleep 60; exit 1; }}")
    partes.append("mkdir -p /app")
    for nome in ("comum.sh", script):
        conteudo = (SRC / nome).read_text(encoding="utf-8")
        marca = "FIM_" + nome.split(".")[0].upper()
        assert marca not in conteudo
        partes.append(f"cat > /app/{nome} <<'{marca}'\n{conteudo.rstrip()}\n{marca}")
    partes.append(f"exec bash /app/{script} {comando}")
    return bloco("\n".join(partes))


def agente():
    return f"""# GERADO por redundancia/gerar.py a partir de redundancia/src/. Não edite à mão.
#
# Agente do servidor reserva, no PRINCIPAL (Hostinger). Cole no Docker Manager como projeto "dyno-reserva-agente".
# Em "Ambiente", preencha:
#   SERVIDOR_TOKEN=<o mesmo token do .env do reserva>
#   RESERVA_HOST=<IP do servidor reserva>
# Comandos: docker exec dyno-reserva-agente bash /app/agente.sh verificar   (confere tudo)
#           docker exec dyno-reserva-agente bash /app/agente.sh copiar      (manda uma cópia agora)
name: dyno-reserva-agente

services:
  dyno-reserva-agente:
    image: {IMAGEM}
    container_name: dyno-reserva-agente
    restart: unless-stopped
    environment:
      PAPEL: principal
      SUPABASE_URL: {SUPABASE_URL}
      SUPABASE_ANON: ${{SUPABASE_ANON:-{SUPABASE_ANON}}}
      SERVIDOR_TOKEN: ${{SERVIDOR_TOKEN}}
      RESERVA_HOST: ${{RESERVA_HOST}}
      RESERVA_PORTA: ${{RESERVA_PORTA:-22}}
      INTERVALO_COPIA: ${{INTERVALO_COPIA:-300}}
      PROJETOS: ${{PROJETOS:-n8n evolution-dyno dyno-site dyno-n8n-dominio}}
      DADOS: /dados
      MONTAGEM: dyno_reserva_dados:/dados
      TZ: America/Sao_Paulo
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - dyno_reserva_dados:/dados
    entrypoint: ["/bin/sh", "-c"]
    command:
      - |
{entrypoint("agente.sh", "rodar", "bash curl jq rsync", cerca=True)}
    logging:
      driver: json-file
      options:
        max-size: 10m
        max-file: "3"

volumes:
  dyno_reserva_dados:
    name: dyno_reserva_dados
"""


def vigia():
    return f"""# GERADO por redundancia/gerar.py a partir de redundancia/src/. Não edite à mão.
#
# Vigia do servidor RESERVA. Fica em /opt/dyno-reserva/docker-compose.yml, com o .env criado por preparar-servidor.sh.
# Subir: cd /opt/dyno-reserva && docker compose up -d
# Comandos: docker exec dyno-vigia bash /app/vigia.sh verificar
#           docker exec -it dyno-vigia bash /app/vigia.sh voltar      (devolve o atendimento ao principal)
name: dyno-vigia

services:
  dyno-vigia:
    image: {IMAGEM}
    container_name: dyno-vigia
    restart: unless-stopped
    environment:
      PAPEL: reserva
      SUPABASE_URL: {SUPABASE_URL}
      SUPABASE_ANON: ${{SUPABASE_ANON:-{SUPABASE_ANON}}}
      SERVIDOR_TOKEN: ${{SERVIDOR_TOKEN}}
      PRINCIPAL_IP: ${{PRINCIPAL_IP:-77.37.41.74}}
      RESERVA_IP: ${{RESERVA_IP}}
      CF_TOKEN: ${{CF_TOKEN}}
      CF_ZONA: ${{CF_ZONA}}
      CF_NOMES: ${{CF_NOMES:-dynoapp.com.br wa.dynoapp.com.br n8n.dynoapp.com.br}}
      AUTO: ${{AUTO:-1}}
      SILENCIO_S: ${{SILENCIO_S:-180}}
      FALHAS_DIRETAS: ${{FALHAS_DIRETAS:-4}}
      PROJETOS: ${{PROJETOS:-n8n evolution-dyno dyno-site dyno-n8n-dominio}}
      DADOS: /srv/dyno-reserva
      MONTAGEM: /srv/dyno-reserva:/srv/dyno-reserva
      TZ: America/Sao_Paulo
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - /srv/dyno-reserva:/srv/dyno-reserva
    entrypoint: ["/bin/sh", "-c"]
    command:
      - |
{entrypoint("vigia.sh", "rodar", "bash curl jq")}
    logging:
      driver: json-file
      options:
        max-size: 10m
        max-file: "3"
"""


if __name__ == "__main__":
    (AQUI / "principal" / "dyno-reserva-agente.yml").write_text(agente(), encoding="utf-8")
    (AQUI / "reserva").mkdir(exist_ok=True)
    (AQUI / "reserva" / "docker-compose.yml").write_text(vigia(), encoding="utf-8")
    print("gerados: principal/dyno-reserva-agente.yml e reserva/docker-compose.yml")
