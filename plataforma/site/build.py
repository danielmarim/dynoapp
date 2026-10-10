#!/usr/bin/env python3
"""Monta o site estático do Dyno (www/) a partir de um layout comum."""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "www")
WA = "https://wa.me/5511939497178"
IG_DM = "https://ig.me/m/dynoapp.ia"
IG = "https://instagram.com/dynoapp.ia"

ICON = {
    "money": '<circle cx="12" cy="12" r="9"/><path d="M15 9.2c-.5-1-1.6-1.6-2.8-1.6-1.6 0-2.7.8-2.7 2s1.1 1.8 2.7 2.1 3 .9 3 2.3-1.3 2.3-2.9 2.3c-1.3 0-2.4-.6-2.9-1.6M12 6v1.6M12 16.4V18"/>',
    "bell": '<path d="M6.5 17V11a5.5 5.5 0 0 1 11 0v6l1.5 1.5h-14z"/><path d="M10 21a2 2 0 0 0 4 0M12 3.5v1.5"/>',
    "check": '<rect x="4" y="4" width="16" height="16" rx="4"/><path d="m8.5 12.5 2.5 2.5 5-6"/>',
    "bill": '<path d="M6 3h12v18l-3-2-3 2-3-2-3 2z"/><path d="M9 8h6M9 12h6M9 16h3"/>',
    "chart": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
    "people": '<circle cx="9" cy="8" r="3.2"/><path d="M3 19c.6-3.2 3-5 6-5s5.4 1.8 6 5"/><circle cx="17" cy="9" r="2.5"/><path d="M16 14c2.6.2 4.4 1.8 5 4.5"/>',
    "car": '<path d="M5 16V12l2-5h10l2 5v4z"/><circle cx="8" cy="16.5" r="1.8"/><circle cx="16" cy="16.5" r="1.8"/><path d="M5 12h14"/>',
    "mic": '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5.5 11a6.5 6.5 0 0 0 13 0M12 17.5V21"/>',
    "shield": '<path d="M12 3 5 6v5c0 4.5 3 8.3 7 10 4-1.7 7-5.5 7-10V6z"/><path d="m9 12 2 2 4-4"/>',
    "phone": '<rect x="7" y="2.5" width="10" height="19" rx="2.5"/><path d="M11 18.5h2"/>',
    "building": '<path d="M4 21V6l8-3v18M12 21h8V9l-8-2"/><path d="M7 9h2M7 13h2M7 17h2M15 12h2M15 16h2"/>',
    "door": '<path d="M5 21V4h10v17"/><path d="M15 6h4v15M3 21h18M12 12.5v.5"/>',
    "lock": '<rect x="5" y="10" width="14" height="10" rx="3"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>',
}


def ico(n, bg="var(--mint)"):
    return f'<div class="ico" style="background:{bg}" aria-hidden="true"><svg viewBox="0 0 24 24">{ICON[n]}</svg></div>'


APPNAV = f"""<nav class="nav nav-app" id="nav">
    <a href="/funcionalidades">O que pedir</a><a href="/duvidas">Ajuda</a><a href="{WA}" rel="noopener">WhatsApp do Dyno</a>
    <span class="user-chip" title="Conectado"><span class="av" id="u-av" aria-hidden="true">•</span><span id="u-nome">Minha área</span></span>
    <button class="btn btn-dark btn-sm" id="sair">Sair</button>
  </nav>"""
LOGADOJS = """<script>(function(){try{var n=localStorage.getItem('dyno_nome');if(n===null)return;var a=document.getElementById('nav-entrar');if(!a)return;a.href='/conta';a.textContent='';var s=document.createElement('span');s.className='av';s.textContent=(n||'D').charAt(0).toUpperCase();a.appendChild(s);a.appendChild(document.createTextNode(' Minha área'));a.classList.add('logado');}catch(e){}})();</script>"""


def page(path, title, desc, body, nav="", scripts="", noindex=False, app=False):
    links = [("/", "Início"), ("/como-funciona", "Como funciona"), ("/funcionalidades", "Funcionalidades"), ("/precos", "Preços"), ("/duvidas", "Dúvidas")]
    navhtml = "".join(f'<a href="{h}"{" aria-current=page" if h == nav else ""}>{t}</a>' for h, t in links)
    html = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{'<meta name="robots" content="noindex">' if noindex else ''}
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://dynoapp.com.br{path if path != '/index' else '/'}">
<meta property="og:site_name" content="Dyno">
<meta property="og:locale" content="pt_BR">
<meta property="og:image" content="https://dynoapp.com.br/og-dyno.png?v=1">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Logo do Dyno: círculo verde com a letra D">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://dynoapp.com.br/og-dyno.png?v=1">
<meta name="theme-color" content="#1B1F3B">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css?v=9">
</head>
<body>
<a class="sr" href="#conteudo">Pular para o conteúdo</a>
<header class="top"><div class="wrap">
  <a class="brand" href="/" aria-label="Dyno, página inicial"><span class="mark">D</span>Dyno</a>
  {APPNAV if app else f'<nav class="nav" id="nav">{navhtml}<a class="btn btn-dark btn-sm" href="/entrar" id="nav-entrar">Entrar</a></nav>'}
  <button class="menu-btn" aria-controls="nav" aria-expanded="false" onclick="var n=document.getElementById('nav');n.classList.toggle('open');this.setAttribute('aria-expanded',n.classList.contains('open'))">Menu</button>
