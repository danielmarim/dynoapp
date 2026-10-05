exec(open('base.py').read())
OL = 'stroke="#1E1E1E" stroke-width="5" stroke-linejoin="round"'
S = {}

def pts(vals, x0, x1, ymap):
    n = len(vals)
    return ' '.join(f'{x0 + (x1 - x0) * i / (n - 1):.0f},{ymap(v):.0f}' for i, v in enumerate(vals))

# ---------- 1 ESPERA ----------
v1 = [5.16, 5.21, 5.12, 5.19, 5.09, 5.18, 5.11, 5.20, 5.13, 5.17, 5.10, 5.15]
y1 = lambda v: 1300 - (v - 5.05) / 0.18 * 360
S['01-espera'] = (4.8, '''
.k01 { position:absolute; left:86px; top:200px; font-size:38px; font-weight:700; letter-spacing:.16em; text-transform:uppercase; color:#3EE9AF; }
.t01 { position:absolute; left:86px; right:86px; top:260px; font-size:128px; color:#fff; }
.t01 .g01 { color:#3EE9AF; }
.svg01 { position:absolute; left:0; top:0; width:1080px; height:1920px; }
.f01 { font-family:"Space Grotesk"; font-weight:700; }
.s01 { position:absolute; left:86px; right:86px; top:1560px; font-size:54px; line-height:1.25; font-weight:700; color:#fff; }
''', f'''  <svg § class="svg01" viewBox="0 0 1080 1920">
    <rect x="70" y="760" width="940" height="700" rx="44" fill="#FFF6EA" {OL}/>
    <text class="f01" x="120" y="850" font-size="34" fill="#5E6280" letter-spacing="3">💵 DÓLAR · USD/BRL</text>
    <text class="f01 val01" x="120" y="950" font-size="92" fill="#1B1F3B">R$ 5,16</text>
    <g class="ref01" transform="translate(880 880)"><circle r="52" fill="#FF8A3D" {OL}/><text y="18" font-size="52" text-anchor="middle">🔄</text></g>
    <g opacity=".5" stroke="#E2D6C2" stroke-width="3"><path d="M120 1050 H960 M120 1180 H960 M120 1310 H960"/></g>
    <polyline class="ln01" pathLength="1" points="{pts(v1, 120, 960, y1)}" fill="none" stroke="#FF8A3D" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="1" stroke-dashoffset="1"/>
  </svg>
  <div § class="k01">você também? 😩</div>
  <div § class="h01 t01">Esperando o<br>dólar <span § class="g01">cair</span>…</div>
  <div § class="s01">…e atualizando a cotação<br>toda hora?</div>''', '''  tl.fromTo(one('.k01'), { x: -40, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: 'power2.out' }, 0.1);
  tl.fromTo(one('.t01'), { y: 50, opacity: 0 }, { y: 0, opacity: 1, duration: 0.55, ease: 'power3.out' }, 0.2);
  tl.fromTo(one('.svg01'), { y: 260, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: 'power3.out' }, 0.5);
  tl.to(one('.ln01'), { attr: { 'stroke-dashoffset': 0 }, duration: 2.8, ease: 'none' }, 0.9);
  const vals = [5.16, 5.21, 5.12, 5.19, 5.09, 5.18, 5.11, 5.20, 5.13, 5.17, 5.10, 5.15], el = one('.val01');
  const o = { i: 0 };
  tl.to(o, { i: vals.length - 1, duration: 2.8, ease: 'none', onUpdate: () => { el.textContent = 'R$ ' + vals[Math.round(o.i)].toFixed(2).replace('.', ','); } }, 0.9);
  for (let k = 0; k < 4; k++) tl.fromTo(one('.ref01'), { rotation: 0, svgOrigin: '880 880' }, { rotation: 360, svgOrigin: '880 880', duration: 0.5, ease: 'power2.inOut', immediateRender: false }, 1.1 + k * 0.75);
  tl.fromTo(one('.s01'), { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: 'power2.out' }, 2.4);''', '#1B1F3B')

