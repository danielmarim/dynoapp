# Whisper no VPS da Hostinger

Transcrição de áudio local com o [Whisper da OpenAI](https://github.com/openai/whisper), servido por HTTP pelo
[whisper-asr-webservice](https://github.com/ahmetoner/whisper-asr-webservice) (imagem
`onerahmet/openai-whisper-asr-webservice`, versão fixa `v1.10.0`).

O container fica na rede `n8n_default`, sem porta pública e sem Traefik. Só o n8n (e outros containers da mesma
rede) chega nele, em `http://dyno-whisper:9000`. O firewall `dyno-vps-padrao` não precisa mudar.

Hoje o cérebro transcreve com a OpenAI (`gpt-4o-mini-transcribe`). Este serviço **não muda o cérebro sozinho**: ele
só fica disponível para o n8n chamar. Ver [Usar no n8n](#usar-no-n8n).

## Antes de instalar

- **VPS em dia:** a documentação técnica diz que o srv1825327 vencia em 09/10/2026 sem renovação automática.
  Confirme no hPanel que ele foi renovado.
- **Disco:** cerca de 3 GB (imagem de \~2,7 GB + modelo `small` de \~0,5 GB). O VPS usa \~40 GB.
- **Memória:** o limite do container é 6 GB (`mem_limit`), e o VPS usa \~6 GB de 16 GB. Cabe com folga até o modelo
  `medium`.

## Instalar

### Pelo Docker Manager da Hostinger

1. hPanel → **VPS** → **Docker Manager** → criar projeto por **Compose**.
2. Nome do projeto: `dyno-whisper`. Cole o conteúdo de [`docker-compose.yml`](docker-compose.yml).
3. Implante. Na primeira subida o container baixa a imagem e depois o modelo; leva alguns minutos até ficar
   *healthy*.

### Ou por SSH

```bash
mkdir -p /opt/dyno-whisper && cd /opt/dyno-whisper
# copie o docker-compose.yml desta pasta para cá
docker compose up -d
docker logs -f dyno-whisper    # espere aparecer "Uvicorn running on http://0.0.0.0:9000"
```

## Testar

O serviço não tem porta pública, então o teste roda num container temporário dentro da rede `n8n_default`.
Com um áudio `teste.ogg` na pasta atual do servidor:

```bash
docker run --rm --network n8n_default -v "$PWD":/a curlimages/curl:8.10.1 -s \
  -F "audio_file=@/a/teste.ogg" \
  "http://dyno-whisper:9000/asr?task=transcribe&language=pt&output=json"
```

A resposta traz o texto em `text`, além dos trechos com tempo em `segments`. A documentação interativa da API fica
em `http://dyno-whisper:9000/docs` (só de dentro da rede).

## Usar no n8n

No workflow **Dyno | WhatsApp (cérebro)**, o nó **Transcrever áudio** chama a OpenAI. Para usar o Whisper local,
um nó **HTTP Request** fica assim:

| Campo | Valor |
| --- | --- |
| Method | POST |
| URL | `http://dyno-whisper:9000/asr?task=transcribe&language=pt&output=json` |
| Authentication | None (o serviço só existe na rede interna) |
| Body Content Type | Form-Data |
| Body | `audio_file` = n8n Binary File, campo `data` (o mesmo do nó **Converter áudio em arquivo**) |
| Options → Response → Response Format | JSON (o serviço responde como `text/plain`) |
| Options → Timeout | 120000 |

O texto sai em `$json.text`, o mesmo campo que o nó **Preparar entrada** já lê da OpenAI. Como a transcrição
local não tem custo por áudio, o nó **Uso IA: áudio** pode registrar `provedor: 'whisper-local'` com uso vazio.

Sugestão: antes de trocar, rode os dois em paralelo por alguns dias (Whisper em modo sombra, como foi feito com o
Jev) e compare a qualidade nos áudios reais dos clientes.

## Escolher o modelo

Troque `ASR_MODEL` no compose e reimplante. Memória aproximada com o motor `openai_whisper`:

| Modelo | Memória | Observação |
| --- | --- | --- |
| `base` | \~1 GB | Rápido, erra bastante em português |
| `small` | \~2 GB | **Padrão.** Bom equilíbrio em CPU |
| `medium` | \~5 GB | Melhor em português, bem mais lento em CPU |
| `turbo` | \~6 GB | Qualidade perto do `large`; aumente o `mem_limit` para 8g |
| `large-v3` | \~10 GB | Lento demais para 4 vCPU divididos; não recomendado |

O VPS não tem GPU, então tudo roda em CPU. Áudio de WhatsApp costuma ser curto, mas um áudio de 1 minuto no `small`
pode levar alguns segundos a mais que a OpenAI.

**Mais velocidade:** com `ASR_ENGINE: faster_whisper` o mesmo modelo roda com int8, cerca de 4 vezes mais rápido e
com menos memória, e ganha o parâmetro `vad_filter=true` (corta silêncio). Os modelos são os mesmos do Whisper,
convertidos; a API não muda.

## Custo e privacidade

- A OpenAI cobra cerca de US$ 0,003 por minuto no `gpt-4o-mini-transcribe`. O Whisper local não tem custo por
  áudio, mas usa CPU do VPS que é dividido com Dynamo Wear e Chatwoot (por isso o limite de 3 vCPUs).
- Com o Whisper local o áudio do cliente não sai do servidor. Se a transcrição sair da OpenAI, atualize o mapa de
  dados da LGPD e a Política de Privacidade.

## Alternativa: só o Whisper, sem Docker

Para usar o Whisper pela linha de comando no servidor (por SSH):

```bash
sudo apt update && sudo apt install -y ffmpeg python3-venv
python3 -m venv /opt/whisper && . /opt/whisper/bin/activate
pip install torch --index-url https://download.pytorch.org/whl/cpu   # PyTorch só CPU (evita \~2 GB de CUDA)
pip install -U openai-whisper
whisper teste.ogg --model small --language Portuguese --output_format txt
```

Assim o n8n não consegue chamar o Whisper (ele roda num container separado), então para o Dyno o caminho é o
Docker acima.
