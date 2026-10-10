#!/usr/bin/env python3
"""Gera os 6 frames do vídeo promo do Beta do Dyno (sub-composições HyperFrames 1080x1920)."""
import os
import re

OUT = os.path.join(os.path.dirname(__file__), "compositions", "frames")
os.makedirs(OUT, exist_ok=True)

NAVY = "#1B1F3B"
CREAM = "#FFF6EA"


def base_css(p, navy):
    bg = NAVY if navy else CREAM
    dot = "rgba(255,246,234,.06)" if navy else "rgba(27,31,59,.10)"
    return f"""
@font-face {{ font-family: "Bodoni Moda"; src: url("assets/fonts/bodoni-moda-latin-700-normal.woff2") format("woff2"); font-weight: 700; }}
@font-face {{ font-family: "Space Grotesk"; src: url("assets/fonts/space-grotesk-latin-400-normal.woff2") format("woff2"); font-weight: 400; }}
@font-face {{ font-family: "Space Grotesk"; src: url("assets/fonts/space-grotesk-latin-700-normal.woff2") format("woff2"); font-weight: 700; }}
#root {{ position: absolute; inset: 0; width: 1080px; height: 1920px; overflow: hidden; font-family: "Space Grotesk", sans-serif; color: {NAVY}; }}
.{p}-bg {{ position: absolute; inset: 0; background: {bg}; }}
.{p}-dots {{ position: absolute; inset: 0; opacity: .5; background-image: radial-gradient({dot} 2px, transparent 2.5px); background-size: 54px 54px; }}
.{p}-h {{ font-family: "Bodoni Moda", serif; font-weight: 700; line-height: 1.0; letter-spacing: -0.02em; }}
.{p}-kicker {{ position: absolute; left: 86px; top: 130px; font-size: 38px; line-height: 1; font-weight: 700; letter-spacing: .16em; text-transform: uppercase; color: #0E8A60; }}
.{p}-title {{ position: absolute; left: 86px; right: 86px; top: 200px; font-size: 118px; line-height: 1.0; }}
.{p}-bub {{ position: absolute; border: 5px solid #1E1E1E; border-radius: 54px; font-size: 48px; line-height: 1.28; padding: 30px 46px; max-width: 880px; box-shadow: 12px 12px 0 rgba(26,26,26,.10); }}
.{p}-me {{ right: 76px; background: #fff; border-bottom-right-radius: 12px; }}
.{p}-dy {{ left: 76px; background: #9AF4D5; border-bottom-left-radius: 12px; }}
.{p}-who {{ display: block; font-size: 30px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; opacity: .6; margin-bottom: 8px; }}
.{p}-logo {{ position: absolute; border-radius: 50%; background: #14B37D; display: flex; align-items: center; justify-content: center; font-family: "Bodoni Moda", serif; font-weight: 700; color: {NAVY}; line-height: 1; }}
"""


def frame(fid, dur, css, body, js, navy=False):
    p = "f" + fid.split("-")[0]
    css_all = base_css(p, navy) + css.replace("{p}", p)
    body = body.replace("{p}", p)
    # crossfades entre cenas sobrepõem texto de propósito por ~0,5 s
    body = re.sub(r'<(div|span|b|small|i) class="', r'<\1 data-layout-allow-overlap data-layout-allow-overflow class="', body)
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


# ---------- 01 Gancho (3.5s, cena 0–3) ----------
b1 = """  <div class="{p}-bub {p}-dy {p}-typing" style="top:380px"><span class="{p}-dot"></span><span class="{p}-dot"></span><span class="{p}-dot"></span></div>
  <div class="{p}-h {p}-q"><span class="{p}-l">E se você</span><span class="{p}-l">tivesse um</span><span class="{p}-l">assessor</span><span class="{p}-l">pessoal…</span></div>
  <div class="{p}-h {p}-wa">no WhatsApp?</div>
  <div class="{p}-logo {p}-mk">D</div>"""
