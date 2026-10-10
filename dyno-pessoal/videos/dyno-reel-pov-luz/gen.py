FONTS = '''@font-face { font-family: "Bodoni Moda"; src: url("assets/fonts/bodoni-moda-latin-700-normal.woff2") format("woff2"); font-weight: 700; }
@font-face { font-family: "Space Grotesk"; src: url("assets/fonts/space-grotesk-latin-400-normal.woff2") format("woff2"); font-weight: 400; }
@font-face { font-family: "Space Grotesk"; src: url("assets/fonts/space-grotesk-latin-700-normal.woff2") format("woff2"); font-weight: 700; }'''
def comp(cid, dur, css, body, js, bg):
    p = cid.split('-')[0]
    A = 'data-layout-allow-overlap data-layout-allow-overflow'
    body = body.replace('§', A)
    return f'''<template>
<script src="assets/js/gsap.min.js"></script>
<style>
{FONTS}
[data-composition-id="{cid}"]#root, #root {{ position: absolute; inset: 0; width: 1080px; height: 1920px; overflow: hidden; font-family: "Space Grotesk", sans-serif; color: #1B1F3B; }}
.h{p} {{ font-family: "Bodoni Moda", serif; font-weight: 700; line-height: 1.0; letter-spacing: -0.02em; }}
.bub{p} {{ position: absolute; border: 5px solid #1E1E1E; border-radius: 54px; font-size: 46px; line-height: 1.28; padding: 26px 42px; max-width: 880px; box-shadow: 12px 12px 0 rgba(26,26,26,.10); }}
.me{p} {{ right: 76px; background: #fff; border-bottom-right-radius: 12px; }}
.dy{p} {{ left: 76px; background: #9AF4D5; border-bottom-left-radius: 12px; }}
.who{p} {{ display: block; font-size: 28px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; opacity: .6; margin-bottom: 6px; }}
.logo{p} {{ position: absolute; border-radius: 50%; background: #14B37D; border: 5px solid #1E1E1E; display: flex; align-items: center; justify-content: center; font-family: "Bodoni Moda", serif; font-weight: 700; color: #1B1F3B; line-height: 1; }}
{css}
</style>
<div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920" data-duration="{dur}">
  <div id="f{p}-bg" class="clip" data-start="0" data-duration="{dur}" data-track-index="0" style="position:absolute;inset:0;background:{bg}"></div>
{body}
</div>
<script>
(function () {{
  window.__timelines = window.__timelines || {{}};
  const tl = gsap.timeline({{ paused: true }});
  const one = (s) => document.querySelector('[data-composition-id="{cid}"] ' + s);
{js}
  tl.to({{}}, {{ duration: {dur} }}, 0);
  window.__timelines["{cid}"] = tl;
}})();
</script>
</template>
'''
S = {}
# 1 POV
S['01-pov'] = (4, '''
.glow01 { position:absolute; left:340px; top:150px; width:400px; height:400px; border-radius:50%; background:radial-gradient(circle,#FFE27A 0%,rgba(255,226,122,.35) 40%,rgba(255,226,122,0) 70%); }
.bulb01 { position:absolute; left:440px; top:200px; width:200px; font-size:200px; line-height:1; text-align:center; }
.pill01 { position:absolute; left:86px; top:640px; background:#3EE9AF; border:5px solid #1E1E1E; border-radius:999px; padding:16px 40px; font-size:56px; font-weight:700; letter-spacing:.06em; }
.t01 { position:absolute; left:86px; right:86px; top:790px; font-size:124px; color:#fff; }
.t01b { position:absolute; left:86px; right:86px; top:1250px; font-size:150px; color:#FF8A3D; }
.handle01 { position:absolute; left:86px; top:1560px; font-size:34px; font-weight:700; letter-spacing:.1em; color:#A9ADC6; }
''', '''  <div § class="glow01"></div>
  <div § class="bulb01">💡</div>
  <div § class="pill01">POV:</div>
  <div § class="h01 t01">você esqueceu de pagar a luz…</div>
  <div § class="h01 t01b">de novo 🫠</div>
  <div § class="handle01">@dynoapp.ia</div>''', '''  tl.fromTo(one('.glow01'), { scale: 0.6, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.6, ease: 'power2.out' }, 0);
  tl.fromTo(one('.bulb01'), { y: -60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.55, ease: 'back.out(1.6)' }, 0.05);
  tl.fromTo(one('.pill01'), { scale: 0, transformOrigin: '0% 50%' }, { scale: 1, duration: 0.4, ease: 'back.out(2)' }, 0.35);
  tl.fromTo(one('.t01'), { y: 60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: 'power3.out' }, 0.6);
  tl.fromTo(one('.t01b'), { scale: 1.6, opacity: 0, transformOrigin: '0% 50%' }, { scale: 1, opacity: 1, duration: 0.35, ease: 'power4.out' }, 2.0);
  tl.fromTo(one('.t01b'), { rotation: 0 }, { rotation: -3, duration: 0.12, yoyo: true, repeat: 3, ease: 'sine.inOut' }, 2.35);
  tl.fromTo(one('.handle01'), { opacity: 0 }, { opacity: 1, duration: 0.4 }, 0.8);
  [0,1,2,3,4].forEach((k) => tl.to(one('.glow01'), { opacity: k % 2 ? 1 : 0.25, duration: 0.07 }, 3.25 + k * 0.1));''', '#1B1F3B')
