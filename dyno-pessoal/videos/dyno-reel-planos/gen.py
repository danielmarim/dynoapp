exec(open('/home/claude/videos/_dark/base_dark.py').read())
S = {}
S['01-hook'] = (3.8, '''
.eb¤ { position:absolute; left:90px; top:480px; }
.t¤ { position:absolute; left:90px; right:90px; top:540px; font-size:190px; }
.tags¤ { position:absolute; left:90px; right:90px; top:1150px; display:flex; flex-wrap:wrap; gap:22px; }
.tg¤ { font-size:40px; padding:20px 36px; }
.tg¤.on { background:#2FD47E; color:#04210F; border-color:#2FD47E; }
''', '''  <div § class="eb¤">Quiz rápido · 10 segundos</div>
  <div § class="h¤ t¤">Qual Dyno é <span class="g¤">o seu?</span></div>
  <div § class="tags¤"><span class="pill¤ tg¤">Essencial</span><span class="pill¤ tg¤ on">Completo</span><span class="pill¤ tg¤">Premium</span></div>''', '''  tl.fromTo(one('.eb¤'), { y: 20, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4 }, 0.1);
  tl.fromTo(one('.t¤'), { y: 70, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: 'power3.out' }, 0.25);
  tl.fromTo(all('.tg¤'), { y: 40, opacity: 0, scale: 0.8 }, { y: 0, opacity: 1, scale: 1, duration: 0.45, ease: 'back.out(2)', stagger: 0.18 }, 1.1);''', '50% 60%')

opts = ['Esqueço de pagar contas e compromissos', 'Não sei para onde vai o meu dinheiro', 'Compro parcelado ou empresto dinheiro', 'Minha rotina e minha agenda embolam', 'Divido as contas da casa com outras pessoas']
oh = ''.join(f'    <div § class="op¤ o¤{i}"><span class="k¤">{"ABCDE"[i]}</span>{t}</div>\n' for i, t in enumerate(opts))
S['02-quiz'] = (7.4, '''
.eb¤ { position:absolute; left:90px; top:200px; }
.t¤ { position:absolute; left:90px; right:90px; top:250px; font-size:110px; }
.list¤ { position:absolute; left:80px; right:80px; top:580px; display:flex; flex-direction:column; gap:24px; }
.op¤ { display:flex; align-items:center; gap:26px; padding:30px 34px; background:#0B1220; border:2px solid rgba(160,185,225,.16); border-radius:32px; font-size:38px; font-weight:600; line-height:1.2; }
.k¤ { width:64px; height:64px; border-radius:18px; border:2px solid rgba(160,185,225,.3); display:flex; align-items:center; justify-content:center; font-family:"JetBrains Mono"; font-size:30px; color:#8C9AB3; flex:none; }
.res¤ { position:absolute; left:80px; right:80px; top:1500px; padding:34px 40px; border-color:rgba(47,212,126,.5); }
.res¤ small { display:block; font-family:"JetBrains Mono"; font-size:26px; letter-spacing:.12em; text-transform:uppercase; color:#8C9AB3; }
.res¤ b { display:block; font-family:"Bricolage Grotesque"; font-weight:800; font-size:64px; letter-spacing:-.03em; margin-top:6px; }
.res¤ span { display:block; font-size:32px; color:#A9B4CA; margin-top:6px; }
.tap¤ { position:absolute; left:820px; top:880px; width:90px; height:90px; border-radius:50%; background:rgba(233,238,247,.85); box-shadow:0 0 0 14px rgba(233,238,247,.18); }
''', f'''  <div § class="eb¤">Quiz rápido</div>
  <div § class="h¤ t¤">Qual é sua <span class="g¤">maior dor?</span></div>
  <div § class="list¤">
{oh}  </div>
  <div § class="card¤ res¤"><small>Recomendado para você</small><b>Completo <span class="g¤" style="display:inline;font-size:64px;color:#2FD47E">· R$ 19,90</span></b><span>limites, extrato, assinaturas e o resumo do dia</span></div>
  <div § class="tap¤"></div>''', '''  tl.fromTo([one('.eb¤'), one('.t¤')], { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: 'power3.out', stagger: 0.1 }, 0.15);
  tl.fromTo(all('.op¤'), { x: 140, opacity: 0 }, { x: 0, opacity: 1, duration: 0.45, ease: 'power3.out', stagger: 0.22 }, 0.6);
  tl.fromTo(one('.tap¤'), { opacity: 0, scale: 1.6, x: 60, y: 300 }, { opacity: 1, scale: 1, x: 0, y: 0, duration: 0.7, ease: 'power2.out' }, 2.4);
  tl.to(one('.tap¤'), { scale: 0.7, duration: 0.12, yoyo: true, repeat: 1 }, 3.15);
  tl.to(one('.o¤1'), { backgroundColor: 'rgba(47,212,126,.14)', borderColor: '#2FD47E', duration: 0.25 }, 3.2);
  tl.to(one('.o¤1 .k¤'), { backgroundColor: '#2FD47E', color: '#04210F', borderColor: '#2FD47E', duration: 0.25 }, 3.2);
  tl.to(one('.tap¤'), { opacity: 0, duration: 0.3 }, 3.6);
  tl.fromTo(one('.res¤'), { y: 120, opacity: 0 }, { y: 0, opacity: 1, duration: 0.55, ease: 'back.out(1.5)' }, 3.9);''', '70% 45%')

