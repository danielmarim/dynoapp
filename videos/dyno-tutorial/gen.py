#!/usr/bin/env python3
"""Vídeo tutorial (~39 s, 1080x1920) para os Beta testers: como usar o Dyno."""
import os, shutil, json
SRC = "/home/claude/videos/dyno-destaques/gen.py"
code = open(SRC, encoding="utf-8").read().split("STORIES = {")[0]
code = code.replace('ROOT = os.path.dirname(os.path.abspath(__file__))', 'ROOT = "/home/claude/videos/dyno-tutorial"')
exec(code)
ICONS["d"] = '<path d="M34 24h18a26 26 0 0 1 0 52H34z"/>'

STEP_CSS = """.{p}-step { display:flex; align-items:center; gap:36px; font-size:46px; font-weight:700; }
.{p}-n { flex:none; width:110px; height:110px; border-radius:50%; background:#14B37D; display:flex; align-items:center; justify-content:center; font-family:"Bodoni Moda",serif; font-size:64px; color:#1B1F3B; }"""
BAR_CSS = """.{p}-row { display:flex; justify-content:space-between; font-size:40px; font-weight:700; margin-top:14px; }
.{p}-track { height:26px; border-radius:13px; background:#EDE6DA; margin-top:10px; overflow:hidden; }
.{p}-track i { display:block; height:100%; border-radius:13px; background:#14B37D; }"""
E_CSS = """.{p}-e { display:inline-block; }
.{p}-foot { position:absolute; left:86px; right:86px; top:1470px; font-size:38px; font-weight:700; letter-spacing:.08em; text-transform:uppercase; opacity:.6; }"""
CTA_CSS = """.{p}-try { position:absolute; left:90px; right:90px; top:1290px; text-align:center; background:#FFF6EA; color:#1B1F3B; border:5px solid #14B37D; border-radius:44px; padding:30px 36px; font-size:46px; font-weight:700; }
.{p}-small { position:absolute; left:60px; right:60px; top:1700px; text-align:center; font-size:36px; color:#A9ADC6; }"""

SCENES = [
  (True, cover("chat", "Bem-vindo!", "seu guia rápido do Dyno"), "", 4.5),
  (False, head("comece aqui", "3 passos") + "".join(
      f'  <div class="{{p}}-card {{p}}-step" style="top:{620 + i * 250}px" data-in="card" data-t="{0.5 + i * 0.5}"><b class="{{p}}-n">{i + 1}</b><span>{t}</span></div>\n'
      for i, t in enumerate(["Salve o contato do Dyno", "Mande texto, áudio ou foto", "Ele anota, organiza e lembra"])), STEP_CSS, 4.5),
  (False, head("gastos", "Gastou? Só avisa") + me("uber 23 pra casa 🚗", 620, 0.5)
     + dy("Anotado! R$ 23 em transporte", 790, 1.0) + me("🎤 ▶︎ ▬▬▬▬▬ 0:06", 1060, 1.8)
     + dy("Anotei R$ 32 na padaria 🥐", 1230, 2.4), "", 5),
  (False, head("foto ou pdf", "Manda a foto") + me("📷 nota do mercado", 620, 0.5)
     + dy("R$ 186,40 em mercado ✅", 790, 1.0) + me("📄 boleto da luz", 1060, 1.8)
     + dy("Conta de luz R$ 187,90, vence dia 10. Te aviso antes ✅", 1230, 2.4), "", 5),
  (False, head("acompanhe", "Resumo do mês") + me("quanto gastei esse mês?", 620, 0.5)
     + '  <div class="{p}-card" style="top:790px" data-in="pop" data-t="1.0"><span class="{p}-who">Dyno · outubro</span>'
     + "".join(f'<div class="{{p}}-row"><span>{c}</span><b>R$ {v}</b></div><div class="{{p}}-track"><i style="width:{w}%" data-in="bar" data-t="{1.4 + i * 0.2}"></i></div>'
               for i, (c, v, w) in enumerate([("Mercado", "620", 100), ("Contas", "480", 77), ("Transporte", "190", 31), ("Lazer", "150", 24)]))
     + '</div>\n' + dy("Peça também o dashboard em imagem 📊", 1400, 2.8, bg="#FFB98B"), BAR_CSS, 5),
  (False, head("lembretes", "É só pedir") + me("me lembra de pagar a luz dia 10 às 9h", 620, 0.5)
     + '  <div class="{p}-bub {p}-dy" style="top:850px" data-in="left" data-t="1.2"><span class="{p}-who">Dyno · 09:00</span><span class="{p}-e" data-shake="1.6">⏰</span> Pagar a conta de luz</div>\n'
     + '  <div class="{p}-bub {p}-dy" style="top:1080px;background:#FFB98B" data-in="pop" data-t="2.1"><span class="{p}-who">Dyno · 09:10</span><span class="{p}-e" data-shake="2.5">🔔</span> Ainda não vi seu ok…</div>\n'
     + '  <div class="{p}-bub {p}-me" style="top:1330px;font-size:60px" data-in="right" data-t="3.0">paguei ✅</div>\n', E_CSS, 5),
  (False, head("listas e tarefas", "Organiza tudo") + me("lista do mercado: arroz, café e leite", 620, 0.5)
     + dy("Lista criada 📝 3 itens", 850, 1.1) + me("tarefa: renovar o seguro do carro até sexta", 1080, 1.9)
     + dy("Tarefa anotada para sexta ✅", 1310, 2.5), "", 5),
  (False, head("área do cliente", "Seu painel")
     + '  <div class="{p}-card" style="top:640px" data-in="card" data-t="0.5"><span class="{p}-who">no site</span><b style="font-family:\'Bodoni Moda\',serif;font-size:64px">dynoapp.com.br</b><br><span style="font-size:42px;line-height:1.4">Entre com seu WhatsApp e veja gastos, contas e lembretes num só lugar.</span></div>\n'
     + '  <div class="{p}-foot" style="top:1180px" data-in="up" data-t="1.4">seus dados são só seus 🔒</div>\n', E_CSS, 4.5),
  (True, cover("d", "Experimente", "comece agora pelo WhatsApp")
     + '  <div class="{p}-try" data-in="up" data-t="1.0">Mande: “gastei 30 no almoço”</div>\n'
     + '  <div class="{p}-small" data-in="fade" data-t="1.8">Dúvidas? É só perguntar ao Dyno</div>\n', CTA_CSS, 5),
]
# remove a marca padrão da capa final (fica no lugar do aviso)
SCENES[-1] = (True, SCENES[-1][1].replace('<div class="{p}-brand" data-in="fade" data-t="1.4"><span class="{p}-mk">D</span>Dyno</div>', ''), SCENES[-1][2], SCENES[-1][3])

