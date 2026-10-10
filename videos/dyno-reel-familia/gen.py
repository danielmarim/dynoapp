exec(open('/home/claude/videos/_dark/base_dark.py').read())
S = {}
# ---------- 1 HOOK ----------
S['01-hook'] = (4.6, '''
.eb¤ { position:absolute; left:90px; top:300px; }
.t¤ { position:absolute; left:90px; right:90px; top:360px; font-size:150px; }
.ring¤ { position:absolute; left:140px; right:140px; top:1000px; height:620px; }
.p¤ { position:absolute; width:200px; text-align:center; }
.p¤ .c¤ { width:170px; height:170px; margin:0 auto; border-radius:50%; display:flex; align-items:center; justify-content:center; font-family:"Bricolage Grotesque"; font-weight:800; font-size:76px; color:#0A1A33; border:6px solid #060A13; box-shadow:0 0 0 3px rgba(160,185,225,.22); }
.p¤ span { display:block; margin-top:16px; font-size:34px; font-weight:700; }
.mid¤ { position:absolute; left:50%; top:50%; width:190px; height:190px; margin:-95px 0 0 -95px; font-size:110px; box-shadow:0 0 0 18px rgba(47,212,126,.12), 0 0 80px rgba(47,212,126,.45); }
.ln¤ { position:absolute; left:0; top:0; width:800px; height:620px; }
''', '''  <div § class="eb¤ eb¤x">Modo família · Premium</div>
  <div § class="h¤ t¤">A casa toda no <span class="g¤">mesmo Dyno.</span></div>
  <div § class="ring¤">
    <svg § class="ln¤" viewBox="0 0 800 620"><g stroke="rgba(47,212,126,.45)" stroke-width="4" stroke-dasharray="10 12" fill="none">
      <path class="l¤" d="M400 310 L110 90"/><path class="l¤" d="M400 310 L690 90"/><path class="l¤" d="M400 310 L110 530"/><path class="l¤" d="M400 310 L690 530"/></g></svg>
    <div § class="logo¤ mid¤">D</div>
    <div § class="p¤" style="left:10px;top:-5px"><div class="c¤" style="background:#2FD47E">V</div><span>Você</span></div>
    <div § class="p¤" style="left:590px;top:-5px"><div class="c¤" style="background:#F2B544">A</div><span>Ana</span></div>
    <div § class="p¤" style="left:10px;top:395px"><div class="c¤" style="background:#7FB2FF">P</div><span>Pedro</span></div>
    <div § class="p¤" style="left:590px;top:395px"><div class="c¤" style="background:#FF9B8A">L</div><span>Léo</span></div>
  </div>''', '''  tl.fromTo(one('.eb¤x'), { y: 20, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: 'power2.out' }, 0.1);
  tl.fromTo(one('.t¤'), { y: 60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: 'power3.out' }, 0.25);
  tl.fromTo(one('.mid¤'), { scale: 0 }, { scale: 1, duration: 0.5, ease: 'back.out(2)' }, 0.9);
  tl.fromTo(all('.p¤'), { scale: 0, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.45, ease: 'back.out(2)', stagger: 0.18 }, 1.25);
  tl.fromTo(all('.l¤'), { opacity: 0 }, { opacity: 1, duration: 0.3, stagger: 0.18 }, 1.3);
  tl.to(all('.l¤'), { attr: { 'stroke-dashoffset': -88 }, duration: 2.6, ease: 'none' }, 1.8);''', '50% 72%')

