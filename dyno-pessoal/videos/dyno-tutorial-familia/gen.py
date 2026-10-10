exec(open('/home/claude/videos/_dark/base_dark.py').read())
S = {}
STEP = '''
.st¤ { position:absolute; left:90px; top:170px; display:flex; align-items:center; gap:24px; }
.sn¤ { width:96px; height:96px; border-radius:50%; background:#2FD47E; color:#04210F; display:flex; align-items:center; justify-content:center; font-family:"Bricolage Grotesque"; font-weight:800; font-size:56px; flex:none; }
.t¤ { position:absolute; left:90px; right:90px; top:300px; font-size:92px; }
.ph¤ { left:110px; right:110px; top:600px; bottom:170px; }
.tip¤ { position:absolute; left:0; right:0; bottom:70px; text-align:center; }
'''
def step(n, eb):
    return f'<div § class="st¤"><div class="sn¤">{n}</div><div class="eb¤">{eb}</div></div>'
IN = '''  tl.fromTo(one('.st¤'), { x: -60, opacity: 0 }, { x: 0, opacity: 1, duration: 0.45, ease: 'power3.out' }, 0.15);
  tl.fromTo(one('.t¤'), { y: 50, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: 'power3.out' }, 0.3);
  tl.fromTo(one('.ph¤'), { y: 300, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: 'power3.out' }, 0.45);
'''
HEAD = lambda t, s, av='<div class="logo¤" style="width:84px;height:84px;font-size:46px">D</div>': f'<div class="ph-head¤">{av}<div><b>{t}</b><small>{s}</small></div></div>'
GAV = '<div style="width:84px;height:84px;border-radius:50%;background:#142036;display:flex;align-items:center;justify-content:center;font-size:44px;flex:none">🏠</div>'

S['01-hook'] = (4.4, '''
.eb¤ { position:absolute; left:90px; top:430px; }
.t¤ { position:absolute; left:90px; right:90px; top:490px; font-size:150px; }
.s¤ { position:absolute; left:90px; right:90px; top:1110px; font-family:"Bricolage Grotesque"; font-weight:700; font-size:66px; letter-spacing:-.03em; line-height:1.08; color:#A9B4CA; }
.dots3¤ { position:absolute; left:90px; top:1400px; display:flex; gap:22px; }
.dots3¤ span { width:110px; height:110px; border-radius:50%; background:#0F1828; border:3px solid rgba(47,212,126,.5); display:flex; align-items:center; justify-content:center; font-family:"Bricolage Grotesque"; font-weight:800; font-size:56px; color:#2FD47E; }
''', '''  <div § class="eb¤">Modo família · tutorial</div>
  <div § class="h¤ t¤">Ative em <span class="g¤">3 passos.</span></div>
  <div § class="s¤">Você, sua família e o Dyno no mesmo grupo do WhatsApp.</div>
  <div § class="dots3¤"><span>1</span><span>2</span><span>3</span></div>''', '''  tl.fromTo(one('.eb¤'), { y: 20, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4 }, 0.1);
  tl.fromTo(one('.t¤'), { y: 60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: 'power3.out' }, 0.25);
  tl.fromTo(one('.s¤'), { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5 }, 1.0);
  tl.fromTo(all('.dots3¤ span'), { scale: 0 }, { scale: 1, duration: 0.45, ease: 'back.out(2.2)', stagger: 0.2 }, 1.5);''', '50% 70%')

S['02-euquero'] = (6.6, STEP, f'''  {step('0', 'Antes de tudo')}
  <div § class="h¤ t¤">Responda <span class="g¤">EU QUERO</span> no privado do Dyno.</div>
  <div § class="phone¤ ph¤">
    {HEAD('Dyno', 'conta verificada')}
    <div § class="b¤ bot¤ d1¤" style="top:190px"><div class="who¤"><span class="av¤ avdy¤">D</span>Dyno</div>Você foi convidado a testar o Modo família! Digite <b>EU QUERO</b>. 💚</div>
    <div § class="b¤ me¤ m1¤" style="top:440px">EU QUERO<span class="tm¤">10:02</span></div>
    <div § class="b¤ bot¤ d2¤" style="top:580px"><div class="who¤"><span class="av¤ avdy¤">D</span>Dyno</div>Pronto! 🎉 O Modo família já está ativo na sua conta.</div>
  </div>''', IN + '''  tl.fromTo(one('.d1¤'), { x: -140, opacity: 0 }, { x: 0, opacity: 1, duration: 0.45, ease: 'back.out(1.5)' }, 1.2);
  tl.fromTo(one('.m1¤'), { x: 140, opacity: 0 }, { x: 0, opacity: 1, duration: 0.45, ease: 'back.out(1.5)' }, 2.6);
  tl.fromTo(one('.d2¤'), { x: -140, opacity: 0 }, { x: 0, opacity: 1, duration: 0.45, ease: 'back.out(1.5)' }, 3.8);''', '50% 60%')

