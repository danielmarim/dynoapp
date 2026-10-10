#!/usr/bin/env python3
"""Gera os 7 frames da vinheta do Dyno (sub-composições HyperFrames 1080x1920)."""
import os

OUT = os.path.join(os.path.dirname(__file__), "compositions", "frames")
os.makedirs(OUT, exist_ok=True)

MASCOT = """<svg class="{cls}" viewBox="0 0 200 200" aria-hidden="true">
  <g class="{p}-antL"><line x1="76" y1="40" x2="66" y2="16" stroke="#1E1E1E" stroke-width="5" stroke-linecap="round"/><circle cx="64" cy="12" r="8" fill="#FF8A3D" stroke="#1E1E1E" stroke-width="4"/></g>
  <g class="{p}-antR"><line x1="124" y1="40" x2="134" y2="16" stroke="#1E1E1E" stroke-width="5" stroke-linecap="round"/><circle cx="136" cy="12" r="8" fill="#FF8A3D" stroke="#1E1E1E" stroke-width="4"/></g>
  <path d="M40 44 h120 a26 26 0 0 1 26 26 v62 a26 26 0 0 1 -26 26 h-74 l-30 24 v-24 h-16 a26 26 0 0 1 -26 -26 v-62 a26 26 0 0 1 26 -26z" fill="#0F9468" stroke="#1E1E1E" stroke-width="5"/>
  <text x="100" y="128" text-anchor="middle" font-family="Bodoni Moda" font-weight="700" font-size="74" fill="#FFF6EA">D</text>
</svg>"""


def base_css(p):
    return f"""
@font-face {{ font-family: "Bodoni Moda"; src: url("assets/fonts/bodoni-moda-latin-700-normal.woff2") format("woff2"); font-weight: 700; }}
@font-face {{ font-family: "Bodoni Moda"; src: url("assets/fonts/bodoni-moda-latin-400-normal.woff2") format("woff2"); font-weight: 400; }}
@font-face {{ font-family: "Space Grotesk"; src: url("assets/fonts/space-grotesk-latin-400-normal.woff2") format("woff2"); font-weight: 400; }}
@font-face {{ font-family: "Space Grotesk"; src: url("assets/fonts/space-grotesk-latin-700-normal.woff2") format("woff2"); font-weight: 700; }}
#root {{ position: absolute; inset: 0; width: 1080px; height: 1920px; overflow: hidden; font-family: "Space Grotesk", sans-serif; color: #1B1F3B; }}
.{p}-bg {{ position: absolute; inset: 0; background: #FFF6EA; }}
.{p}-dots {{ position: absolute; inset: 0; opacity: .5; background-image: radial-gradient(rgba(27,31,59,.10) 2px, transparent 2.5px); background-size: 54px 54px; }}
.{p}-h {{ font-family: "Bodoni Moda", serif; font-weight: 700; line-height: 1.0; letter-spacing: -0.02em; color: #1B1F3B; }}
.{p}-kicker {{ position: absolute; left: 86px; top: 120px; font-size: 38px; line-height: 1; font-weight: 700; letter-spacing: .16em; text-transform: uppercase; color: #0E8A60; }}
.{p}-title {{ position: absolute; left: 86px; right: 86px; top: 196px; font-size: 118px; line-height: 1.0; }}
.{p}-pill {{ position: absolute; border: 5px solid #1E1E1E; border-radius: 999px; background: #fff; font-size: 44px; font-weight: 700; padding: 24px 46px; white-space: nowrap; box-shadow: 12px 12px 0 rgba(26,26,26,.10); }}
.{p}-bub {{ position: absolute; border: 5px solid #1E1E1E; border-radius: 54px; font-size: 48px; line-height: 1.28; padding: 32px 46px; max-width: 900px; box-shadow: 12px 12px 0 rgba(26,26,26,.10); }}
.{p}-me {{ right: 76px; background: #fff; border-bottom-right-radius: 12px; }}
.{p}-dy {{ left: 76px; background: #9AF4D5; border-bottom-left-radius: 12px; }}
.{p}-who {{ display: block; font-size: 32px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; opacity: .6; margin-bottom: 10px; }}
"""