# ---------- 2 PAINEL ----------
rows = [('Ana', '+55 11 9••••-4410', '#F2B544'), ('Pedro', '+55 11 9••••-1938', '#7FB2FF'), ('Léo', '+55 11 9••••-5507', '#FF9B8A')]
rh = ''.join(f'''    <div § class="row¤ r¤{i}"><div class="ci¤" style="background:{c}">{n[0]}</div><div><b>{n}</b><small>{w}</small></div><span class="rm¤">Remover</span></div>
''' for i, (n, w, c) in enumerate(rows))
S['02-painel'] = (6.0, '''
.eb¤ { position:absolute; left:90px; top:200px; }
.t¤ { position:absolute; left:90px; right:90px; top:250px; font-size:96px; }
.win¤ { position:absolute; left:70px; right:70px; top:560px; padding:0 0 40px; overflow:hidden; }
.bar¤ { display:flex; align-items:center; gap:14px; padding:26px 34px; border-bottom:2px solid rgba(160,185,225,.12); font-family:"JetBrains Mono"; font-size:26px; color:#8C9AB3; }
.bar¤ i { width:18px; height:18px; border-radius:50%; background:#1E2A40; display:block; }
.tabs¤ { display:flex; gap:14px; padding:30px 34px 10px; }
.tab¤ { padding:14px 26px; border-radius:999px; font-size:28px; font-weight:600; color:#8C9AB3; border:2px solid rgba(160,185,225,.14); }
.tab¤.on { background:#2FD47E; color:#04210F; border-color:#2FD47E; }
.cnt¤ { padding:26px 34px 8px; font-size:32px; color:#A9B4CA; }
.cnt¤ b { color:#2FD47E; }
.row¤ { display:flex; align-items:center; gap:24px; margin:16px 34px 0; padding:24px 28px; background:#0F1828; border:2px solid rgba(160,185,225,.12); border-radius:30px; }
.row¤ b { display:block; font-size:36px; } .row¤ small { display:block; font-size:26px; color:#8C9AB3; font-family:"JetBrains Mono"; }
.ci¤ { width:80px; height:80px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-family:"Bricolage Grotesque"; font-weight:800; font-size:40px; color:#0A1A33; flex:none; }
.rm¤ { margin-left:auto; font-size:24px; color:#8C9AB3; border:2px solid rgba(160,185,225,.2); border-radius:999px; padding:10px 20px; }
.add¤ { margin:28px 34px 0; text-align:center; background:#2FD47E; color:#04210F; border-radius:999px; padding:26px; font-size:34px; font-weight:700; }
''', f'''  <div § class="eb¤">dynoapp.com.br · área do cliente</div>
  <div § class="h¤ t¤">Você monta o grupo <span class="g¤">pelo site.</span></div>
  <div § class="card¤ win¤">
    <div class="bar¤"><i></i><i></i><i></i><span style="margin-left:14px">dynoapp.com.br/conta</span></div>
    <div class="tabs¤"><span class="tab¤">Resumo</span><span class="tab¤">Listas</span><span class="tab¤ on">Família</span><span class="tab¤">Conta</span></div>
    <div class="cnt¤"><b class="n¤">1</b> de 4 pessoas no grupo</div>
    <div § class="row¤"><div class="ci¤" style="background:#2FD47E">V</div><div><b>Você</b><small>titular do plano</small></div></div>
{rh}    <div § class="add¤">+ Adicionar pessoa</div>
  </div>''', '''  tl.fromTo([one('.eb¤'), one('.t¤')], { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: 'power3.out', stagger: 0.1 }, 0.25);
  tl.fromTo(one('.win¤'), { y: 200, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: 'power3.out' }, 0.5);
  const n = one('.n¤'), o = { i: 1 };
  [0, 1, 2].forEach((i) => {
    const t = 1.6 + i * 1.0;
    tl.to(one('.add¤'), { scale: 0.94, duration: 0.12, yoyo: true, repeat: 1, ease: 'power1.inOut' }, t - 0.3);
    tl.fromTo(one('.r¤' + i), { x: 120, opacity: 0 }, { x: 0, opacity: 1, duration: 0.45, ease: 'back.out(1.6)' }, t);
  });
  tl.fromTo(o, { i: 1 }, { i: 4, duration: 3.0, ease: 'steps(3)', onUpdate: () => { n.textContent = String(Math.round(o.i)); } }, 0.6);
  tl.to(one('.cnt¤'), { scale: 1.06, transformOrigin: '0% 50%', duration: 0.2, yoyo: true, repeat: 1 }, 3.7);''', '50% 60%')