</div></header>
<main id="conteudo">
{body}
</main>
<footer><div class="wrap">
  <div><a class="brand" href="/"><span class="mark">D</span>Dyno</a><p style="margin-top:12px;max-width:340px">Dyno e Dina, seus assessores pessoais no WhatsApp: o Dyno cuida do dinheiro e a Dina, da agenda e da rotina. Por texto, áudio ou foto.</p></div>
  <div><b style="color:#fff">Produto</b><a href="/como-funciona">Como funciona</a><a href="/funcionalidades">Funcionalidades</a><a href="/precos">Preços</a><a href="/duvidas">Dúvidas</a><a href="/entrar">Área do cliente</a></div>
  <div><b style="color:#fff">Contato</b><a href="{IG}" rel="noopener">Instagram @dynoapp.ia</a><a href="{WA}" rel="noopener">WhatsApp do Dyno</a><a href="/termos">Termos de uso</a><a href="/privacidade">Privacidade</a></div>
  <div class="copy">© 2026 Dyno · DM OBSERVAIT SOLUCOES EM TECNOLOGIA LTDA · CNPJ 65.176.391/0001-45 · Curitiba/PR · <a href="mailto:privacidade@dynoapp.com.br">privacidade@dynoapp.com.br</a>. Beta fechado; lançamento público previsto para 01/12/2026.</div>
</div></footer>
{"" if app else LOGADOJS}{scripts}
</body>
</html>
"""
    fn = os.path.join(OUT, (path.strip("/") or "index") + ".html")
    os.makedirs(os.path.dirname(fn), exist_ok=True)
    open(fn, "w", encoding="utf-8").write(html)


CHAT = """<div class="phone" aria-label="Exemplo de conversa com o Dyno no WhatsApp"><div class="screen">
  <div class="chat-head"><span class="mark" style="width:34px;height:34px;font-size:20px">D</span><div><b>Dyno &amp; Dina</b><small data-status>online</small></div></div>
  <div class="b me">gastei 45 no mercado 🛒</div>
  <div class="b dy"><small>Dyno</small>Prontinho! R$ 45 em mercado. Você já usou 62% do limite do mês.</div>
  <div class="b me">🎤 me lembra de pagar a luz dia 10</div>
  <div class="b dy dina"><small>Dina</small>Combinado ⏰ Dia 10, às 9h. Se você não responder, eu lembro de novo.</div>
  <div class="b dy al"><small>Dina · 09:10</small>🔔 Ainda não vi seu ok da conta de luz…</div>
  <div class="b me">paguei ✅</div>
</div></div>"""

FEATURES = [
    ("money", "var(--mint)", "Gastos sem planilha", "Mande um texto, um áudio ou a foto do comprovante. O Dyno entende, categoriza e soma.", "“uber 23 pra casa” → R$ 23 em transporte"),
    ("bell", "var(--peach)", "Lembretes que insistem", "Ele avisa na hora certa e, se você não confirmar, lembra de novo até você fazer.", "“me lembra do remédio todo dia às 8h”"),
    ("bill", "#fff", "Contas a pagar", "Boletos e contas com vencimento: ele avisa antes e marca como paga quando você confirma.", "“conta de luz 180 vence dia 10”"),
    ("check", "var(--mint)", "Tarefas e listas", "Anote tarefas, prazos e listas de compras sem sair do WhatsApp.", "“coloca leite e café na lista”"),
    ("chart", "var(--peach)", "Resumo do mês", "Peça um painel com gastos por categoria, maiores despesas e assinaturas. Também no site.", "“me mostra o resumo do mês”"),
    ("people", "#fff", "No grupo da família", "Coloque o Dyno no grupo e organizem juntos as contas e os lembretes da casa.", "“quem pagou a internet?”"),
]


def features_html(n=6):
    return "".join(f'<div class="card">{ico(i, bg)}<h3>{t}</h3><p>{d}</p><div class="ex">{e}</div></div>' for i, bg, t, d, e in FEATURES[:n])


SELOS = [
    ("shield", "var(--mint)", "Dados protegidos pela LGPD", "Usamos seus dados só para prestar o serviço. Peça cópia ou exclusão quando quiser."),
    ("lock", "var(--peach)", "Não mexe no seu dinheiro", "O Dyno só anota e organiza. Ele não acessa sua conta no banco nem faz pagamentos."),
    ("phone", "#fff", "Número exclusivo do Dyno", "Um número só nosso: +55 11 93949-7178. Salve o contato e desconfie de outros."),
    ("building", "var(--mint)", "Empresa brasileira", "DM OBSERVAIT · CNPJ 65.176.391/0001-45 · Curitiba/PR."),
    ("door", "var(--peach)", "Sem fidelidade", "Cancele pela área do cliente quando quiser, sem multa."),
]
SELOS_HTML = f"""<section style="padding-top:0"><div class="wrap">
  <div class="sec-head"><span class="kicker">Pode confiar</span><h2 class="h">Feito para ser seguro.</h2></div>
  <div class="selos">{''.join(f'<div class="selo">{ico(i, bg)}<div><b>{t}</b><p>{d}</p></div></div>' for i, bg, t, d in SELOS)}</div>
