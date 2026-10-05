#!/usr/bin/env python3
"""Gera 4 projetos HyperFrames (stories 1080x1920) para os destaques do Instagram do Dyno."""
import os, re, shutil, json

ROOT = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = "/home/claude/videos/dyno-beta-promo"
NAVY, CREAM = "#1B1F3B", "#FFF6EA"

ICONS = {
    "chat": '<path d="M20 22h60a8 8 0 0 1 8 8v34a8 8 0 0 1-8 8H44l-16 14V72h-8a8 8 0 0 1-8-8V30a8 8 0 0 1 8-8z"/><path d="M34 47h.1M50 47h.1M66 47h.1" stroke-width="12"/>',
    "money": '<circle cx="50" cy="50" r="34"/><path d="M58 38c-2-4-6-6-10-6-6 0-10 3-10 8s4 7 10 8 12 3 12 9-5 9-11 9c-5 0-9-2-11-6M50 26v6M50 68v6"/>',
    "bell": '<path d="M28 70V46a22 22 0 0 1 44 0v24l6 6H22z"/><path d="M42 82a8 8 0 0 0 16 0M50 18v6"/>',
    "help": '<circle cx="50" cy="50" r="36"/><path d="M38 40a12 12 0 1 1 18 10c-4 2-6 5-6 9"/><path d="M50 72h.1" stroke-width="12"/>',
}


def css_base(p, navy):
    bg = NAVY if navy else CREAM
    dot = "rgba(255,246,234,.06)" if navy else "rgba(27,31,59,.10)"
    return f"""
@font-face {{ font-family: "Bodoni Moda"; src: url("assets/fonts/bodoni-moda-latin-700-normal.woff2") format("woff2"); font-weight: 700; }}
@font-face {{ font-family: "Space Grotesk"; src: url("assets/fonts/space-grotesk-latin-400-normal.woff2") format("woff2"); font-weight: 400; }}
@font-face {{ font-family: "Space Grotesk"; src: url("assets/fonts/space-grotesk-latin-700-normal.woff2") format("woff2"); font-weight: 700; }}
#root {{ position:absolute; inset:0; width:1080px; height:1920px; overflow:hidden; font-family:"Space Grotesk",sans-serif; color:{NAVY}; }}
.{p}-bg {{ position:absolute; inset:0; background:{bg}; }}
.{p}-dots {{ position:absolute; inset:0; opacity:.5; background-image:radial-gradient({dot} 2px, transparent 2.5px); background-size:54px 54px; }}
.{p}-h {{ font-family:"Bodoni Moda",serif; font-weight:700; line-height:1.0; letter-spacing:-.02em; }}
.{p}-kicker {{ position:absolute; left:86px; top:300px; font-size:36px; line-height:1; font-weight:700; letter-spacing:.16em; text-transform:uppercase; color:#0E8A60; }}
.{p}-title {{ position:absolute; left:86px; right:86px; top:360px; font-size:104px; color:{NAVY}; }}
.{p}-bub {{ position:absolute; border:5px solid #1E1E1E; border-radius:54px; font-size:46px; line-height:1.28; padding:28px 44px; max-width:860px; box-shadow:12px 12px 0 rgba(26,26,26,.10); }}
.{p}-me {{ right:76px; background:#fff; border-bottom-right-radius:12px; }}
.{p}-dy {{ left:76px; background:#9AF4D5; border-bottom-left-radius:12px; }}
.{p}-who {{ display:block; font-size:28px; font-weight:700; letter-spacing:.08em; text-transform:uppercase; opacity:.6; margin-bottom:8px; }}
.{p}-card {{ position:absolute; left:76px; right:76px; border:5px solid #1E1E1E; border-radius:48px; background:#fff; padding:36px 48px; box-shadow:12px 12px 0 rgba(26,26,26,.10); }}
.{p}-pill {{ position:absolute; left:76px; right:76px; text-align:center; background:{NAVY}; color:{CREAM}; border-radius:999px; padding:34px 40px; font-size:44px; font-weight:700; }}
.{p}-glow {{ position:absolute; width:1300px; height:1300px; left:-110px; top:-40px; border-radius:50%; background:radial-gradient(circle, rgba(20,179,125,.28), rgba(20,179,125,0) 62%); }}
.{p}-ic {{ position:absolute; left:290px; top:420px; width:500px; height:500px; border-radius:50%; background:#252A4D; display:flex; align-items:center; justify-content:center; }}
.{p}-ic svg {{ width:290px; height:290px; stroke:#3EE9AF; fill:none; stroke-width:7; stroke-linecap:round; stroke-linejoin:round; }}
.{p}-big {{ position:absolute; left:40px; right:40px; top:1020px; font-size:128px; text-align:center; white-space:nowrap; color:{CREAM}; }}
.{p}-sub {{ position:absolute; left:60px; right:60px; top:1190px; font-size:48px; text-align:center; color:#A9ADC6; }}
.{p}-brand {{ position:absolute; left:0; right:0; top:1460px; display:flex; justify-content:center; align-items:center; gap:22px; font-family:"Bodoni Moda",serif; font-weight:700; font-size:54px; color:{CREAM}; }}
.{p}-mk {{ width:84px; height:84px; border-radius:50%; background:#14B37D; color:{NAVY}; display:flex; align-items:center; justify-content:center; font-size:54px; padding-top:4px; }}
"""

