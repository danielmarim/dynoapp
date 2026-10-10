exec(open('/home/claude/videos/_dark/base_dark.py').read())
S = {}
# Zonas seguras do Stories: topo 0-250 e base 1580-1920 ficam livres.

S['01-abre'] = (2.8, '''
.brand¤ { position:absolute; left:0; right:0; top:560px; display:flex; justify-content:center; align-items:center; gap:28px; font-family:"Bricolage Grotesque"; font-weight:800; font-size:86px; letter-spacing:-.03em; }
.t¤ { position:absolute; left:80px; right:80px; top:780px; font-size:150px; text-align:center; }
.eb¤ { position:absolute; left:0; right:0; top:1180px; text-align:center; }
''', '''  <div § class="brand¤"><div class="logo¤" style="width:130px;height:130px;font-size:74px">D</div>Dyno</div>
  <div § class="h¤ t¤">Novidades <span class="g¤">no ar.</span></div>
  <div § class="eb¤">5 funções novas · outubro</div>''', '''  tl.fromTo(one('.brand¤'), { scale: 0.6, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.55, ease: 'back.out(1.8)' }, 0.1);
  tl.fromTo(one('.t¤'), { y: 70, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: 'power3.out' }, 0.6);
  tl.fromTo(one('.eb¤'), { opacity: 0 }, { opacity: 1, duration: 0.4 }, 1.3);''', '50% 45%')

itens = [('💊', 'Remédio com confirmação', 'a Dina pergunta "já tomou?" e registra'),
         ('💳', 'Fatura do cartão com parcelas', 'foto ou PDF, parcelas separadas'),
         ('🔎', 'Aviso de gasto fora do normal', 'compara com os seus meses anteriores'),
         ('🎭', 'Personalidades', 'padrão, zen, profissional, coach, extrovertido'),
         ('🔊', 'Voz no mesmo tom', 'responde por áudio do jeito que você escolheu')]
lh = ''.join(f'''    <div § class="it¤ i¤{i}"><div class="ic¤">{e}</div><div class="tx¤"><b>{t}</b><span>{s}</span></div><div class="ck¤ c¤{i}">✓</div></div>
''' for i, (e, t, s) in enumerate(itens))
S['02-lista'] = (9.4, '''
.eb¤ { position:absolute; left:90px; top:300px; }
.t¤ { position:absolute; left:90px; right:90px; top:350px; font-size:96px; }
.list¤ { position:absolute; left:80px; right:80px; top:600px; display:flex; flex-direction:column; gap:22px; }
.it¤ { display:flex; align-items:center; gap:24px; padding:26px 30px; background:#0B1220; border:2px solid rgba(160,185,225,.16); border-radius:32px; }
.ic¤ { width:84px; height:84px; border-radius:24px; background:rgba(47,212,126,.12); display:flex; align-items:center; justify-content:center; font-size:46px; flex:none; }
.tx¤ { flex:1; min-width:0; }
.tx¤ b { display:block; font-family:"Bricolage Grotesque"; font-weight:800; font-size:42px; letter-spacing:-.02em; line-height:1.05; }
.tx¤ span { display:block; font-size:28px; color:#A9B4CA; margin-top:6px; }
.ck¤ { width:64px; height:64px; border-radius:50%; border:3px solid rgba(160,185,225,.3); display:flex; align-items:center; justify-content:center; font-size:36px; font-weight:800; color:#04210F; flex:none; }
''', f'''  <div § class="eb¤">O que chegou</div>
  <div § class="h¤ t¤">Já está no seu <span class="g¤">WhatsApp.</span></div>
  <div § class="list¤">
{lh}  </div>''', '''  tl.fromTo([one('.eb¤'), one('.t¤')], { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: 'power3.out', stagger: 0.1 }, 0.15);
  all('.it¤').forEach((el, i) => {
    tl.fromTo(el, { x: 140, opacity: 0 }, { x: 0, opacity: 1, duration: 0.45, ease: 'power3.out' }, 0.7 + i * 1.5);
    tl.to(one('.c¤' + i), { backgroundColor: '#2FD47E', borderColor: '#2FD47E', scale: 1.15, duration: 0.25, ease: 'back.out(2)' }, 1.35 + i * 1.5);
    tl.to(one('.c¤' + i), { scale: 1, duration: 0.2 }, 1.6 + i * 1.5);
  });''', '50% 55%')

S['03-cta'] = (3.0, '''
.t¤ { position:absolute; left:80px; right:80px; top:560px; font-size:124px; text-align:center; }
.s¤ { position:absolute; left:80px; right:80px; top:1010px; text-align:center; font-size:46px; font-weight:600; color:#A9B4CA; line-height:1.3; }
.btnw¤ { position:absolute; left:120px; right:120px; top:1200px; }
.pw¤ { position:absolute; left:0; right:0; top:1400px; text-align:center; }
''', '''  <div § class="h¤ t¤">Quer <span class="g¤">testar?</span></div>
  <div § class="s¤">Manda <b style="color:#E9EEF7">"quero testar"</b> no WhatsApp do Dyno</div>
  <div § class="btnw¤"><div class="btn¤">dynoapp.com.br →</div></div>
  <div § class="pw¤"><span class="pill¤"><span class="dot¤"></span>Beta · 60 dias grátis</span></div>''', '''  tl.fromTo(one('.t¤'), { y: 70, opacity: 0 }, { y: 0, opacity: 1, duration: 0.55, ease: 'power3.out' }, 0.15);
  tl.fromTo(one('.s¤'), { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: 'power2.out' }, 0.6);
  tl.fromTo(one('.btnw¤'), { y: 80, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: 'back.out(1.6)' }, 1.0);
  tl.to(one('.btn¤'), { scale: 1.04, duration: 0.3, yoyo: true, repeat: 3, ease: 'sine.inOut' }, 1.6);
  tl.fromTo(one('.pw¤'), { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.4 }, 1.5);''', '50% 45%')

scenes = [('01-abre', 0, 2.8), ('02-lista', 2.6, 9.4), ('03-cta', 11.8, 3.0)]
TOTAL = 14.0
for cid, (dur, css, body, js, glow) in S.items():
    open(f'compositions/frames/{cid}.html', 'w').write(comp(cid, dur, css, body, js, glow))
trans = '''        tl.fromTo("#el-02-lista", { clipPath: "inset(0% 0% 0% 100%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.4, ease: "power3.inOut" }, 2.6);
        tl.fromTo("#el-03-cta", { clipPath: "circle(0% at 50% 50%)" }, { clipPath: "circle(90% at 50% 50%)", duration: 0.45, ease: "power3.inOut" }, 11.8);'''
open('index.html', 'w').write(index('stories-novidades', TOTAL, scenes, trans))
