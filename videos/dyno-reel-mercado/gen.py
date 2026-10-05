exec(open('base.py').read())
OL = 'stroke="#1E1E1E" stroke-width="5" stroke-linejoin="round"'
SKIN = '#E9B98F'

def person(cls, x, y, arm='down', shirt='#14B37D'):
    if arm == 'down':
        rarm = f'<rect x="96" y="-610" width="52" height="270" rx="26" fill="{shirt}" {OL} transform="rotate(-8 122 -610)"/><circle cx="160" cy="-335" r="30" fill="{SKIN}" {OL}/>'
    elif arm == 'phone':
        rarm = f'<path d="M110 -600 Q190 -520 150 -430 L 60 -470" fill="none" stroke="#1E1E1E" stroke-width="58" stroke-linecap="round"/><path d="M110 -600 Q190 -520 150 -430 L 60 -470" fill="none" stroke="{shirt}" stroke-width="48" stroke-linecap="round"/><rect x="0" y="-560" width="70" height="120" rx="14" fill="#1B1F3B" {OL}/><circle cx="52" cy="-470" r="28" fill="{SKIN}" {OL}/>'
    else:  # bag
        rarm = f'<rect x="96" y="-610" width="52" height="260" rx="26" fill="{shirt}" {OL} transform="rotate(-6 122 -610)"/><path d="M120 -340 L 250 -340 L 270 -150 L 100 -150 Z" fill="#FFB98B" {OL}/><path d="M150 -340 Q185 -400 220 -340" fill="none" {OL}/><circle cx="150" cy="-345" r="28" fill="{SKIN}" {OL}/><text x="185" y="-215" font-size="70" text-anchor="middle">🥖</text>'
    return f'''<g transform="translate({x} {y})"><g class="{cls}">
  <rect x="-72" y="-330" width="60" height="330" rx="24" fill="#1B1F3B" {OL}/>
  <rect x="12" y="-330" width="60" height="330" rx="24" fill="#1B1F3B" {OL}/>
  <ellipse cx="-50" cy="0" rx="50" ry="22" fill="#2B2233" {OL}/><ellipse cx="50" cy="0" rx="50" ry="22" fill="#2B2233" {OL}/>
  <rect x="-148" y="-610" width="52" height="270" rx="26" fill="{shirt}" {OL} transform="rotate(8 -122 -610)"/><circle cx="-160" cy="-335" r="30" fill="{SKIN}" {OL}/>
  {rarm}
  <rect x="-115" y="-650" width="230" height="350" rx="70" fill="{shirt}" {OL}/>
  <rect x="-28" y="-690" width="56" height="60" fill="{SKIN}" {OL}/>
  <circle cx="0" cy="-770" r="92" fill="{SKIN}" {OL}/>
  <path d="M-96 -775 Q-100 -880 0 -880 Q100 -880 96 -775 Q60 -830 -10 -820 Q-60 -815 -96 -775 Z" fill="#2B2233" {OL}/>
  <circle cx="-32" cy="-765" r="9" fill="#1E1E1E"/><circle cx="32" cy="-765" r="9" fill="#1E1E1E"/>
  <path class="mouth" d="M-30 -728 Q0 -700 30 -728" fill="none" stroke="#1E1E1E" stroke-width="6" stroke-linecap="round"/>
  <circle cx="-55" cy="-735" r="14" fill="#FF8A3D" opacity=".35"/><circle cx="55" cy="-735" r="14" fill="#FF8A3D" opacity=".35"/>
</g></g>'''

def shelves():
    cols = ['#FF8A3D', '#3EE9AF', '#FFB98B', '#14B37D', '#9AF4D5', '#FFC096']
    out = ['<rect x="0" y="600" width="1080" height="760" fill="#F2E6D3"/>']
    for r, y in enumerate([760, 1020]):
        out.append(f'<rect x="40" y="{y+120}" width="1000" height="22" rx="8" fill="#C9B9A0" {OL}/>')
        x = 70
        k = r * 2
        while x < 1000:
            c = cols[k % len(cols)]
            if k % 3 == 0:
                out.append(f'<rect x="{x}" y="{y}" width="80" height="120" rx="10" fill="{c}" {OL}/>'); x += 100
            elif k % 3 == 1:
                out.append(f'<rect x="{x+10}" y="{y+30}" width="60" height="90" rx="26" fill="{c}" {OL}/><rect x="{x+28}" y="{y+5}" width="24" height="30" rx="6" fill="{c}" {OL}/>'); x += 95
            else:
                out.append(f'<circle cx="{x+40}" cy="{y+80}" r="40" fill="{c}" {OL}/>'); x += 100
            k += 1
    return ''.join(out)

