exec(open('/home/claude/videos/_dark/base_dark.py').read())
S = {}
S['01-hook'] = (4.4, '''
.eb¤ { position:absolute; left:90px; top:420px; }
.t¤ { position:absolute; left:90px; right:90px; top:480px; font-size:150px; }
.s¤ { position:absolute; left:90px; right:90px; top:1180px; font-family:"Bricolage Grotesque"; font-weight:700; font-size:72px; letter-spacing:-.03em; line-height:1.05; color:#A9B4CA; }
.bell¤ { position:absolute; right:110px; top:1500px; width:190px; height:190px; border-radius:50%; background:rgba(242,181,68,.14); border:3px solid rgba(242,181,68,.5); display:flex; align-items:center; justify-content:center; font-size:100px; }
''', '''  <div § class="eb¤">Novo no Dyno</div>
  <div § class="h¤ t¤"><span class="l1¤" style="display:block;white-space:nowrap">Você lembra.</span><span class="l2¤ g¤" style="display:block;white-space:nowrap">Ela esquece.</span></div>
  <div § class="s¤">E se o Dyno lembrasse <span class="g¤">por você?</span></div>
  <div § class="bell¤">🔔</div>''', '''  tl.fromTo(one('.eb¤'), { y: 20, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4 }, 0.1);
  tl.fromTo(one('.l1¤'), { y: 60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.55, ease: 'power3.out' }, 0.25);
  tl.fromTo(one('.l2¤'), { y: 60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.55, ease: 'power3.out' }, 0.95);
  tl.fromTo(one('.s¤'), { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: 'power2.out' }, 1.9);
  tl.fromTo(one('.bell¤'), { scale: 0 }, { scale: 1, duration: 0.5, ease: 'back.out(2.2)' }, 2.4);
  tl.to(one('.bell¤'), { rotation: 14, duration: 0.08, yoyo: true, repeat: 7, ease: 'sine.inOut' }, 2.9);''', '50% 75%')

S['02-pede'] = (6.0, '''
.eb¤ { position:absolute; left:90px; top:180px; }
.t¤ { position:absolute; left:90px; right:90px; top:230px; font-size:100px; }
.ph¤ { left:110px; right:110px; top:560px; bottom:240px; }
.ok¤ { position:absolute; left:0; right:0; bottom:120px; text-align:center; }
''', '''  <div § class="eb¤">WhatsApp do Pedro · 14:20</div>
  <div § class="h¤ t¤">É só <span class="g¤">pedir.</span></div>
  <div § class="phone¤ ph¤">
    <div class="ph-head¤"><div class="logo¤" style="width:84px;height:84px;font-size:46px">D</div><div><b>Dyno</b><small>conta verificada</small></div></div>
    <div § class="b¤ me¤ m1¤" style="top:200px">Dyno, lembra a Ana de passar no mercado às 18h<span class="tm¤">14:20</span></div>
    <div § class="b¤ bot¤ d1¤" style="top:470px"><div class="who¤"><span class="av¤ avdi¤">D</span>Dina <em>agenda</em></div>Combinado! Às <b class="g¤">18h</b> eu aviso a Ana. 🔔<span class="tm¤">14:20</span></div>
  </div>
  <div § class="ok¤"><span class="pill¤ okp¤"><span class="dot¤"></span>Lembrete criado para a Ana</span></div>''', '''  tl.fromTo([one('.eb¤'), one('.t¤')], { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: 'power3.out', stagger: 0.1 }, 0.2);
  tl.fromTo(one('.ph¤'), { y: 300, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: 'power3.out' }, 0.3);
  tl.fromTo(one('.m1¤'), { x: 140, opacity: 0 }, { x: 0, opacity: 1, duration: 0.45, ease: 'back.out(1.5)' }, 1.1);
  tl.fromTo(one('.d1¤'), { x: -140, opacity: 0 }, { x: 0, opacity: 1, duration: 0.45, ease: 'back.out(1.5)' }, 2.5);
  tl.fromTo(one('.okp¤'), { scale: 0, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.45, ease: 'back.out(2.2)' }, 3.6);''', '50% 60%')

