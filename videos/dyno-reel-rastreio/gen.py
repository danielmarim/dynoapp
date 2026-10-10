exec(open('/home/claude/videos/_dark/base_dark.py').read())
S = {}
BOLHA = "{ x: 140, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: 'back.out(1.5)' }"
BOT = "{ x: -140, opacity: 0 }, { x: 0, opacity: 1, duration: 0.45, ease: 'back.out(1.4)' }"
TOPO = "tl.fromTo([one('.eb¤'), one('.t¤')], { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: 'power3.out', stagger: 0.1 }, 0.15);"
HEAD = '<div class="ph-head¤"><div class="logo¤" style="width:84px;height:84px;font-size:46px">D</div><div><b>Dyno</b><small>Dyno e Dina · online</small></div></div>'

# 1. Hook ------------------------------------------------------------------
S['01-hook'] = (3.4, '''
.brand¤ { position:absolute; left:90px; top:300px; display:flex; align-items:center; gap:22px; font-family:"Bricolage Grotesque"; font-weight:800; font-size:64px; letter-spacing:-.03em; }
.eb¤ { position:absolute; left:90px; top:520px; }
.t¤ { position:absolute; left:90px; right:90px; top:580px; font-size:148px; }
.box¤ { position:absolute; right:110px; top:330px; font-size:120px; }
.tags¤ { position:absolute; left:90px; right:90px; top:1160px; display:flex; flex-direction:column; align-items:flex-start; gap:22px; }
.tg¤ { font-size:40px; padding:20px 34px; }
.tg¤.on { background:#2FD47E; color:#04210F; border-color:#2FD47E; }
''', '''  <div § class="brand¤"><div class="logo¤" style="width:96px;height:96px;font-size:54px">D</div>Dyno</div>
  <div § class="box¤">📦</div>
  <div § class="eb¤">Novo no Dyno</div>
  <div § class="h¤ t¤">Cadê minha <span class="g¤">encomenda?</span></div>
  <div § class="tags¤"><span class="pill¤ tg¤">📸 Manda o código ou o print</span><span class="pill¤ tg¤">🔔 A Dina avisa cada mudança</span><span class="pill¤ tg¤ on">✅ Até chegar na sua porta</span></div>''', '''  tl.fromTo(one('.brand¤'), { y: -30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: 'power2.out' }, 0.05);
  tl.fromTo(one('.box¤'), { y: -200, rotation: -25, opacity: 0 }, { y: 0, rotation: 0, opacity: 1, duration: 0.7, ease: 'bounce.out' }, 0.2);
  tl.fromTo(one('.eb¤'), { y: 20, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4 }, 0.3);
  tl.fromTo(one('.t¤'), { y: 70, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: 'power3.out' }, 0.45);
  tl.fromTo(all('.tg¤'), { x: -60, opacity: 0 }, { x: 0, opacity: 1, duration: 0.45, ease: 'back.out(1.8)', stagger: 0.25 }, 1.3);''', '50% 55%')

# 2. Print com códigos ----------------------------------------------------
S['02-print'] = (6.2, '''
.eb¤ { position:absolute; left:90px; top:170px; }
.t¤ { position:absolute; left:90px; right:90px; top:220px; font-size:96px; }
.ph¤ { left:110px; right:110px; top:470px; bottom:110px; }
.b¤ { font-size:32px; }
.shot¤ { background:#1A1F2B; border-radius:22px; padding:16px 18px; margin-bottom:12px; display:flex; flex-direction:column; gap:10px; }
.sms¤ { background:#2A3142; border-radius:18px; padding:12px 16px; font-size:24px; line-height:1.3; color:#D5DCEA; font-weight:500; }
.sms¤ b { font-family:"JetBrains Mono"; font-weight:500; color:#fff; }
.cod¤ { font-family:"JetBrains Mono"; font-weight:500; font-size:30px; color:#2FD47E; }
''', f'''  <div § class="eb¤">Rastreio de encomendas</div>
  <div § class="h¤ t¤">Manda o código <span class="g¤">ou o print.</span></div>
  <div § class="phone¤ ph¤">
    {HEAD}
    <div § class="b¤ me¤ m1¤" style="top:150px;width:470px"><div class="shot¤"><div class="sms¤">Seu código de rastreamento é <b>NB482913657BR</b></div><div class="sms¤">Seu código de rastreamento é <b>QP705218344BR</b></div><div class="sms¤">Seu código de rastreamento é <b>LX339046812BR</b></div></div>meus rastreios 👆<span class="tm¤">09:19</span></div>
    <div § class="b¤ bot¤ d1¤" style="top:590px"><div class="who¤"><span class="av¤ avdi¤">D</span>Dina <em>rotina</em></div>📦 Achei 3 códigos e já estou acompanhando:<br><span class="cod¤">NB482913657BR<br>QP705218344BR<br>LX339046812BR</span><br>Guardo numa lista <b>Rastreios</b>?<span class="tm¤">09:19</span></div>
    <div § class="b¤ me¤ m2¤" style="top:965px">Sim 👍<span class="tm¤">09:20</span></div>
    <div § class="b¤ bot¤ d2¤" style="top:1075px"><div class="who¤"><span class="av¤ avdi¤">D</span>Dina</div>📝 Lista criada. O 1º status chega em minutos.<span class="tm¤">09:20</span></div>
  </div>''', f'''  {TOPO}
  tl.fromTo(one('.ph¤'), {{ y: 300, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.6, ease: 'power3.out' }}, 0.25);
  tl.fromTo(one('.m1¤'), {BOLHA}, 0.9);
  tl.fromTo(one('.d1¤'), {BOT}, 2.1);
  tl.fromTo(all('.cod¤'), {{ opacity: 0.2 }}, {{ opacity: 1, duration: 0.5 }}, 2.4);
  tl.fromTo(one('.m2¤'), {BOLHA}, 4.2);
  tl.fromTo(one('.d2¤'), {BOT}, 4.9);''', '50% 60%')