</div></section>"""

COMPARA = """<section style="padding-top:0"><div class="wrap">
  <div class="sec-head"><span class="kicker">Compare</span><h2 class="h">Mesmo assessor no WhatsApp. Quase metade do preço.</h2><p>Veja quanto custa o principal assistente do mercado e quanto custa o Dyno.</p></div>
  <div class="compara">
    <div class="cmp-col"><span class="kicker" style="color:var(--muted)">Principal concorrente*</span>
      <div class="cmp-row"><span>Plano anual</span><b>R$ 358,80</b></div>
      <div class="cmp-row"><span>Por mês</span><b>R$ 29,90</b></div>
      <div class="cmp-row"><span>Para testar</span><b>7 dias de garantia</b></div></div>
    <div class="cmp-col dy"><span class="kicker" style="color:var(--lime)">Dyno</span>
      <div class="cmp-row"><span>Plano anual</span><b>R$ 199,90</b></div>
      <div class="cmp-row"><span>Por mês</span><b>R$ 16,66</b></div>
      <div class="cmp-row"><span>Para testar</span><b>60 dias grátis no Beta</b></div>
      <div class="cmp-save">Você economiza <b>R$ 158,90 por ano</b></div></div>
  </div>
  <p class="note" style="margin-top:16px">*Plano anual em 12x de R$ 29,90 de um assistente de IA no WhatsApp com grande presença no mercado, consultado em outubro de 2026. O Dyno também tem plano mensal de R$ 19,90, sem fidelidade.</p>
</div></section>"""

DUPLA = """<section style="padding-top:0"><div class="wrap">
  <div class="sec-head"><span class="kicker">Conheça a dupla</span><h2 class="h">Dois assessores. Uma conversa só.</h2><p>No mesmo número do WhatsApp, o Dyno cuida do seu dinheiro e a Dina cuida da sua agenda e rotina. Fale normalmente: quem responde é quem entende do assunto. Quer falar com um deles? É só chamar pelo nome.</p></div>
  <div class="dupla">
    <div class="duo"><div class="duo-top"><span class="mark duo-mark">D</span><div><b>Dyno</b><small>o do dinheiro 💰</small></div></div>
      <ul class="list"><li>Gastos por texto, áudio ou foto</li><li>Contas a pagar e boletos</li><li>Limites por categoria e alertas</li><li>Extrato, parcelados e quem te deve</li><li>Resumo e painel do mês</li><li>Alerta de dólar e euro</li></ul>
      <div class="ex">“Dyno, quanto gastei com iFood?”</div></div>
    <div class="duo dina"><div class="duo-top"><span class="mark duo-mark">D</span><div><b>Dina</b><small>a da agenda e da rotina ⏰</small></div></div>
      <ul class="list"><li>Lembretes que insistem até você fazer</li><li>Compromissos e agenda do dia</li><li>Tarefas e projetos</li><li>Listas e notas</li><li>Manutenções da casa e do carro</li></ul>
      <div class="ex">“Dina, o que eu tenho amanhã?”</div></div>
  </div>
</div></section>"""

CAMBIO = """<section style="padding-top:0"><div class="wrap">
  <div class="cambio">
    <div><span class="kicker">Novidade · alerta de câmbio</span><h2 class="h">O dólar caiu? O Dyno te avisa.</h2>
      <p class="lead" style="font-size:18px">Diga o valor que você quer pagar no dólar ou no euro. O Dyno confere a cotação a cada 15 minutos nos dias úteis e te chama no WhatsApp quando chegar lá.</p>
      <ul class="list"><li>“me avisa quando o dólar ficar abaixo de 4,90”</li><li>“me avisa se o euro passar de 6”</li><li>“quanto tá o dólar hoje?”</li><li>“cancela meus alertas de câmbio”</li></ul>
      <p class="note">Ideal para quem vai viajar ou compra lá fora. É só aviso de cotação, não é recomendação de investimento.</p></div>
    <div class="phone" style="margin:0 auto"><div class="screen" style="min-height:auto">
      <div class="b me">me avisa quando o dólar ficar abaixo de 4,90</div>
      <div class="b dy"><small>Dyno</small>Combinado! Hoje está em R$ 4,98. Te aviso quando ficar abaixo de R$ 4,90 💵</div>
      <div class="b dy al"><small>Dyno · 2 dias depois</small>💵 O dólar chegou a <b>R$ 4,88</b>. Você pediu aviso abaixo de R$ 4,90. 📉 -2,1% na semana.</div>
    </div></div>
  </div>
</div></section>"""

HOMEJS = '<script src="/assets/home.js?v=1" defer></script>'

OFFER = f"""<section class="band"><div class="wrap">
  <div class="sec-head"><span class="kicker">Beta fechado</span><h2 class="h">Teste o Dyno antes de todo mundo.</h2>
  <p>Estamos abrindo poucas vagas para quem quer usar de verdade e dizer o que achou.</p></div>
  <div class="tiles"><div class="tile"><b data-vagas>10</b><span data-vagas-txt>vagas no Beta</span></div><div class="tile hi"><b>60 dias</b><span>grátis para usar</span></div><div class="tile"><b>1</b><span>pedido: seu feedback sincero</span></div></div>
  <p style="margin-top:22px;color:#D9DAE6">Depois do teste: R$ 19,90 por mês ou R$ 199,90 no plano anual. Quem não quiser continuar, é só sair, sem custo algum.</p>
  <div class="cta-row"><a class="btn btn-primary" href="/beta">Quero participar</a><a class="btn btn-ghost" href="{WA}?text=Tenho%20um%20convite" rel="noopener">Já tenho convite</a></div>
