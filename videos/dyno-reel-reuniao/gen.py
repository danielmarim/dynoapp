exec(open('/home/claude/videos/_dark/base_dark.py').read())
S = {}
BOLHA = "{ x: 140, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: 'back.out(1.5)' }"
BOT = "{ x: -140, opacity: 0 }, { x: 0, opacity: 1, duration: 0.45, ease: 'back.out(1.4)' }"
TOPO = "tl.fromTo([one('.eb¤'), one('.t¤')], { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: 'power3.out', stagger: 0.1 }, 0.15);"
HEAD = '<div class="ph-head¤"><div class="logo¤" style="width:84px;height:84px;font-size:46px">D</div><div><b>Dyno</b><small>Dyno e Dina · online</small></div></div>'
WHO = '<div class="who¤"><span class="av¤ avdi¤">D</span>Dina <em>agenda</em></div>'
MEET = 'meet.google.com/kzr-pqwd-tmh'

# 1. Hook ------------------------------------------------------------------
S['01-hook'] = (3.4, '''
.brand¤ { position:absolute; left:90px; top:300px; display:flex; align-items:center; gap:22px; font-family:"Bricolage Grotesque"; font-weight:800; font-size:64px; letter-spacing:-.03em; }
.eb¤ { position:absolute; left:90px; top:520px; }
.t¤ { position:absolute; left:90px; right:90px; top:580px; font-size:140px; }
.ico¤ { position:absolute; right:110px; top:280px; width:170px; border-radius:30px; overflow:hidden; background:#F6F4EF; box-shadow:0 30px 80px rgba(0,0,0,.5); text-align:center; font-family:"Bricolage Grotesque"; }
.ico¤ i { display:block; font-style:normal; background:#2FD47E; color:#06261A; font-weight:800; font-size:34px; letter-spacing:.12em; padding:10px 0 6px; }
.ico¤ b { display:block; color:#0D1424; font-weight:800; font-size:96px; line-height:1; padding:12px 0 18px; }
.tags¤ { position:absolute; left:90px; right:90px; top:1180px; display:flex; flex-direction:column; align-items:flex-start; gap:22px; }
.tg¤ { font-size:40px; padding:20px 34px; }
.tg¤.on { background:#2FD47E; color:#04210F; border-color:#2FD47E; }
''', '''  <div § class="brand¤"><div class="logo¤" style="width:96px;height:96px;font-size:54px">D</div>Dyno</div>
  <div § class="ico¤"><i>OUT</i><b>15</b></div>
  <div § class="eb¤">Novo no Dyno</div>
  <div § class="h¤ t¤">Marcou a reunião? <span class="g¤">O link já vem junto.</span></div>
  <div § class="tags¤"><span class="pill¤ tg¤">🗓️ Direto no seu Google Agenda</span><span class="pill¤ tg¤">🎥 Sala do Google Meet criada</span><span class="pill¤ tg¤ on">✉️ Convite por e-mail ou WhatsApp</span></div>''', '''  tl.fromTo(one('.brand¤'), { y: -30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: 'power2.out' }, 0.05);
  tl.fromTo(one('.ico¤'), { y: -200, rotation: -20, opacity: 0 }, { y: 0, rotation: 0, opacity: 1, duration: 0.7, ease: 'bounce.out' }, 0.2);
  tl.fromTo(one('.eb¤'), { y: 20, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4 }, 0.3);
  tl.fromTo(one('.t¤'), { y: 70, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: 'power3.out' }, 0.45);
  tl.fromTo(all('.tg¤'), { x: -60, opacity: 0 }, { x: 0, opacity: 1, duration: 0.45, ease: 'back.out(1.8)', stagger: 0.25 }, 1.3);''', '50% 55%')