# Animação genérica: cada elemento com data-in (up/right/left/pop/bar/fade) entra no tempo data-t.
JS = """
  q('[data-in]').forEach((el) => {
    const t = parseFloat(el.dataset.t || '0'), k = el.dataset.in;
    if (k === 'up') tl.fromTo(el, { y: 60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: 'power3.out' }, t);
    else if (k === 'right') tl.fromTo(el, { x: 260, opacity: 0 }, { x: 0, opacity: 1, duration: 0.45, ease: 'back.out(1.4)' }, t);
    else if (k === 'left') tl.fromTo(el, { x: -260, opacity: 0 }, { x: 0, opacity: 1, duration: 0.45, ease: 'back.out(1.4)' }, t);
    else if (k === 'pop') tl.fromTo(el, { scale: 0.6, opacity: 0, transformOrigin: '0% 100%' }, { scale: 1, opacity: 1, duration: 0.45, ease: 'back.out(1.9)' }, t);
    else if (k === 'zoom') tl.fromTo(el, { scale: 0, rotation: -25 }, { scale: 1, rotation: 0, duration: 0.8, ease: 'elastic.out(1, 0.6)' }, t);
    else if (k === 'bar') tl.fromTo(el, { scaleX: 0, transformOrigin: '0% 50%' }, { scaleX: 1, duration: 0.8, ease: 'power2.out' }, t);
    else if (k === 'card') tl.fromTo(el, { y: 300, rotation: -3, opacity: 0 }, { y: 0, rotation: 0, opacity: 1, duration: 0.55, ease: 'back.out(1.4)' }, t);
    else tl.fromTo(el, { opacity: 0 }, { opacity: 1, duration: 0.6, ease: 'power2.out' }, t);
  });
  q('[data-shake]').forEach((el) => {
    const t = parseFloat(el.dataset.shake);
    [0, 1, 2, 3, 4].forEach((i) => tl.to(el, { rotation: i % 2 ? -20 : 20, duration: 0.08, ease: 'sine.inOut' }, t + i * 0.08));
    tl.to(el, { rotation: 0, duration: 0.1 }, t + 0.4);
  });
"""