S['03-relogio'] = (3.0, '''
.wrap¤ { position:absolute; left:0; right:0; top:620px; text-align:center; }
.clk¤ { font-family:"Bricolage Grotesque"; font-weight:800; font-size:300px; letter-spacing:-.04em; line-height:1; font-variant-numeric:tabular-nums; }
.ring¤ { position:absolute; left:50%; top:760px; width:760px; height:760px; margin-left:-380px; margin-top:-380px; border-radius:50%; border:4px solid rgba(47,212,126,.5); }
.cap¤ { margin-top:70px; }
''', '''  <div § class="ring¤"></div>
  <div § class="wrap¤"><div class="clk¤"><span class="c1¤">17:59</span></div><div class="eb¤ cap¤">mais tarde…</div></div>''', '''  const c = one('.c1¤'), o = { v: 0 };
  tl.fromTo(one('.wrap¤'), { scale: 0.8, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.45, ease: 'power3.out' }, 0.05);
  tl.fromTo(o, { v: 0 }, { v: 1, duration: 1.2, ease: 'steps(1)', onUpdate: () => { const on = o.v >= 1; c.textContent = on ? '18:00' : '17:59'; c.style.color = on ? '#2FD47E' : '#E9EEF7'; } }, 0.3);
  tl.fromTo(one('.ring¤'), { scale: 0.4, opacity: 1 }, { scale: 1.3, opacity: 0, duration: 1.0, ease: 'power2.out' }, 1.5);
  tl.fromTo(one('.clk¤'), { scale: 1 }, { scale: 1.08, duration: 0.18, yoyo: true, repeat: 1 }, 1.5);''', '50% 40%')

S['04-recebe'] = (6.4, '''
.eb¤ { position:absolute; left:90px; top:180px; }
.t¤ { position:absolute; left:90px; right:90px; top:230px; font-size:100px; }
.ph¤ { left:110px; right:110px; top:560px; bottom:240px; }
.nt¤ { position:absolute; left:130px; right:130px; top:470px; z-index:5; background:rgba(20,32,54,.96); border:2px solid rgba(160,185,225,.22); border-radius:36px; padding:24px 28px; box-shadow:0 30px 80px rgba(0,0,0,.6); display:flex; gap:20px; align-items:center; }
.nt¤ b { display:block; font-size:28px; } .nt¤ span { display:block; font-size:30px; color:#A9B4CA; }
.cf¤ { position:absolute; left:0; right:0; bottom:120px; text-align:center; }
''', '''  <div § class="eb¤">WhatsApp da Ana · 18:00</div>
  <div § class="h¤ t¤">E chega <span class="g¤">para ela.</span></div>
  <div § class="phone¤ ph¤">
    <div class="ph-head¤"><div class="logo¤" style="width:84px;height:84px;font-size:46px">D</div><div><b>Dyno</b><small>conta verificada</small></div></div>
    <div § class="b¤ bot¤ d1¤" style="top:200px"><div class="who¤"><span class="av¤ avdi¤">D</span>Dina <em>agenda</em></div>🔔 <b>Pedro</b> pediu para te lembrar: <b class="g¤">passar no mercado</b>.<span class="tm¤">18:00</span></div>
    <div § class="b¤ me¤ m1¤" style="top:520px">ok, passo agora ✅<span class="tm¤">18:03</span></div>
    <div § class="b¤ bot¤ d2¤" style="top:680px"><div class="who¤"><span class="av¤ avdi¤">D</span>Dina <em>agenda</em></div>Feito! Lembrete concluído. 💚<span class="tm¤">18:03</span></div>
  </div>
  <div § class="nt¤"><div class="logo¤" style="width:72px;height:72px;font-size:40px">D</div><div><b>Dyno · agora</b><span>🔔 Pedro pediu para te lembrar…</span></div></div>
  <div § class="cf¤"><span class="pill¤ okp¤"><span class="dot¤"></span>Quem recebe é quem confirma</span></div>''', '''  tl.fromTo([one('.eb¤'), one('.t¤')], { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: 'power3.out', stagger: 0.1 }, 0.2);
  tl.fromTo(one('.ph¤'), { y: 300, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: 'power3.out' }, 0.3);
  tl.fromTo(one('.nt¤'), { y: -260, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: 'back.out(1.4)' }, 0.9);
  tl.to(one('.nt¤'), { y: -260, opacity: 0, duration: 0.4, ease: 'power2.in' }, 2.0);
  tl.fromTo(one('.d1¤'), { x: -140, opacity: 0 }, { x: 0, opacity: 1, duration: 0.45, ease: 'back.out(1.5)' }, 2.2);
  tl.fromTo(one('.m1¤'), { x: 140, opacity: 0 }, { x: 0, opacity: 1, duration: 0.45, ease: 'back.out(1.5)' }, 3.4);
  tl.fromTo(one('.d2¤'), { x: -140, opacity: 0 }, { x: 0, opacity: 1, duration: 0.45, ease: 'back.out(1.5)' }, 4.3);
  tl.fromTo(one('.okp¤'), { scale: 0, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.45, ease: 'back.out(2.2)' }, 4.9);''', '50% 60%')