# ---------- 3 CONVERSA ----------
S['03-conversa'] = (7.0, '''
.eb¤ { position:absolute; left:90px; top:170px; }
.t¤ { position:absolute; left:90px; right:90px; top:220px; font-size:96px; }
.ph¤ { left:90px; right:90px; top:520px; bottom:150px; }
.tag¤ { position:absolute; font-family:"JetBrains Mono"; font-size:24px; letter-spacing:.1em; text-transform:uppercase; color:#8C9AB3; }
.tag¤.r { right:40px; } .tag¤.l { left:40px; }
''', '''  <div § class="eb¤">Cada um no próprio WhatsApp</div>
  <div § class="h¤ t¤">Todo mundo vê <span class="g¤">a mesma conta.</span></div>
  <div § class="phone¤ ph¤">
    <div class="ph-head¤"><div class="logo¤" style="width:84px;height:84px;font-size:46px">D</div><div><b>Dyno</b><small>grupo família · 4 pessoas</small></div></div>
    <div § class="tag¤ r m1t¤" style="top:190px">WhatsApp da Ana</div>
    <div § class="b¤ me¤ m1¤" style="top:230px">gastei 120 no mercado 🛒<span class="tm¤">18:42</span></div>
    <div § class="b¤ bot¤ d1¤" style="top:390px"><div class="who¤"><span class="av¤ avdy¤">D</span>Dyno <em>finanças</em></div>Anotado na conta da casa: <b>R$ 120</b> em mercado.<span class="tm¤">18:42</span></div>
    <div § class="tag¤ r m2t¤" style="top:640px">WhatsApp do Pedro</div>
    <div § class="b¤ me¤ m2¤" style="top:680px">quanto a gente já gastou de mercado esse mês?<span class="tm¤">20:15</span></div>
    <div § class="b¤ bot¤ d2¤" style="top:890px"><div class="who¤"><span class="av¤ avdy¤">D</span>Dyno <em>finanças</em></div>Este mês: <b class="g¤">R$ 620</b> em mercado, somando a casa toda. 🧾<span class="tm¤">20:15</span></div>
  </div>''', '''  tl.fromTo([one('.eb¤'), one('.t¤')], { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: 'power3.out', stagger: 0.1 }, 0.2);
  tl.fromTo(one('.ph¤'), { y: 300, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: 'power3.out' }, 0.35);
  tl.fromTo([one('.m1t¤'), one('.m1¤')], { x: 120, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: 'back.out(1.5)', stagger: 0.08 }, 1.1);
  tl.fromTo(one('.d1¤'), { x: -120, opacity: 0 }, { x: 0, opacity: 1, duration: 0.45, ease: 'back.out(1.5)' }, 2.1);
  tl.fromTo([one('.m2t¤'), one('.m2¤')], { x: 120, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: 'back.out(1.5)', stagger: 0.08 }, 3.4);
  tl.fromTo(one('.d2¤'), { x: -120, opacity: 0 }, { x: 0, opacity: 1, duration: 0.45, ease: 'back.out(1.5)' }, 4.5);''', '50% 55%')

# ---------- 4 BENEFICIOS ----------
items = [('👥', 'Até 4 pessoas', 'você e mais 3, no mesmo grupo'), ('💬', 'Cada um no seu WhatsApp', 'é só mandar um “oi” para o Dyno'), ('🧾', 'Os mesmos dados', 'gastos, contas, lembretes e listas'), ('🔒', 'Você no controle', 'adiciona e remove pelo site')]
ih = ''.join(f'''    <div § class="card¤ it¤"><div class="ic¤">{e}</div><div><b>{a}</b><span>{b}</span></div></div>
''' for e, a, b in items)
S['04-beneficios'] = (4.8, '''
.eb¤ { position:absolute; left:90px; top:240px; }
.t¤ { position:absolute; left:90px; right:90px; top:290px; font-size:110px; }
.list¤ { position:absolute; left:80px; right:80px; top:660px; display:flex; flex-direction:column; gap:30px; }
.it¤ { display:flex; align-items:center; gap:32px; padding:36px 40px; border-radius:36px; }
.ic¤ { width:110px; height:110px; border-radius:30px; background:rgba(47,212,126,.12); border:2px solid rgba(47,212,126,.35); display:flex; align-items:center; justify-content:center; font-size:58px; flex:none; }
.it¤ b { display:block; font-family:"Bricolage Grotesque"; font-weight:800; font-size:52px; letter-spacing:-.02em; }
.it¤ span { display:block; font-size:34px; color:#8C9AB3; margin-top:4px; }
''', f'''  <div § class="eb¤">Modo família</div>
  <div § class="h¤ t¤">Feito para <span class="g¤">dividir a casa.</span></div>
  <div § class="list¤">
{ih}  </div>''', '''  tl.fromTo([one('.eb¤'), one('.t¤')], { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: 'power3.out', stagger: 0.1 }, 0.15);
  tl.fromTo(all('.it¤'), { x: -160, opacity: 0 }, { x: 0, opacity: 1, duration: 0.5, ease: 'power3.out', stagger: 0.32 }, 0.6);
  tl.fromTo(all('.ic¤'), { scale: 0.4 }, { scale: 1, duration: 0.5, ease: 'back.out(2.4)', stagger: 0.32 }, 0.7);''', '20% 60%')