S = {}
# ---------- 1 CAIXA ----------
items = ''.join(f'<g transform="translate(0 1300)"><g data-layout-allow-overlap class="it01 it01-{i}" opacity="0">{g}</g></g>' for i, g in enumerate([
    f'<rect x="-50" y="-90" width="100" height="90" rx="12" fill="#FF8A3D" {OL}/><text x="0" y="-30" font-size="44" text-anchor="middle">🍝</text>',
    f'<rect x="-34" y="-120" width="68" height="120" rx="24" fill="#3EE9AF" {OL}/><text x="0" y="-40" font-size="40" text-anchor="middle">🥛</text>',
    f'<circle cx="0" cy="-48" r="48" fill="#FFB98B" {OL}/><text x="0" y="-32" font-size="44" text-anchor="middle">🍎</text>',
    f'<rect x="-55" y="-80" width="110" height="80" rx="12" fill="#9AF4D5" {OL}/><text x="0" y="-26" font-size="42" text-anchor="middle">🧀</text>',
]))
S['01-caixa'] = (5, '''
.k01 { position:absolute; left:86px; top:200px; font-size:38px; font-weight:700; letter-spacing:.16em; text-transform:uppercase; color:#0E8A60; }
.t01 { position:absolute; left:86px; right:86px; top:250px; font-size:100px; }
.svg01 { position:absolute; left:0; top:0; width:1080px; height:1920px; }
.tot01 { font-family:"Space Grotesk"; font-weight:700; }
''', f'''  <svg § class="svg01" viewBox="0 0 1080 1920">
    {shelves()}
    {person('p01', 770, 1820)}
    <rect x="0" y="1300" width="1080" height="70" fill="#3A3F66" {OL}/>
    {items}
    <rect x="455" y="1240" width="30" height="70" rx="8" fill="#1B1F3B" {OL}/><rect class="laser01" x="445" y="1290" width="50" height="10" rx="5" fill="#FF3B3B" opacity="0"/>
    <rect x="-10" y="1365" width="1100" height="40" fill="#FFB98B" {OL}/>
    <rect x="-10" y="1400" width="1100" height="540" fill="#252A4D" {OL}/><g opacity=".5" fill="none" stroke="#3A3F66" stroke-width="6"><path d="M80 1520 H1000 M80 1660 H1000"/></g>
    <g transform="translate(90 1060)">
      <rect x="0" y="0" width="330" height="210" rx="22" fill="#1B1F3B" {OL}/>
      <rect x="22" y="22" width="286" height="166" rx="12" fill="#0F1230"/>
      <text x="44" y="75" font-size="30" fill="#9AF4D5" class="tot01" letter-spacing="3">TOTAL</text>
      <text class="tot01 val01" x="44" y="150" font-size="62" fill="#3EE9AF">R$ 0,00</text>
      <rect x="140" y="210" width="50" height="40" fill="#1B1F3B" {OL}/>
    </g>
  </svg>
  <div § class="k01">na vida real 🛒</div>
  <div § class="h01 t01">Passou as compras no caixa…</div>''', '''  tl.fromTo(one('.k01'), { x: -40, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: 'power2.out' }, 0.1);
  tl.fromTo(one('.t01'), { y: 50, opacity: 0 }, { y: 0, opacity: 1, duration: 0.55, ease: 'power3.out' }, 0.2);
  tl.fromTo(one('.p01'), { x: 160, opacity: 0 }, { x: 0, opacity: 1, duration: 0.6, ease: 'power3.out' }, 0.15);
  const vals = [18.9, 25.8, 33.7, 86.4];
  for (let i = 0; i < 4; i++) {
    const t0 = 0.9 + i * 0.8;
    tl.fromTo(one('.it01-' + i), { x: 1100, opacity: 1 }, { x: 470, opacity: 1, immediateRender: false, duration: 0.55, ease: 'power1.inOut' }, t0);
    tl.to(one('.laser01'), { opacity: 1, duration: 0.05 }, t0 + 0.55);
    tl.to(one('.laser01'), { opacity: 0, duration: 0.05 }, t0 + 0.68);
    tl.to(one('.it01-' + i), { x: 120, opacity: 0, duration: 0.35, ease: 'power1.in' }, t0 + 0.6);
    const prev = i ? vals[i - 1] : 0, o = { v: prev }, el = one('.val01');
    tl.to(o, { v: vals[i], duration: 0.25, ease: 'none', onUpdate: () => { el.textContent = 'R$ ' + o.v.toFixed(2).replace('.', ','); } }, t0 + 0.56);
  }
  tl.fromTo(one('.val01'), { scale: 1 }, { scale: 1.12, duration: 0.15, yoyo: true, repeat: 1, transformOrigin: '0% 50%' }, 4.2);''', '#FFF6EA')