# 2. Pedido no WhatsApp + confirmação com link ------------------------------
S['02-pedido'] = (6.2, '''
.eb¤ { position:absolute; left:90px; top:170px; }
.t¤ { position:absolute; left:90px; right:90px; top:220px; font-size:96px; }
.ph¤ { left:110px; right:110px; top:470px; bottom:110px; }
.b¤ { font-size:33px; }
.lk¤ { font-family:"JetBrains Mono"; font-weight:500; font-size:27px; color:#2FD47E; }
.cf¤ b { font-size:35px; }
''', f'''  <div § class="eb¤">Agenda + Google Meet</div>
  <div § class="h¤ t¤">Pede por texto <span class="g¤">ou áudio.</span></div>
  <div § class="phone¤ ph¤">
    {HEAD}
    <div § class="b¤ me¤ m1¤" style="top:150px;width:560px">marca uma reunião amanhã às 15h com a Ana e o Bruno sobre o orçamento<span class="tm¤">10:12</span></div>
    <div § class="b¤ bot¤ d1¤" style="top:380px">{WHO}Marcando a reunião! Já te mando o link da sala. 🎥<span class="tm¤">10:12</span></div>
    <div § class="b¤ bot¤ d2¤ cf¤" style="top:590px">{WHO}🎥 <b>Reunião marcada na sua Google Agenda</b><br><b>Orçamento 2027</b><br>🗓️ qui, 15/10 · 15:00–16:00<br>🔗 Sala do Google Meet:<br><span class="lk¤">{MEET}</span><br><br>Quer que eu envie o convite para <b>Ana e Bruno</b>? <span class="mut¤">e-mail, WhatsApp ou os dois</span><span class="tm¤">10:12</span></div>
  </div>''', f'''  {TOPO}
  tl.fromTo(one('.ph¤'), {{ y: 300, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.6, ease: 'power3.out' }}, 0.25);
  tl.fromTo(one('.m1¤'), {BOLHA}, 0.9);
  tl.fromTo(one('.d1¤'), {BOT}, 2.0);
  tl.fromTo(one('.d2¤'), {BOT}, 3.2);
  tl.fromTo(one('.lk¤'), {{ opacity: 0.2 }}, {{ opacity: 1, duration: 0.5, repeat: 1, yoyo: true }}, 3.8);''', '50% 60%')

# 3. Convite: e-mail + WhatsApp --------------------------------------------
S['03-convite'] = (5.6, '''
.eb¤ { position:absolute; left:90px; top:170px; }
.t¤ { position:absolute; left:90px; right:90px; top:220px; font-size:96px; }
.r¤ { position:absolute; right:90px; top:470px; max-width:70%; font-size:38px; padding:24px 30px 18px; border-radius:34px; font-weight:600; background:#0E3B27; border:2px solid rgba(47,212,126,.25); border-bottom-right-radius:10px; }
.mail¤ { position:absolute; left:90px; right:90px; top:640px; background:#F6F4EF; color:#0D1424; border-radius:34px; padding:34px 40px; box-shadow:0 40px 100px rgba(0,0,0,.5); }
.mh¤ { display:flex; justify-content:space-between; font-size:24px; color:#5b6270; font-weight:600; }
.mail¤ h3 { font-family:"Bricolage Grotesque"; font-weight:800; font-size:48px; letter-spacing:-.02em; margin:14px 0 8px; }
.mail¤ p { font-size:30px; margin:0 0 6px; }
.mb¤ { display:inline-block; margin-top:18px; background:#12A866; color:#fff; font-weight:700; font-size:30px; padding:16px 30px; border-radius:999px; }
.ics¤ { display:inline-flex; align-items:center; gap:10px; margin:18px 0 0 16px; font-family:"JetBrains Mono"; font-size:24px; color:#0B1A3A; border:2px solid #d9d4c7; border-radius:14px; padding:12px 16px; }
.zap¤ { position:absolute; left:90px; right:90px; top:1130px; background:#0F1828; border:2px solid rgba(160,185,225,.14); border-radius:34px; padding:26px 32px; }
.zh¤ { display:flex; align-items:center; gap:14px; font-size:26px; font-weight:700; color:#8C9AB3; margin-bottom:10px; }
.zap¤ .tx¤ { font-size:34px; line-height:1.3; font-weight:600; }
.lk¤ { font-family:"JetBrains Mono"; font-weight:500; font-size:26px; color:#2FD47E; }
.ok¤ { position:absolute; left:90px; right:90px; top:1480px; display:flex; gap:18px; flex-wrap:wrap; }
.ok¤ .pill¤ { font-size:32px; }
''', f'''  <div § class="eb¤">Convite enviado</div>
  <div § class="h¤ t¤">Por e-mail <span class="g¤">ou WhatsApp.</span></div>
  <div § class="r¤">os dois 👍</div>
  <div § class="mail¤"><div class="mh¤"><span>De: Dyno &lt;no-reply@dynoapp.com.br&gt;</span><span>Para: Ana</span></div><h3>Orçamento 2027</h3><p><b>Daniel</b> te convidou para uma reunião.</p><p>quinta-feira, 15 de outubro · 15:00–16:00</p><span class="mb¤">Entrar no Google Meet</span><span class="ics¤">📎 convite.ics</span></div>
  <div § class="zap¤"><div class="zh¤"><span class="av¤ avdy¤" style="width:40px;height:40px;font-size:22px">D</span>Dyno → Bruno</div><div class="tx¤">🗓️ <b>Convite para reunião</b><br>Olá, Bruno! <b>Daniel</b> pediu para eu te enviar o convite: <b>Orçamento 2027</b> · qui, 15/10 · 15:00<br><span class="lk¤">🎥 {MEET}</span></div></div>
  <div § class="ok¤"><span class="pill¤"><span class="dot¤"></span>✉️ Ana: e-mail</span><span class="pill¤"><span class="dot¤"></span>💬 Bruno: WhatsApp</span></div>''', f'''  {TOPO}
  tl.fromTo(one('.r¤'), {BOLHA}, 0.6);
  tl.fromTo(one('.mail¤'), {{ y: 160, rotation: -3, opacity: 0 }}, {{ y: 0, rotation: 0, opacity: 1, duration: 0.6, ease: 'back.out(1.3)' }}, 1.3);
  tl.fromTo(one('.zap¤'), {{ x: -180, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.5, ease: 'back.out(1.4)' }}, 2.6);
  tl.fromTo(all('.ok¤ .pill¤'), {{ y: 30, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.35, stagger: 0.25, ease: 'back.out(1.8)' }}, 3.6);''', '50% 45%')