ppl = [('Ana', '#F2B544'), ('Pedro', '#7FB2FF'), ('Léo', '#FF9B8A'), ('Carla', '#B69CFF')]
rows = ''.join(f'''    <div § class="ct¤ c¤{i}"><div class="ci¤" style="background:{c}">{n[0]}</div><b>{n}</b><span class="ck¤ k¤{i}">{'✓' if i < 3 else ''}</span></div>
''' for i, (n, c) in enumerate(ppl))
S['03-grupo'] = (7.4, STEP + '''
.ct¤ { position:relative; margin:0 34px; display:flex; align-items:center; gap:26px; padding:20px 10px; border-bottom:2px solid rgba(160,185,225,.08); }
.ct¤ b { font-size:40px; }
.ci¤ { width:84px; height:84px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-family:"Bricolage Grotesque"; font-weight:800; font-size:42px; color:#0A1A33; flex:none; }
.ck¤ { margin-left:auto; width:56px; height:56px; border-radius:50%; border:3px solid rgba(160,185,225,.35); display:flex; align-items:center; justify-content:center; font-size:34px; font-weight:800; color:#04210F; }
.nm¤ { position:absolute; left:34px; right:34px; bottom:40px; padding:24px 28px; background:#0F1828; border:2px solid rgba(47,212,126,.4); border-radius:26px; font-size:36px; }
.nm¤ small { display:block; font-family:"JetBrains Mono"; font-size:22px; color:#8C9AB3; letter-spacing:.1em; text-transform:uppercase; margin-bottom:6px; }
''', f'''  {step('1', 'Passo 1')}
  <div § class="h¤ t¤">Crie um grupo com <span class="g¤">quem vai dividir.</span></div>
  <div § class="phone¤ ph¤">
    {HEAD('Novo grupo', 'até 3 pessoas além de você', '<div style="width:84px;height:84px;border-radius:50%;background:#142036;display:flex;align-items:center;justify-content:center;font-size:44px;flex:none">👥</div>')}
    <div style="position:absolute;left:0;right:0;top:160px">
{rows}    </div>
    <div § class="nm¤"><small>Nome do grupo</small>Casa 🏠</div>
  </div>''', IN + '''  for (let i = 0; i < 4; i++) tl.fromTo(one('.c¤' + i), { x: 80, opacity: 0 }, { x: 0, opacity: 1, duration: 0.35, ease: 'power2.out' }, 1.1 + i * 0.15);
  for (let i = 0; i < 3; i++) tl.fromTo(one('.k¤' + i), { backgroundColor: 'rgba(47,212,126,0)', borderColor: 'rgba(160,185,225,.35)', scale: 1 }, { backgroundColor: '#2FD47E', borderColor: '#2FD47E', scale: 1.15, duration: 0.25, ease: 'back.out(2)' }, 2.3 + i * 0.6);
  tl.fromTo(one('.nm¤'), { y: 80, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: 'back.out(1.5)' }, 4.4);''', '50% 60%')