plans = [('Essencial', '9,90', 'Contas, lembretes, tarefas e listas', False, ''), ('Completo', '19,90', 'Tudo do Dyno e da Dina: limites, extrato, agenda', True, 'Mais escolhido'), ('Premium', '39,90', 'Completo + Modo família: até 4 pessoas', False, 'Para a casa toda')]
ph = ''.join(f'''    <div § class="pl¤ {'best' if b else ''} p¤{i}"><div class="top¤"><b>{n}</b>{f'<span class="tag¤">{tg}</span>' if tg else ''}</div><div class="pr¤">R$ {p}<small>/mês</small></div><div class="d¤">{d}</div></div>
''' for i, (n, p, d, b, tg) in enumerate(plans))
S['03-planos'] = (7.6, '''
.eb¤ { position:absolute; left:90px; top:200px; }
.t¤ { position:absolute; left:90px; right:90px; top:250px; font-size:110px; }
.list¤ { position:absolute; left:80px; right:80px; top:560px; display:flex; flex-direction:column; gap:30px; }
.pl¤ { padding:38px 42px; background:#0B1220; border:2px solid rgba(160,185,225,.16); border-radius:40px; }
.pl¤.best { background:linear-gradient(180deg, rgba(47,212,126,.16), rgba(47,212,126,.04)); border-color:#2FD47E; box-shadow:0 0 80px rgba(47,212,126,.18); }
.top¤ { display:flex; align-items:center; gap:20px; }
.top¤ b { font-family:"Bricolage Grotesque"; font-weight:800; font-size:58px; letter-spacing:-.03em; }
.tag¤ { margin-left:auto; font-size:26px; font-weight:700; padding:10px 22px; border-radius:999px; background:#2FD47E; color:#04210F; }
.pl¤:not(.best) .tag¤ { background:rgba(242,181,68,.16); color:#F2B544; border:2px solid rgba(242,181,68,.45); }
.pr¤ { font-family:"Bricolage Grotesque"; font-weight:800; font-size:92px; letter-spacing:-.04em; margin-top:8px; }
.pr¤ small { font-family:"Figtree"; font-weight:600; font-size:34px; color:#8C9AB3; margin-left:8px; letter-spacing:0; }
.best .pr¤ { color:#2FD47E; }
.d¤ { font-size:34px; color:#A9B4CA; margin-top:4px; }
''', f'''  <div § class="eb¤">Os 3 planos</div>
  <div § class="h¤ t¤">Escolha o seu <span class="g¤">ritmo.</span></div>
  <div § class="list¤">
{ph}  </div>''', '''  tl.fromTo([one('.eb¤'), one('.t¤')], { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: 'power3.out', stagger: 0.1 }, 0.15);
  tl.fromTo(all('.pl¤'), { y: 120, opacity: 0 }, { y: 0, opacity: 1, duration: 0.55, ease: 'power3.out', stagger: 0.45 }, 0.6);
  tl.to(one('.p¤1'), { scale: 1.035, duration: 0.35, yoyo: true, repeat: 3, ease: 'sine.inOut' }, 2.8);''', '50% 55%')