def write_frame(proj, fid, dur, body, navy=False, extra_css=""):
    p = "f" + fid.split("-")[0]
    body = body.replace("{p}", p)
    body = re.sub(r'<(div|span|b|i) class="', r'<\1 data-layout-allow-overlap data-layout-allow-overflow class="', body)
    html = f"""<template>
<script src="assets/js/gsap.min.js"></script>
<style>{css_base(p, navy)}{extra_css.replace('{p}', p)}</style>
<div id="root" data-composition-id="{fid}" data-width="1080" data-height="1920" data-duration="{dur}">
  <div id="{p}-bg" class="clip {p}-bg" data-start="0" data-duration="{dur}" data-track-index="0"><div class="{p}-dots"></div></div>
{body}
</div>
<script>
(function () {{
  window.__timelines = window.__timelines || {{}};
  const tl = gsap.timeline({{ paused: true }});
  const q = (s) => document.querySelectorAll('[data-composition-id="{fid}"] ' + s);
{JS}
  tl.to({{}}, {{ duration: {dur} }}, 0);
  window.__timelines["{fid}"] = tl;
}})();
</script>
</template>
"""
    os.makedirs(os.path.join(proj, "compositions", "frames"), exist_ok=True)
    with open(os.path.join(proj, "compositions", "frames", fid + ".html"), "w", encoding="utf-8") as f:
        f.write(html)


def cover(icon, title, sub):
    return f"""  <div class="{{p}}-glow" data-in="fade" data-t="0"></div>
  <div class="{{p}}-ic" data-in="zoom" data-t="0.1"><svg viewBox="0 0 100 100">{ICONS[icon]}</svg></div>
  <div class="{{p}}-h {{p}}-big" data-in="up" data-t="0.55">{title}</div>
  <div class="{{p}}-sub" data-in="up" data-t="0.9">{sub}</div>
  <div class="{{p}}-brand" data-in="fade" data-t="1.4"><span class="{{p}}-mk">D</span>Dyno</div>"""


def head(kicker, title, t=0.05):
    return f"""  <div class="{{p}}-kicker" data-in="left" data-t="{t}">{kicker}</div>
  <div class="{{p}}-h {{p}}-title" data-in="up" data-t="{t + 0.1}">{title}</div>
"""


def me(text, top, t):
    return f'  <div class="{{p}}-bub {{p}}-me" style="top:{top}px" data-in="right" data-t="{t}">{text}</div>\n'


def dy(text, top, t, who="Dyno", bg=None, extra=""):
    st = f"top:{top}px" + (f";background:{bg}" if bg else "")
    return f'  <div class="{{p}}-bub {{p}}-dy" style="{st}" data-in="pop" data-t="{t}"><span class="{{p}}-who">{who}</span>{text}</div>\n'