def frame(fid, dur, css, body, js, extra_note=""):
    p = fid.split("-")[0]
    p = "f" + p  # prefixo curto e único por frame
    css_all = base_css(p) + css.replace("{p}", p)
    body = body.replace("{p}", p)
    import re as _re
    # crossfades entre cenas sobrepõem texto de propósito por ~0,5 s
    body = _re.sub(r'<(div|span|b|small) class="', r'<\1 data-layout-allow-overlap class="', body)
    body = body.replace('<svg class="', '<svg data-layout-allow-overlap class="')
    js = js.replace("{p}", p)
    html = f"""<template>
<script src="assets/js/gsap.min.js"></script>
<style>{css_all}</style>
<div id="root" data-composition-id="{fid}" data-width="1080" data-height="1920" data-duration="{dur}">
  <div id="{p}-bg" class="clip {p}-bg" data-start="0" data-duration="{dur}" data-track-index="0"><div class="{p}-dots"></div></div>
{body}
</div>
<script>
(function () {{
  window.__timelines = window.__timelines || {{}};
  const tl = gsap.timeline({{ paused: true }});
  const q = (s) => document.querySelectorAll('[data-composition-id="{fid}"] ' + s);
  const one = (s) => document.querySelector('[data-composition-id="{fid}"] ' + s);
{js}
  tl.to({{}}, {{ duration: {dur} }}, 0);
  window.__timelines["{fid}"] = tl;
}})();
</script>
</template>
"""
    with open(os.path.join(OUT, fid + ".html"), "w", encoding="utf-8") as f:
        f.write(html)


# ---------- 01 Gancho (3s) ----------
pills = [
    ("💸 Conta de luz vence…", 70, 150, -6, "#fff"),
    ("🍞 Comprar pão", 560, 330, 5, "#FFB98B"),
    ("🚗 Troca de óleo?", 110, 520, 3, "#9AF4D5"),
    ("🧾 Gastei quanto?", 470, 1180, -4, "#fff"),
    ("📺 Netflix renova…", 60, 1360, 6, "#FFB98B"),
    ("⏰ Reunião 9h", 600, 1520, -3, "#fff"),
]
b1 = "\n".join(
    f'  <div class="{{p}}-pill {{p}}-n" style="left:{x}px;top:{y}px;background:{bg}" data-rot="{r}">{t}</div>'
    for (t, x, y, r, bg) in pills
)
b1 += '\n  <div class="{p}-h {p}-q">Muita coisa<br>pra lembrar?</div>'
css1 = ".{p}-q { position:absolute; left:60px; right:60px; top:760px; font-size:150px; text-align:center; }"
js1 = """
  q('.{p}-n').forEach((el, i) => {
    const r = parseFloat(el.dataset.rot);
    tl.fromTo(el, { y: -260, rotation: r * 3, opacity: 0, scale: 0.8 },
      { y: 0, rotation: r, opacity: 1, scale: 1, duration: 0.45, ease: 'back.out(1.7)' }, 0.05 + i * 0.28);
    tl.to(el, { y: 26 + i * 4, rotation: r - 2, duration: 1.6, ease: 'sine.inOut' }, 0.55 + i * 0.28);
  });
  tl.fromTo(one('.{p}-q'), { scale: 0.86, opacity: 0, y: 30 }, { scale: 1, opacity: 1, y: 0, duration: 0.5, ease: 'power3.out' }, 0.25);
  tl.to(one('.{p}-q'), { scale: 1.05, duration: 2.2, ease: 'none' }, 0.75);
"""
frame("01-gancho", 3, css1, b1, js1)

# ---------- 02 Apresentação (4s) ----------
b2 = """  <div class="{p}-glow"></div>
  """ + MASCOT.format(cls="{p}-mascot", p="{p}") + """
  <div class="{p}-h {p}-ola">Olá, sou o Dyno</div>
  <div class="{p}-sub">seu assessor pessoal</div>
  <div class="{p}-pill {p}-grp" style="background:#9AF4D5">💬 no grupo da família</div>"""