# ---------- 2 PEDE ----------
S['02-pede'] = (4.8, '''
.k02 { position:absolute; left:86px; right:86px; top:150px; font-size:58px; font-weight:700; text-align:center; }
.svg02 { position:absolute; left:0; top:0; width:1080px; height:1920px; }
.bubw { position:absolute; border:4px solid #1E1E1E; border-radius:34px; font-size:40px; line-height:1.3; padding:22px 30px; max-width:580px; }
.mew { right:240px; background:#D7F8C4; border-bottom-right-radius:8px; }
.dyw { left:240px; background:#fff; border-bottom-left-radius:8px; }
.tw { display:block; font-size:22px; font-weight:700; opacity:.55; margin-top:6px; text-align:right; }
.ok02 { position:absolute; left:0; right:0; top:1600px; text-align:center; }
.ok02 span { display:inline-block; background:#1B1F3B; color:#3EE9AF; border:4px solid #1E1E1E; border-radius:999px; padding:16px 34px; font-size:40px; font-weight:700; }
''', f'''  <svg § class="svg02" viewBox="0 0 1080 1920">
    <rect x="200" y="290" width="680" height="1240" rx="80" fill="#1B1F3B" {OL}/>
    <rect x="225" y="320" width="630" height="1180" rx="60" fill="#ECE5DA"/>
    <rect x="225" y="320" width="630" height="130" rx="60" fill="#1B1F3B"/><rect x="225" y="400" width="630" height="50" fill="#1B1F3B"/>
    <circle cx="300" cy="395" r="36" fill="#14B37D" stroke="#fff" stroke-width="3"/>
    <text x="300" y="410" font-size="40" text-anchor="middle" font-family="Bodoni Moda" font-weight="700" fill="#1B1F3B">D</text>
    <text x="355" y="388" font-size="34" font-family="Space Grotesk" font-weight="700" fill="#fff">Dyno</text>
    <text x="355" y="420" font-size="22" font-family="Space Grotesk" fill="#9AF4D5">online</text>
    <rect x="245" y="1400" width="590" height="76" rx="38" fill="#fff"/>
  </svg>
  <div § class="k02">é só pedir pro Dyno 💬</div>
  <div § class="bubw mew m1" style="top:520px">Me avisa quando o dólar ficar abaixo de R$&nbsp;4,90<span § class="tw">09:12</span></div>
  <div § class="bubw dyw d1" style="top:820px">Combinado! 💵<br>Hoje está em <b>R$&nbsp;4,98</b>.<br>Te aviso quando chegar lá.<span § class="tw">09:12</span></div>
  <div § class="ok02"><span § class="okp02">✅ alerta criado</span></div>''', '''  tl.fromTo(one('.k02'), { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: 'power2.out' }, 0.1);
  tl.fromTo(one('.svg02'), { y: 300, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: 'power3.out' }, 0.05);
  tl.fromTo(one('.m1'), { x: 200, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: 'back.out(1.5)' }, 0.9);
  tl.fromTo(one('.d1'), { x: -200, opacity: 0 }, { x: 0, opacity: 1, duration: 0.45, ease: 'back.out(1.5)' }, 2.0);
  tl.fromTo(one('.okp02'), { scale: 0, opacity: 0, transformOrigin: '50% 50%' }, { scale: 1, opacity: 1, duration: 0.4, ease: 'back.out(2.2)' }, 3.0);''', '#9AF4D5')

