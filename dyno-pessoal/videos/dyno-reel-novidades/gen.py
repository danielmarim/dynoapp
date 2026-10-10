exec(open('/home/claude/videos/_dark/base_dark.py').read())
S = {}

# 1. Hook ------------------------------------------------------------------
S['01-hook'] = (3.6, '''
.brand¤ { position:absolute; left:90px; top:300px; display:flex; align-items:center; gap:22px; font-family:"Bricolage Grotesque"; font-weight:800; font-size:64px; letter-spacing:-.03em; }
.eb¤ { position:absolute; left:90px; top:520px; }
.t¤ { position:absolute; left:90px; right:90px; top:580px; font-size:168px; }
.tags¤ { position:absolute; left:90px; right:90px; top:1150px; display:flex; flex-wrap:wrap; gap:20px; }
.tg¤ { font-size:36px; padding:18px 30px; }
.tg¤.on { background:#2FD47E; color:#04210F; border-color:#2FD47E; }
''', '''  <div § class="brand¤"><div class="logo¤" style="width:96px;height:96px;font-size:54px">D</div>Dyno</div>
  <div § class="eb¤">Novidades de outubro</div>
  <div § class="h¤ t¤"><span class="g¤">5 coisas novas</span> no seu Dyno.</div>
  <div § class="tags¤"><span class="pill¤ tg¤">💊 Remédio</span><span class="pill¤ tg¤">💳 Fatura com parcelas</span><span class="pill¤ tg¤">🔎 Gasto fora do normal</span><span class="pill¤ tg¤">🎭 Personalidades</span><span class="pill¤ tg¤ on">🔊 Voz no mesmo tom</span></div>''', '''  tl.fromTo(one('.brand¤'), { y: -30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: 'power2.out' }, 0.05);
  tl.fromTo(one('.eb¤'), { y: 20, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4 }, 0.3);
  tl.fromTo(one('.t¤'), { y: 70, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: 'power3.out' }, 0.45);
  tl.fromTo(all('.tg¤'), { y: 40, opacity: 0, scale: 0.8 }, { y: 0, opacity: 1, scale: 1, duration: 0.45, ease: 'back.out(2)', stagger: 0.16 }, 1.3);''', '50% 55%')

# 2. Remédio com confirmação ----------------------------------------------
S['02-remedio'] = (5.8, '''
.eb¤ { position:absolute; left:90px; top:170px; }
.t¤ { position:absolute; left:90px; right:90px; top:220px; font-size:96px; }
.ph¤ { left:110px; right:110px; top:470px; bottom:120px; }
.b¤ { font-size:34px; }
''', '''  <div § class="eb¤">Novo · 1 de 5</div>
  <div § class="h¤ t¤">Remédio com <span class="g¤">confirmação.</span></div>
  <div § class="phone¤ ph¤">
    <div class="ph-head¤"><div class="logo¤" style="width:84px;height:84px;font-size:46px">D</div><div><b>Dyno</b><small>Dyno e Dina · online</small></div></div>
    <div § class="b¤ me¤ m1¤" style="top:170px">me lembra de tomar Losartana 50 mg todo dia às 8h<span class="tm¤">21:58</span></div>
    <div § class="b¤ bot¤ d1¤" style="top:360px"><div class="who¤"><span class="av¤ avdi¤">D</span>Dina <em>rotina</em></div>Combinado! 💊 Todo dia às <b class="g¤">8h</b> eu te lembro.<span class="tm¤">21:58</span></div>
    <div § class="b¤ bot¤ d2¤" style="top:560px"><div class="who¤"><span class="av¤ avdi¤">D</span>Dina <em>08:00</em></div>💊 <b>Hora do remédio, Ana:</b> Losartana 50 mg.<br>Já tomou? Responda <b class="g¤">sim</b>.<span class="tm¤">08:00</span></div>
    <div § class="b¤ me¤ m2¤" style="top:830px">Sim ✅<span class="tm¤">08:03</span></div>
    <div § class="b¤ bot¤ d3¤" style="top:960px"><div class="who¤"><span class="av¤ avdi¤">D</span>Dina</div>Registrado! Até amanhã. 💚<span class="tm¤">08:03</span></div>
  </div>''', '''  tl.fromTo([one('.eb¤'), one('.t¤')], { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: 'power3.out', stagger: 0.1 }, 0.15);
  tl.fromTo(one('.ph¤'), { y: 300, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: 'power3.out' }, 0.25);
  tl.fromTo(one('.m1¤'), { x: 140, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: 'back.out(1.5)' }, 0.9);
  tl.fromTo(one('.d1¤'), { x: -140, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: 'back.out(1.5)' }, 1.8);
  tl.fromTo(one('.d2¤'), { x: -140, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: 'back.out(1.5)' }, 2.8);
  tl.fromTo(one('.m2¤'), { x: 140, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: 'back.out(1.5)' }, 4.0);
  tl.fromTo(one('.d3¤'), { x: -140, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: 'back.out(1.5)' }, 4.7);''', '50% 60%')