css2 = """
.{p}-glow { position:absolute; width:1300px; height:1300px; left:-110px; top:220px; border-radius:50%; background: radial-gradient(circle, rgba(20,179,125,.28), transparent 60%); }
.{p}-mascot { position:absolute; left:270px; top:380px; width:540px; height:540px; overflow:visible; }
.{p}-ola { position:absolute; left:40px; right:40px; top:1010px; font-size:124px; text-align:center; }
.{p}-sub { position:absolute; left:40px; right:40px; top:1170px; font-size:56px; text-align:center; }
.{p}-grp { left:265px; top:1300px; }
"""
js2 = """
  tl.fromTo(one('.{p}-glow'), { scale: 0, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.9, ease: 'power2.out' }, 0);
  tl.fromTo(one('.{p}-mascot'), { scale: 0, rotation: -12, transformOrigin: '50% 60%' }, { scale: 1, rotation: 0, duration: 0.9, ease: 'elastic.out(1, 0.55)' }, 0.15);
  [['.{p}-antL', -18], ['.{p}-antR', 18]].forEach(([s, a]) => {
    const el = one(s);
    tl.fromTo(el, { rotation: 0, svgOrigin: s.includes('antL') ? '76 40' : '124 40' }, { rotation: a, duration: 0.25, ease: 'sine.inOut' }, 1.0);
    tl.to(el, { rotation: -a * 0.6, duration: 0.3, ease: 'sine.inOut' }, 1.25);
    tl.to(el, { rotation: 0, duration: 0.35, ease: 'sine.out' }, 1.55);
  });
  tl.fromTo(one('.{p}-ola'), { y: 70, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: 'power3.out' }, 0.9);
  tl.fromTo(one('.{p}-sub'), { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: 'power3.out' }, 1.35);
  tl.fromTo(one('.{p}-grp'), { scale: 0.5, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.55, ease: 'back.out(2)' }, 1.9);
  tl.to(one('.{p}-mascot'), { scale: 1.05, y: -14, duration: 2.6, ease: 'sine.inOut' }, 1.1);
"""
frame("02-apresentacao", 4, css2, b2, js2)

# ---------- 03 Finanças (5s) ----------
b3 = """  <div class="{p}-kicker">finanças</div>
  <div class="{p}-h {p}-title">Seu dinheiro<br>no controle</div>
  <div class="{p}-bub {p}-me {p}-b1" style="top:640px"><span class="{p}-who">Daniel</span>gastei 42 no mercado</div>
  <div class="{p}-bub {p}-dy {p}-typing" style="top:900px"><span class="{p}-dot"></span><span class="{p}-dot"></span><span class="{p}-dot"></span></div>
  <div class="{p}-bub {p}-dy {p}-b2" style="top:900px"><span class="{p}-who">Dyno</span>Fechou! R$ 42,00 anotado 🛒</div>
  <div class="{p}-lbl">Orçamento mercado · <b class="{p}-pct">0</b>%</div>
  <div class="{p}-bar"><i class="{p}-fill"></i></div>
  <div class="{p}-foot">📷 comprovante por foto · relatório do mês só seu</div>"""
css3 = """
.{p}-typing { display:flex; gap:16px; padding:40px 50px; }
.{p}-dot { width:22px; height:22px; border-radius:50%; background:#1B1F3B; opacity:.5; display:block; }
.{p}-lbl { position:absolute; left:86px; top:1250px; font-size:42px; font-weight:700; letter-spacing:.08em; text-transform:uppercase; }
.{p}-bar { position:absolute; left:86px; right:86px; top:1330px; height:76px; border:5px solid #1E1E1E; border-radius:999px; background:#fff; overflow:hidden; }
.{p}-fill { display:block; height:100%; width:80%; background:#FF8A3D; transform-origin:0 50%; }
.{p}-foot { position:absolute; left:86px; right:86px; top:1470px; font-size:36px; font-weight:700; letter-spacing:.06em; text-transform:uppercase; opacity:.62; }
"""
js3 = """
  tl.fromTo(one('.{p}-kicker'), { x: -40, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: 'power2.out' }, 0.05);
  tl.fromTo(one('.{p}-title'), { y: 50, opacity: 0 }, { y: 0, opacity: 1, duration: 0.55, ease: 'power3.out' }, 0.12);
  tl.fromTo(one('.{p}-b1'), { x: 260, opacity: 0 }, { x: 0, opacity: 1, duration: 0.5, ease: 'back.out(1.4)' }, 0.65);
  tl.fromTo(one('.{p}-typing'), { scale: 0.6, opacity: 0, transformOrigin: '0% 100%' }, { scale: 1, opacity: 1, duration: 0.3, ease: 'back.out(2)' }, 1.15);
  q('.{p}-dot').forEach((d, i) => {
    tl.fromTo(d, { y: 0 }, { y: -14, duration: 0.18, ease: 'sine.out' }, 1.3 + i * 0.12);
    tl.to(d, { y: 0, duration: 0.18, ease: 'sine.in' }, 1.48 + i * 0.12);
  });
  tl.to(one('.{p}-typing'), { opacity: 0, duration: 0.12 }, 1.85);
  tl.fromTo(one('.{p}-b2'), { scale: 0.7, opacity: 0, transformOrigin: '0% 100%' }, { scale: 1, opacity: 1, duration: 0.45, ease: 'back.out(1.8)' }, 1.9);
  tl.fromTo(one('.{p}-lbl'), { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: 'power2.out' }, 2.7);
  tl.fromTo(one('.{p}-bar'), { scaleX: 0.6, opacity: 0, transformOrigin: '0% 50%' }, { scaleX: 1, opacity: 1, duration: 0.35, ease: 'power2.out' }, 2.8);
  tl.fromTo(one('.{p}-fill'), { scaleX: 0 }, { scaleX: 1, duration: 1.1, ease: 'power2.inOut' }, 3.05);
  const c = { v: 0 };
  tl.fromTo(c, { v: 0 }, { v: 80, duration: 1.1, ease: 'power2.inOut', onUpdate: () => { one('.{p}-pct').textContent = Math.round(c.v); } }, 3.05);
  tl.fromTo(one('.{p}-foot'), { y: 20, opacity: 0 }, { y: 0, opacity: 0.62, duration: 0.4, ease: 'power2.out' }, 4.0);
"""
frame("03-financas", 5, css3, b3, js3)