S['04-gratis'] = (3.8, '''
.t¤ { position:absolute; left:90px; right:90px; top:560px; font-size:330px; line-height:.86; }
.s¤ { position:absolute; left:90px; right:90px; top:930px; font-family:"Bricolage Grotesque"; font-weight:800; font-size:92px; letter-spacing:-.03em; line-height:1.0; }
.n¤ { position:absolute; left:90px; right:90px; top:1200px; font-size:42px; line-height:1.3; color:#A9B4CA; }
''', '''  <div § class="h¤ t¤"><span class="g¤ num¤">60</span></div>
  <div § class="s¤">dias grátis no Beta, <span class="g¤">em qualquer plano.</span></div>
  <div § class="n¤">Sem boleto no cadastro. Não gostou? É só sair, sem custo.</div>''', '''  const el = one('.num¤'), o = { v: 0 };
  tl.fromTo(o, { v: 0 }, { v: 60, duration: 1.0, ease: 'power2.out', onUpdate: () => { el.textContent = String(Math.round(o.v)); } }, 0.1);
  tl.fromTo(one('.t¤'), { scale: 0.7, opacity: 0, transformOrigin: '0% 50%' }, { scale: 1, opacity: 1, duration: 0.5, ease: 'back.out(1.6)' }, 0.05);
  tl.fromTo(one('.s¤'), { y: 50, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: 'power3.out' }, 0.9);
  tl.fromTo(one('.n¤'), { opacity: 0 }, { opacity: 1, duration: 0.4 }, 1.5);''', '30% 40%')

S['05-cta'] = (4.4, '''
.brand¤ { position:absolute; left:90px; top:250px; display:flex; align-items:center; gap:26px; font-family:"Bricolage Grotesque"; font-weight:800; font-size:76px; letter-spacing:-.03em; }
.t¤ { position:absolute; left:90px; right:90px; top:460px; font-size:150px; }
.btnw¤ { position:absolute; left:90px; right:90px; top:1120px; }
.url¤ { position:absolute; left:0; right:0; top:1330px; text-align:center; font-family:"JetBrains Mono"; font-size:40px; color:#2FD47E; }
.pw¤ { position:absolute; left:0; right:0; top:1500px; text-align:center; }
''', '''  <div § class="brand¤"><div class="logo¤" style="width:116px;height:116px;font-size:66px">D</div>Dyno</div>
  <div § class="h¤ t¤">Faça o quiz e <span class="g¤">descubra.</span></div>
  <div § class="btnw¤"><div class="btn¤">Ver os planos →</div></div>
  <div § class="url¤">dynoapp.com.br/precos</div>
  <div § class="pw¤"><span class="pill¤"><span class="dot¤"></span>Beta fechado · vagas limitadas</span></div>''', '''  tl.fromTo(one('.brand¤'), { y: -30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: 'power2.out' }, 0.05);
  tl.fromTo(one('.t¤'), { y: 70, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: 'power3.out' }, 0.3);
  tl.fromTo(one('.btnw¤'), { y: 80, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: 'back.out(1.6)' }, 1.0);
  tl.to(one('.btn¤'), { scale: 1.04, duration: 0.3, yoyo: true, repeat: 3, ease: 'sine.inOut' }, 1.7);
  tl.fromTo(one('.url¤'), { opacity: 0 }, { opacity: 1, duration: 0.4 }, 1.4);
  tl.fromTo(one('.pw¤'), { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.4 }, 1.8);''', '50% 40%')

scenes = [('01-hook', 0, 3.8), ('02-quiz', 3.5, 7.4), ('03-planos', 10.6, 7.6), ('04-gratis', 17.9, 3.8), ('05-cta', 21.4, 4.4)]
TOTAL = 25.8
for cid, (dur, css, body, js, glow) in S.items():
    open(f'compositions/frames/{cid}.html', 'w').write(comp(cid, dur, css, body, js, glow))
trans = '''        tl.fromTo("#el-02-quiz", { clipPath: "inset(0% 0% 0% 100%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.4, ease: "power3.inOut" }, 3.5);
        tl.fromTo("#el-03-planos", { clipPath: "inset(100% 0% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.4, ease: "power3.inOut" }, 10.6);
        tl.to("#el-02-quiz", { y: -180, duration: 0.4, ease: "power3.inOut" }, 10.6);
        tl.fromTo("#el-04-gratis", { clipPath: "circle(0% at 30% 40%)" }, { clipPath: "circle(90% at 30% 40%)", duration: 0.45, ease: "power3.inOut" }, 17.9);
        tl.fromTo("#el-05-cta", { clipPath: "inset(0% 0% 100% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.4, ease: "power3.inOut" }, 21.4);'''
open('index.html', 'w').write(index('planos', TOTAL, scenes, trans))