proj = ROOT
for f in ["package.json", "hyperframes.json", "CLAUDE.md", "AGENTS.md"]:
    s = os.path.join(TEMPLATE, f)
    if os.path.exists(s): shutil.copy(s, proj)
for d in ["assets/fonts", "assets/js"]:
    shutil.copytree(os.path.join(TEMPLATE, d), os.path.join(proj, d), dirs_exist_ok=True)
os.makedirs(os.path.join(proj, "assets", "audio"), exist_ok=True)

starts, t = [], 0.0
for (_, _, _, dur) in SCENES:
    starts.append(round(t, 2)); t += dur - 0.5
TOTAL = round(starts[-1] + SCENES[-1][3], 2)
os.system(f'ffmpeg -v error -y -i /home/claude/videos/dyno-destaques/financas/assets/audio/heygen.wav -t {TOTAL} -af "afade=t=in:d=0.4,afade=t=out:st={TOTAL - 2}:d=2" {proj}/assets/audio/bgm.wav')
ids = []
for i, (navy, body, css, dur) in enumerate(SCENES):
    fid = f"{i + 1:02d}-tutorial"
    ids.append(fid)
    write_frame(proj, fid, dur, body, navy, css)
divs = "\n".join(
    f'      <div id="el-{fid}" class="scene" data-composition-id="{fid}" data-composition-src="compositions/frames/{fid}.html" data-start="{starts[i]}" data-duration="{SCENES[i][3]}" data-track-index="{i % 2}"></div>'
    for i, fid in enumerate(ids))
tr = []
for i in range(1, len(ids)):
    s = starts[i]
    tr.append(f'        tl.to("#el-{ids[i-1]}", {{ opacity: 0, duration: 0.5, ease: "power2.inOut" }}, {s});')
    if i % 2:
        tr.append(f'        tl.fromTo("#el-{ids[i]}", {{ clipPath: "inset(100% 0% 0% 0%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", duration: 0.5, ease: "power3.inOut" }}, {s});')
    else:
        tr.append(f'        tl.fromTo("#el-{ids[i]}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5, ease: "power2.inOut" }}, {s});')
tr.append(f'        tl.to({{}}, {{ duration: {TOTAL} }}, 0);')
html = f"""<!doctype html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/js/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #000; }}
      #root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #1B1F3B; }}
      .scene {{ position: absolute; inset: 0; width: 100%; height: 100%; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
{divs}
      <audio id="el-bgm" src="assets/audio/bgm.wav" data-start="0" data-duration="{TOTAL}" data-track-index="11" data-volume="0.7"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
      (function () {{ var tl = window.__timelines["main"];
{chr(10).join(tr)}
      }})();
    </script>
  </body>
</html>
"""
open(os.path.join(proj, "index.html"), "w", encoding="utf-8").write(html)
json.dump({"id": "dyno-tutorial-beta", "name": "Dyno tutorial Beta"}, open(os.path.join(proj, "meta.json"), "w"))
print("total", TOTAL)