# ---------- 04 Lembretes (5s) ----------
b4 = """  <div class="{p}-kicker">lembretes e contas</div>
  <div class="{p}-h {p}-title">Lembra até você<br>dizer ok</div>
  <div class="{p}-bub {p}-dy {p}-r1" style="top:640px"><span class="{p}-who">Dyno · 09:00</span><span class="{p}-bell">⏰</span> Conta de luz vence hoje</div>
  <div class="{p}-bub {p}-dy {p}-r2" style="top:900px;background:#FFB98B"><span class="{p}-who">Dyno · 09:10</span><span class="{p}-bell2">🔔</span> E aí, já pagou?</div>
  <div class="{p}-bub {p}-me {p}-ok" style="top:1160px"><span class="{p}-who">Quézia</span>paguei <span class="{p}-chk">✅</span></div>
  <div class="{p}-pill {p}-nf" style="left:86px;top:1440px">📺 Netflix renova sexta</div>"""
css4 = ".{p}-bell,.{p}-bell2,.{p}-chk { display:inline-block; }"
js4 = """
  tl.fromTo(one('.{p}-kicker'), { x: -40, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: 'power2.out' }, 0.05);
  tl.fromTo(one('.{p}-title'), { y: 50, opacity: 0 }, { y: 0, opacity: 1, duration: 0.55, ease: 'power3.out' }, 0.12);
  tl.fromTo(one('.{p}-r1'), { x: -240, opacity: 0 }, { x: 0, opacity: 1, duration: 0.5, ease: 'back.out(1.4)' }, 0.6);
  [0, 1, 2, 3].forEach((k) => tl.to(one('.{p}-bell'), { rotation: k % 2 ? -18 : 18, duration: 0.09, ease: 'sine.inOut' }, 1.05 + k * 0.09));
  tl.to(one('.{p}-bell'), { rotation: 0, duration: 0.12 }, 1.41);
  tl.fromTo(one('.{p}-r2'), { scale: 0.6, opacity: 0, transformOrigin: '0% 100%' }, { scale: 1, opacity: 1, duration: 0.45, ease: 'back.out(2)' }, 1.75);
  tl.to(one('.{p}-r2'), { scale: 1.06, duration: 0.15, ease: 'power2.out' }, 2.25);
  tl.to(one('.{p}-r2'), { scale: 1, duration: 0.2, ease: 'power2.in' }, 2.4);
  [0, 1, 2, 3].forEach((k) => tl.to(one('.{p}-bell2'), { rotation: k % 2 ? -20 : 20, duration: 0.08, ease: 'sine.inOut' }, 2.2 + k * 0.08));
  tl.to(one('.{p}-bell2'), { rotation: 0, duration: 0.1 }, 2.52);
  tl.fromTo(one('.{p}-ok'), { x: 240, opacity: 0 }, { x: 0, opacity: 1, duration: 0.45, ease: 'back.out(1.5)' }, 2.85);
  tl.fromTo(one('.{p}-chk'), { scale: 0 }, { scale: 1.35, duration: 0.25, ease: 'back.out(3)' }, 3.2);
  tl.to(one('.{p}-chk'), { scale: 1, duration: 0.2 }, 3.45);
  tl.fromTo(one('.{p}-nf'), { y: 60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: 'back.out(1.6)' }, 3.8);
"""
frame("04-lembretes", 5, css4, b4, js4)