# 3. Fatura com parcelas --------------------------------------------------
S['03-fatura'] = (5.6, '''
.eb¤ { position:absolute; left:90px; top:170px; }
.t¤ { position:absolute; left:90px; right:90px; top:220px; font-size:96px; }
.ph¤ { left:110px; right:110px; top:470px; bottom:120px; }
.b¤ { font-size:32px; }
.doc¤ { display:flex; align-items:center; gap:16px; background:rgba(47,212,126,.12); border:2px solid rgba(47,212,126,.35); border-radius:20px; padding:14px 18px; margin-bottom:10px; font-size:30px; }
.doc¤ i { font-style:normal; font-size:40px; }
.res¤ { max-width:88%; }
.res¤ p { margin:0; }
.res¤ .ln { color:#A9B4CA; font-weight:500; }
.res¤ .pc { margin-top:10px; padding-top:10px; border-top:2px solid rgba(160,185,225,.14); }
''', '''  <div § class="eb¤">Novo · 2 de 5</div>
  <div § class="h¤ t¤">Fatura do cartão, <span class="g¤">com parcelas.</span></div>
  <div § class="phone¤ ph¤">
    <div class="ph-head¤"><div class="logo¤" style="width:84px;height:84px;font-size:46px">D</div><div><b>Dyno</b><small>Dyno e Dina · online</small></div></div>
    <div § class="b¤ me¤ m1¤" style="top:170px"><div class="doc¤"><i>📎</i>fatura-outubro.pdf</div>fatura do cartão<span class="tm¤">19:37</span></div>
    <div § class="b¤ bot¤ res¤ d1¤" style="top:420px"><div class="who¤"><span class="av¤ avdy¤">D</span>Dyno <em>finanças</em></div><p>📄 <b>Fatura do cartão</b> (31/08 a 29/09)</p><p class="ln">Encontrei <b>23 lançamentos</b>: 20 novos, 3 já estavam no Dyno.</p><p class="pc"><b class="g¤">Parceladas:</b> 3 compras, R$ 350,00 nesta fatura. Ainda faltam <b>R$ 600,00</b> nas próximas.</p><p class="ln" style="margin-top:10px">Responda <b>IMPORTAR</b> para salvar os 20 novos.</p><span class="tm¤">19:38</span></div>
    <div § class="b¤ me¤ m2¤" style="top:930px">IMPORTAR<span class="tm¤">19:38</span></div>
    <div § class="b¤ bot¤ d2¤" style="top:1045px"><div class="who¤"><span class="av¤ avdy¤">D</span>Dyno</div>✅ 20 salvos, sem duplicar.<span class="tm¤">19:38</span></div>
  </div>''', '''  tl.fromTo([one('.eb¤'), one('.t¤')], { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: 'power3.out', stagger: 0.1 }, 0.15);
  tl.fromTo(one('.ph¤'), { y: 300, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: 'power3.out' }, 0.25);
  tl.fromTo(one('.m1¤'), { x: 140, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: 'back.out(1.5)' }, 0.9);
  tl.fromTo(one('.d1¤'), { x: -140, opacity: 0 }, { x: 0, opacity: 1, duration: 0.45, ease: 'back.out(1.4)' }, 1.9);
  tl.fromTo(one('.m2¤'), { x: 140, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: 'back.out(1.5)' }, 3.9);
  tl.fromTo(one('.d2¤'), { x: -140, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: 'back.out(1.5)' }, 4.6);''', '50% 60%')