# 4. Na agenda --------------------------------------------------------------
horas = ['13:00', '14:00', '15:00', '16:00', '17:00']
linhas = ''.join(f'<div class="hr¤" style="top:{i * 200}px"><span>{h}</span></div>' for i, h in enumerate(horas))
S['04-agenda'] = (4.6, '''
.eb¤ { position:absolute; left:90px; top:170px; }
.t¤ { position:absolute; left:90px; right:90px; top:220px; font-size:96px; }
.cal¤ { position:absolute; left:90px; right:90px; top:470px; padding:40px 40px 50px 40px; }
.dia¤ { display:flex; align-items:baseline; gap:18px; margin-bottom:34px; }
.dia¤ b { font-family:"Bricolage Grotesque"; font-weight:800; font-size:64px; }
.dia¤ span { font-size:32px; color:#8C9AB3; font-weight:600; }
.grade¤ { position:relative; height:830px; margin-top:20px; }
.hr¤ { position:absolute; left:0; right:0; border-top:2px solid rgba(160,185,225,.12); }
.hr¤ span { position:absolute; left:0; top:-18px; font-family:"JetBrains Mono"; font-size:24px; color:#8C9AB3; background:#0B1220; padding-right:12px; }
.ev¤ { position:absolute; left:130px; right:10px; top:406px; height:186px; border-radius:26px; background:#0E2A20; border:2px solid rgba(47,212,126,.55); border-left:12px solid #2FD47E; padding:20px 26px; }
.ev¤ b { display:block; font-size:38px; }
.ev¤ small { display:block; font-size:28px; color:#A9B4CA; margin-top:6px; }
.pp¤ { position:absolute; left:130px; right:10px; top:636px; display:flex; gap:16px; flex-wrap:wrap; }
.pp¤ .pill¤ { font-size:28px; padding:12px 22px; }
.av2¤ { width:40px; height:40px; border-radius:50%; display:inline-flex; align-items:center; justify-content:center; font-size:22px; font-weight:700; color:#0A1A33; }
''', f'''  <div § class="eb¤">Tudo no lugar</div>
  <div § class="h¤ t¤">Já está na <span class="g¤">sua agenda.</span></div>
  <div § class="card¤ cal¤">
    <div class="dia¤"><b>Quinta, 15</b><span>outubro</span></div>
    <div class="grade¤">{linhas}
      <div § class="ev¤"><b>Orçamento 2027</b><small>15:00–16:00 · 🎥 Google Meet</small></div>
      <div § class="pp¤"><span class="pill¤"><span class="av2¤" style="background:#F2B544">A</span>Ana ✓ vai</span><span class="pill¤"><span class="av2¤" style="background:#7FB2FF">B</span>Bruno ✓ vai</span></div>
    </div>
  </div>''', f'''  {TOPO}
  tl.fromTo(one('.cal¤'), {{ y: 260, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.6, ease: 'power3.out' }}, 0.25);
  tl.fromTo(one('.ev¤'), {{ scaleY: 0, transformOrigin: '50% 0%', opacity: 0 }}, {{ scaleY: 1, opacity: 1, duration: 0.5, ease: 'back.out(1.6)' }}, 1.0);
  tl.fromTo(all('.pp¤ .pill¤'), {{ x: -40, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.35, stagger: 0.35, ease: 'back.out(1.8)' }}, 1.9);''', '50% 55%')

