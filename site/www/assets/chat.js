/* 08/10/2026: Conversar com o Dyno e a Dina dentro da área do cliente (o mesmo cérebro do WhatsApp).
   v2: botão flutuante, janela de conversa e gráficos/tabelas com os números do banco. */
!function () {
  "use strict";
  var API = function (corpo) {
    return fetch("/api", { method: "POST", credentials: "same-origin", headers: { "Content-Type": "application/json", "X-Requested-With": "dyno" }, body: JSON.stringify(corpo) })
      .then(function (r) { return r.json().catch(function () { return { ok: false, erro: "indisponivel" }; }).then(function (j) { if (r.status === 401) j.erro = "sessao"; return j; }); })
      .catch(function () { return { ok: false, erro: "rede" }; });
  };
  var ERROS = {
    sessao: "Sua sessão expirou. Entre de novo para conversar.",
    limite: "Muitas mensagens em pouco tempo. Espere uns minutinhos e tente de novo.",
    aguarde: "Ainda estou respondendo a mensagem anterior. Só um instante.",
    vazio: "Escreva sua mensagem.",
    sem_conta: "Sua conta ainda não está ligada ao WhatsApp do Dyno. Fale com a gente pelo WhatsApp.",
    rede: "Sem conexão agora. Confira a internet e tente de novo.",
    indisponivel: "O Dyno está instável agora. Tente de novo em instantes."
  };
  var SUGESTOES = ["Onde mais gastei este mês?", "Quanto ainda posso gastar este mês?", "Quais contas vencem esta semana?", "O que tenho na agenda hoje?", "Minhas assinaturas", "Gastei 32 no almoço"];
  var CAT = { alimentacao: "Alimentação", educacao: "Educação", saude: "Saúde", combustivel: "Combustível", moradia: "Moradia", contas: "Contas", lazer: "Lazer", compras: "Compras", viagem: "Viagem", trabalho: "Trabalho", impostos: "Impostos", outros: "Outros", assinaturas: "Assinaturas", transporte: "Transporte", mercado: "Mercado", salario: "Salário", reembolso: "Reembolso", investimentos: "Investimentos" };
  var ultimo = 0, carregado = false, enviando = false, poll = null, flutuante = false;

  var css = document.createElement("style");
  css.textContent =
    ".chatbox{display:flex;flex-direction:column;gap:14px;max-width:820px;min-height:0;min-width:0;box-sizing:border-box}.chatbox>*{min-width:0}" +
    ".chat-head h2{margin:0}.chat-head p{margin:4px 0 0;color:var(--muted,#8C9AB3);font-size:14px}" +
    ".chat-list{display:flex;flex-direction:column;gap:10px;min-height:280px;max-height:min(62vh,640px);overflow-y:auto;padding:16px;border-radius:16px;background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);overscroll-behavior:contain;box-sizing:border-box}.chat-list>*{max-width:100%;min-width:0;box-sizing:border-box}" +
    ".msg-b{max-width:min(85%,560px);padding:10px 14px;border-radius:16px;line-height:1.5;overflow-wrap:anywhere;font-size:15px}" +
    ".msg-b .tx{white-space:pre-wrap}" +
    ".msg-b.eu{align-self:flex-end;background:var(--green,#2FD47E);color:#04210F;border-bottom-right-radius:4px}" +
    ".msg-b.ele{align-self:flex-start;background:#16233A;border:1px solid rgba(255,255,255,.08);border-bottom-left-radius:4px}" +
    ".msg-b.ele.vis{width:min(100%,560px);max-width:100%}" +
    ".msg-b .quem{display:block;font-size:12px;font-weight:700;margin-bottom:2px;color:var(--green,#2FD47E)}.msg-b .quem.dina{color:#F5B14C}" +
    ".msg-b time{display:block;font-size:11px;opacity:.6;margin-top:4px;text-align:right}" +
    ".chat-dia{align-self:center;font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--muted,#8C9AB3);margin:6px 0}" +
    ".digitando{align-self:flex-start;color:var(--muted,#8C9AB3);font-size:14px;padding:4px 6px}" +
    ".digitando i{display:inline-block;width:6px;height:6px;border-radius:50%;background:currentColor;margin-right:3px;animation:dg 1s infinite ease-in-out}" +
    ".digitando i:nth-child(2){animation-delay:.15s}.digitando i:nth-child(3){animation-delay:.3s}" +
    "@keyframes dg{0%,80%,100%{opacity:.25}40%{opacity:1}}" +
    ".chat-sug{display:flex;gap:8px;flex-wrap:wrap}" +
    ".chat-sug button{flex:none;border:1px solid rgba(255,255,255,.14);background:rgba(255,255,255,.04);color:inherit;border-radius:999px;padding:7px 12px;font:inherit;font-size:13px;cursor:pointer}" +
    ".chat-sug button:hover{border-color:var(--green,#2FD47E)}" +
    ".chat-form{display:flex;gap:8px;align-items:flex-end}" +
    ".chat-form textarea{flex:1;min-width:0;resize:none;box-sizing:border-box;border:1px solid rgba(255,255,255,.14);background:rgba(255,255,255,.04);color:inherit;border-radius:14px;padding:11px 14px;font:inherit;font-size:16px;line-height:1.4;max-height:140px}" +
    ".chat-form textarea:focus{outline:2px solid var(--green,#2FD47E);outline-offset:1px}" +
    ".chat-err{color:#FF8A8A;margin:0;font-size:14px}.chat-nota{color:var(--muted,#8C9AB3);font-size:13px;margin:0}" +
    ".chat-vazio{margin:auto;text-align:center;color:var(--muted,#8C9AB3);max-width:360px}" +
    /* visuais */
    ".vz{margin-top:10px;padding:12px;border-radius:12px;background:rgba(0,0,0,.22);font-size:13px}" +
    ".vz h4{margin:0 0 10px;font-size:13px;font-weight:700;color:#E9EEF7}" +
    ".vz .lin{display:grid;grid-template-columns:minmax(70px,32%) 1fr auto;gap:8px;align-items:center;margin:5px 0}" +
    ".vz .rot{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:#C9D3E3}" +
    ".vz .trilho{height:10px;border-radius:6px;background:rgba(255,255,255,.07);overflow:hidden}" +
    ".vz .bar{height:100%;border-radius:6px;background:var(--green,#2FD47E)}" +
    ".vz .bar.al{background:#F5B14C}.vz .bar.ex{background:#FF6B6B}" +
    ".vz .val{font-variant-numeric:tabular-nums;white-space:nowrap;color:#E9EEF7;text-align:right}.vz .lin.f{grid-template-columns:minmax(70px,30%) 1fr 6.8em}" +
    ".vz .tot{display:flex;justify-content:space-between;margin-top:8px;padding-top:8px;border-top:1px solid rgba(255,255,255,.08);font-weight:700}" +
    ".vz .cols{display:flex;align-items:flex-end;gap:2px;height:110px}" +
    ".vz .cols div{flex:1;min-width:2px;background:var(--green,#2FD47E);border-radius:3px 3px 0 0}" +
    ".vz .eixo{display:flex;justify-content:space-between;color:var(--muted,#8C9AB3);font-size:11px;margin-top:4px}" +
    ".vz .flx{display:grid;grid-template-columns:repeat(6,1fr);gap:8px;align-items:end;height:120px}" +
    ".vz .flx .g{display:flex;gap:3px;align-items:flex-end;height:100%}" +
    ".vz .flx .g div{flex:1;border-radius:3px 3px 0 0;min-height:2px}" +
    ".vz .e{background:var(--green,#2FD47E)}.vz .s{background:#F08A4B}" +
    ".vz .flxr{display:grid;grid-template-columns:repeat(6,1fr);gap:8px;text-align:center;color:var(--muted,#8C9AB3);font-size:11px;margin-top:4px}" +
    ".vz .leg{display:flex;gap:14px;color:var(--muted,#8C9AB3);font-size:12px;margin-bottom:8px}.vz .leg i{display:inline-block;width:10px;height:10px;border-radius:3px;margin-right:5px;vertical-align:-1px}" +
    ".vz .tw{overflow-x:auto}.vz table{width:100%;border-collapse:collapse;font-size:13px}" +
    ".vz th{text-align:left;font-weight:600;color:var(--muted,#8C9AB3);padding:4px 6px;border-bottom:1px solid rgba(255,255,255,.1);white-space:nowrap}" +
    ".vz td{padding:6px;border-bottom:1px solid rgba(255,255,255,.05);vertical-align:top}" +
    ".vz td.n,.vz th.n{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}" +
    ".vz .nada{color:var(--muted,#8C9AB3);margin:0}" +
    /* botão flutuante e janela */
    ".chat-fab{position:fixed;right:20px;bottom:calc(20px + env(safe-area-inset-bottom,0px));z-index:60;display:flex;align-items:center;gap:8px;height:56px;padding:0 18px 0 16px;border:0;border-radius:999px;background:var(--green,#2FD47E);color:#04210F;font:inherit;font-weight:700;font-size:15px;cursor:pointer;box-shadow:0 10px 30px rgba(0,0,0,.45)}" +
    ".chat-fab svg{width:24px;height:24px}.chat-fab:focus-visible{outline:3px solid #fff;outline-offset:3px}" +
    ".chat-fab[hidden]{display:none}" +
    ".chat-float{position:fixed;z-index:70;right:20px;bottom:calc(20px + env(safe-area-inset-bottom,0px));width:min(410px,calc(100vw - 40px));height:min(640px,calc(100vh - 110px));display:flex;flex-direction:column;background:#0B1322;border:1px solid rgba(255,255,255,.1);border-radius:20px;box-shadow:0 24px 60px rgba(0,0,0,.6);overflow:hidden}" +
    ".chat-float[hidden]{display:none}" +
    ".chat-float .fhead{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:14px 16px;border-bottom:1px solid rgba(255,255,255,.08)}" +
    ".chat-float .fhead b{font-size:16px}.chat-float .fhead span{display:block;font-size:12px;color:var(--muted,#8C9AB3);font-weight:400}" +
    ".chat-float .fx{border:0;background:rgba(255,255,255,.07);color:inherit;width:36px;height:36px;border-radius:50%;font-size:18px;cursor:pointer;flex:none}" +
    ".chat-float .fbody{flex:1;min-height:0;min-width:0;display:flex;padding:12px}" +
    ".chat-float .chatbox{flex:1;gap:10px;max-width:none;width:100%;padding:0;background:none;border:0;box-shadow:none;border-radius:0}" +
    ".chat-float .chat-head,.chat-float .chat-nota{display:none}" +
    ".chat-float .chat-list{flex:1;min-height:0;max-height:none;padding:12px}" +
    ".chat-float .chat-sug{flex-wrap:nowrap;overflow-x:auto;padding-bottom:2px;scrollbar-width:none}" +
    "@media (max-width:640px){.chat-float{inset:0;width:auto;height:auto;border-radius:0;border:0;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}.chat-fab{right:16px;padding:0 16px}}" +
    "@media (prefers-reduced-motion:reduce){.digitando i{animation:none}}";
  document.head.appendChild(css);

  var esc = function (s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };
  var fmt = function (s) {
    var t = esc(s);
    t = t.replace(/\*([^*\n]{1,200})\*/g, "<b>$1</b>").replace(/(^|\s)_([^_\n]{1,200})_(?=\s|$|[.,!?])/g, "$1<i>$2</i>");
    t = t.replace(/\b(dynoapp\.com\.br\/[\w\/.\-?=&#%]*)/g, '<a href="https://$1" rel="noopener">$1</a>');
    return t;
  };
  var brl = function (v) { return Number(v || 0).toLocaleString("pt-BR", { style: "currency", currency: "BRL" }); };
  var curto = function (v) { v = Number(v || 0); return v >= 1000 ? "R$ " + (v / 1000).toLocaleString("pt-BR", { maximumFractionDigits: 1 }) + " mil" : brl(v); };
  var cat = function (s) { var k = String(s || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, ""); return CAT[k] || s; };
  var hora = function (q) { var d = new Date(q); return isNaN(d) ? "" : d.toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit", timeZone: "America/Sao_Paulo" }); };
  var diaDe = function (q) { var d = new Date(q); return isNaN(d) ? "" : d.toLocaleDateString("pt-BR", { weekday: "short", day: "2-digit", month: "2-digit", timeZone: "America/Sao_Paulo" }); };
  var $ = function (id) { return document.getElementById(id); };

  /* ---------- visuais (dados do banco, via API) ---------- */
  function desenhar(alvo, v) {
    if (!v || !v.ok) { alvo.innerHTML = '<p class="nada">Não consegui montar o gráfico agora.</p>'; return; }
    var h = "<h4>" + esc(v.titulo || "") + "</h4>";
    var itens = Array.isArray(v.itens) ? v.itens : [];
    if (v.forma === "barras") {
      if (!itens.length) { alvo.innerHTML = h + '<p class="nada">Nenhum gasto nesse período.</p>'; return; }
      var mx = Math.max.apply(null, itens.map(function (i) { return Number(i.valor) || 0; })) || 1;
      h += itens.map(function (i) { return '<div class="lin f"><span class="rot" title="' + esc(cat(i.rotulo)) + '">' + esc(cat(i.rotulo)) + '</span><span class="trilho"><span class="bar" style="display:block;width:' + Math.max(2, Math.round(Number(i.valor) / mx * 100)) + '%"></span></span><span class="val">' + brl(i.valor) + "</span></div>"; }).join("");
      if (v.total != null) h += '<div class="tot"><span>Total</span><span>' + brl(v.total) + "</span></div>";
    } else if (v.forma === "colunas") {
      var m2 = Math.max.apply(null, itens.map(function (i) { return Number(i.valor) || 0; })) || 1;
      h += '<div class="cols" role="img" aria-label="' + esc(v.titulo) + '">' + itens.map(function (i) { return '<div title="' + esc(i.rotulo + ": " + brl(i.valor)) + '" style="height:' + Math.max(1, Math.round(Number(i.valor) / m2 * 100)) + '%;' + (Number(i.valor) ? "" : "opacity:.25") + '"></div>'; }).join("") + "</div>";
      if (itens.length) h += '<div class="eixo"><span>' + esc(itens[0].rotulo) + "</span><span>maior dia: " + brl(m2) + "</span><span>" + esc(itens[itens.length - 1].rotulo) + "</span></div>";
      if (v.total != null) h += '<div class="tot"><span>Total</span><span>' + brl(v.total) + "</span></div>";
    } else if (v.forma === "fluxo") {
      var m3 = Math.max.apply(null, itens.map(function (i) { return Math.max(Number(i.entradas) || 0, Number(i.saidas) || 0); })) || 1;
      h += '<div class="leg"><span><i class="e"></i>Entradas</span><span><i class="s"></i>Saídas</span></div>';
      h += '<div class="flx">' + itens.map(function (i) { return '<div class="g"><div class="e" title="Entradas ' + esc(i.rotulo) + ": " + brl(i.entradas) + '" style="height:' + Math.round((Number(i.entradas) || 0) / m3 * 100) + '%"></div><div class="s" title="Saídas ' + esc(i.rotulo) + ": " + brl(i.saidas) + '" style="height:' + Math.round((Number(i.saidas) || 0) / m3 * 100) + '%"></div></div>'; }).join("") + "</div>";
      h += '<div class="flxr">' + itens.map(function (i) { return "<span>" + esc(i.rotulo) + "</span>"; }).join("") + "</div>";
      var u = itens[itens.length - 1] || {};
      h += '<div class="tot"><span>Este mês</span><span>' + curto(u.entradas) + " × " + curto(u.saidas) + "</span></div>";
    } else if (v.forma === "limites") {
      if (!itens.length) { alvo.innerHTML = h + '<p class="nada">Você ainda não tem limites. Diga, por exemplo: "no máximo 800 em mercado por mês".</p>'; return; }
      h += itens.map(function (i) { var p = Number(i.limite) ? Number(i.valor) / Number(i.limite) * 100 : 0; return '<div class="lin"><span class="rot">' + esc(cat(i.rotulo)) + '</span><span class="trilho"><span class="bar' + (p >= 100 ? " ex" : p >= 80 ? " al" : "") + '" style="display:block;width:' + Math.min(100, Math.max(2, Math.round(p))) + '%"></span></span><span class="val">' + Math.round(p) + "% de " + curto(i.limite) + "</span></div>"; }).join("");
    } else if (v.forma === "tabela") {
      var cols = Array.isArray(v.colunas) ? v.colunas : [], ln = Array.isArray(v.linhas) ? v.linhas : [], mi = Number(v.moeda);
      if (!ln.length) { alvo.innerHTML = h + '<p class="nada">Nada por aqui ainda.</p>'; return; }
      h += '<div class="tw"><table><thead><tr>' + cols.map(function (c, k) { return "<th" + (k === mi ? ' class="n"' : "") + ">" + esc(c) + "</th>"; }).join("") + "</tr></thead><tbody>" +
        ln.map(function (r) { return "<tr>" + r.map(function (c, k) { return k === mi ? '<td class="n">' + brl(c) + "</td>" : "<td>" + esc(cols[k] === "Categoria" ? cat(c) : c) + "</td>"; }).join("") + "</tr>"; }).join("") + "</tbody></table></div>";
      if (v.total != null) h += '<div class="tot"><span>' + esc(v.total_rotulo || "Total") + "</span><span>" + brl(v.total) + "</span></div>";
    } else { alvo.innerHTML = '<p class="nada">Não consegui montar o gráfico agora.</p>'; return; }
    alvo.innerHTML = h;
  }

  /* ---------- montagem ---------- */
  function caixa() {
    var c = document.createElement("div");
    c.className = "box chatbox"; c.id = "chatbox";
    c.innerHTML =
      '<div class="chat-head"><h2>Converse com o Dyno e a Dina</h2><p>Os mesmos assistentes do seu WhatsApp. Pergunte, registre ou mude algo por aqui.</p></div>' +
      '<div class="chat-list" id="chat-list" aria-live="polite" aria-label="Conversa"><div class="chat-vazio">Carregando a conversa…</div></div>' +
      '<div class="chat-sug" id="chat-sug"></div>' +
      '<form class="chat-form" id="chat-form" novalidate><label class="sr" for="chat-txt">Mensagem</label>' +
      '<textarea id="chat-txt" rows="1" maxlength="1500" placeholder="Escreva como no WhatsApp…" autocomplete="off"></textarea>' +
      '<button class="btn btn-primary btn-sm" type="submit" id="chat-btn">Enviar</button></form>' +
      '<p class="chat-err" id="chat-err" role="alert" hidden></p>' +
      '<p class="chat-nota">O que você faz aqui também vale no WhatsApp. Confirmações extras e imagens (painel, cartões) continuam chegando por lá.</p>';
    SUGESTOES.forEach(function (s) { var x = document.createElement("button"); x.type = "button"; x.textContent = s; x.addEventListener("click", function () { enviar(s); }); c.querySelector("#chat-sug").appendChild(x); });
    var ta = c.querySelector("#chat-txt");
    c.querySelector("#chat-form").addEventListener("submit", function (e) { e.preventDefault(); enviar(ta.value); });
    ta.addEventListener("keydown", function (e) { if (e.key === "Enter" && !e.shiftKey && !e.isComposing) { e.preventDefault(); enviar(ta.value); } });
    ta.addEventListener("input", function () { ta.style.height = "auto"; ta.style.height = Math.min(140, ta.scrollHeight) + "px"; });
    return c;
  }

  function criar() {
    var tp = $("t-painel"), pp = $("p-painel");
    if (!tp || !pp || $("t-chat")) return;
    var b = document.createElement("button");
    b.className = "tab"; b.id = "t-chat"; b.type = "button"; b.textContent = "Conversar";
    b.setAttribute("role", "tab"); b.setAttribute("aria-selected", "false"); b.setAttribute("aria-controls", "p-chat");
    tp.parentNode.insertBefore(b, tp.nextSibling);
    var p = document.createElement("section");
    p.className = "panel"; p.id = "p-chat"; p.hidden = true; p.setAttribute("role", "tabpanel"); p.setAttribute("aria-labelledby", "t-chat");
    p.appendChild(caixa());
    pp.parentNode.insertBefore(p, pp.nextSibling);
    b.addEventListener("click", abrirAba);
    document.querySelectorAll('[role="tab"]').forEach(function (t) { if (t !== b) t.addEventListener("click", function () { p.hidden = true; b.setAttribute("aria-selected", "false"); fab(true); }); });

    // botão flutuante + janela
    var f = document.createElement("button");
    f.className = "chat-fab"; f.id = "chat-fab"; f.type = "button"; f.setAttribute("aria-label", "Conversar com o Dyno e a Dina"); f.setAttribute("aria-controls", "chat-float"); f.setAttribute("aria-expanded", "false");
    f.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12a8 8 0 0 1-11.6 7.1L4 20.5l1.4-4.9A8 8 0 1 1 21 12z"/><path d="M8.5 11h.01M12 11h.01M15.5 11h.01"/></svg><span>Conversar</span>';
    f.addEventListener("click", abrirJanela);
    document.body.appendChild(f);
    var j = document.createElement("div");
    j.className = "chat-float"; j.id = "chat-float"; j.hidden = true; j.setAttribute("role", "dialog"); j.setAttribute("aria-modal", "false"); j.setAttribute("aria-label", "Conversa com o Dyno e a Dina");
    j.innerHTML = '<div class="fhead"><div><b>Dyno e Dina</b><span>Os mesmos do seu WhatsApp</span></div><button class="fx" type="button" id="chat-fx" aria-label="Fechar conversa">✕</button></div><div class="fbody" id="chat-fbody"></div>';
    document.body.appendChild(j);
    $("chat-fx").addEventListener("click", fecharJanela);
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && flutuante) fecharJanela(); });

    try { if (sessionStorage.getItem("dyno_aba") === "chat") abrirAba(); } catch (e) {}
    if (location.hash === "#conversar") abrirAba();
  }

  function fab(mostrar) { var f = $("chat-fab"); if (f) f.hidden = !mostrar || flutuante || ($("t-chat") && $("t-chat").getAttribute("aria-selected") === "true"); }
  function focar() { setTimeout(function () { var ta = $("chat-txt"); if (ta && window.matchMedia("(min-width: 760px)").matches) ta.focus(); }, 60); }
  function iniciar() { if (!carregado) carregar(); else ler(); }

  function abrirAba() {
    if (flutuante) fecharJanela();
    var b = $("t-chat"), p = $("p-chat"); if (!b || !p) return;
    if ($("chatbox").parentNode !== p) p.appendChild($("chatbox"));
    document.querySelectorAll('[role="tab"]').forEach(function (t) { t.setAttribute("aria-selected", String(t === b)); });
    document.querySelectorAll('[role="tabpanel"]').forEach(function (x) { x.hidden = x !== p; });
    try { sessionStorage.setItem("dyno_aba", "chat"); } catch (e) {}
    fab(false); iniciar(); focar();
  }

  function abrirJanela() {
    var j = $("chat-float"); if (!j) return;
    flutuante = true;
    $("chat-fbody").appendChild($("chatbox"));
    j.hidden = false; $("chat-fab").setAttribute("aria-expanded", "true"); fab(false);
    if (window.matchMedia("(max-width:640px)").matches) document.documentElement.style.overflow = "hidden";
    iniciar(); focar();
    var l = $("chat-list"); if (l) l.scrollTop = l.scrollHeight;
  }

  function fecharJanela() {
    var j = $("chat-float"); if (!j) return;
    flutuante = false; j.hidden = true; document.documentElement.style.overflow = "";
    $("p-chat").appendChild($("chatbox"));
    $("chat-fab").setAttribute("aria-expanded", "false"); fab(true); $("chat-fab").focus();
  }

  /* ---------- conversa ---------- */
  function erro(m) { var e = $("chat-err"); if (!e) return; e.textContent = m || ""; e.hidden = !m; }

  function bolha(m) {
    var el = document.createElement("div"), txt = String(m.texto || ""), quem = "", vis = null;
    var cab = txt.match(/^\s*\*?\s*(⏰|💰)?\s*(Dina|Dyno)\s*\*?\s*\n/);
    if (cab) { quem = cab[2]; txt = txt.slice(cab[0].length); }
    txt = txt.replace(/^​+/, "");
    var mv = txt.match(/\n?\[\[visual:([a-z_]+):([a-z_0-9]+)\]\]\s*$/);
    if (mv) { vis = { tipo: mv[1], periodo: mv[2] }; txt = txt.slice(0, mv.index); }
    if (m.papel === "usuario") txt = txt.replace(/^\[áudio transcrito\]\s*/i, "🎤 ").replace(/\s*\[(foto|PDF)(: sb:\/\/[^\]]*)?\]\s*$/, " 📎");
    el.className = "msg-b " + (m.papel === "usuario" ? "eu" : "ele") + (vis ? " vis" : "");
    el.innerHTML = (m.papel !== "usuario" ? '<span class="quem' + (quem === "Dina" ? " dina" : "") + '">' + (quem === "Dina" ? "⏰ Dina" : "💰 Dyno") + "</span>" : "") + '<div class="tx">' + fmt(txt.trim()) + "</div>" + (vis ? '<div class="vz"><p class="nada">Montando o gráfico…</p></div>' : "") + "<time>" + hora(m.quando) + "</time>";
    if (vis) { var alvo = el.querySelector(".vz"); API({ acao: "chat_visual", tipo: vis.tipo, periodo: vis.periodo }).then(function (r) { desenhar(alvo, r); var l = $("chat-list"); if (l && l.scrollHeight - l.scrollTop - l.clientHeight < 260) l.scrollTop = l.scrollHeight; }); }
    return el;
  }

  var ultimoDia = "";
  function acrescentar(ms, limpar) {
    var l = $("chat-list"); if (!l) return;
    if (limpar) { l.innerHTML = ""; ultimoDia = ""; }
    var dig = $("chat-dig"); if (dig) dig.remove();
    if (ms.some(function (m) { return m.papel === "usuario"; })) l.querySelectorAll('[data-temp="1"]').forEach(function (x) { x.remove(); });
    ms.forEach(function (m) {
      if (Number(m.id) <= ultimo) return;
      ultimo = Math.max(ultimo, Number(m.id) || 0);
      var d = diaDe(m.quando);
      if (d && d !== ultimoDia) { var s = document.createElement("div"); s.className = "chat-dia"; s.textContent = d; l.appendChild(s); ultimoDia = d; }
      l.appendChild(bolha(m));
    });
    if (!l.querySelector(".msg-b")) l.innerHTML = '<div class="chat-vazio">Ainda não há conversa. Comece com uma das sugestões abaixo ou escreva do seu jeito.</div>';
    l.scrollTop = l.scrollHeight;
  }

  function digitando(on) {
    var l = $("chat-list"); if (!l) return;
    var d = $("chat-dig");
    if (on && !d) { d = document.createElement("div"); d.id = "chat-dig"; d.className = "digitando"; d.innerHTML = "<i></i><i></i><i></i> respondendo…"; l.appendChild(d); l.scrollTop = l.scrollHeight; }
    if (!on && d) d.remove();
  }

  function carregar() {
    carregado = true;
    API({ acao: "chat_ler", desde: 0 }).then(function (r) {
      if (!r || !r.ok) { carregado = false; acrescentar([], true); erro(ERROS[r && r.erro] || ERROS.indisponivel); return; }
      acrescentar(r.mensagens || [], true);
      if (r.aguardando) acompanhar();
    });
  }
  function ler() { return API({ acao: "chat_ler", desde: ultimo }).then(function (r) { if (r && r.ok) acrescentar(r.mensagens || [], false); return r; }); }

  function acompanhar() {
    clearTimeout(poll);
    var inicio = Date.now(), viu = false, desde = 0;
    digitando(true);
    var passo = function () {
      ler().then(function (r) {
        var tem = !!(r && r.ok && (r.mensagens || []).some(function (m) { return m.papel === "assistente"; }));
        if (tem && !viu) { viu = true; desde = Date.now(); digitando(false); }
        var fim = viu ? (Date.now() - desde > 6000 && !(r && r.aguardando)) : Date.now() - inicio > 75000;
        if (fim) { digitando(false); enviando = false; botao(); if (!viu) erro("A resposta está demorando. Ela vai aparecer aqui e no seu WhatsApp assim que sair."); return; }
        if (viu) { enviando = false; botao(); }
        poll = setTimeout(passo, viu ? 2000 : 1500);
      });
    };
    poll = setTimeout(passo, 1500);
  }

  function botao() { var b = $("chat-btn"); if (b) { b.disabled = enviando; b.textContent = enviando ? "Enviando…" : "Enviar"; } }

  function enviar(texto) {
    var t = String(texto || "").trim();
    if (!t) { erro(ERROS.vazio); return; }
    if (enviando) { erro(ERROS.aguarde); return; }
    erro(""); enviando = true; botao();
    var ta = $("chat-txt");
    API({ acao: "chat_enviar", texto: t }).then(function (r) {
      if (!r || !r.ok) { enviando = false; botao(); erro(ERROS[r && r.erro] || ERROS.indisponivel); return; }
      if (ta) { ta.value = ""; ta.style.height = "auto"; }
      var l = $("chat-list"); var v = l && l.querySelector(".chat-vazio"); if (v) v.remove();
      if (l) { var eu = bolha({ papel: "usuario", texto: t, quando: new Date().toISOString() }); eu.setAttribute("data-temp", "1"); l.appendChild(eu); l.scrollTop = l.scrollHeight; }
      if (Number(r.desde) > ultimo) ultimo = Number(r.desde);
      acompanhar();
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", criar); else criar();
  var tent = 0, iv = setInterval(function () { criar(); if ($("t-chat") || ++tent > 40) clearInterval(iv); }, 250);
}();