# ---------- 3 ALERTA ----------
v3 = [4.98, 4.99, 4.96, 4.97, 4.94, 4.95, 4.92, 4.93, 4.91, 4.89, 4.88]
y3 = lambda v: 820 + (5.00 - v) / 0.15 * 520
yT = y3(4.90)
S['03-alerta'] = (5.6, '''
.k03 { position:absolute; left:86px; top:200px; font-size:38px; font-weight:700; letter-spacing:.16em; text-transform:uppercase; color:#0E8A60; }
.t03 { position:absolute; left:86px; right:86px; top:250px; font-size:120px; }
.svg03 { position:absolute; left:0; top:0; width:1080px; height:1920px; }
.f03 { font-family:"Space Grotesk"; font-weight:700; }
.nt03 { position:absolute; left:60px; right:60px; top:1430px; background:#fff; border:5px solid #1E1E1E; border-radius:40px; padding:30px 36px; box-shadow:12px 12px 0 rgba(26,26,26,.15); }
.nh03 { display:flex; align-items:center; gap:16px; font-size:30px; font-weight:700; color:#5E6280; }
.nl03 { width:56px; height:56px; border-radius:50%; background:#14B37D; border:3px solid #1E1E1E; display:flex; align-items:center; justify-content:center; font-family:"Bodoni Moda",serif; font-weight:700; font-size:34px; color:#1B1F3B; }
.nb03 { margin-top:14px; font-size:48px; line-height:1.25; font-weight:700; }
.ns03 { margin-top:8px; font-size:30px; color:#5E6280; }
''', f'''  <svg § class="svg03" viewBox="0 0 1080 1920">
    <rect x="70" y="580" width="940" height="800" rx="44" fill="#fff" {OL}/>
    <text class="f03" x="120" y="670" font-size="34" fill="#5E6280" letter-spacing="3">💵 DÓLAR · USD/BRL</text>
    <text class="f03 val03" x="120" y="770" font-size="92" fill="#1B1F3B">R$ 4,98</text>
    <line x1="120" y1="{yT:.0f}" x2="960" y2="{yT:.0f}" stroke="#14B37D" stroke-width="6" stroke-dasharray="18 14"/>
    <rect x="120" y="{yT+22:.0f}" width="260" height="54" rx="27" fill="#0B6E4D"/>
    <text class="f03" x="250" y="{yT+59:.0f}" font-size="30" fill="#fff" text-anchor="middle">seu alvo R$ 4,90</text>
    <polyline class="ln03" pathLength="1" points="{pts(v3, 120, 960, y3)}" fill="none" stroke="#1B1F3B" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="1" stroke-dashoffset="1"/>
    <circle class="dot03" cx="960" cy="{y3(4.88):.0f}" r="22" fill="#3EE9AF" {OL} opacity="0"/>
  </svg>
  <div § class="k03">dias depois…</div>
  <div § class="h03 t03">Caiu. 📉</div>
  <div § class="nt03">
    <div § class="nh03"><span § class="nl03">D</span>Dyno · agora</div>
    <div § class="nb03">🔔 Dólar a R$&nbsp;4,88 — bateu o seu alerta!</div>
    <div § class="ns03">Só informo, não é recomendação.</div>
  </div>''', '''  tl.fromTo(one('.k03'), { x: -40, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: 'power2.out' }, 0.1);
  tl.fromTo(one('.t03'), { y: 50, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: 'power3.out' }, 0.2);
  tl.fromTo(one('.svg03'), { y: 200, opacity: 0 }, { y: 0, opacity: 1, duration: 0.55, ease: 'power3.out' }, 0.3);
  tl.to(one('.ln03'), { attr: { 'stroke-dashoffset': 0 }, duration: 2.4, ease: 'none' }, 0.8);
  const o = { v: 4.98 }, el = one('.val03');
  tl.to(o, { v: 4.88, duration: 2.4, ease: 'none', onUpdate: () => { el.textContent = 'R$ ' + o.v.toFixed(2).replace('.', ','); } }, 0.8);
  tl.to(one('.val03'), { attr: { fill: '#0E8A60' }, duration: 0.2 }, 3.0);
  tl.fromTo(one('.dot03'), { attr: { r: 0 }, opacity: 1 }, { attr: { r: 22 }, opacity: 1, duration: 0.3, ease: 'back.out(3)' }, 3.2);
  tl.fromTo(one('.nt03'), { y: 300, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: 'back.out(1.6)' }, 3.4);
  tl.fromTo(one('.nt03'), { rotation: 0 }, { rotation: 2, duration: 0.08, yoyo: true, repeat: 5, ease: 'sine.inOut' }, 3.9);''', '#FFF6EA')