css1 = """
.{p}-typing { display:flex; gap:18px; padding:40px 54px; }
.{p}-dot { width:24px; height:24px; border-radius:50%; background:#1B1F3B; opacity:.55; display:block; }
.{p}-q { position:absolute; left:86px; right:86px; top:600px; font-size:132px; color:#1B1F3B; }
.{p}-l { display:block; }
.{p}-wa { position:absolute; left:86px; right:60px; top:1150px; font-size:132px; color:#14B37D; white-space:nowrap; }
.{p}-mk { left:455px; top:1560px; width:170px; height:170px; font-size:108px; padding-top:6px; }
"""
js1 = """
  tl.fromTo(one('.{p}-typing'), { scale: 0.5, opacity: 0, transformOrigin: '0% 100%' }, { scale: 1, opacity: 1, duration: 0.35, ease: 'back.out(2)' }, 0.0);
  q('.{p}-dot').forEach((d, i) => {
    [0, 0.5, 1.0, 1.5, 2.0].forEach((t) => {
      tl.to(d, { y: -16, opacity: 1, duration: 0.15, ease: 'sine.out' }, 0.2 + t + i * 0.1);
      tl.to(d, { y: 0, opacity: 0.55, duration: 0.15, ease: 'sine.in' }, 0.35 + t + i * 0.1);
    });
  });
  q('.{p}-l').forEach((el, i) => {
    tl.fromTo(el, { y: 60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: 'power3.out' }, 0.2 + i * 0.22);
  });
  tl.fromTo(one('.{p}-wa'), { scale: 0.6, opacity: 0, transformOrigin: '0% 50%' }, { scale: 1, opacity: 1, duration: 0.5, ease: 'back.out(2.4)' }, 1.35);
  tl.fromTo(one('.{p}-mk'), { scale: 0, rotation: -30 }, { scale: 1, rotation: 0, duration: 0.6, ease: 'back.out(2)' }, 1.85);
  tl.to(one('.{p}-q'), { y: -16, duration: 2.6, ease: 'none' }, 0.6);
"""
frame("01-gancho", 3.5, css1, b1, js1)

# ---------- 02 Anota (5.5s, cena 3–8) ----------
bars = "".join(f'<i class="{{p}}-wv" style="height:{h}px"></i>' for h in [18, 34, 26, 46, 30, 52, 22, 40, 28, 44, 20, 36, 24])
b2 = f"""  <div class="{{p}}-kicker">texto, áudio ou foto</div>
  <div class="{{p}}-h {{p}}-title">Você fala,<br>ele anota</div>
  <div class="{{p}}-bub {{p}}-me {{p}}-u" style="top:560px">gastei 45 no mercado 🛒</div>
  <div class="{{p}}-bub {{p}}-dy {{p}}-d" style="top:730px"><span class="{{p}}-who">Dyno</span>Prontinho! R$ 45 em mercado</div>
  <div class="{{p}}-bub {{p}}-me {{p}}-u {{p}}-aud" style="top:950px">🎤 <span class="{{p}}-play">▶</span><span class="{{p}}-wave">{bars}</span> 0:04</div>
  <div class="{{p}}-bub {{p}}-dy {{p}}-d" style="top:1120px"><span class="{{p}}-who">Dyno</span>R$ 120 em farmácia ✅</div>
  <div class="{{p}}-bub {{p}}-me {{p}}-u" style="top:1340px">📷 comprovante.jpg</div>
  <div class="{{p}}-bub {{p}}-dy {{p}}-d" style="top:1510px"><span class="{{p}}-who">Dyno</span>Conta de luz lançada ✅</div>"""
css2 = """
.{p}-title { color:#1B1F3B; }
.{p}-aud { display:flex; align-items:center; gap:18px; }
.{p}-play { font-size:40px; }
.{p}-wave { display:flex; align-items:center; gap:7px; height:56px; }
.{p}-wv { display:block; width:8px; border-radius:4px; background:#1B1F3B; opacity:.75; }
"""
js2 = """
  tl.fromTo(one('.{p}-kicker'), { x: -40, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: 'power2.out' }, 0.05);
  tl.fromTo(one('.{p}-title'), { y: 50, opacity: 0 }, { y: 0, opacity: 1, duration: 0.55, ease: 'power3.out' }, 0.12);
  const us = q('.{p}-u'), ds = q('.{p}-d');
  [0, 1, 2].forEach((k) => {
    const t = 0.6 + k * 1.3;
    tl.fromTo(us[k], { x: 280, opacity: 0 }, { x: 0, opacity: 1, duration: 0.45, ease: 'back.out(1.4)' }, t);
    tl.fromTo(ds[k], { scale: 0.6, opacity: 0, transformOrigin: '0% 100%' }, { scale: 1, opacity: 1, duration: 0.45, ease: 'back.out(1.9)' }, t + 0.55);
  });
  q('.{p}-wv').forEach((w, i) => {
    tl.fromTo(w, { scaleY: 0.3 }, { scaleY: 1, duration: 0.18, ease: 'sine.inOut' }, 2.0 + i * 0.04);
  });
"""
frame("02-anota", 5.5, css2, b2, js2)