</div></section>"""

# ---------- Início ----------
page("/index", "Dyno · Seu assessor pessoal no WhatsApp", "Gastos, contas, lembretes e tarefas organizados por mensagem, áudio ou foto, direto no WhatsApp. Beta com 60 dias grátis.", f"""
<section class="hero dots"><div class="wrap">
  <div>
    <span class="pill">Beta fechado · 60 dias grátis<span data-vagas-pill></span></span>
    <h1 class="h">Seu assessor pessoal <em>no WhatsApp.</em></h1>
    <p class="lead">Você fala, o Dyno anota. Gastos, contas, lembretes e tarefas organizados por mensagem, áudio ou foto do comprovante, sem baixar nenhum app.</p>
    <div class="cta-row"><a class="btn btn-primary" href="/beta">Quero participar do Beta</a><a class="btn btn-ghost" href="/como-funciona">Ver como funciona</a></div>
    <p class="note">Já é cliente? <a href="/entrar">Entre na sua área</a> com um código enviado pelo WhatsApp.</p>
  </div>
  {CHAT}
</div></section>
<section><div class="wrap">
  <div class="sec-head"><span class="kicker">O que ele faz</span><h2 class="h">Tudo o que você ia anotar, ele anota.</h2><p>Converse do seu jeito. O Dyno organiza e te lembra na hora certa.</p></div>
  <div class="grid3">{features_html()}</div>
</div></section>
<section style="padding-top:0"><div class="wrap">
  <div class="sec-head"><span class="kicker">Simples assim</span><h2 class="h">Três passos e pronto.</h2></div>
  <div class="steps">
    <div class="step"><h3>Salve o contato</h3><p>Com o convite, você chama o Dyno no WhatsApp e faz o cadastro na própria conversa.</p></div>
    <div class="step"><h3>Fale do seu jeito</h3><p>Texto, áudio ou foto. “Gastei 30 no almoço”, “me lembra amanhã às 9h”, “paguei a luz”.</p></div>
    <div class="step"><h3>Acompanhe tudo</h3><p>Resumos no WhatsApp e um painel na área do cliente, com gastos do mês, contas e lembretes.</p></div>
  </div>
</div></section>
{CAMBIO}
{DUPLA}
{SELOS_HTML}
{COMPARA}
{OFFER}
""", nav="/", scripts=HOMEJS)

# ---------- Como funciona ----------
page("/como-funciona", "Como funciona · Dyno", "Veja como o Dyno organiza gastos, contas, lembretes e tarefas pelo WhatsApp.", f"""
<section class="dots"><div class="wrap">
  <div class="sec-head"><span class="kicker">Como funciona</span><h2 class="h">Uma conversa que se organiza sozinha.</h2><p>O Dyno é um assessor que vive no seu WhatsApp. Você manda mensagens como mandaria para um amigo, e ele transforma isso em registros, lembretes e resumos.</p></div>
  <div class="grid2">
    <div class="card">{ico("mic")}<h3>Texto, áudio ou foto</h3><p>Escreva, grave um áudio ou mande a foto do comprovante ou do boleto. Ele entende o valor, a categoria e a data.</p></div>
    <div class="card">{ico("bell", "var(--peach)")}<h3>Avisos que não te deixam esquecer</h3><p>Lembretes únicos ou recorrentes. Se você não responder “ok”, ele insiste. Dá para adiar com “adiar 30”.</p></div>
    <div class="card">{ico("chart", "#fff")}<h3>Orçamentos e resumos</h3><p>Defina limites por categoria e receba um alerta quando chegar perto. Peça o resumo do mês quando quiser.</p></div>
    <div class="card">{ico("car")}<h3>Casa e carro em dia</h3><p>Manutenções, troca de óleo, IPVA, filtro de água: ele registra e avisa na época certa.</p></div>
  </div>
</div></section>
<section style="padding-top:0"><div class="wrap">
  <div class="sec-head"><span class="kicker">Exemplos</span><h2 class="h">Frases que funcionam</h2></div>
  <div class="grid3">
    <div class="card"><h3>Finanças</h3><ul class="list"><li>gastei 45 no mercado</li><li>recebi 1500 de salário</li><li>quanto gastei esse mês?</li><li>limite de 800 para mercado</li></ul></div>
    <div class="card"><h3>Lembretes</h3><ul class="list"><li>me lembra amanhã às 9h</li><li>todo dia às 8h tomar remédio</li><li>adiar 30</li><li>ok, feito</li></ul></div>
    <div class="card"><h3>Organização</h3><ul class="list"><li>tarefa: renovar CNH até sexta</li><li>coloca pão na lista</li><li>conta de luz 180 vence dia 10</li><li>me mostra o resumo</li></ul></div>
  </div>