# ---------- 05 Casa e carro (4s) ----------
cards = [("🚗", "#9AF4D5", "Troca de óleo", "aos 50.500 km", 640),
         ("📄", "#FFB98B", "IPVA", "vence em janeiro", 900),
         ("🏠", "#fff", "Filtro de água", "a cada 6 meses", 1160)]
b5 = """  <div class="{p}-kicker">casa e carro</div>
  <div class="{p}-h {p}-title">Casa e carro<br>em dia</div>
""" + "\n".join(
    f'  <div class="{{p}}-card" style="top:{y}px"><span class="{{p}}-ic" style="background:{bg}">{ic}</span><span>{t}<small>{s}</small></span></div>'
    for (ic, bg, t, s, y) in cards
) + """
  <div class="{p}-km">🚦 km do carro: <b class="{p}-kmv">49.000</b></div>"""
css5 = """
.{p}-card { position:absolute; left:86px; right:86px; border:5px solid #1E1E1E; border-radius:64px; background:#fff; padding:36px 50px; display:flex; align-items:center; gap:40px; font-size:56px; font-weight:700; box-shadow:12px 12px 0 rgba(26,26,26,.10); }
.{p}-card small { display:block; font-size:38px; opacity:.65; font-weight:400; margin-top:6px; }
.{p}-ic { width:140px; height:140px; border-radius:50%; border:5px solid #1E1E1E; display:grid; place-items:center; font-size:70px; flex:none; }
.{p}-km { position:absolute; left:86px; top:1460px; font-size:42px; font-weight:700; letter-spacing:.06em; text-transform:uppercase; }
"""
js5 = """
  tl.fromTo(one('.{p}-kicker'), { x: -40, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: 'power2.out' }, 0.05);
  tl.fromTo(one('.{p}-title'), { y: 50, opacity: 0 }, { y: 0, opacity: 1, duration: 0.55, ease: 'power3.out' }, 0.12);
  q('.{p}-card').forEach((el, i) => {
    tl.fromTo(el, { y: 160, opacity: 0, rotation: i % 2 ? 3 : -3 }, { y: 0, opacity: 1, rotation: 0, duration: 0.55, ease: 'back.out(1.5)' }, 0.55 + i * 0.45);
    tl.fromTo(el.querySelector('.{p}-ic'), { scale: 0 }, { scale: 1, duration: 0.4, ease: 'back.out(2.4)' }, 0.75 + i * 0.45);
  });
  tl.fromTo(one('.{p}-km'), { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: 'power2.out' }, 2.1);
  const k = { v: 49000 };
  tl.fromTo(k, { v: 49000 }, { v: 49820, duration: 1.4, ease: 'power2.out', onUpdate: () => { one('.{p}-kmv').textContent = Math.round(k.v).toLocaleString('pt-BR'); } }, 2.2);
"""
frame("05-casa-carro", 4, css5, b5, js5)

# ---------- 06 Dia a dia (5s) ----------
b6 = """  <div class="{p}-sun"></div>
  <div class="{p}-kicker">todo dia</div>
  <div class="{p}-h {p}-title" style="font-size:100px">Bom dia, lugares<br>e resumos</div>
  <div class="{p}-bub {p}-dy {p}-m1" style="top:620px"><span class="{p}-who">Dyno · 06:00</span>☀️ Bom dia, família!<br>📖 Devocional do dia</div>
  <div class="{p}-bub {p}-dy {p}-m2" style="top:1000px;background:#fff"><span class="{p}-who">Dyno</span>🔎 Padaria aberta a 300 m</div>
  <div class="{p}-bub {p}-dy {p}-m3" style="top:1270px;background:#FFB98B"><span class="{p}-who">Dyno · domingo 20h</span>📊 Seu resumo da semana</div>"""