# 2 apagou
S['02-apagou'] = (4, '''
.flash02 { position:absolute; inset:0; background:#2A2F55; }
.t02 { position:absolute; left:86px; right:86px; top:640px; font-size:150px; color:#fff; text-align:center; }
.s02 { position:absolute; left:110px; right:110px; top:1080px; font-size:54px; line-height:1.3; color:#D6D9EC; text-align:center; }
.e02 { position:absolute; left:0; right:0; top:1330px; font-size:150px; text-align:center; }
''', '''  <div § class="flash02"></div>
  <div § class="h02 t02">cortaram<br>a luz.</div>
  <div § class="s02">e ainda vem juros<br>+ taxa de religação</div>
  <div § class="e02">😭</div>''', '''  [0,1,2,3,4,5].forEach((k) => tl.to(one('.flash02'), { opacity: k % 2 ? 0.9 : 0, duration: 0.06 }, 0.05 + k * 0.11));
  tl.to(one('.flash02'), { opacity: 0, duration: 0.05 }, 0.75);
  tl.fromTo(one('.t02'), { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.5, ease: 'power3.out' }, 1.0);
  tl.fromTo(one('.s02'), { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.45, ease: 'power2.out' }, 1.9);
  tl.fromTo(one('.e02'), { scale: 0 }, { scale: 1, duration: 0.4, ease: 'back.out(2.4)' }, 2.5);''', '#05060C')
# 3 pede
S['03-pede'] = (4.5, '''
.k03 { position:absolute; left:86px; top:300px; font-size:38px; font-weight:700; letter-spacing:.16em; text-transform:uppercase; color:#0E8A60; }
.t03 { position:absolute; left:86px; right:86px; top:370px; font-size:124px; }
.logo03 { left:840px; top:250px; width:150px; height:150px; font-size:96px; }
''', '''  <div § class="logo03 logo03">D</div>
  <div § class="k03">agora, com o Dyno</div>
  <div § class="h03 t03">Pede uma vez.</div>
  <div § class="bub03 me03 r1" style="top:720px"><span § class="who03">Você · 21:02</span>me lembra de pagar a luz dia 10 às 9h</div>
  <div § class="bub03 dy03 r2" style="top:1080px"><span § class="who03">Dyno · 21:02</span>⏰ Combinado! Dia 10, às 9h, eu te chamo.</div>''', '''  tl.fromTo(one('.logo03'), { scale: 0, rotation: -90 }, { scale: 1, rotation: 0, duration: 0.55, ease: 'back.out(1.8)' }, 0.1);
  tl.fromTo(one('.k03'), { x: -40, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: 'power2.out' }, 0.2);
  tl.fromTo(one('.t03'), { y: 50, opacity: 0 }, { y: 0, opacity: 1, duration: 0.55, ease: 'power3.out' }, 0.3);
  tl.fromTo(one('.r1'), { x: 260, opacity: 0 }, { x: 0, opacity: 1, duration: 0.5, ease: 'back.out(1.4)' }, 0.9);
  tl.fromTo(one('.r2'), { x: -260, opacity: 0 }, { x: 0, opacity: 1, duration: 0.5, ease: 'back.out(1.4)' }, 2.1);''', '#FFF6EA')