# ---------- 4 COMANDOS ----------
cmds = ['“cotação do dólar”', '“euro hoje”', '“avisa se o euro passar de R$ 6”', '“meus alertas de câmbio”', '“cancela o alerta do dólar”']
chips = ''.join(f'<span § class="chip04">{c}</span>' for c in cmds)
S['04-comandos'] = (3.8, '''
.t04 { position:absolute; left:86px; right:86px; top:260px; font-size:150px; color:#fff; }
.s04 { position:absolute; left:86px; right:86px; top:600px; font-size:60px; font-weight:700; color:#3EE9AF; }
.chips04 { position:absolute; left:86px; right:86px; top:820px; display:flex; flex-direction:column; align-items:flex-start; gap:26px; }
.chip04 { background:#fff; border:4px solid #1E1E1E; border-radius:999px; padding:18px 34px; font-size:44px; font-weight:700; }
.n04 { position:absolute; left:86px; right:86px; top:1640px; font-size:36px; font-weight:700; color:#A9ADC6; }
''', f'''  <div § class="h04 t04">Dólar e euro.</div>
  <div § class="s04">do jeito que você fala:</div>
  <div § class="chips04">{chips}</div>
  <div § class="n04">até 5 alertas por pessoa · confere a cada 15 min</div>''', '''  tl.fromTo(one('.t04'), { scale: 1.6, opacity: 0, transformOrigin: '0% 50%' }, { scale: 1, opacity: 1, duration: 0.35, ease: 'power4.out' }, 0.1);
  tl.fromTo(one('.s04'), { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: 'power2.out' }, 0.45);
  tl.fromTo(document.querySelectorAll('[data-composition-id="04-comandos"] .chip04'), { x: -80, opacity: 0 }, { x: 0, opacity: 1, duration: 0.35, stagger: 0.22, ease: 'back.out(1.6)' }, 0.8);
  tl.fromTo(one('.n04'), { opacity: 0 }, { opacity: 1, duration: 0.4 }, 2.2);''', '#1B1F3B')

# ---------- 5 CTA ----------
S['05-cta'] = (4.2, '''
.logo05 { left:86px; top:260px; width:120px; height:120px; font-size:78px; }
.brand05 { position:absolute; left:236px; top:285px; font-family:"Bodoni Moda",serif; font-weight:700; font-size:72px; }
.pill05 { position:absolute; left:86px; top:500px; background:#FF8A3D; border:5px solid #1E1E1E; border-radius:999px; padding:16px 36px; font-size:40px; font-weight:700; letter-spacing:.08em; }
.t05 { position:absolute; left:86px; right:86px; top:640px; font-size:170px; line-height:.95; }
.t05 .g05 { color:#0E8A60; }
.s05 { position:absolute; left:86px; top:1020px; font-size:54px; }
.btn05 { position:absolute; left:86px; right:86px; top:1180px; background:#1B1F3B; color:#fff; border:5px solid #1E1E1E; border-radius:40px; padding:34px 40px; font-size:52px; font-weight:700; text-align:center; box-shadow:12px 12px 0 rgba(26,26,26,.15); }
.url05 { position:absolute; left:86px; right:86px; top:1400px; font-size:46px; font-weight:700; text-align:center; color:#0E8A60; }
''', '''  <div § class="logo05 logo05">D</div>
  <div § class="brand05">Dyno</div>
  <div § class="pill05">NOVIDADE · JÁ NO AR</div>
  <div § class="h05 t05">Alerta de<br><span § class="g05">câmbio.</span></div>
  <div § class="s05">incluso no seu Dyno, sem custo extra</div>
  <div § class="btn05">💬 Manda “cotação do dólar”</div>
  <div § class="url05">dynoapp.com.br</div>''', '''  tl.fromTo([one('.logo05'), one('.brand05')], { y: -30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: 'power2.out', stagger: 0.08 }, 0.05);
  tl.fromTo(one('.pill05'), { scale: 0, transformOrigin: '0% 50%' }, { scale: 1, duration: 0.4, ease: 'back.out(2)' }, 0.25);
  tl.fromTo(one('.t05'), { y: 60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.55, ease: 'power3.out' }, 0.45);
  tl.fromTo(one('.s05'), { opacity: 0 }, { opacity: 1, duration: 0.4 }, 0.9);
  tl.fromTo(one('.btn05'), { y: 80, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: 'back.out(1.6)' }, 1.15);
  tl.to(one('.btn05'), { scale: 1.04, duration: 0.3, yoyo: true, repeat: 3, ease: 'sine.inOut' }, 1.8);
  tl.fromTo(one('.url05'), { opacity: 0 }, { opacity: 1, duration: 0.4 }, 1.5);''', '#FFF6EA')

for cid, (dur, css, body, js, bg) in S.items():
    open(f'compositions/frames/{cid}.html', 'w').write(comp(cid, dur, css, body, js, bg))