# ---------- 03 Lembra (4.5s, cena 8–12) ----------
b3 = """  <div class="{p}-kicker">lembretes</div>
  <div class="{p}-h {p}-title">Lembra até<br>você fazer</div>
  <div class="{p}-bub {p}-dy {p}-r1" style="top:620px"><span class="{p}-who">Dyno · 09:00</span><span class="{p}-bell">⏰</span> Pagar a conta de luz</div>
  <div class="{p}-bub {p}-dy {p}-r2" style="top:880px;background:#FFB98B"><span class="{p}-who">Dyno · 09:10</span><span class="{p}-bell2">🔔</span> Ainda não vi seu ok…</div>
  <div class="{p}-bub {p}-me {p}-ok" style="top:1150px;font-size:66px">ok <span class="{p}-chk">✅</span></div>
  <div class="{p}-foot">contas · remédios · compromissos</div>"""
css3 = """
.{p}-title { color:#1B1F3B; }
.{p}-bell,.{p}-bell2,.{p}-chk { display:inline-block; }
.{p}-foot { position:absolute; left:86px; right:86px; top:1460px; font-size:38px; font-weight:700; letter-spacing:.08em; text-transform:uppercase; color:#1B1F3B; opacity:.6; }
"""
js3 = """
  tl.fromTo(one('.{p}-kicker'), { x: -40, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: 'power2.out' }, 0.05);
  tl.fromTo(one('.{p}-title'), { y: 50, opacity: 0 }, { y: 0, opacity: 1, duration: 0.55, ease: 'power3.out' }, 0.12);
  tl.fromTo(one('.{p}-r1'), { x: -260, opacity: 0 }, { x: 0, opacity: 1, duration: 0.5, ease: 'back.out(1.4)' }, 0.55);
  [0, 1, 2, 3].forEach((k) => tl.to(one('.{p}-bell'), { rotation: k % 2 ? -18 : 18, duration: 0.09, ease: 'sine.inOut' }, 1.0 + k * 0.09));
  tl.to(one('.{p}-bell'), { rotation: 0, duration: 0.12 }, 1.36);
  tl.fromTo(one('.{p}-r2'), { scale: 0.6, opacity: 0, transformOrigin: '0% 100%' }, { scale: 1, opacity: 1, duration: 0.45, ease: 'back.out(2)' }, 1.55);
  [0, 1, 2, 3, 4, 5].forEach((k) => tl.to(one('.{p}-bell2'), { rotation: k % 2 ? -22 : 22, duration: 0.08, ease: 'sine.inOut' }, 2.0 + k * 0.08));
  tl.to(one('.{p}-bell2'), { rotation: 0, duration: 0.1 }, 2.48);
  tl.fromTo(one('.{p}-ok'), { x: 260, opacity: 0 }, { x: 0, opacity: 1, duration: 0.45, ease: 'back.out(1.5)' }, 2.55);
  tl.fromTo(one('.{p}-chk'), { scale: 0 }, { scale: 1.45, duration: 0.25, ease: 'back.out(3)' }, 2.85);
  tl.to(one('.{p}-chk'), { scale: 1, duration: 0.2 }, 3.1);
  tl.fromTo(one('.{p}-foot'), { y: 24, opacity: 0 }, { y: 0, opacity: 0.6, duration: 0.4, ease: 'power2.out' }, 3.2);
"""
frame("03-lembra", 4.5, css3, b3, js3)

# ---------- 04 Organiza (3.5s, cena 12–15) ----------
cards = [("✅ Tarefas", "#fff", 600, -3), ("🛒 Listas de compras", "#9AF4D5", 840, 2),
         ("💸 Contas a pagar", "#FFB98B", 1080, -2), ("📊 Resumo do mês", "#fff", 1320, 3)]