# ---------- 2 PAGA ----------
S['02-paga'] = (4, '''
.t02 { position:absolute; left:86px; right:86px; top:220px; font-size:150px; }
.s02 { position:absolute; left:86px; right:86px; top:1440px; font-size:58px; line-height:1.25; font-weight:700; }
.svg02 { position:absolute; left:0; top:0; width:1080px; height:1920px; }
.f02 { font-family:"Space Grotesk"; font-weight:700; }
''', f'''  <svg § class="svg02" viewBox="0 0 1080 1920">
    <circle cx="540" cy="930" r="400" fill="#9AF4D5" opacity=".45"/>
    <g transform="translate(330 560)">
      <rect x="0" y="0" width="420" height="720" rx="60" fill="#1B1F3B" {OL}/>
      <rect class="scr02" x="40" y="50" width="340" height="270" rx="22" fill="#0F1230"/>
      <text class="f02 amt02" x="210" y="170" font-size="62" fill="#fff" text-anchor="middle">R$ 86,40</text>
      <text class="f02 ap02" x="210" y="250" font-size="40" fill="#1B1F3B" text-anchor="middle" opacity="0">✅ APROVADO</text>
      <g fill="#3A3F66">{''.join(f'<rect x="{60+c*110}" y="{380+r*80}" width="80" height="56" rx="14"/>' for r in range(4) for c in range(3))}</g>
    </g>
    <g transform="translate(0 820)"><g class="card02"><g transform="rotate(-12)">
      <rect x="0" y="0" width="380" height="240" rx="26" fill="#FF8A3D" {OL}/>
      <rect x="40" y="70" width="70" height="54" rx="10" fill="#FFE27A" {OL}/>
      <text class="f02" x="40" y="200" font-size="34" fill="#1B1F3B" letter-spacing="4">•••• 4821</text>
      <path d="M300 60 q20 30 0 60 M320 45 q30 45 0 90" fill="none" stroke="#1B1F3B" stroke-width="6" stroke-linecap="round"/>
    </g></g></g>
    <g transform="translate(0 1000)"><g class="hand02"><rect x="0" y="0" width="300" height="120" rx="60" fill="{SKIN}" {OL}/><rect x="-30" y="-20" width="110" height="70" rx="35" fill="{SKIN}" {OL}/></g></g>
  </svg>
  <div § class="h02 t02">Pagou.</div>
  <div § class="s02">…e já ia esquecer<br>de anotar 😅</div>''', '''  tl.fromTo(one('.t02'), { y: 50, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: 'power3.out' }, 0.1);
  tl.fromTo(one('.card02'), { x: 1200 }, { x: 740, duration: 0.7, ease: 'power3.out' }, 0.3);
  tl.fromTo(one('.hand02'), { x: 1400 }, { x: 980, duration: 0.7, ease: 'power3.out' }, 0.3);
  tl.to(one('.scr02'), { fill: '#3EE9AF', duration: 0.15 }, 1.1);
  tl.to(one('.amt02'), { fill: '#1B1F3B', y: -20, duration: 0.15 }, 1.1);
  tl.fromTo(one('.ap02'), { opacity: 0, scale: 0.6, transformOrigin: '50% 50%' }, { opacity: 1, scale: 1, duration: 0.3, ease: 'back.out(2.5)' }, 1.15);
  tl.to([one('.card02'), one('.hand02')], { x: '+=700', duration: 0.6, ease: 'power2.in' }, 1.8);
  tl.fromTo(one('.s02'), { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: 'power2.out' }, 2.1);''', '#FFF6EA')