# 5. CTA ------------------------------------------------------------------
S['05-cta'] = (4.0, '''
.brand¤ { position:absolute; left:90px; top:250px; display:flex; align-items:center; gap:26px; font-family:"Bricolage Grotesque"; font-weight:800; font-size:76px; letter-spacing:-.03em; }
.t¤ { position:absolute; left:90px; right:90px; top:460px; font-size:132px; }
.btnw¤ { position:absolute; left:90px; right:90px; top:1120px; }
.url¤ { position:absolute; left:0; right:0; top:1330px; text-align:center; font-family:"JetBrains Mono"; font-size:40px; color:#2FD47E; }
.pw¤ { position:absolute; left:0; right:0; top:1500px; text-align:center; }
''', '''  <div § class="brand¤"><div class="logo¤" style="width:116px;height:116px;font-size:66px">D</div>Dyno</div>
  <div § class="h¤ t¤">Fala que marca. <span class="g¤">A Dina cuida do convite.</span></div>
  <div § class="btnw¤"><div class="btn¤">Quero testar o Dyno →</div></div>
  <div § class="url¤">dynoapp.com.br</div>
  <div § class="pw¤"><span class="pill¤"><span class="dot¤"></span>Beta · 60 dias grátis</span></div>''', '''  tl.fromTo(one('.brand¤'), { y: -30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: 'power2.out' }, 0.05);
  tl.fromTo(one('.t¤'), { y: 70, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: 'power3.out' }, 0.3);
  tl.fromTo(one('.btnw¤'), { y: 80, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: 'back.out(1.6)' }, 1.0);
  tl.to(one('.btn¤'), { scale: 1.04, duration: 0.3, yoyo: true, repeat: 3, ease: 'sine.inOut' }, 1.7);
  tl.fromTo(one('.url¤'), { opacity: 0 }, { opacity: 1, duration: 0.4 }, 1.4);
  tl.fromTo(one('.pw¤'), { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.4 }, 1.8);''', '50% 40%')

scenes = [('01-hook', 0, 3.4), ('02-pedido', 3.2, 6.2), ('03-convite', 9.2, 5.6), ('04-agenda', 14.6, 4.6), ('05-cta', 19.0, 4.0)]
TOTAL = 23.0
for cid, (dur, css, body, js, glow) in S.items():
    open(f'compositions/frames/{cid}.html', 'w').write(comp(cid, dur, css, body, js, glow))
trans = '''        tl.fromTo("#el-02-pedido", { clipPath: "inset(0% 0% 0% 100%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.4, ease: "power3.inOut" }, 3.2);
        tl.fromTo("#el-03-convite", { clipPath: "inset(100% 0% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.4, ease: "power3.inOut" }, 9.2);
        tl.to("#el-02-pedido", { y: -180, duration: 0.4, ease: "power3.inOut" }, 9.2);
        tl.fromTo("#el-04-agenda", { clipPath: "inset(0% 0% 0% 100%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.4, ease: "power3.inOut" }, 14.6);
        tl.fromTo("#el-05-cta", { clipPath: "circle(0% at 50% 50%)" }, { clipPath: "circle(90% at 50% 50%)", duration: 0.45, ease: "power3.inOut" }, 19.0);'''
open('index.html', 'w').write(index('reuniao', TOTAL, scenes, trans))

# Efeitos sonoros ----------------------------------------------------------
exec(open('/home/claude/videos/_dark/sfx_base.py').read())
EV = [(0.3, pop, 0.7), (0.5, thump, 0.8)] + [(1.35 + k * 0.25, pop, 0.7) for k in range(3)]
EV += [(3.2, sent, 0.8), (4.1, sent, 0.9), (5.2, ping, 1.0), (6.4, ping, 1.1)]
EV += [(9.2, thump, 0.8), (9.8, sent, 0.9), (10.5, pop, 0.9), (11.8, ping, 1.0), (12.8, pop, 0.7), (13.05, pop, 0.7)]
EV += [(14.6, sent, 0.8), (15.6, thump, 0.9), (16.5, ping, 0.9), (16.85, ping, 0.9)]
EV += [(19.0, sent, 0.8), (20.0, thump, 1.0), (22.2, ping, 0.7)]
out = np.zeros(int(SR * TOTAL))
for t0, fn, g in EV:
    s = fn() * g; i = int(t0 * SR)
    if i < len(out): out[i:i + len(s)] += s[:len(out) - i]
out = np.clip(out * 0.7, -1, 1)
w = wave.open('assets/sfx/sfx-mix.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((out * 32767).astype(np.int16).tobytes()); w.close()