b4 = """  <div class="{p}-kicker">e mais</div>
  <div class="{p}-h {p}-title">E organiza<br>o resto</div>
""" + "\n".join(
    f'  <div class="{{p}}-card" style="top:{y}px;background:{bg}" data-rot="{r}">{t}</div>' for (t, bg, y, r) in cards
)
css4 = """
.{p}-title { color:#1B1F3B; }
.{p}-card { position:absolute; left:86px; right:86px; height:180px; display:flex; align-items:center; padding:0 60px; border:5px solid #1E1E1E; border-radius:70px; font-size:60px; font-weight:700; color:#1B1F3B; box-shadow:12px 12px 0 rgba(26,26,26,.10); }
"""
js4 = """
  tl.fromTo(one('.{p}-kicker'), { x: -40, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: 'power2.out' }, 0.05);
  tl.fromTo(one('.{p}-title'), { y: 50, opacity: 0 }, { y: 0, opacity: 1, duration: 0.55, ease: 'power3.out' }, 0.12);
  q('.{p}-card').forEach((el, i) => {
    const r = parseFloat(el.dataset.rot);
    tl.fromTo(el, { y: 420, rotation: r * 4, opacity: 0 }, { y: 0, rotation: r, opacity: 1, duration: 0.55, ease: 'back.out(1.5)' }, 0.5 + i * 0.35);
    tl.to(el, { rotation: 0, duration: 0.5, ease: 'sine.out' }, 1.05 + i * 0.35);
  });
"""
frame("04-organiza", 3.5, css4, b4, js4)

# ---------- 05 Beta (4.5s, cena 15–19) — azul-marinho ----------
b5 = """  <div class="{p}-glow"></div>
  <div class="{p}-pill">BETA FECHADO</div>
  <div class="{p}-h {p}-tt">Teste o Dyno<br><span class="{p}-lime">antes de todo mundo.</span></div>
  <div class="{p}-tile" style="top:690px"><b class="{p}-n1">0</b><span>vagas no Beta</span></div>
  <div class="{p}-tile {p}-hi" style="top:990px"><b><span class="{p}-n2">0</span> dias</b><span>grátis para usar</span></div>
  <div class="{p}-tile" style="top:1290px"><b>1</b><span>pedido: seu feedback sincero</span></div>
  <div class="{p}-price">Depois do teste: R$ 19,90/mês ou R$ 199,90 no plano anual.<br>Quem não quiser, é só sair sem custo algum 😁</div>"""
css5 = """
.{p}-glow { position:absolute; width:1200px; height:1200px; right:-520px; top:-420px; border-radius:50%; background: radial-gradient(circle, rgba(20,179,125,.30), rgba(20,179,125,0) 65%); }
.{p}-pill { position:absolute; left:86px; top:140px; border:4px solid #3EE9AF; color:#3EE9AF; border-radius:999px; padding:16px 36px; font-size:36px; font-weight:700; letter-spacing:.22em; }
.{p}-tt { position:absolute; left:86px; right:60px; top:260px; font-size:112px; color:#FFF6EA; }
.{p}-lime { color:#3EE9AF; }
.{p}-tile { position:absolute; left:86px; right:86px; height:250px; border:4px solid #3A3F66; border-radius:48px; background:#252A4D; padding:34px 54px; color:#FFF6EA; }
.{p}-tile b { display:block; font-family:"Bodoni Moda", serif; font-weight:700; font-size:120px; line-height:1; }
.{p}-tile span { display:block; font-size:42px; color:#A9ADC6; margin-top:14px; }
.{p}-tile b span { display:inline; font-size:inherit; color:inherit; margin:0; }
.{p}-hi { border-color:#3EE9AF; }
.{p}-hi b { color:#3EE9AF; }
.{p}-price { position:absolute; left:86px; right:86px; top:1600px; font-size:38px; line-height:1.45; color:#C9CCE0; }
"""
js5 = """
  tl.fromTo(one('.{p}-glow'), { scale: 0.4, opacity: 0 }, { scale: 1, opacity: 1, duration: 1.2, ease: 'power2.out' }, 0);
  tl.fromTo(one('.{p}-pill'), { scale: 0.6, opacity: 0, transformOrigin: '0% 50%' }, { scale: 1, opacity: 1, duration: 0.45, ease: 'back.out(2.2)' }, 0.25);
  tl.fromTo(one('.{p}-pill'), { boxShadow: '0 0 0px rgba(62,233,175,0)' }, { boxShadow: '0 0 40px rgba(62,233,175,.55)', duration: 0.3, yoyo: true, repeat: 1 }, 0.7);
  tl.fromTo(one('.{p}-tt'), { y: 60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.55, ease: 'power3.out' }, 0.35);
  q('.{p}-tile').forEach((el, i) => {
    tl.fromTo(el, { y: 140, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: 'back.out(1.4)' }, 0.8 + i * 0.4);
  });
  const c1 = { v: 0 }, c2 = { v: 0 };
  tl.to(c1, { v: 10, duration: 0.7, ease: 'power2.out', onUpdate: () => { one('.{p}-n1').textContent = Math.round(c1.v); } }, 0.9);
  tl.to(c2, { v: 60, duration: 0.8, ease: 'power2.out', onUpdate: () => { one('.{p}-n2').textContent = Math.round(c2.v); } }, 1.3);
  tl.fromTo(one('.{p}-price'), { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: 'power2.out' }, 2.3);
"""
frame("05-beta", 4.5, css5, b5, js5, navy=True)