</div></section>
<section style="padding-top:0"><div class="wrap">
  <div class="card" style="display:flex;gap:20px;align-items:flex-start;flex-wrap:wrap">{ico("lock", "var(--mint)")}<div style="flex:1;min-width:240px"><h3 style="margin-top:0">Seus dados são seus</h3><p>Usamos suas informações só para prestar o serviço. Você pode pedir uma cópia ou a exclusão a qualquer momento. Veja a <a href="/privacidade">Política de privacidade</a>.</p></div></div>
</div></section>
{DUPLA}
{SELOS_HTML}
{OFFER}
""", nav="/como-funciona", scripts=HOMEJS)

# ---------- Preços ----------
page("/precos", "Preços · Dyno", "60 dias grátis no Beta. Depois, R$ 19,90 por mês ou R$ 199,90 por ano. Sem fidelidade.", f"""
<section class="dots"><div class="wrap">
  <div class="sec-head"><span class="kicker">Preços</span><h2 class="h">Simples e sem pegadinha.</h2><p>No Beta você usa <b>60 dias grátis</b>. Depois, escolha o plano que fizer mais sentido. Quem não quiser continuar, é só sair, sem custo algum.</p></div>
  <div class="plans">
    <div class="plan"><span class="kicker">Mensal</span><div class="price">R$ 19,90 <small>/mês</small></div><p>Pague mês a mês e cancele quando quiser.</p>
      <ul><li>Gastos por texto, áudio e foto</li><li>Lembretes que insistem</li><li>Contas a pagar e assinaturas</li><li>Tarefas e listas</li><li>Painel na área do cliente</li></ul></div>
    <div class="plan best"><span class="tag">Economize R$ 38,90</span><span class="kicker" style="color:var(--lime)">Anual</span><div class="price">R$ 199,90 <small>/ano</small></div><p style="color:#D9DAE6">Equivale a R$ 16,66 por mês.</p>
      <ul><li>Tudo do plano mensal</li><li>Um pagamento por ano</li><li>Preço garantido por 12 meses</li></ul></div>
  </div>
  <p class="note" style="margin-top:24px">Sem boleto e sem cobrança no cadastro: no fim dos 60 dias grátis você decide se continua e paga por Pix ou cartão de crédito, processado pelo Asaas. Ao assinar, você concorda com nossos <a href="/termos">Termos de Uso</a> e confirma que leu nossa <a href="/privacidade">Política de Privacidade</a>. Você pode cancelar os pagamentos recorrentes a qualquer momento pela <a href="/entrar">área do cliente</a>.</p>
</div></section>
{COMPARA}
{SELOS_HTML}
{OFFER}
""", nav="/precos", scripts=HOMEJS)

# ---------- Dúvidas ----------
FAQ = [
    ("Quem é a Dina?", "É a parceira do Dyno. No mesmo número e na mesma conversa, o Dyno cuida do dinheiro (gastos, contas, limites, resumo) e a Dina cuida da agenda e da rotina (lembretes, compromissos, tarefas e listas). Você não paga nada a mais por ela. Quer falar com um deles? Comece a mensagem com o nome: “Dina, ...” ou “Dyno, ...”."),
    ("Como funciona o alerta de dólar e euro?", "Mande para o Dyno o valor que você quer, por exemplo “me avisa quando o dólar ficar abaixo de 4,90”. Ele confere a cotação a cada 15 minutos nos dias úteis, das 9h às 18h, e te avisa uma vez quando bater. Dá para ter até 5 alertas e perguntar “quanto tá o dólar?” a qualquer hora. É só informação de cotação, não é recomendação de investimento."),
    ("Preciso baixar algum aplicativo?", "Não. O Dyno funciona direto no seu WhatsApp. O site serve para acompanhar o painel e gerenciar sua assinatura."),
    ("Como entro no Beta?", f'<a href="/beta">Peça sua vaga aqui</a> com seu nome e WhatsApp. Quando o pedido for aprovado, o convite chega pelo <a href="{WA}">WhatsApp do Dyno</a> e o cadastro é feito na própria conversa.'),
    ("Quanto custa?", "No Beta, 60 dias grátis, sem boleto nem cobrança no cadastro. No fim do teste você escolhe se continua: R$ 19,90 por mês ou R$ 199,90 por ano, pagando por Pix ou cartão de crédito. Se não quiser continuar, é só dizer, sem custo."),
    ("Como faço para cancelar?", 'Pela <a href="/entrar">área do cliente</a>, em “Minha conta”, ou falando com a gente. Não há multa nem fidelidade.'),
    ("Funciona em grupo?", "Sim. Dá para usar no grupo da família para dividir contas e lembretes da casa."),
    ("Ele entende áudio e foto?", "Sim. Áudios são transcritos e fotos de comprovantes e boletos são lidas para extrair valor, data e descrição."),
    ("Como entro na área do cliente?", "Digite o seu número de WhatsApp cadastrado. O Dyno manda um código de 6 dígitos para você entrar, sem senha."),
    ("Meus dados ficam seguros?", 'Usamos seus dados apenas para prestar o serviço, com acesso restrito. Você pode pedir cópia ou exclusão quando quiser. Detalhes na <a href="/privacidade">Política de privacidade</a>.'),
]
page("/duvidas", "Dúvidas frequentes · Dyno", "Respostas para as perguntas mais comuns sobre o Dyno, o Beta, preços e privacidade.", f"""
<section class="dots"><div class="wrap" style="max-width:820px">
  <div class="sec-head"><span class="kicker">Dúvidas</span><h2 class="h">Perguntas frequentes</h2></div>
  {''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)}
  <div class="card" style="margin-top:28px"><h3 style="margin-top:0">Ficou alguma dúvida?</h3><p>Fale com a gente no <a href="{IG_DM}">direct do Instagram</a>.</p></div>