# 3. Avisos de status ------------------------------------------------------
etapas = [('📝', 'Postagem informada', 'seg 09:12', ''), ('🚚', 'Em trânsito', 'ter 14:40', 'Curitiba/PR'),
          ('🛵', 'Saiu para entrega', 'qua 08:05', 'São Paulo/SP'), ('✅', 'Entregue!', 'qua 13:22', 'São Paulo/SP')]
cards = ''.join(f'''<div § class="nt¤ n¤{i}" style="top:{560 + i * 270}px"><div class="nh¤"><span class="av¤ avdi¤" style="width:40px;height:40px;font-size:22px">D</span>Dina · <span class="mut¤">{q}</span></div><div class="nb¤">📦 Tênis · NB482913657BR</div><div class="ns¤">{e} <b>{s}</b>{(' — ' + l) if l else ''}</div></div>
  <div § class="pt¤ p¤{i}" style="top:{640 + i * 270}px"></div>''' for i, (e, s, q, l) in enumerate(etapas))
S['03-status'] = (5.6, '''
.eb¤ { position:absolute; left:90px; top:170px; }
.t¤ { position:absolute; left:90px; right:90px; top:220px; font-size:96px; }
.trilho¤ { position:absolute; left:126px; top:600px; width:8px; height:820px; border-radius:4px; background:rgba(160,185,225,.14); overflow:hidden; }
.trilho¤ i { display:block; width:100%; height:0; background:#2FD47E; }
.pt¤ { position:absolute; left:110px; width:40px; height:40px; border-radius:50%; background:#0B1220; border:6px solid rgba(160,185,225,.3); }
.nt¤ { position:absolute; left:190px; right:90px; background:#0F1828; border:2px solid rgba(160,185,225,.14); border-radius:30px; padding:22px 30px; }
.nh¤ { display:flex; align-items:center; gap:12px; font-size:26px; font-weight:700; margin-bottom:6px; }
.nb¤ { font-size:28px; color:#A9B4CA; font-weight:600; }
.ns¤ { font-size:38px; font-weight:600; margin-top:6px; }
.n¤3 { border-color:rgba(47,212,126,.5); background:#0E2A20; }
''', f'''  <div § class="eb¤">Avisos automáticos</div>
  <div § class="h¤ t¤">Ela avisa a cada <span class="g¤">mudança.</span></div>
  <div § class="trilho¤"><i class="fill¤"></i></div>
  {cards}''', f'''  {TOPO}
  tl.to(one('.fill¤'), {{ height: '100%', duration: 3.6, ease: 'none' }}, 0.8);
  [0, 1, 2, 3].forEach(function (i) {{
    var t = 0.8 + i * 1.15;
    tl.fromTo(one('.n¤' + i), {{ x: 160, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.45, ease: 'back.out(1.4)' }}, t);
    tl.to(one('.p¤' + i), {{ backgroundColor: '#2FD47E', borderColor: '#2FD47E', scale: 1.15, duration: 0.25 }}, t + 0.1);
  }});''', '50% 50%')

# 4. Cadê minha encomenda? ------------------------------------------------
S['04-cade'] = (4.6, '''
.eb¤ { position:absolute; left:90px; top:170px; }
.t¤ { position:absolute; left:90px; right:90px; top:220px; font-size:96px; }
.ph¤ { left:110px; right:110px; top:470px; bottom:110px; }
.b¤ { font-size:38px; }
.li¤ { display:block; margin-top:10px; }
''', f'''  <div § class="eb¤">A qualquer hora</div>
  <div § class="h¤ t¤">Perguntou? <span class="g¤">Ela responde.</span></div>
  <div § class="phone¤ ph¤">
    {HEAD}
    <div § class="b¤ me¤ m1¤" style="top:170px">cadê minhas encomendas?<span class="tm¤">10:31</span></div>
    <div § class="b¤ bot¤ d1¤" style="top:330px"><div class="who¤"><span class="av¤ avdi¤">D</span>Dina <em>rotina</em></div><span class="li¤">📦 <b>Tênis:</b> 🛵 saiu para entrega hoje, 08:05</span><span class="li¤">📦 <b>Fone:</b> 🚚 em trânsito, Curitiba/PR</span><span class="li¤">📦 <b>Livro:</b> 📝 postagem informada</span><span class="li¤ mut¤" style="font-size:28px">Eu aviso quando mudar. 😉</span><span class="tm¤">10:31</span></div>
  </div>''', f'''  {TOPO}
  tl.fromTo(one('.ph¤'), {{ y: 300, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.6, ease: 'power3.out' }}, 0.25);
  tl.fromTo(one('.m1¤'), {BOLHA}, 0.9);
  tl.fromTo(one('.d1¤'), {BOT}, 1.8);
  tl.fromTo(all('.li¤'), {{ x: -30, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.3, stagger: 0.3 }}, 2.1);''', '50% 60%')