# 4 insiste
S['04-insiste'] = (7, '''
.t04 { position:absolute; left:86px; right:86px; top:250px; font-size:118px; }
.bell04 { display:inline-block; }
''', '''  <div § class="h04 t04">E ele insiste.</div>
  <div § class="bub04 dy04 r1" style="top:460px"><span § class="who04">Dyno · 09:00</span><span § class="bell04 b1">⏰</span> Hora de pagar a luz 💡</div>
  <div § class="bub04 dy04 r2" style="top:680px;background:#FFB98B"><span § class="who04">Dyno · 09:30</span><span § class="bell04 b2">🔔</span> Ainda não vi seu ok…</div>
  <div § class="bub04 dy04 r3" style="top:900px;background:#FF8A3D"><span § class="who04">Dyno · 10:00</span><span § class="bell04 b3">👀</span> Tô aqui, hein. Vence hoje!</div>
  <div § class="bub04 me04 r4" style="top:1120px;font-size:60px"><span § class="who04">Você · 10:02</span>paguei ✅</div>
  <div § class="bub04 dy04 r5" style="top:1360px"><span § class="who04">Dyno · 10:02</span>Boa! Anotei R$ 187,40 em Casa 🏠</div>''', '''  tl.fromTo(one('.t04'), { y: 50, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: 'power3.out' }, 0.1);
  tl.fromTo(one('.r1'), { x: -260, opacity: 0 }, { x: 0, opacity: 1, duration: 0.45, ease: 'back.out(1.4)' }, 0.6);
  [0,1,2,3].forEach((k) => tl.to(one('.b1'), { rotation: k % 2 ? -18 : 18, duration: 0.09 }, 1.05 + k * 0.09));
  tl.to(one('.b1'), { rotation: 0, duration: 0.1 }, 1.42);
  tl.fromTo(one('.r2'), { scale: 0.6, opacity: 0, transformOrigin: '0% 100%' }, { scale: 1, opacity: 1, duration: 0.42, ease: 'back.out(2)' }, 1.6);
  [0,1,2,3,4,5].forEach((k) => tl.to(one('.b2'), { rotation: k % 2 ? -22 : 22, duration: 0.08 }, 2.0 + k * 0.08));
  tl.to(one('.b2'), { rotation: 0, duration: 0.1 }, 2.5);
  tl.fromTo(one('.r3'), { scale: 0.6, opacity: 0, transformOrigin: '0% 100%' }, { scale: 1, opacity: 1, duration: 0.42, ease: 'back.out(2.2)' }, 2.65);
  tl.fromTo(one('.r3'), { x: 0 }, { x: 14, duration: 0.05, yoyo: true, repeat: 7, ease: 'none' }, 3.1);
  tl.fromTo(one('.r4'), { x: 260, opacity: 0 }, { x: 0, opacity: 1, duration: 0.45, ease: 'back.out(1.5)' }, 3.9);
  tl.fromTo(one('.r5'), { x: -260, opacity: 0 }, { x: 0, opacity: 1, duration: 0.45, ease: 'back.out(1.4)' }, 4.8);''', '#FFF6EA')