</div></section>
""", nav="/duvidas")

# ---------- Termos e privacidade ----------
AVISO = '<div class="aviso"><b>Versão preliminar.</b> Este texto está em revisão jurídica e pode mudar antes do lançamento público. Mudanças relevantes serão avisadas pelo WhatsApp.</div>'
page("/termos", "Termos de uso · Dyno", "Termos de uso do Dyno.", f"""
<section><div class="wrap legal">
  <span class="kicker">Documento</span><h1 class="h">Termos de uso</h1>{AVISO}
  <p>Estes termos regulam o uso do Dyno, assistente pessoal oferecido por DM OBSERVAIT SOLUCOES EM TECNOLOGIA LTDA, CNPJ 65.176.391/0001-45, com sede na Rua Zeila Moura dos Santos, 101, conj. 1105, 11º andar, Cond. Time Work Station, Bloco Work Station, Cristo Rei, Curitiba/PR, CEP 80050-605 (“Dyno”, “nós”). O Dyno é destinado a maiores de 18 anos.</p>
  <h2>1. O serviço</h2><p>O Dyno é um assistente que funciona pelo WhatsApp para registrar gastos, contas, lembretes, tarefas e informações que você enviar, e para apresentar resumos dessas informações no WhatsApp e na área do cliente do site.</p>
  <h2>2. Beta e período grátis</h2><p>Durante o Beta, o acesso é por convite e inclui 60 dias sem custo. No cadastro não emitimos boleto nem geramos cobrança. Perto do fim do período, perguntamos pelo WhatsApp se você quer continuar. A cobrança só começa se você escolher um plano (mensal de R$ 19,90 ou anual de R$ 199,90) e a forma de pagamento. Sem resposta, o atendimento é pausado, sem custo.</p>
  <h2>3. Pagamento e cancelamento</h2><p>Os pagamentos são feitos por Pix ou cartão de crédito e processados pelo Asaas; não emitimos boleto. Ao finalizar o pagamento, você concorda com estes Termos de Uso e confirma que leu a Política de Privacidade. Você pode trocar de plano ou cancelar os pagamentos recorrentes a qualquer momento pela área do cliente, sem multa. O cancelamento interrompe as cobranças futuras.</p>
  <h2>4. Uso adequado</h2><p>Você se compromete a usar o Dyno de forma lícita e a não enviar conteúdo de terceiros sem autorização. O Dyno não substitui orientação financeira, médica ou jurídica profissional.</p>
  <h2>5. Disponibilidade</h2><p>O serviço depende do WhatsApp e de provedores terceiros. Trabalhamos para mantê-lo disponível, mas podem ocorrer interrupções, especialmente durante o Beta.</p>
  <h2>6. Alterações</h2><p>Podemos atualizar estes termos. Avisaremos mudanças relevantes pelo WhatsApp com antecedência.</p>
  <h2>7. Contato</h2><p>privacidade@dynoapp.com.br · Instagram @dynoapp.ia · DM OBSERVAIT SOLUCOES EM TECNOLOGIA LTDA, CNPJ 65.176.391/0001-45, Rua Zeila Moura dos Santos, 101, conj. 1105, 11º andar, Cond. Time Work Station, Bloco Work Station, Cristo Rei, Curitiba/PR, CEP 80050-605.</p>