STORIES = {
    "como-funciona": [
        (True, cover("chat", "Como funciona", "o Dyno em 3 passos"), ""),
        (False, head("passo a passo", "Simples assim") + "".join(
            f'  <div class="{{p}}-card {{p}}-step" style="top:{620 + i * 250}px" data-in="card" data-t="{0.6 + i * 0.45}"><b class="{{p}}-n">{i + 1}</b><span>{t}</span></div>\n'
            for i, t in enumerate(["Salve o contato do Dyno", "Mande texto, áudio ou foto", "Ele anota, organiza e te lembra"])),
         """.{p}-step { display:flex; align-items:center; gap:36px; font-size:46px; font-weight:700; }
.{p}-n { flex:none; width:110px; height:110px; border-radius:50%; background:#14B37D; display:flex; align-items:center; justify-content:center; font-family:"Bodoni Moda",serif; font-size:64px; color:#1B1F3B; }"""),
        (False, head("na prática", "Sem app novo") + me("🎤 ▶︎ ▬▬▬▬▬ 0:06", 640, 0.6)
         + dy("Anotei R$ 32 na padaria 🥐 e te lembro da reunião amanhã às 10h ✅", 820, 1.3)
         + '  <div class="{p}-pill" style="top:1340px" data-in="up" data-t="2.3">Quer testar? Me chama no direct 💬</div>\n', ""),
    ],
    "financas": [
        (True, cover("money", "Finanças", "sem planilha, sem esforço"), ""),
        (False, head("registre", "Gastou? Só avisa") + me("uber 23 pra casa 🚗", 620, 0.6)
         + dy("Anotado! R$ 23 em transporte", 790, 1.1) + me("📷 nota do mercado", 1060, 1.9)
         + dy("R$ 186,40 em mercado ✅", 1230, 2.4), ""),
        (False, head("acompanhe", "Resumo do mês") + me("quanto gastei esse mês?", 620, 0.5)
         + '  <div class="{p}-card" style="top:790px" data-in="pop" data-t="1.0"><span class="{p}-who">Dyno · outubro</span>'
         + "".join(f'<div class="{{p}}-row"><span>{c}</span><b>R$ {v}</b></div><div class="{{p}}-track"><i style="width:{w}%" data-in="bar" data-t="{1.4 + i * 0.2}"></i></div>'
                   for i, (c, v, w) in enumerate([("Mercado", "620", 100), ("Contas", "480", 77), ("Transporte", "190", 31), ("Lazer", "150", 24)]))
         + '</div>\n' + dy("⚠️ Mercado já está em 80% do limite do mês", 1400, 2.8, bg="#FFB98B"),
         """.{p}-row { display:flex; justify-content:space-between; font-size:40px; font-weight:700; margin-top:14px; }
.{p}-track { height:26px; border-radius:13px; background:#EDE6DA; margin-top:10px; overflow:hidden; }
.{p}-track i { display:block; height:100%; border-radius:13px; background:#14B37D; }"""),
    ],
    "lembretes": [
        (True, cover("bell", "Lembretes", "que insistem até você fazer"), ""),
        (False, head("peça", "É só pedir") + me("me lembra de pagar a luz dia 10 às 9h", 620, 0.6)
         + dy("Combinado! ⏰ Dia 10, às 09:00", 850, 1.2) + me("e o remédio todo dia às 8h 💊", 1080, 2.0)
         + dy("Feito ✅ Todo dia às 08:00", 1250, 2.5), ""),
        (False, head("e ele cobra", "Até você fazer")
         + '  <div class="{p}-bub {p}-dy" style="top:640px" data-in="left" data-t="0.6"><span class="{p}-who">Dyno · 09:00</span><span class="{p}-e" data-shake="1.0">⏰</span> Pagar a conta de luz</div>\n'
         + '  <div class="{p}-bub {p}-dy" style="top:900px;background:#FFB98B" data-in="pop" data-t="1.6"><span class="{p}-who">Dyno · 09:10</span><span class="{p}-e" data-shake="2.0">🔔</span> Ainda não vi seu ok…</div>\n'
         + '  <div class="{p}-bub {p}-me" style="top:1170px;font-size:64px" data-in="right" data-t="2.6">paguei ✅</div>\n'
         + '  <div class="{p}-foot" data-in="up" data-t="3.2">contas · remédios · compromissos</div>\n',
         """.{p}-e { display:inline-block; }
.{p}-foot { position:absolute; left:86px; right:86px; top:1450px; font-size:38px; font-weight:700; letter-spacing:.08em; text-transform:uppercase; opacity:.6; }"""),
    ],
    "duvidas": [
        (True, cover("help", "Dúvidas", "as perguntas mais comuns"), ""),
        (False, head("perguntas frequentes", "Respondendo") + "".join(
            f'  <div class="{{p}}-card" style="top:{y}px" data-in="card" data-t="{t}"><b class="{{p}}-qq">{qq}</b><span class="{{p}}-aa">{aa}</span></div>\n'
            for (qq, aa, y, t) in [("Preciso baixar app?", "Não. Funciona direto no seu WhatsApp.", 640, 0.6),
                                   ("Funciona em grupo?", "Sim, dá pra usar no grupo da família.", 1010, 1.4)]), ""),
        (False, head("perguntas frequentes", "E o preço?") + "".join(
            f'  <div class="{{p}}-card" style="top:{y}px" data-in="card" data-t="{t}"><b class="{{p}}-qq">{qq}</b><span class="{{p}}-aa">{aa}</span></div>\n'
            for (qq, aa, y, t) in [("Quanto custa?", "No Beta, 60 dias grátis. Depois, R$ 19,90/mês ou R$ 199,90/ano.", 640, 0.6),
                                   ("Posso cancelar?", "Quando quiser, sem custo algum.", 1060, 1.4)])
         + '  <div class="{p}-pill" style="top:1400px" data-in="up" data-t="2.3">Outra dúvida? Chama no direct 💬</div>\n', ""),
    ],
}
QA_CSS = """.{p}-qq { display:block; font-family:"Bodoni Moda",serif; font-size:62px; line-height:1.05; margin-bottom:18px; }
.{p}-aa { display:block; font-size:44px; line-height:1.35; }"""

