"""Árbitro (RPCs do Supabase) e API de DNS da Cloudflare falsos, para testar a virada sem tocar em produção.

Mesmas regras de public.dyno_servidor_batimento / dyno_servidor_mudar, com o silêncio mínimo configurável
(MIN_SILENCIO, padrão 120 s como no banco; no teste, poucos segundos).
Uso: python3 falsos.py PORTA TOKEN [MIN_SILENCIO]
Extras para o teste: GET /_estado (estado + DNS), POST /_reset.
"""
import json
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

PORTA, TOKEN = int(sys.argv[1]), sys.argv[2]
MIN_SILENCIO = int(sys.argv[3]) if len(sys.argv) > 3 else 120


def novo_estado():
    return {"ativo": "principal", "mudou_em": time.time(), "motivo": None,
            "principal_visto_em": None, "reserva_visto_em": None, "principal_info": {}, "reserva_info": {},
            "eventos": []}


E = novo_estado()
DNS = {"dynoapp.com.br": "1.1.1.1", "wa.dynoapp.com.br": "1.1.1.1", "n8n.dynoapp.com.br": "1.1.1.1"}
IDS = {f"id-{i}": n for i, n in enumerate(DNS)}


def silencio(campo):
    v = E[campo]
    return None if v is None else int(time.time() - v)


def resposta_estado():
    return {"ok": True, "ativo": E["ativo"], "mudou_em": E["mudou_em"], "motivo": E["motivo"],
            "principal_silencio_s": silencio("principal_visto_em"), "reserva_silencio_s": silencio("reserva_visto_em"),
            "principal_info": E["principal_info"], "reserva_info": E["reserva_info"]}


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def enviar(self, obj, codigo=200):
        corpo = json.dumps(obj).encode()
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def corpo(self):
        n = int(self.headers.get("Content-Length") or 0)
        return json.loads(self.rfile.read(n) or b"{}")

    def do_GET(self):
        u = urlparse(self.path)
        if u.path == "/_estado":
            return self.enviar({"estado": resposta_estado(), "eventos": E["eventos"], "dns": DNS})
        if u.path.endswith("/user/tokens/verify"):
            return self.enviar({"success": True, "result": {"status": "active"}})
        if u.path.endswith("/dns_records"):
            nome = parse_qs(u.query).get("name", [""])[0]
            res = [{"id": i, "name": n, "content": DNS[n], "proxied": True} for i, n in IDS.items() if n == nome]
            return self.enviar({"success": True, "result": res})
        self.enviar({"erro": "rota"}, 404)

    def do_PATCH(self):
        u = urlparse(self.path)
        rid = u.path.rsplit("/", 1)[-1]
        if rid in IDS:
            DNS[IDS[rid]] = self.corpo()["content"]
            return self.enviar({"success": True})
        self.enviar({"success": False}, 404)

    def do_POST(self):
        global E
        u = urlparse(self.path)
        if u.path == "/_reset":
            E = novo_estado()
            return self.enviar({"ok": True})
        p = self.corpo()
        if p.get("p_token") != TOKEN:
            return self.enviar({"ok": False, "erro": "token"})
        if u.path.endswith("/dyno_servidor_batimento"):
            s = p.get("p_servidor")
            if s not in ("principal", "reserva"):
                return self.enviar({"ok": False, "erro": "servidor"})
            E[f"{s}_visto_em"] = time.time()
            E[f"{s}_info"].update(p.get("p_info") or {})
            return self.enviar(resposta_estado())
        if u.path.endswith("/dyno_servidor_mudar"):
            de, para = p["p_de"], p["p_para"]
            if (de, para) not in {("principal", "reserva"), ("reserva", "devolvendo"),
                                  ("devolvendo", "principal"), ("devolvendo", "reserva")}:
                return self.enviar({"ok": False, "erro": "transicao"})
            sil = silencio("principal_visto_em")
            limite = max(p.get("p_silencio_s") or 180, MIN_SILENCIO)
            if E["ativo"] != de or (de == "principal" and (sil is None or sil < limite)):
                return self.enviar({"ok": False, "erro": "recusado", "ativo": E["ativo"], "principal_silencio_s": sil})
            E.update(ativo=para, mudou_em=time.time(), motivo=p.get("p_motivo"))
            if para == "principal":
                E["principal_visto_em"] = time.time()
            E["eventos"].append([de, para, p.get("p_motivo")])
            return self.enviar({"ok": True, "ativo": para, "mudou_em": E["mudou_em"]})
        self.enviar({"erro": "rota"}, 404)


ThreadingHTTPServer(("127.0.0.1", PORTA), H).serve_forever()