# ---------- 06 Chamada (3.5s, cena 19–22.5) — azul-marinho ----------
b6 = """  <div class="{p}-glow"></div>
  <div class="{p}-ring"></div>
  <div class="{p}-logo {p}-mk">D</div>
  <div class="{p}-h {p}-name"><span class="{p}-ch">D</span><span class="{p}-ch">y</span><span class="{p}-ch">n</span><span class="{p}-ch">o</span></div>
  <div class="{p}-tag">seu assessor pessoal no WhatsApp</div>
  <div class="{p}-cta">Quer participar?<br>Me chama no privado 💬</div>"""
css6 = """
.{p}-glow { position:absolute; width:1400px; height:1400px; left:-160px; top:-60px; border-radius:50%; background: radial-gradient(circle, rgba(20,179,125,.26), rgba(20,179,125,0) 62%); }
.{p}-ring { position:absolute; left:290px; top:280px; width:500px; height:500px; border-radius:50%; background:rgba(20,179,125,.18); }
.{p}-mk { left:345px; top:335px; width:390px; height:390px; font-size:250px; padding-top:16px; }
.{p}-name { position:absolute; left:0; right:0; top:840px; font-size:220px; text-align:center; color:#FFF6EA; }
.{p}-ch { display:inline-block; }
.{p}-tag { position:absolute; left:40px; right:40px; top:1110px; font-size:42px; font-weight:700; letter-spacing:.14em; text-transform:uppercase; text-align:center; color:#A9ADC6; }
.{p}-cta { position:absolute; left:86px; right:86px; top:1290px; background:#14B37D; color:#1B1F3B; border-radius:999px; padding:48px 40px; font-size:56px; line-height:1.25; font-weight:700; text-align:center; }
"""
js6 = """
  tl.fromTo(one('.{p}-glow'), { scale: 0.3, opacity: 0 }, { scale: 1, opacity: 1, duration: 1.0, ease: 'power2.out' }, 0);
  tl.fromTo(one('.{p}-mk'), { scale: 0, rotation: -40 }, { scale: 1, rotation: 0, duration: 0.8, ease: 'elastic.out(1, 0.6)' }, 0.1);
  tl.fromTo(one('.{p}-ring'), { scale: 0.6, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.6, ease: 'power2.out' }, 0.35);
  tl.to(one('.{p}-ring'), { scale: 1.12, duration: 2.4, ease: 'sine.inOut' }, 0.95);
  q('.{p}-ch').forEach((el, i) => {
    tl.fromTo(el, { y: 120, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: 'back.out(2)' }, 0.55 + i * 0.08);
  });
  tl.fromTo(one('.{p}-tag'), { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: 'power2.out' }, 1.0);
  tl.fromTo(one('.{p}-cta'), { scale: 0.6, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.5, ease: 'back.out(2)' }, 1.3);
  tl.to(one('.{p}-cta'), { scale: 1.06, duration: 0.2, ease: 'power2.out' }, 1.95);
  tl.to(one('.{p}-cta'), { scale: 1, duration: 0.25, ease: 'power2.in' }, 2.15);
"""
frame("06-chamada", 3.5, css6, b6, js6, navy=True)

print("ok")