# 5. CTA ------------------------------------------------------------------
S['05-cta'] = (4.0, '''
.brand¤ { position:absolute; left:90px; top:250px; display:flex; align-items:center; gap:26px; font-family:"Bricolage Grotesque"; font-weight:800; font-size:76px; letter-spacing:-.03em; }
.t¤ { position:absolute; left:90px; right:90px; top:460px; font-size:132px; }
.btnw¤ { position:absolute; left:90px; right:90px; top:1120px; }
.url¤ { position:absolute; left:0; right:0; top:1330px; text-align:center; font-family:"JetBrains Mono"; font-size:40px; color:#2FD47E; }
.pw¤ { position:absolute; left:0; right:0; top:1500px; text-align:center; }
''', '''  <div § class="brand¤"><div class="logo¤" style="width:116px;height:116px;font-size:66px">D</div>Dyno</div>
  <div § class="h¤ t¤">Manda o código. <span class="g¤">A Dina cuida do resto.</span></div>
  <div § class="btnw¤"><div class="btn¤">Quero testar o Dyno →</div></div>
  <div § class="url¤">dynoapp.com.br</div>
  <div § class="pw¤"><span class="pill¤"><span class="dot¤"></span>Beta · 60 dias grátis</span></div>''', '''  tl.fromTo(one('.brand¤'), { y: -30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: 'power2.out' }, 0.05);
  tl.fromTo(one('.t¤'), { y: 70, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: 'power3.out' }, 0.3);
  tl.fromTo(one('.btnw¤'), { y: 80, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: 'back.out(1.6)' }, 1.0);
  tl.to(one('.btn¤'), { scale: 1.04, duration: 0.3, yoyo: true, repeat: 3, ease: 'sine.inOut' }, 1.7);
  tl.fromTo(one('.url¤'), { opacity: 0 }, { opacity: 1, duration: 0.4 }, 1.4);
  tl.fromTo(one('.pw¤'), { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.4 }, 1.8);''', '50% 40%')

scenes = [('01-hook', 0, 3.4), ('02-print', 3.2, 6.2), ('03-status', 9.2, 5.6), ('04-cade', 14.6, 4.6), ('05-cta', 19.0, 4.0)]
TOTAL = 23.0
for cid, (dur, css, body, js, glow) in S.items():
    open(f'compositions/frames/{cid}.html', 'w').write(comp(cid, dur, css, body, js, glow))
trans = '''        tl.fromTo("#el-02-print", { clipPath: "inset(0% 0% 0% 100%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.4, ease: "power3.inOut" }, 3.2);
        tl.fromTo("#el-03-status", { clipPath: "inset(100% 0% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.4, ease: "power3.inOut" }, 9.2);
        tl.to("#el-02-print", { y: -180, duration: 0.4, ease: "power3.inOut" }, 9.2);
        tl.fromTo("#el-04-cade", { clipPath: "inset(0% 0% 0% 100%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.4, ease: "power3.inOut" }, 14.6);
        tl.fromTo("#el-05-cta", { clipPath: "circle(0% at 50% 50%)" }, { clipPath: "circle(90% at 50% 50%)", duration: 0.45, ease: "power3.inOut" }, 19.0);'''
open('index.html', 'w').write(index('rastreio', TOTAL, scenes, trans))

# Efeitos sonoros ----------------------------------------------------------
exec(open('/home/claude/videos/_dark/sfx_base.py').read())
EV = [(0.3, pop, 0.7), (0.5, thump, 0.8)] + [(1.35 + k * 0.25, pop, 0.7) for k in range(3)]
EV += [(3.2, sent, 0.8), (4.1, sent, 0.9), (5.3, ping, 1.0), (7.4, sent, 0.9), (8.1, ping, 1.0)]
EV += [(9.2, thump, 0.8)] + [(10.0 + k * 1.15, ping, 1.0 if k < 3 else 1.2) for k in range(4)]
EV += [(14.6, sent, 0.8), (15.5, sent, 0.9), (16.4, ping, 1.0)]
EV += [(19.0, sent, 0.8), (20.0, thump, 1.0), (22.2, ping, 0.7)]
out = np.zeros(int(SR * TOTAL))
for t0, fn, g in EV:
    s = fn() * g; i = int(t0 * SR)
    if i < len(out): out[i:i + len(s)] += s[:len(out) - i]
out = np.clip(out * 0.7, -1, 1)
w = wave.open('assets/sfx/sfx-mix.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((out * 32767).astype(np.int16).tobytes()); w.close()