# ---------- 3 AUDIO ----------
bars = ''.join(f'<rect class="bar03" x="{150+i*16}" y="-{h//2}" width="9" height="{h}" rx="4" fill="#0E8A60"/>' for i, h in enumerate([20,38,26,50,30,44,18,40,28,52,24,36,20,46,30,22,40,26]))
S['03-audio'] = (7, '''
.k03 { position:absolute; left:86px; right:86px; top:150px; font-size:56px; font-weight:700; text-align:center; }
.svg03 { position:absolute; left:0; top:0; width:1080px; height:1920px; }
.bubw { position:absolute; border:4px solid #1E1E1E; border-radius:34px; font-size:38px; line-height:1.3; padding:22px 30px; max-width:580px; }
.mew { right:240px; background:#D7F8C4; border-bottom-right-radius:8px; }
.dyw { left:240px; background:#fff; border-bottom-left-radius:8px; }
.tw { display:block; font-size:22px; font-weight:700; opacity:.55; margin-top:6px; text-align:right; }
.rec03 { position:absolute; left:250px; top:1385px; font-size:32px; font-weight:700; color:#B3261E; }
''', f'''  <svg § class="svg03" viewBox="0 0 1080 1920">
    <rect x="200" y="290" width="680" height="1240" rx="80" fill="#1B1F3B" {OL}/>
    <rect x="225" y="320" width="630" height="1180" rx="60" fill="#ECE5DA"/>
    <rect x="225" y="320" width="630" height="130" rx="60" fill="#1B1F3B"/><rect x="225" y="400" width="630" height="50" fill="#1B1F3B"/>
    <circle cx="300" cy="395" r="36" fill="#14B37D" stroke="#fff" stroke-width="3"/>
    <text x="300" y="410" font-size="40" text-anchor="middle" font-family="Bodoni Moda" font-weight="700" fill="#1B1F3B">D</text>
    <text x="355" y="388" font-size="34" font-family="Space Grotesk" font-weight="700" fill="#fff">Dyno</text>
    <text x="355" y="420" font-size="22" font-family="Space Grotesk" fill="#9AF4D5">online</text>
    <rect x="245" y="1360" width="490" height="80" rx="40" fill="#fff"/>
    <circle class="mic03" cx="790" cy="1400" r="44" fill="#14B37D"/>
    <text x="790" y="1414" font-size="40" text-anchor="middle">🎙️</text>
  </svg>
  <div § class="k03">pegou o celular e mandou<br>um áudio pro Dyno 🎙️</div>
  <div § class="rec03">● Gravando… 0:03</div>
  <div § class="bubw mew m1" style="top:500px;width:470px;height:110px"><svg § viewBox="0 0 470 70" width="410" height="50" style="display:block"><g transform="translate(-110 35)"><text x="115" y="12" font-size="34">▶</text>{bars}</g></svg><span § class="tw" style="margin-top:-2px">0:03 · 12:41</span></div>
  <div § class="bubw dyw d1" style="top:650px"><b>🎧 Entendi:</b> “gastei 86 e 40 no mercado”<span § class="tw">12:41</span></div>
  <div § class="bubw dyw d2" style="top:900px">✅ <b>Anotado!</b><br>R$ 86,40 em <b>Mercado 🛒</b><br>No mês: R$ 412 nessa categoria.<span § class="tw">12:41</span></div>''', '''  tl.fromTo(one('.k03'), { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: 'power2.out' }, 0.1);
  tl.fromTo(one('.svg03'), { y: 300, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: 'power3.out' }, 0.05);
  tl.fromTo(one('.rec03'), { opacity: 0 }, { opacity: 1, duration: 0.1 }, 0.8);
  tl.to(one('.rec03'), { opacity: 0.3, duration: 0.25, yoyo: true, repeat: 5 }, 0.9);
  tl.to(one('.mic03'), { attr: { r: 56 }, fill: '#FF3B3B', duration: 0.2 }, 0.8);
  tl.to(one('.mic03'), { attr: { r: 44 }, fill: '#14B37D', duration: 0.2 }, 2.4);
  tl.to(one('.rec03'), { opacity: 0, duration: 0.1 }, 2.4);
  tl.fromTo(one('.m1'), { x: 200, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: 'back.out(1.5)' }, 2.5);
  tl.fromTo(document.querySelectorAll('[data-composition-id="03-audio"] .bar03'), { scaleY: 0.3, transformOrigin: '50% 50%' }, { scaleY: 1, duration: 0.2, stagger: 0.03, ease: 'power1.out' }, 2.7);
  tl.fromTo(one('.d1'), { x: -200, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: 'back.out(1.5)' }, 3.5);
  tl.fromTo(one('.d2'), { x: -200, opacity: 0 }, { x: 0, opacity: 1, duration: 0.45, ease: 'back.out(1.5)' }, 4.5);
  tl.fromTo(one('.d2'), { scale: 1 }, { scale: 1.04, duration: 0.18, yoyo: true, repeat: 1, transformOrigin: '0% 100%' }, 5.1);''', '#9AF4D5')