# 4. Aviso de gasto fora do normal ----------------------------------------
S['04-gasto'] = (4.8, '''
.eb¤ { position:absolute; left:90px; top:170px; }
.t¤ { position:absolute; left:90px; right:90px; top:220px; font-size:96px; }
.card¤ { position:absolute; left:90px; right:90px; top:560px; padding:44px 48px; }
.lbl¤ { display:flex; justify-content:space-between; font-size:34px; color:#A9B4CA; margin-bottom:14px; }
.lbl¤ b { color:#E9EEF7; }
.bar¤ { height:54px; border-radius:16px; background:rgba(160,185,225,.14); overflow:hidden; margin-bottom:30px; }
.bar¤ i { display:block; height:100%; width:0; border-radius:16px; }
.bar¤.n i { background:#8C9AB3; }
.bar¤.h i { background:#F2B544; }
.msg¤ { position:absolute; left:90px; right:90px; top:1010px; max-width:none; font-size:36px; }
.msg¤.bot¤ { left:90px; right:220px; }
.rep¤ { position:absolute; right:90px; top:1420px; max-width:none; font-size:36px; }
.ok¤ { position:absolute; left:90px; right:220px; top:1570px; max-width:none; font-size:36px; }
''', '''  <div § class="eb¤">Novo · 3 de 5</div>
  <div § class="h¤ t¤">Aviso quando o gasto <span class="g¤">foge do normal.</span></div>
  <div § class="card¤">
    <div class="lbl¤"><span>Delivery · seu normal</span><b>R$ 260</b></div>
    <div class="bar¤ n"><i class="b1¤"></i></div>
    <div class="lbl¤"><span>Delivery · este mês</span><b style="color:#F2B544">R$ 420</b></div>
    <div class="bar¤ h"><i class="b2¤"></i></div>
  </div>
  <div § class="b¤ bot¤ msg¤"><div class="who¤"><span class="av¤ avdy¤">D</span>Dyno <em>finanças</em></div>🔎 Ana, delivery este mês já deu <b>R$ 420</b>, 60% acima do seu normal. Quer um limite de <b class="g¤">R$ 300</b>?</div>
  <div § class="b¤ me¤ rep¤">Quero 👍</div>
  <div § class="b¤ bot¤ ok¤"><div class="who¤"><span class="av¤ avdy¤">D</span>Dyno</div>Limite de R$ 300 definido. Eu aviso quando chegar perto. ✅</div>''', '''  tl.fromTo([one('.eb¤'), one('.t¤')], { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: 'power3.out', stagger: 0.1 }, 0.15);
  tl.fromTo(one('.card¤'), { y: 120, opacity: 0 }, { y: 0, opacity: 1, duration: 0.55, ease: 'power3.out' }, 0.5);
  tl.to(one('.b1¤'), { width: '62%', duration: 0.7, ease: 'power2.out' }, 1.0);
  tl.to(one('.b2¤'), { width: '100%', duration: 0.9, ease: 'power2.out' }, 1.2);
  tl.fromTo(one('.msg¤'), { x: -140, opacity: 0 }, { x: 0, opacity: 1, duration: 0.45, ease: 'back.out(1.4)' }, 2.2);
  tl.fromTo(one('.rep¤'), { x: 140, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: 'back.out(1.5)' }, 3.4);
  tl.fromTo(one('.ok¤'), { x: -140, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: 'back.out(1.5)' }, 4.0);''', '50% 45%')