STARTS, DURS = [0, 4, 8], [4.5, 4.5, 5]
TOTAL = 13

for name, scenes in STORIES.items():
    proj = os.path.join(ROOT, name)
    os.makedirs(proj, exist_ok=True)
    for f in ["package.json", "hyperframes.json", "meta.json", "CLAUDE.md", "AGENTS.md"]:
        src = os.path.join(TEMPLATE, f)
        if os.path.exists(src):
            shutil.copy(src, proj)
    for d in ["assets/fonts", "assets/js"]:
        shutil.copytree(os.path.join(TEMPLATE, d), os.path.join(proj, d), dirs_exist_ok=True)
    os.makedirs(os.path.join(proj, "assets", "audio"), exist_ok=True)
    music = os.path.join(proj, "assets", "audio", "bgm.wav")
    if not os.path.exists(music):
        os.system(f'ffmpeg -v error -y -i {TEMPLATE}/assets/audio/dyno-bgm.wav -t {TOTAL} -af "afade=t=in:d=0.3,afade=t=out:st={TOTAL - 1.5}:d=1.5" {music}')
    ids = []
    for i, (navy, body, css) in enumerate(scenes):
        fid = f"0{i + 1}-{name}"
        ids.append(fid)
        write_frame(proj, fid, DURS[i], body, navy, css + "\n" + (QA_CSS if name == "duvidas" else ""))
    divs = "\n".join(
        f'      <div id="el-{fid}" class="scene" data-composition-id="{fid}" data-composition-src="compositions/frames/{fid}.html" data-start="{STARTS[i]}" data-duration="{DURS[i]}" data-track-index="{i % 2}"></div>'
        for i, fid in enumerate(ids))
    tr = f"""        tl.to("#el-{ids[0]}", {{ opacity: 0, duration: 0.5, ease: "power2.inOut" }}, 4);
        tl.fromTo("#el-{ids[1]}", {{ clipPath: "inset(100% 0% 0% 0%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", duration: 0.5, ease: "power3.inOut" }}, 4);
        tl.to("#el-{ids[1]}", {{ opacity: 0, duration: 0.5, ease: "power2.inOut" }}, 8);
        tl.fromTo("#el-{ids[2]}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5, ease: "power2.inOut" }}, 8);
        tl.to({{}}, {{ duration: {TOTAL} }}, 0);"""
    html = f"""<!doctype html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/js/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #000; }}
      #root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #1B1F3B; }}
      .scene {{ position: absolute; inset: 0; width: 100%; height: 100%; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
{divs}
      <audio id="el-bgm" src="assets/audio/bgm.wav" data-start="0" data-duration="{TOTAL}" data-track-index="11" data-volume="0.8"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
      (function () {{ var tl = window.__timelines["main"];
{tr}
      }})();
    </script>
  </body>
</html>
"""
    with open(os.path.join(proj, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    json.dump({"id": "dyno-destaque-" + name, "name": "Dyno destaque " + name}, open(os.path.join(proj, "meta.json"), "w"))
print("ok")