# ---------- 5 CTA ----------
S['05-cta'] = (4.6, '''
.brand¤ { position:absolute; left:90px; top:250px; display:flex; align-items:center; gap:26px; font-family:"Bricolage Grotesque"; font-weight:800; font-size:76px; letter-spacing:-.03em; }
.pillw¤ { position:absolute; left:90px; top:470px; }
.t¤ { position:absolute; left:90px; right:90px; top:600px; font-size:178px; }
.s¤ { position:absolute; left:90px; right:90px; top:1010px; font-size:46px; line-height:1.3; color:#A9B4CA; }
.s¤ b { color:#E9EEF7; }
.btnw¤ { position:absolute; left:90px; right:90px; top:1250px; }
.url¤ { position:absolute; left:0; right:0; top:1460px; text-align:center; font-family:"JetBrains Mono"; font-size:40px; color:#2FD47E; }
''', '''  <div § class="brand¤"><div class="logo¤" style="width:116px;height:116px;font-size:66px">D</div>Dyno</div>
  <div § class="pillw¤"><span class="pill¤"><span class="dot¤"></span>Plano Premium · R$ 39,90/mês</span></div>
  <div § class="h¤ t¤">Modo <span class="g¤">família.</span></div>
  <div § class="s¤"><b>60 dias grátis no Beta.</b> No Beta, a equipe do Dyno ativa o Modo família para você.</div>
  <div § class="btnw¤"><div class="btn¤">💬 Peça no WhatsApp do Dyno</div></div>
  <div § class="url¤">dynoapp.com.br/precos</div>''', '''  tl.fromTo(one('.brand¤'), { y: -30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: 'power2.out' }, 0.05);
  tl.fromTo(one('.pillw¤'), { scale: 0, transformOrigin: '0% 50%' }, { scale: 1, duration: 0.45, ease: 'back.out(2)' }, 0.3);
  tl.fromTo(one('.t¤'), { y: 70, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: 'power3.out' }, 0.5);
  tl.fromTo(one('.s¤'), { opacity: 0 }, { opacity: 1, duration: 0.4 }, 1.0);
  tl.fromTo(one('.btnw¤'), { y: 80, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: 'back.out(1.6)' }, 1.3);
  tl.to(one('.btn¤'), { scale: 1.04, duration: 0.3, yoyo: true, repeat: 3, ease: 'sine.inOut' }, 2.0);
  tl.fromTo(one('.url¤'), { opacity: 0 }, { opacity: 1, duration: 0.4 }, 1.6);''', '50% 40%')

scenes = [('01-hook', 0, 4.6), ('02-painel', 4.3, 6.0), ('03-conversa', 10.0, 7.0), ('04-beneficios', 16.7, 4.8), ('05-cta', 21.2, 4.6)]
TOTAL = 25.8
for cid, (dur, css, body, js, glow) in S.items():
    open(f'compositions/frames/{cid}.html', 'w').write(comp(cid, dur, css, body, js, glow))
trans = '''        tl.fromTo("#el-02-painel", { clipPath: "circle(0% at 50% 60%)" }, { clipPath: "circle(80% at 50% 60%)", duration: 0.45, ease: "power3.inOut" }, 4.3);
        tl.fromTo("#el-03-conversa", { clipPath: "inset(0% 0% 0% 100%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.4, ease: "power3.inOut" }, 10.0);
        tl.to("#el-02-painel", { x: -160, duration: 0.4, ease: "power3.inOut" }, 10.0);
        tl.fromTo("#el-04-beneficios", { clipPath: "inset(100% 0% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.4, ease: "power3.inOut" }, 16.7);
        tl.to("#el-03-conversa", { y: -180, duration: 0.4, ease: "power3.inOut" }, 16.7);
        tl.fromTo("#el-05-cta", { clipPath: "circle(0% at 50% 50%)" }, { clipPath: "circle(80% at 50% 50%)", duration: 0.45, ease: "power3.inOut" }, 21.2);'''
open('index.html', 'w').write(index('familia', TOTAL, scenes, trans))