S['04-adiciona'] = (7.0, STEP + '''
.card2¤ { position:absolute; left:34px; right:34px; top:200px; padding:30px; background:#0F1828; border:2px solid rgba(160,185,225,.14); border-radius:30px; display:flex; align-items:center; gap:26px; }
.card2¤ b { display:block; font-size:42px; } .card2¤ small { display:block; font-family:"JetBrains Mono"; font-size:28px; color:#A9B4CA; margin-top:4px; }
.btn2¤ { position:absolute; left:34px; right:34px; top:420px; text-align:center; background:#2FD47E; color:#04210F; border-radius:999px; padding:28px; font-size:38px; font-weight:700; }
.sys¤ { position:absolute; left:60px; right:60px; top:620px; text-align:center; font-size:30px; color:#A9B4CA; background:#0B1220; border:2px solid rgba(160,185,225,.12); border-radius:20px; padding:16px 20px; }
''', f'''  {step('2', 'Passo 2')}
  <div § class="h¤ t¤">Adicione o <span class="g¤">Dyno</span> ao grupo.</div>
  <div § class="phone¤ ph¤">
    {HEAD('Casa 🏠', 'Adicionar participante', GAV)}
    <div § class="card2¤"><div class="logo¤" style="width:96px;height:96px;font-size:54px">D</div><div><b>Dyno</b><small>+55 11 93949-7178</small></div></div>
    <div § class="btn2¤">Adicionar ao grupo</div>
    <div § class="sys¤">Você adicionou Dyno ✅</div>
  </div>
  <div § class="tip¤"><span class="pill¤"><span class="dot¤"></span>Dica: salve o contato do Dyno antes</span></div>''', IN + '''  tl.fromTo(one('.card2¤'), { y: 60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: 'power3.out' }, 1.2);
  tl.fromTo(one('.btn2¤'), { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4 }, 1.8);
  tl.to(one('.btn2¤'), { scale: 0.94, duration: 0.12, yoyo: true, repeat: 1 }, 2.9);
  tl.fromTo(one('.sys¤'), { scale: 0.6, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.4, ease: 'back.out(2)' }, 3.3);
  tl.fromTo(one('.tip¤'), { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4 }, 4.0);''', '50% 60%')

S['05-oi'] = (8.0, STEP + '''
.b¤ { font-size:33px; }
.wl¤ { max-width:88%; }
''', f'''  {step('3', 'Passo 3')}
  <div § class="h¤ t¤">Você manda <span class="g¤">“oi Dyno”</span> no grupo.</div>
  <div § class="phone¤ ph¤">
    {HEAD('Casa 🏠', 'Você, Ana, Pedro, Léo, Dyno', GAV)}
    <div § class="b¤ me¤ m1¤" style="top:180px">oi Dyno 👋<span class="tm¤">10:05</span></div>
    <div § class="b¤ bot¤ wl¤ d1¤" style="top:320px"><div class="who¤"><span class="av¤ avdy¤">D</span>Dyno <em>e Dina</em></div>Oi, gente! 👋 Aqui são o Dyno e a Dina. Muito obrigado por confiarem em nós para ajudar a organizar a rotina de vocês. 💚<br><br>Mandem gastos, contas e lembretes por texto, áudio ou foto: fica tudo na mesma conta da casa.<span class="tm¤">10:05</span></div>
  </div>''', IN + '''  tl.fromTo(one('.m1¤'), { x: 140, opacity: 0 }, { x: 0, opacity: 1, duration: 0.45, ease: 'back.out(1.5)' }, 1.2);
  tl.fromTo(one('.d1¤'), { y: 80, opacity: 0 }, { y: 0, opacity: 1, duration: 0.55, ease: 'back.out(1.3)' }, 2.4);''', '50% 60%')

S['06-uso'] = (7.6, STEP + '''
.b¤ { font-size:34px; }
''', f'''  {step('✓', 'Pronto! Agora é só usar')}
  <div § class="h¤ t¤">Todo mundo usa <span class="g¤">a mesma conta.</span></div>
  <div § class="phone¤ ph¤">
    {HEAD('Casa 🏠', 'Você, Ana, Pedro, Léo, Dyno', GAV)}
    <div § class="b¤ bot¤ a1¤" style="top:180px;background:#142036"><div class="who¤" style="color:#F2B544">Ana</div>gastei 80 na farmácia 💊</div>
    <div § class="b¤ bot¤ d1¤" style="top:350px"><div class="who¤"><span class="av¤ avdy¤">D</span>Dyno</div>Anotado, Ana: <b>R$ 80</b> em saúde.</div>
    <div § class="b¤ bot¤ a2¤" style="top:540px;background:#142036"><div class="who¤" style="color:#7FB2FF">Pedro</div>Dyno, lembra a Ana de pagar a luz amanhã às 9h</div>
    <div § class="b¤ bot¤ d2¤" style="top:760px"><div class="who¤"><span class="av¤ avdi¤">D</span>Dina</div>Combinado! Amanhã às <b class="g¤">9h</b> eu aviso a Ana. 🔔</div>
  </div>''', IN + '''  tl.fromTo(one('.a1¤'), { x: -140, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: 'back.out(1.5)' }, 1.1);
  tl.fromTo(one('.d1¤'), { x: -140, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: 'back.out(1.5)' }, 2.1);
  tl.fromTo(one('.a2¤'), { x: -140, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: 'back.out(1.5)' }, 3.4);
  tl.fromTo(one('.d2¤'), { x: -140, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: 'back.out(1.5)' }, 4.6);''', '50% 60%')