# 5. Personalidades + voz -------------------------------------------------
pers = ['Padrão', 'Zen', 'Profissional', 'Coach', 'Extrovertido']
ph_ = ''.join(f'<span § class="pill¤ pr¤ p¤{i}">{n}</span>' for i, n in enumerate(pers))
bars = ''.join(f'<i style="height:{int(h*1.5)}px"></i>' for h in [14, 26, 40, 22, 48, 30, 18, 42, 26, 36, 16, 44, 28, 20, 38, 24, 12, 34, 22, 16])
S['05-persona'] = (5.6, '''
.eb¤ { position:absolute; left:90px; top:170px; }
.t¤ { position:absolute; left:90px; right:90px; top:220px; font-size:96px; }
.row¤ { position:absolute; left:90px; right:90px; top:560px; display:flex; flex-wrap:wrap; gap:18px; }
.pr¤ { font-size:34px; padding:16px 28px; }
.tap¤ { position:absolute; left:690px; top:640px; width:90px; height:90px; border-radius:50%; background:rgba(233,238,247,.85); box-shadow:0 0 0 14px rgba(233,238,247,.18); }
.msg¤ { position:absolute; left:90px; right:200px; top:880px; max-width:none; font-size:36px; }
.aud¤ { position:absolute; left:90px; top:1250px; max-width:none; display:flex; align-items:center; gap:22px; padding:22px 30px; }
.play¤ { width:72px; height:72px; border-radius:50%; background:#2FD47E; color:#04210F; display:flex; align-items:center; justify-content:center; font-size:30px; flex:none; }
.wave¤ { display:flex; align-items:center; gap:8px; height:76px; }
.wave¤ i { display:block; width:9px; border-radius:4px; background:#2FD47E; }
.dur¤ { font-family:"JetBrains Mono"; font-size:28px; color:#A9B4CA; }
.cap¤ { position:absolute; left:90px; top:1420px; }
''', f'''  <div § class="eb¤">Novo · 4 e 5 de 5</div>
  <div § class="h¤ t¤">Escolha o jeito. <span class="g¤">A voz acompanha.</span></div>
  <div § class="row¤">{ph_}</div>
  <div § class="tap¤"></div>
  <div § class="b¤ bot¤ msg¤"><div class="who¤"><span class="av¤ avdy¤">D</span>Dyno <em>coach</em></div>Bora, Ana! 💪 R$ 42 no almoço, registrado. Ainda sobram <b class="g¤">R$ 180</b> de folga no mês. Segue firme!</div>
  <div § class="b¤ bot¤ aud¤"><div class="play¤">▶</div><div class="wave¤">{bars}</div><span class="dur¤">0:06</span></div>
  <div § class="cap¤"><span class="pill¤"><span class="dot¤"></span>Responde em áudio, no mesmo tom</span></div>''', '''  tl.fromTo([one('.eb¤'), one('.t¤')], { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: 'power3.out', stagger: 0.1 }, 0.15);
  tl.fromTo(all('.pr¤'), { y: 40, opacity: 0, scale: 0.8 }, { y: 0, opacity: 1, scale: 1, duration: 0.4, ease: 'back.out(2)', stagger: 0.12 }, 0.6);
  tl.fromTo(one('.tap¤'), { opacity: 0, scale: 1.6, x: 60, y: 200 }, { opacity: 1, scale: 1, x: 0, y: 0, duration: 0.55, ease: 'power2.out' }, 1.5);
  tl.to(one('.tap¤'), { scale: 0.7, duration: 0.12, yoyo: true, repeat: 1 }, 2.1);
  tl.to(one('.p¤3'), { backgroundColor: '#2FD47E', color: '#04210F', borderColor: '#2FD47E', duration: 0.25 }, 2.15);
  tl.to(one('.tap¤'), { opacity: 0, duration: 0.3 }, 2.5);
  tl.fromTo(one('.msg¤'), { x: -140, opacity: 0 }, { x: 0, opacity: 1, duration: 0.45, ease: 'back.out(1.4)' }, 2.7);
  tl.fromTo(one('.aud¤'), { x: -140, opacity: 0 }, { x: 0, opacity: 1, duration: 0.45, ease: 'back.out(1.4)' }, 3.6);
  tl.fromTo(all('.wave¤ i'), { scaleY: 0.25, transformOrigin: '50% 50%' }, { scaleY: 1, duration: 0.3, ease: 'sine.inOut', stagger: { each: 0.06, repeat: 5, yoyo: true } }, 3.9);
  tl.fromTo(one('.cap¤'), { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.4 }, 4.3);''', '50% 50%')

