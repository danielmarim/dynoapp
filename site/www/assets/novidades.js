/* 09/10/2026: novidades na área do cliente.
   - Aviso "Novidades" no Painel (pode fechar).
   - Barra do orçamento do mês (quando a pessoa definiu um teto geral pelo WhatsApp).
   - Aba "Documentos": documentos com vencimento (sem número) e encomendas rastreadas. */
!function () {
  "use strict";
  var VERSAO = "0910", D = null, montou = false;
  var esc = function (t) { return String(t == null ? "" : t).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };
  var brl = function (v) { return (Number(v) || 0).toLocaleString("pt-BR", { style: "currency", currency: "BRL" }); };
  var dataBR = function (s) { var p = String(s || "").slice(0, 10).split("-"); return p.length === 3 ? p[2] + "/" + p[1] + "/" + p[0] : ""; };
  var quandoBR = function (s) { var d = new Date(s); return isNaN(d) ? "" : d.toLocaleString("pt-BR", { day: "2-digit", month: "2-digit", hour: "2-digit", minute: "2-digit", timeZone: "America/Sao_Paulo" }); };
  var ls = { get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } }, set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} } };

  var st = document.createElement("style");
  st.textContent =
    ".nv-box{display:flex;gap:14px;align-items:flex-start;justify-content:space-between;flex-wrap:wrap;margin:0 0 18px;padding:16px 18px;border-radius:16px;border:1.5px solid rgba(47,212,126,.45);background:rgba(47,212,126,.08)}" +
    ".nv-box>div{flex:1;min-width:0}.nv-box b.k{display:inline-block;font-size:11px;letter-spacing:.08em;text-transform:uppercase;background:#2FD47E;color:#04210F;border-radius:999px;padding:3px 9px;margin-bottom:8px}" +
    ".nv-box p{margin:0;line-height:1.5;overflow-wrap:anywhere}.nv-box .nv-act{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}" +
    ".nv-x{flex:none;border:0;background:transparent;color:var(--muted,#8C9AB3);cursor:pointer;font-size:18px;line-height:1;padding:4px 6px;border-radius:8px}" +
    ".nv-orc{margin:0 0 18px;padding:16px 18px;border-radius:16px;border:1px solid rgba(140,154,179,.25)}.nv-orc h3{margin:0 0 6px;font-size:15px}" +
    ".nv-orc .bar{height:10px;border-radius:999px;background:rgba(140,154,179,.2);overflow:hidden;margin:8px 0 6px}.nv-orc .bar i{display:block;height:100%;border-radius:999px;background:#2FD47E}" +
    ".nv-orc .bar i.w{background:#F2B544}.nv-orc .bar i.x{background:#FF6B6B}.nv-orc small{color:var(--muted,#8C9AB3);font-variant-numeric:tabular-nums}" +
    ".dc-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,320px),1fr));gap:20px;align-items:start}" +
    ".dc-list{list-style:none;margin:10px 0 0;padding:0;display:grid;gap:10px}.dc-list li{display:flex;gap:12px;align-items:flex-start;padding:10px 0;border-top:1px solid rgba(140,154,179,.18);min-width:0}" +
    ".dc-list li:first-child{border-top:0}.dc-list .ic{flex:none;font-size:20px;line-height:1.2}.dc-list .tx{flex:1;min-width:0;overflow-wrap:anywhere}.dc-list .tx b{display:block}" +
    ".dc-list .tx small{display:block;color:var(--muted,#8C9AB3);margin-top:2px}.dc-pill{flex:none;font-size:12px;font-weight:600;border-radius:999px;padding:3px 9px;background:rgba(140,154,179,.16);white-space:nowrap;font-variant-numeric:tabular-nums}" +
    ".dc-pill.ok{background:rgba(47,212,126,.16);color:#2FD47E}.dc-pill.w{background:rgba(242,181,68,.16);color:#F2B544}.dc-pill.x{background:rgba(255,107,107,.16);color:#FF6B6B}" +
    ".dc-vazio{color:var(--muted,#8C9AB3);margin:8px 0 0;line-height:1.5}.dc-vazio code{font:inherit;font-weight:600;color:inherit}";
  document.head.appendChild(st);

  function irPara(id) { var t = document.getElementById(id); if (t) { t.click(); window.scrollTo({ top: 0, behavior: "smooth" }); } }

  /* ---------- Painel: aviso de novidades e orçamento do mês ---------- */
  function painel() {
    var p = document.getElementById("p-painel");
    if (!p || !D) return;
    if (ls.get("dyno_novid") !== VERSAO && !p.querySelector(".nv-box")) {
      var b = document.createElement("div");
      b.className = "nv-box"; b.setAttribute("role", "note");
      b.innerHTML = '<div><b class="k">Novidades</b><p>Agora o Dyno e a Dina acompanham suas <b>encomendas</b> e o vencimento dos seus <b>documentos</b>, dizem a <b>previsão do tempo</b>, mandam <b>recados para outros clientes Dyno</b>, insistem no lembrete até você responder e avisam quando você chega perto do <b>orçamento do mês</b>. E dá para conversar com eles por aqui, na aba Conversar.</p>' +
        '<div class="nv-act"><button class="btn btn-primary btn-sm" type="button" data-ir="t-docs">Ver documentos e encomendas</button><button class="btn btn-ghost btn-sm" type="button" data-ir="t-chat">Conversar</button><a class="btn btn-ghost btn-sm" href="/funcionalidades">Tudo o que eles fazem</a></div></div>' +
        '<button class="nv-x" type="button" aria-label="Fechar aviso de novidades" title="Fechar">✕</button>';
      b.querySelector(".nv-x").addEventListener("click", function () { ls.set("dyno_novid", VERSAO); b.remove(); });
      b.querySelectorAll("[data-ir]").forEach(function (x) { if (!document.getElementById(x.getAttribute("data-ir"))) x.remove(); else x.addEventListener("click", function () { irPara(x.getAttribute("data-ir")); }); });
      p.insertBefore(b, p.firstChild);
    }
    var o = D.orcamento_mes, ja = p.querySelector(".nv-orc");
    if (o && o.limite > 0) {
      var pct = Math.max(0, Number(o.pct) || 0), cls = pct >= 100 ? "x" : pct >= 80 ? "w" : "";
      var h = '<h3>Orçamento do mês</h3><small>' + esc(brl(o.usado)) + ' de ' + esc(brl(o.limite)) + ' · ' + pct + '%</small>' +
        '<div class="bar" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="' + Math.min(pct, 100) + '" aria-label="Orçamento do mês usado"><i class="' + cls + '" style="width:' + Math.min(pct, 100) + '%"></i></div>' +
        '<small>' + (pct >= 100 ? "Você passou do teto do mês." : pct >= 80 ? "Atenção: você está perto do teto do mês." : "Restam " + esc(brl(o.limite - o.usado)) + " até o teto.") + '</small>';
      if (!ja) { ja = document.createElement("div"); ja.className = "nv-orc"; var nb = p.querySelector(".nv-box"); p.insertBefore(ja, nb ? nb.nextSibling : p.firstChild); }
      ja.innerHTML = h;
    } else if (ja) ja.remove();
  }

  /* ---------- Aba Documentos ---------- */
  function aba() {
    if (montou) return;
    var tc = document.getElementById("t-conta"), pp = document.getElementById("p-painel");
    if (!tc || !pp) return;
    montou = true;
    var b = document.createElement("button");
    b.className = "tab"; b.id = "t-docs"; b.type = "button"; b.textContent = "Documentos";
    b.setAttribute("role", "tab"); b.setAttribute("aria-selected", "false"); b.setAttribute("aria-controls", "p-docs");
    tc.parentNode.insertBefore(b, tc);
    var s = document.createElement("section");
    s.className = "panel"; s.id = "p-docs"; s.hidden = true; s.setAttribute("role", "tabpanel"); s.setAttribute("aria-labelledby", "t-docs");
    s.innerHTML = '<div class="skeleton"></div>';
    pp.parentNode.appendChild(s);
    b.addEventListener("click", function () {
      document.querySelectorAll('[role="tab"]').forEach(function (t) { t.setAttribute("aria-selected", String(t === b)); });
      document.querySelectorAll('[role="tabpanel"]').forEach(function (x) { x.hidden = x !== s; });
      try { sessionStorage.setItem("dyno_aba", "docs"); } catch (e) {}
      render();
    });
    document.addEventListener("click", function (ev) {
      var t = ev.target && ev.target.closest ? ev.target.closest('[role="tab"]') : null;
      if (t && t !== b) { s.hidden = true; b.setAttribute("aria-selected", "false"); }
    }, true);
  }

  function render() {
    var s = document.getElementById("p-docs");
    if (!s || !D) return;
    var docs = D.documentos || [], enc = D.encomendas || [];
    var hd = docs.length ? '<ul class="dc-list">' + docs.map(function (d) {
      var n = d.dias, pill = n == null ? "" : n < 0 ? '<span class="dc-pill x">Vencido</span>' : n === 0 ? '<span class="dc-pill x">Vence hoje</span>' : n <= 30 ? '<span class="dc-pill w">' + n + (n === 1 ? " dia" : " dias") + '</span>' : n <= 90 ? '<span class="dc-pill">' + n + ' dias</span>' : '<span class="dc-pill ok">Em dia</span>';
      return '<li><span class="ic" aria-hidden="true">🪪</span><span class="tx"><b>' + esc(d.tipo) + '</b>' + (d.descricao && d.descricao !== d.tipo ? '<small>' + esc(d.descricao) + '</small>' : '') + '<small>Vence em ' + esc(dataBR(d.vencimento)) + '</small></span>' + pill + '</li>';
    }).join("") + '</ul>' : '<p class="dc-vazio">Nenhum documento ainda. Mande no WhatsApp algo como <code>minha CNH vence em 20/11/2027</code> ou a foto do documento. A Dina avisa antes de vencer, e o número do documento nunca aparece aqui.</p>';
    var he = enc.length ? '<ul class="dc-list">' + enc.map(function (e) {
      var cls = e.entregue ? "ok" : /saiu|retirada/i.test(e.status) ? "w" : /problema|sem sucesso/i.test(e.status) ? "x" : "";
      return '<li><span class="ic" aria-hidden="true">' + (e.entregue ? "✅" : "📦") + '</span><span class="tx"><b>' + esc(e.apelido || e.codigo) + '</b>' + (e.apelido ? '<small>' + esc(e.codigo) + '</small>' : '') +
        (e.ultimo ? '<small>' + esc(e.ultimo) + (e.local ? " · " + esc(e.local) : "") + '</small>' : '') + (quandoBR(e.quando) ? '<small>Atualizado em ' + esc(quandoBR(e.quando)) + '</small>' : '') +
        '</span><span class="dc-pill ' + cls + '">' + esc(e.status) + '</span></li>';
    }).join("") + '</ul>' : '<p class="dc-vazio">Nenhuma encomenda sendo acompanhada. Mande no WhatsApp o código dos Correios (ou um print com vários códigos) e a Dina avisa quando o status mudar.</p>';
    s.innerHTML = '<div class="dc-grid"><div class="box"><h2>Documentos</h2>' + hd + '</div><div class="box"><h2>Encomendas</h2>' + he + '</div></div>' +
      '<p class="dc-vazio" style="margin-top:18px">Para apagar um documento ou parar um rastreio, é só pedir no WhatsApp.</p>';
  }

  var F = window.fetch;
  window.fetch = function (u, o) {
    var r = F.apply(this, arguments);
    try {
      if (String(u) === "/api" && o && typeof o.body === "string" && o.body.indexOf('"painel"') > -1) {
        r.then(function (x) { return x.clone().json(); }).then(function (j) {
          if (!j || !j.ok) return;
          D = j; aba(); render();
          [0, 400, 1500].forEach(function (ms) { setTimeout(painel, ms); });
          var aberta = null; try { aberta = sessionStorage.getItem("dyno_aba"); } catch (e) {}
          if (aberta === "docs") { var t = document.getElementById("t-docs"); if (t && t.getAttribute("aria-selected") !== "true") t.click(); }
        }).catch(function () {});
      }
    } catch (e) {}
    return r;
  };
  var obs = function () { var p = document.getElementById("p-painel"); if (!p || !window.MutationObserver) return; new MutationObserver(function () { if (D && !p.querySelector(".nv-box") && ls.get("dyno_novid") !== VERSAO) painel(); if (D && D.orcamento_mes && !p.querySelector(".nv-orc")) painel(); }).observe(p, { childList: true }); };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", function () { aba(); obs(); }); else { aba(); obs(); }
}();
