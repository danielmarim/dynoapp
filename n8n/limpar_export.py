"""Limpa o export dos workflows do n8n antes do commit.

Uso:
    python n8n/limpar_export.py [entrada ...]

Entrada: arquivos .json, .zip ou pastas (padrão: n8n/_download/, que fica fora do git).
Saída: n8n/workflows/<nome>__<id>.json

O que faz:
- troca o valor da constante SEGREDO (nó "Preparar" da API do site) por '__SEGREDO__';
- troca p_token fixo (enviado às RPCs do Supabase) por "__P_TOKEN__";
- remove pinData e staticData (podem trazer dados de clientes de execuções de teste);
- procura valores com cara de chave/token e telefones; mostra só onde estão, nunca o valor.
Só aceita workflows cujo nome começa com "Dyno" (inclui "Dyno Plataforma |" e "Dyno Business |"; Dynamo Wear fica de fora) (o n8n também tem os da Dynamo Wear e outros);
use --todos para gravar todos.
Sai com código 1 se achar suspeita de segredo (use --permitir para gravar mesmo assim).
"""
import json
import re
import sys
import unicodedata
import zipfile
from pathlib import Path

PASTA = Path(__file__).resolve().parent
SAIDA = PASTA / "workflows"
PADRAO_ENTRADA = PASTA / "_download"

RE_SEGREDO = re.compile(r"""(const\s+SEGREDO\s*=\s*)(['"`])(?!__SEGREDO__\2)[^'"`]*\2""")
# p_token fixo enviado às RPCs do Supabase (ex.: Asaas webhook → dyno_evento_asaas)
RE_P_TOKEN = re.compile(r"""(\bp_token\\?["']?\s*:\s*)(\\?["'])(?!__P_TOKEN__)[^"'\\]+\2""")
SUSPEITAS = {
    "chave OpenAI/Anthropic": re.compile(r"\bsk-(?:ant-|proj-)?[A-Za-z0-9_\-]{16,}"),
    "chave TypeSafe": re.compile(r"\bts_[A-Za-z0-9]{16,}"),
    "JWT (Supabase?)": re.compile(r"\beyJ[A-Za-z0-9_\-]{10,}\.eyJ[A-Za-z0-9_\-]{10,}\."),
    "chave Asaas": re.compile(r"\$aact_[A-Za-z0-9_\-$]{16,}"),
    "Bearer literal": re.compile(r"Bearer\s+[A-Za-z0-9_\-\.]{20,}"),
    "token em URL": re.compile(r"[?&](?:token|apikey|api_key|key)=[A-Za-z0-9_\-]{16,}", re.I),
    "constante com nome de segredo": re.compile(
        r"""\b(?:const|let|var)\s+\w*(?:TOKEN|SECRET|SEGREDO|APIKEY|API_KEY|SENHA)\w*\s*=\s*(['"`])(?!__)[^'"`]{12,}\1""",
        re.I,
    ),
}
RE_TELEFONE = re.compile(r"\b55\d{10,11}\b")


def ler_entradas(caminhos):
    for c in caminhos:
        c = Path(c)
        if c.is_dir():
            for f in sorted(c.iterdir()):
                if f.suffix.lower() in (".json", ".zip"):
                    yield from ler_entradas([f])
        elif c.suffix.lower() == ".zip":
            with zipfile.ZipFile(c) as z:
                for nome in sorted(z.namelist()):
                    if nome.lower().endswith(".json"):
                        yield f"{c.name}:{nome}", json.loads(z.read(nome).decode("utf-8"))
        elif c.suffix.lower() == ".json":
            yield c.name, json.loads(c.read_text(encoding="utf-8"))


def como_lista(dados):
    if isinstance(dados, list):
        return dados
    if isinstance(dados, dict) and isinstance(dados.get("workflows"), list):
        return dados["workflows"]
    return [dados]


def slug(texto):
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")[:60] or "workflow"


def varrer(valor, caminho, achados, telefones):
    if isinstance(valor, dict):
        for k, v in valor.items():
            varrer(v, f"{caminho}.{k}", achados, telefones)
    elif isinstance(valor, list):
        for i, v in enumerate(valor):
            varrer(v, f"{caminho}[{i}]", achados, telefones)
    elif isinstance(valor, str):
        for rotulo, rx in SUSPEITAS.items():
            if rx.search(valor):
                achados.append((caminho, rotulo))
        telefones.update(RE_TELEFONE.findall(valor))


def limpar(wf):
    trocas = 0
    for no in wf.get("nodes", []):
        params = no.get("parameters", {})
        for campo in ("jsCode", "functionCode", "pythonCode"):
            if isinstance(params.get(campo), str):
                novo, n = RE_SEGREDO.subn(r"\1\2__SEGREDO__\2", params[campo])
                params[campo] = novo
                trocas += n
        if isinstance(params.get("jsonBody"), str):
            novo, n = RE_P_TOKEN.subn(r"\1\2__P_TOKEN__\2", params["jsonBody"])
            params["jsonBody"] = novo
            trocas += n
    for chave in ("pinData", "staticData"):
        wf.pop(chave, None)
    return trocas


def main(argv):
    sys.stdout.reconfigure(encoding="utf-8")
    permitir = "--permitir" in argv
    todos = "--todos" in argv
    entradas = [a for a in argv if not a.startswith("--")] or [PADRAO_ENTRADA]
    SAIDA.mkdir(exist_ok=True)
    problema = False
    total = 0
    for origem, dados in ler_entradas(entradas):
        for wf in como_lista(dados):
            if not isinstance(wf, dict) or "nodes" not in wf:
                print(f"? {origem}: não parece um workflow, ignorado")
                continue
            nome = wf.get("name", "sem nome")
            if not todos and not nome.startswith("Dyno"):
                print(f"- {nome}: não é do Dyno, ignorado")
                continue
            trocas = limpar(wf)
            achados, telefones = [], set()
            for no in wf["nodes"]:
                varrer(no.get("parameters", {}), f"[{no.get('name')}]", achados, telefones)
            arq = SAIDA / f"{slug(nome)}__{wf.get('id', 'sem-id')}.json"
            linha = f"{'!' if achados else 'ok'} {nome} -> {arq.name}"
            if trocas:
                linha += f" (segredos trocados: {trocas})"
            if telefones:
                linha += f" (telefones fixos no código: {len(telefones)})"
            print(linha)
            for caminho, rotulo in achados:
                print(f"    suspeita: {rotulo} em {caminho}")
            if achados and not permitir:
                problema = True
                continue
            arq.write_text(json.dumps(wf, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            total += 1
    print(f"\n{total} workflow(s) gravados em {SAIDA}")
    if problema:
        print("Há suspeitas de segredo: os arquivos marcados com ! NÃO foram gravados. Revise e rode de novo.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