css6 = ".{p}-sun { position:absolute; width:520px; height:520px; right:-120px; top:60px; border-radius:50%; background: radial-gradient(circle, #FFD08A 0%, #FF8A3D 55%, rgba(255,138,61,0) 72%); opacity:.55; }"
js6 = """
  tl.fromTo(one('.{p}-sun'), { y: 260, scale: 0.7, opacity: 0 }, { y: 0, scale: 1, opacity: 0.55, duration: 1.4, ease: 'power2.out' }, 0);
  tl.fromTo(one('.{p}-kicker'), { x: -40, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: 'power2.out' }, 0.05);
  tl.fromTo(one('.{p}-title'), { y: 50, opacity: 0 }, { y: 0, opacity: 1, duration: 0.55, ease: 'power3.out' }, 0.12);
  tl.fromTo(one('.{p}-m1'), { scale: 0.6, opacity: 0, transformOrigin: '0% 100%' }, { scale: 1, opacity: 1, duration: 0.5, ease: 'back.out(1.8)' }, 0.75);
  tl.fromTo(one('.{p}-m2'), { scale: 0.6, opacity: 0, transformOrigin: '0% 100%' }, { scale: 1, opacity: 1, duration: 0.5, ease: 'back.out(1.8)' }, 1.95);
  tl.fromTo(one('.{p}-m3'), { scale: 0.6, opacity: 0, transformOrigin: '0% 100%' }, { scale: 1, opacity: 1, duration: 0.5, ease: 'back.out(1.8)' }, 3.15);
  tl.to(one('.{p}-sun'), { rotation: 20, scale: 1.08, duration: 3.6, ease: 'none' }, 1.4);
"""
frame("06-dia-a-dia", 5, css6, b6, js6)

# ---------- 07 É só chamar (6s, final) ----------
b7 = """  <div class="{p}-glow"></div>
  """ + MASCOT.format(cls="{p}-mascot", p="{p}") + """
  <div class="{p}-h {p}-name">""" + "".join(f'<span class="{{p}}-l">{c}</span>' for c in "Dyno") + """</div>
  <div class="{p}-sub">seu assessor pessoal</div>
  <div class="{p}-pill {p}-cta" style="background:#FF8A3D">É só chamar no grupo 💬</div>
  <div class="{p}-foot">DM Assessor Pessoal</div>"""
css7 = """
.{p}-glow { position:absolute; width:1300px; height:1300px; left:-110px; top:120px; border-radius:50%; background: radial-gradient(circle, rgba(20,179,125,.28), transparent 60%); }
.{p}-mascot { position:absolute; left:330px; top:300px; width:420px; height:420px; overflow:visible; }
.{p}-name { position:absolute; left:0; right:0; top:790px; font-size:280px; text-align:center; }
.{p}-l { display:inline-block; }
.{p}-sub { position:absolute; left:0; right:0; top:1110px; font-size:58px; font-weight:700; letter-spacing:.14em; text-transform:uppercase; text-align:center; }
.{p}-cta { left:170px; top:1260px; font-size:54px; }
.{p}-foot { position:absolute; left:0; right:0; top:1480px; font-size:38px; font-weight:700; letter-spacing:.12em; text-transform:uppercase; text-align:center; opacity:.6; }
"""
js7 = """
  tl.fromTo(one('.{p}-glow'), { scale: 0, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.9, ease: 'power2.out' }, 0);
  tl.fromTo(one('.{p}-mascot'), { scale: 0, rotation: 12, transformOrigin: '50% 60%' }, { scale: 1, rotation: 0, duration: 0.85, ease: 'elastic.out(1, 0.55)' }, 0.1);
  q('.{p}-l').forEach((el, i) => tl.fromTo(el, { y: 120, opacity: 0, rotation: i % 2 ? 8 : -8 }, { y: 0, opacity: 1, rotation: 0, duration: 0.55, ease: 'back.out(1.8)' }, 0.75 + i * 0.12));
  tl.fromTo(one('.{p}-sub'), { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: 'power3.out' }, 1.55);
  tl.fromTo(one('.{p}-cta'), { scale: 0.4, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.6, ease: 'back.out(2.2)' }, 2.1);
  tl.fromTo(one('.{p}-foot'), { y: 20, opacity: 0 }, { y: 0, opacity: 0.6, duration: 0.4, ease: 'power2.out' }, 2.6);
  [['.{p}-antL', -16, '76 40'], ['.{p}-antR', 16, '124 40']].forEach(([s, a, o]) => {
    const el = one(s);
    tl.fromTo(el, { rotation: 0, svgOrigin: o }, { rotation: a, duration: 0.25, ease: 'sine.inOut' }, 2.9);
    tl.to(el, { rotation: 0, duration: 0.4, ease: 'sine.out' }, 3.15);
  });
  tl.to(one('.{p}-mascot'), { y: -12, scale: 1.03, duration: 2.8, ease: 'sine.inOut' }, 1.0);
"""
frame("07-so-chamar", 6, css7, b7, js7)
print("ok")