S['05-cta'] = (5.0, '''
.brand¤ { position:absolute; left:90px; top:230px; display:flex; align-items:center; gap:26px; font-family:"Bricolage Grotesque"; font-weight:800; font-size:76px; letter-spacing:-.03em; }
.t¤ { position:absolute; left:90px; right:90px; top:430px; font-size:128px; }
.s¤ { position:absolute; left:90px; right:90px; top:960px; font-size:44px; line-height:1.32; color:#A9B4CA; }
.s¤ b { color:#E9EEF7; }
.say¤ { position:absolute; left:90px; right:90px; top:1180px; padding:34px 40px; font-size:42px; font-weight:600; line-height:1.3; }
.say¤ small { display:block; font-family:"JetBrains Mono"; font-size:24px; letter-spacing:.12em; text-transform:uppercase; color:#8C9AB3; margin-bottom:10px; }
.url¤ { position:absolute; left:0; right:0; top:1520px; text-align:center; font-family:"JetBrains Mono"; font-size:40px; color:#2FD47E; }
''', '''  <div § class="brand¤"><div class="logo¤" style="width:116px;height:116px;font-size:66px">D</div>Dyno</div>
  <div § class="h¤ t¤">Lembre <span class="g¤">quem você ama</span> de tudo.</div>
  <div § class="s¤">Funciona entre as pessoas do seu grupo: <b>Modo família, no plano Premium.</b></div>
  <div § class="card¤ say¤"><small>É só dizer</small>“Dyno, lembra a … de …”</div>
  <div § class="url¤">dynoapp.com.br</div>''', '''  tl.fromTo(one('.brand¤'), { y: -30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: 'power2.out' }, 0.05);
  tl.fromTo(one('.t¤'), { y: 70, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: 'power3.out' }, 0.3);
  tl.fromTo(one('.s¤'), { opacity: 0 }, { opacity: 1, duration: 0.4 }, 1.0);
  tl.fromTo(one('.say¤'), { y: 80, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: 'back.out(1.6)' }, 1.4);
  tl.to(one('.say¤'), { scale: 1.03, duration: 0.3, yoyo: true, repeat: 3, ease: 'sine.inOut' }, 2.1);
  tl.fromTo(one('.url¤'), { opacity: 0 }, { opacity: 1, duration: 0.4 }, 1.8);''', '50% 40%')

scenes = [('01-hook', 0, 4.4), ('02-pede', 4.1, 6.0), ('03-relogio', 9.8, 3.0), ('04-recebe', 12.5, 6.4), ('05-cta', 18.6, 5.0)]
TOTAL = 23.6
for cid, (dur, css, body, js, glow) in S.items():
    open(f'compositions/frames/{cid}.html', 'w').write(comp(cid, dur, css, body, js, glow))
trans = '''        tl.fromTo("#el-02-pede", { clipPath: "inset(0% 0% 100% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.4, ease: "power3.inOut" }, 4.1);
        tl.fromTo("#el-03-relogio", { clipPath: "circle(0% at 50% 40%)" }, { clipPath: "circle(80% at 50% 40%)", duration: 0.45, ease: "power3.inOut" }, 9.8);
        tl.fromTo("#el-04-recebe", { clipPath: "inset(0% 0% 0% 100%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.4, ease: "power3.inOut" }, 12.5);
        tl.fromTo("#el-05-cta", { clipPath: "circle(0% at 50% 50%)" }, { clipPath: "circle(80% at 50% 50%)", duration: 0.45, ease: "power3.inOut" }, 18.6);'''
open('index.html', 'w').write(index('lembrar', TOTAL, scenes, trans))