# 6. CTA ------------------------------------------------------------------
S['06-cta'] = (4.6, '''
.brand¤ { position:absolute; left:90px; top:250px; display:flex; align-items:center; gap:26px; font-family:"Bricolage Grotesque"; font-weight:800; font-size:76px; letter-spacing:-.03em; }
.t¤ { position:absolute; left:90px; right:90px; top:460px; font-size:138px; }
.btnw¤ { position:absolute; left:90px; right:90px; top:1120px; }
.url¤ { position:absolute; left:0; right:0; top:1330px; text-align:center; font-family:"JetBrains Mono"; font-size:40px; color:#2FD47E; }
.pw¤ { position:absolute; left:0; right:0; top:1500px; text-align:center; }
''', '''  <div § class="brand¤"><div class="logo¤" style="width:116px;height:116px;font-size:66px">D</div>Dyno</div>
  <div § class="h¤ t¤">Tudo isso já está no seu <span class="g¤">WhatsApp.</span></div>
  <div § class="btnw¤"><div class="btn¤">Quero testar o Dyno →</div></div>
  <div § class="url¤">dynoapp.com.br</div>
  <div § class="pw¤"><span class="pill¤"><span class="dot¤"></span>Beta · 60 dias grátis</span></div>''', '''  tl.fromTo(one('.brand¤'), { y: -30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: 'power2.out' }, 0.05);
  tl.fromTo(one('.t¤'), { y: 70, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: 'power3.out' }, 0.3);
  tl.fromTo(one('.btnw¤'), { y: 80, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: 'back.out(1.6)' }, 1.0);
  tl.to(one('.btn¤'), { scale: 1.04, duration: 0.3, yoyo: true, repeat: 3, ease: 'sine.inOut' }, 1.7);
  tl.fromTo(one('.url¤'), { opacity: 0 }, { opacity: 1, duration: 0.4 }, 1.4);
  tl.fromTo(one('.pw¤'), { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.4 }, 1.8);''', '50% 40%')

scenes = [('01-hook', 0, 3.6), ('02-remedio', 3.4, 5.8), ('03-fatura', 9.0, 5.6), ('04-gasto', 14.4, 4.8), ('05-persona', 19.0, 5.6), ('06-cta', 24.4, 4.6)]
TOTAL = 29.0
for cid, (dur, css, body, js, glow) in S.items():
    open(f'compositions/frames/{cid}.html', 'w').write(comp(cid, dur, css, body, js, glow))
trans = '''        tl.fromTo("#el-02-remedio", { clipPath: "inset(0% 0% 0% 100%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.4, ease: "power3.inOut" }, 3.4);
        tl.fromTo("#el-03-fatura", { clipPath: "inset(100% 0% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.4, ease: "power3.inOut" }, 9.0);
        tl.to("#el-02-remedio", { y: -180, duration: 0.4, ease: "power3.inOut" }, 9.0);
        tl.fromTo("#el-04-gasto", { clipPath: "inset(0% 0% 0% 100%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.4, ease: "power3.inOut" }, 14.4);
        tl.fromTo("#el-05-persona", { clipPath: "circle(0% at 50% 50%)" }, { clipPath: "circle(90% at 50% 50%)", duration: 0.45, ease: "power3.inOut" }, 19.0);
        tl.fromTo("#el-06-cta", { clipPath: "inset(0% 0% 100% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.4, ease: "power3.inOut" }, 24.4);'''
open('index.html', 'w').write(index('novidades', TOTAL, scenes, trans))