</div></section>
""")
page("/privacidade", "Política de privacidade · Dyno", "Como o Dyno trata os seus dados pessoais.", f"""
<section><div class="wrap legal">
  <span class="kicker">Documento</span><h1 class="h">Política de privacidade</h1>{AVISO}
  <p>Esta política explica como DM OBSERVAIT SOLUCOES EM TECNOLOGIA LTDA, CNPJ 65.176.391/0001-45 (“Dyno”), trata dados pessoais, nos termos da Lei Geral de Proteção de Dados (Lei 13.709/2018).</p>
  <h2>Quais dados usamos</h2><ul>
    <li><b>Cadastro:</b> nome, número de WhatsApp e e-mail.</li>
    <li><b>Cadastro de pagamento:</b> o CPF é enviado diretamente ao Asaas só para criar seu cadastro de cliente; não o guardamos em nossa base. Nenhuma cobrança é gerada no cadastro.</li>
    <li><b>Uso do serviço:</b> mensagens, gastos, contas, lembretes e tarefas que você envia ao Dyno.</li>
    <li><b>Registro do aceite:</b> data, versão dos termos e um código cifrado do IP.</li>
    <li><b>Login no site:</b> um código temporário enviado ao seu WhatsApp e um cookie de sessão de até 30 dias.</li></ul>
  <h2>Para que usamos</h2><p>Para prestar o serviço que você contratou, processar pagamentos, garantir a segurança e cumprir obrigações legais. Não vendemos seus dados.</p>
  <h2>Com quem compartilhamos</h2><p>Somente com fornecedores necessários ao serviço: o provedor de pagamentos (Asaas), a infraestrutura de banco de dados e hospedagem, o WhatsApp e o provedor de inteligência artificial que interpreta as mensagens (OpenAI). Alguns desses fornecedores processam dados nos Estados Unidos; ao aceitar os termos, você concorda com essa transferência internacional. Não precisamos de dados de saúde, religião, biometria ou senhas: evite enviá-los. Se você contar algo assim, será usado só para te atender.</p>
  <h2>Por quanto tempo</h2><p>Enquanto você for cliente. Registros técnicos são apagados em 7 dias. Dados de pagamento são mantidos pelo prazo exigido pela legislação fiscal. Se você cancelar, pode pedir a exclusão a qualquer momento.</p>
  <h2>Pedido para o Beta</h2><p>Quando você pede uma vaga no Beta pelo site, guardamos seu nome e WhatsApp só para analisar o pedido e enviar o convite pelo WhatsApp do Dyno. Pedidos não aprovados são apagados em até 90 dias.</p>
  <h2>Seus direitos</h2><p>Você pode pedir confirmação, acesso, correção, cópia ou exclusão dos seus dados, além de revogar consentimentos. Responderemos em até 15 dias, após confirmar sua identidade pelo WhatsApp cadastrado.</p>
  <h2>Encarregado (DPO)</h2><p>Daniel Marim · <a href="mailto:privacidade@dynoapp.com.br">privacidade@dynoapp.com.br</a>. Você também pode escrever “privacidade” no WhatsApp do Dyno.</p>
  <h2>Cookies</h2><p>O site usa apenas cookies essenciais: o de sessão da área do cliente e um de preferência técnica. Não usamos cookies de publicidade.</p>
</div></section>
""")

# ---------- Entrar ----------
page("/entrar", "Entrar · Dyno", "Acesse a área do cliente do Dyno com um código enviado pelo WhatsApp.", """
<section class="auth dots"><div class="wrap">
  <div class="auth-card">
    <span class="kicker">Área do cliente</span>
    <h1 class="h">Entrar</h1>
    <form id="f1" novalidate>
      <p>Digite o número de WhatsApp cadastrado. Vamos mandar um código pelo Dyno.</p>
      <label for="tel">WhatsApp com DDD</label>
      <input class="input" id="tel" name="tel" type="tel" inputmode="tel" autocomplete="tel-national" placeholder="(11) 91234-5678" required>
      <div style="margin-top:20px"><button class="btn btn-primary" style="width:100%" type="submit" id="b1">Receber código</button></div>
      <div class="msg" id="m1" role="status"></div>
    </form>
    <form id="f2" novalidate hidden>
      <p>Enviamos um código de 6 dígitos para <b id="numShow"></b> pelo WhatsApp do Dyno.</p>
      <label for="cod">Código</label>
      <input class="input code-input" id="cod" name="cod" inputmode="numeric" autocomplete="one-time-code" maxlength="6" pattern="[0-9]{6}" placeholder="••••••" required>
      <div style="margin-top:20px"><button class="btn btn-primary" style="width:100%" type="submit" id="b2">Entrar</button></div>
      <div class="msg" id="m2" role="status"></div>
      <p class="note">Não chegou? <button type="button" class="linkbtn" id="reenviar">Enviar de novo</button> · <button type="button" class="linkbtn" id="trocar">Trocar número</button></p>
    </form>
    <p class="note" style="margin-top:22px">Ainda não é cliente? <a href="/precos">Veja como participar do Beta</a>.</p>
  </div>
</div></section>
""", scripts='<script src="/assets/entrar.js?v=2" defer></script>', noindex=True)


# ---------- Beta ----------
page("/beta", "Quero participar do Beta · Dyno", "Peça sua vaga no Beta fechado do Dyno: 60 dias grátis, convite pelo WhatsApp.", f"""
<section class="auth dots"><div class="wrap">
  <div class="auth-card beta-card">
    <span class="kicker">Beta fechado · 60 dias grátis<span data-vagas-pill></span></span>
    <h1 class="h" id="bh">Quero participar</h1>
    <form id="fb" novalidate>
      <div class="passo"><span class="num">1</span><div>
        <b>Seus dados</b>
        <p>Depois da aprovação, o convite chega pelo WhatsApp do Dyno e o cadastro é feito na conversa.</p>
        <label for="nome">Nome completo</label>
        <input class="input" id="nome" name="nome" autocomplete="name" maxlength="80" placeholder="Maria da Silva" required>
        <label for="tel">WhatsApp com DDD</label>
        <input class="input" id="tel" name="tel" type="tel" inputmode="tel" autocomplete="tel-national" placeholder="(11) 91234-5678" required>
        <div class="hp" aria-hidden="true"><label for="site">Site</label><input id="site" name="site" tabindex="-1" autocomplete="off"></div>
        <label class="check"><input type="checkbox" id="aceite"><span>Li a <a href="/privacidade" target="_blank">Política de Privacidade</a> e autorizo o uso do meu nome e WhatsApp para analisar o pedido e enviar o convite.</span></label>
      </div></div>
      <button class="btn btn-primary" style="width:100%;margin-top:8px" type="submit" id="bb">Enviar pedido</button>
      <div class="msg" id="mb" role="status"></div>
    </form>
    <div id="ok" hidden>
      <h2 class="h" style="font-size:28px;margin:6px 0 10px" id="ok-t">Pedido recebido! 🎉</h2>
      <p id="ok-p">Vamos analisar e, assim que aprovado, você recebe o convite pelo <b>WhatsApp do Dyno: +55 (11) 93949-7178</b>. Salve esse número nos seus contatos como <b>Dyno</b>.</p>
      <div class="cta-row"><a class="btn btn-ghost btn-sm" href="/como-funciona">Ver como funciona</a></div>
    </div>
    <p class="note" style="margin-top:22px">Já recebeu o convite? Responda a mensagem do Dyno no WhatsApp. Já é cliente? <a href="/entrar">Entre na sua área</a>.</p>
  </div>