# 5 nunca
S['05-nunca'] = (3, '''
.logo05 { left:445px; top:330px; width:190px; height:190px; font-size:124px; }
.t05 { position:absolute; left:0; right:0; top:640px; font-size:270px; line-height:.92; color:#fff; text-align:center; }
.t05 .m05 { color:#3EE9AF; display:inline-block; }
.s05 { position:absolute; left:86px; right:86px; top:1240px; font-size:56px; color:#D6D9EC; text-align:center; }
''', '''  <div § class="logo05 logo05">D</div>
  <div § class="h05 t05"><span § class="n05" style="display:inline-block">Nunca</span><br><span § class="m05">mais.</span></div>
  <div § class="s05">esquecer uma conta.</div>''', '''  tl.fromTo(one('.logo05'), { scale: 0 }, { scale: 1, duration: 0.45, ease: 'back.out(2)' }, 0.05);
  tl.fromTo(one('.n05'), { scale: 2.2, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.3, ease: 'power4.out' }, 0.35);
  tl.fromTo(one('.m05'), { scale: 2.2, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.3, ease: 'power4.out' }, 0.8);
  tl.fromTo(one('.s05'), { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: 'power2.out' }, 1.4);''', '#1B1F3B')
# 6 cta
S['06-cta'] = (4.5, '''
.logo06 { left:86px; top:260px; width:120px; height:120px; font-size:78px; }
.brand06 { position:absolute; left:236px; top:285px; font-family:"Bodoni Moda",serif; font-weight:700; font-size:72px; }
.pill06 { position:absolute; left:86px; top:500px; background:#FF8A3D; border:5px solid #1E1E1E; border-radius:999px; padding:16px 36px; font-size:40px; font-weight:700; letter-spacing:.08em; }
.t06 { position:absolute; left:86px; right:86px; top:640px; font-size:190px; line-height:.92; }
.t06 .g06 { color:#0E8A60; }
.s06 { position:absolute; left:86px; top:1060px; font-size:54px; }
.btn06 { position:absolute; left:86px; right:86px; top:1200px; background:#1B1F3B; color:#fff; border:5px solid #1E1E1E; border-radius:40px; padding:34px 40px; font-size:60px; font-weight:700; text-align:center; box-shadow:12px 12px 0 rgba(26,26,26,.15); }
.url06 { position:absolute; left:86px; right:86px; top:1420px; font-size:46px; font-weight:700; text-align:center; color:#0E8A60; }
''', '''  <div § class="logo06 logo06">D</div>
  <div § class="brand06">Dyno</div>
  <div § class="pill06">BETA FECHADO · VAGAS LIMITADAS</div>
  <div § class="h06 t06">60 dias<br><span § class="g06">grátis.</span></div>
  <div § class="s06">em troca do seu feedback</div>
  <div § class="btn06">🔗 Link na bio</div>
  <div § class="url06">dynoapp.com.br/beta</div>''', '''  tl.fromTo([one('.logo06'), one('.brand06')], { y: -30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: 'power2.out', stagger: 0.08 }, 0.05);
  tl.fromTo(one('.pill06'), { scale: 0, transformOrigin: '0% 50%' }, { scale: 1, duration: 0.4, ease: 'back.out(2)' }, 0.25);
  tl.fromTo(one('.t06'), { y: 60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.55, ease: 'power3.out' }, 0.45);
  tl.fromTo(one('.s06'), { opacity: 0 }, { opacity: 1, duration: 0.4 }, 0.9);
  tl.fromTo(one('.btn06'), { y: 80, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: 'back.out(1.6)' }, 1.15);
  tl.to(one('.btn06'), { scale: 1.04, duration: 0.3, yoyo: true, repeat: 3, ease: 'sine.inOut' }, 1.8);
  tl.fromTo(one('.url06'), { opacity: 0 }, { opacity: 1, duration: 0.4 }, 1.5);''', '#FFF6EA')
for cid, (dur, css, body, js, bg) in S.items():
    p = cid.split('-')[0]
    body = body.replace('h01', 'h01').replace('bub03','bub03')
    open(f'compositions/frames/{cid}.html', 'w').write(comp(cid, dur, css, body, js, bg))