# ---------- 4 PRONTO ----------
S['04-pronto'] = (3.2, '''
.svg04 { position:absolute; left:0; top:0; width:1080px; height:1920px; }
.t04 { position:absolute; left:86px; right:86px; top:220px; font-size:220px; color:#fff; }
.s04 { position:absolute; left:86px; right:86px; top:470px; font-size:60px; font-weight:700; color:#3EE9AF; }
.chips04 { position:absolute; left:86px; right:86px; top:1600px; display:flex; flex-wrap:wrap; gap:18px; }
.chip04 { background:#fff; border:4px solid #1E1E1E; border-radius:999px; padding:14px 28px; font-size:36px; font-weight:700; }
''', f'''  <svg § class="svg04" viewBox="0 0 1080 1920"><circle cx="540" cy="1150" r="380" fill="#252A4D"/>{person('p04', 500, 1560, 'bag')}</svg>
  <div § class="h04 t04">Pronto.</div>
  <div § class="s04">registrado em 3 segundos.</div>
  <div § class="chips04"><span § class="chip04">sem planilha</span><span § class="chip04">sem app novo</span><span § class="chip04">texto, áudio ou foto</span></div>''', '''  tl.fromTo(one('.t04'), { scale: 1.8, opacity: 0, transformOrigin: '0% 50%' }, { scale: 1, opacity: 1, duration: 0.35, ease: 'power4.out' }, 0.1);
  tl.fromTo(one('.s04'), { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: 'power2.out' }, 0.5);
  tl.fromTo(one('.p04'), { x: -300, opacity: 0 }, { x: 0, opacity: 1, duration: 0.7, ease: 'power3.out' }, 0.2);
  tl.to(one('.p04'), { y: -14, duration: 0.25, yoyo: true, repeat: 5, ease: 'sine.inOut' }, 0.9);
  tl.fromTo(document.querySelectorAll('[data-composition-id="04-pronto"] .chip04'), { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.35, stagger: 0.12, ease: 'back.out(1.6)' }, 1.1);''', '#1B1F3B')

# ---------- 5 CTA (from pov-luz) ----------
cta = open('../dyno-reel-pov-luz/compositions/frames/06-cta.html').read()
cta = cta.replace('"06-cta"', '"05-cta"').replace('data-duration="4.5"', 'data-duration="4.4"').replace('duration: 4.5 }', 'duration: 4.4 }').replace('f06-bg', 'f05-bg')

for cid, (dur, css, body, js, bg) in S.items():
    open(f'compositions/frames/{cid}.html', 'w').write(comp(cid, dur, css, body, js, bg))
open('compositions/frames/05-cta.html', 'w').write(cta)