steps = [('0', 'Responda EU QUERO'), ('1', 'Crie o grupo da família'), ('2', 'Adicione o Dyno'), ('3', 'Mande “oi Dyno” no grupo')]
sh = ''.join(f'    <div § class="card¤ rs¤"><span class="n¤">{a}</span>{b}</div>\n' for a, b in steps)
S['07-resumo'] = (5.6, '''
.brand¤ { position:absolute; left:90px; top:200px; display:flex; align-items:center; gap:26px; font-family:"Bricolage Grotesque"; font-weight:800; font-size:76px; letter-spacing:-.03em; }
.t¤ { position:absolute; left:90px; right:90px; top:390px; font-size:110px; }
.list¤ { position:absolute; left:80px; right:80px; top:680px; display:flex; flex-direction:column; gap:22px; }
.rs¤ { display:flex; align-items:center; gap:28px; padding:30px 34px; border-radius:32px; font-size:44px; font-weight:700; }
.n¤ { width:76px; height:76px; border-radius:50%; background:#2FD47E; color:#04210F; display:flex; align-items:center; justify-content:center; font-family:"Bricolage Grotesque"; font-weight:800; font-size:42px; flex:none; }
.num¤ { position:absolute; left:0; right:0; top:1460px; text-align:center; font-family:"JetBrains Mono"; font-size:40px; color:#2FD47E; }
.q¤ { position:absolute; left:0; right:0; top:1540px; text-align:center; font-size:36px; color:#A9B4CA; }
''', f'''  <div § class="brand¤"><div class="logo¤" style="width:116px;height:116px;font-size:66px">D</div>Dyno</div>
  <div § class="h¤ t¤">Resumindo:</div>
  <div § class="list¤">
{sh}  </div>
  <div § class="num¤">Dyno: +55 11 93949-7178</div>
  <div § class="q¤">Ficou com dúvida? É só perguntar ao Dyno. 💚</div>''', '''  tl.fromTo([one('.brand¤'), one('.t¤')], { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: 'power3.out', stagger: 0.1 }, 0.1);
  tl.fromTo(all('.rs¤'), { x: -140, opacity: 0 }, { x: 0, opacity: 1, duration: 0.45, ease: 'power3.out', stagger: 0.25 }, 0.6);
  tl.fromTo([one('.num¤'), one('.q¤')], { opacity: 0 }, { opacity: 1, duration: 0.4, stagger: 0.2 }, 1.9);''', '50% 40%')

order = ['01-hook', '02-euquero', '03-grupo', '04-adiciona', '05-oi', '06-uso', '07-resumo']
scenes, t = [], 0.0
for cid in order:
    dur = S[cid][0]; scenes.append((cid, round(t, 2), dur)); t += dur - 0.3
TOTAL = round(scenes[-1][1] + scenes[-1][2], 2)
for cid, (dur, css, body, js, glow) in S.items():
    open(f'compositions/frames/{cid}.html', 'w').write(comp(cid, dur, css, body, js, glow))
kinds = ['inset(0% 0% 0% 100%)', 'inset(100% 0% 0% 0%)', 'circle(0% at 50% 50%)']
ends = ['inset(0% 0% 0% 0%)', 'inset(0% 0% 0% 0%)', 'circle(80% at 50% 50%)']
trans = '\n'.join(f'        tl.fromTo("#el-{cid}", {{ clipPath: "{kinds[i % 3]}" }}, {{ clipPath: "{ends[i % 3]}", duration: 0.4, ease: "power3.inOut" }}, {st});' for i, (cid, st, d) in enumerate(scenes[1:]))
open('index.html', 'w').write(index('tutorial', TOTAL, scenes, trans))
print(TOTAL, scenes)