</div></section>
""", scripts='<script src="/assets/beta.js?v=2" defer></script>' + HOMEJS)

# ---------- Conta ----------
page("/conta", "Minha área · Dyno", "Área do cliente do Dyno.", """
<div class="app-head"><div class="wrap">
  <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:16px;flex-wrap:wrap">
    <div><span class="kicker" style="color:var(--lime)">Área do cliente</span><h1 class="h" id="ola">Olá!</h1><p id="sub">Carregando seus dados…</p></div>
  </div>
  <div class="tabs" role="tablist">
    <button class="tab" role="tab" aria-selected="true" aria-controls="p-painel" id="t-painel">Painel</button>
    <button class="tab" role="tab" aria-selected="false" aria-controls="p-extrato" id="t-extrato">Extrato</button>
    <button class="tab" role="tab" aria-selected="false" aria-controls="p-comp" id="t-comp">Comprovantes</button>
    <button class="tab" role="tab" aria-selected="false" aria-controls="p-conta" id="t-conta">Minha conta</button>
  </div>
</div></div>
<div class="wrap">
  <section class="panel" id="p-painel" role="tabpanel" aria-labelledby="t-painel"><div class="skeleton"></div></section>
  <section class="panel" id="p-extrato" role="tabpanel" aria-labelledby="t-extrato" hidden></section>
  <section class="panel" id="p-comp" role="tabpanel" aria-labelledby="t-comp" hidden></section>
  <section class="panel" id="p-conta" role="tabpanel" aria-labelledby="t-conta" hidden><div class="skeleton"></div></section>
</div>
<dialog id="viewer" class="viewer" aria-labelledby="v-t"><div class="v-head"><div><h3 id="v-t">Comprovante</h3><p id="v-s"></p></div><button class="btn btn-ghost btn-sm" id="v-x" aria-label="Fechar">Fechar</button></div><div id="v-c" class="v-c"></div><div class="actions"><a class="btn btn-primary btn-sm" id="v-b" download>Baixar</a></div></dialog>
<dialog id="dlg"><h3 id="dlg-t"></h3><p id="dlg-p"></p><div class="actions"><button class="btn btn-ghost btn-sm" id="dlg-n">Voltar</button><button class="btn btn-primary btn-sm" id="dlg-s">Confirmar</button></div></dialog>
<div class="toast" id="toast" role="status"></div>
""", scripts='<script src="/assets/conta.js?v=4" defer></script>', noindex=True, app=True)

# ---------- 404 ----------
page("/404", "Página não encontrada · Dyno", "Página não encontrada.", """
<section class="auth dots"><div class="wrap" style="text-align:center">
  <span class="kicker">Erro 404</span><h1 class="h" style="font-size:56px;margin:12px 0">Essa página sumiu.</h1>
  <p>Mas o Dyno não esquece de nada. Volte para o início.</p>
  <div class="cta-row" style="justify-content:center"><a class="btn btn-primary" href="/">Ir para o início</a></div>
</div></section>
""", noindex=True)

exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "func_page.py"), encoding="utf-8").read())
page("/funcionalidades", "Funcionalidades · Dyno e Dina no WhatsApp", "Tudo o que o Dyno e a Dina fazem no WhatsApp: gastos, contas, extratos, limites, lembretes que insistem, tarefas, listas e rotina.", func_body(), nav="/funcionalidades", scripts=FUNCJS)

open(os.path.join(OUT, "favicon.svg"), "w").write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><circle cx="32" cy="32" r="32" fill="#14B37D"/><text x="32" y="45" text-anchor="middle" font-family="Georgia,serif" font-weight="700" font-size="40" fill="#1B1F3B">D</text></svg>')
import shutil
for f in ("og-dyno.png", "apple-touch-icon.png"):
    shutil.copy(os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", f), os.path.join(OUT, f))
open(os.path.join(OUT, "robots.txt"), "w").write("User-agent: *\nDisallow: /conta\nDisallow: /entrar\nDisallow: /api/\nSitemap: https://dynoapp.com.br/sitemap.xml\n")
urls = ["", "beta", "como-funciona", "funcionalidades", "precos", "duvidas", "termos", "privacidade"]
open(os.path.join(OUT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>https://dynoapp.com.br/{u}</loc></url>" for u in urls) + "</urlset>\n")
print("ok")
