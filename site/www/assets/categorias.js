/* 10/10/2026: aba "Categorias" na área do cliente.
   - Gastos por categoria no período (com comparação e limite).
   - Lançamentos sem categoria (outros) para reclassificar, com opção de virar regra.
   - Regras que o Dyno aprendeu ("padaria é alimentação") e limites por categoria.
   Tudo passa por /api acao "categorias"; o banco confere a sessão e o plano. */
!function () {
  "use strict";
  var D = null, PER = "mes", montou = false, ocupado = false;
  var BONITO = { alimentacao: "Alimentação", educacao: "Educação", saude: "Saúde", combustivel: "Combustível", vestuario: "Vestuário", servicos: "Serviços", lazer: "Lazer", mercado: "Mercado", transporte: "Transporte", moradia: "Moradia", contas: "Contas", compras: "Compras", assinaturas: "Assinaturas", viagem: "Viagem", trabalho: "Trabalho", impostos: "Impostos", outros: "Outros", investimentos: "Investimentos" };
  var nome = function (c) { var k = String(c || "outros").toLowerCase().trim(); return BONITO[k] || (k.charAt(0).toUpperCase() + k.slice(1)); };
  var esc = function (t) { return String(t == null ? "" : t).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };
  var brl = function (v) { return (Number(v) || 0).toLocaleString("pt-BR", { style: "currency", currency: "BRL" }); };
  var dataBR = function (s) { var p = String(s || "").slice(0, 10).split("-"); return p.length === 3 ? p[2] + "/" + p[1] : ""; };
  var $ = function (id) { return document.getElementById(id); };
  var ERRO = { plano: "Isso faz parte do plano Completo. Para trocar: aba Minha conta.", padrao: "Escreva a palavra que aparece no gasto (pelo menos 2 letras).", categoria: "Escolha ou escreva uma categoria (até 30 letras).", valor: "Informe um valor maior que zero.", nao_encontrado: "Não encontrei esse item. Atualize a página.", limite_regras: "Você chegou ao limite de 200 regras.", sessao: "Sua sessão expirou. Entre de novo." };

  function toast(t) { var el = $("toast"); if (!el) return; el.textContent = t; el.style.display = "block"; clearTimeout(toast._t); toast._t = setTimeout(function () { el.style.display = "none"; }, 3500); }
  function api(corpo) {
    corpo.acao = "categorias";
    return fetch("/api", { method: "POST", credentials: "same-origin", headers: { "Content-Type": "application/json", "X-Requested-With": "dyno" }, body: JSON.stringify(corpo) })
      .then(function (r) { if (r.status === 401) { location.replace("/entrar"); return { ok: false, erro: "sessao" }; } return r.json().catch(function () { return { ok: false }; }); })
      .catch(function () { return { ok: false, erro: "indisponivel" }; });
  }

  var st = document.createElement("style");
  st.textContent =
    ".ct-top{display:flex;gap:12px;align-items:center;justify-content:space-between;flex-wrap:wrap;margin:0 0 18px}.ct-top h2{margin:0}.ct-top small{color:var(--muted,#8C9AB3)}" +
    ".ct-per{display:flex;gap:6px;flex-wrap:wrap}.ct-per button{border:1px solid rgba(140,154,179,.3);background:transparent;color:inherit;border-radius:999px;padding:6px 12px;font:inherit;font-size:13px;cursor:pointer}" +
    ".ct-per button[aria-pressed=true]{background:#2FD47E;border-color:#2FD47E;color:#04210F;font-weight:600}" +
    ".ct-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,360px),1fr));gap:20px;align-items:start}" +
    ".ct-rows{list-style:none;margin:10px 0 0;padding:0;display:grid;gap:12px}.ct-rows li{min-width:0}" +
    ".ct-l1{display:flex;justify-content:space-between;gap:10px;align-items:baseline}.ct-l1 b{overflow-wrap:anywhere}.ct-l1 span{font-variant-numeric:tabular-nums;white-space:nowrap}" +
    ".ct-bar{height:8px;border-radius:999px;background:rgba(140,154,179,.18);overflow:hidden;margin:6px 0 4px}.ct-bar i{display:block;height:100%;border-radius:999px;background:#2FD47E}" +
    ".ct-bar i.w{background:#F2B544}.ct-bar i.x{background:#FF6B6B}.ct-meta{font-size:12.5px;line-height:1.5;color:var(--muted,#8C9AB3);font-variant-numeric:tabular-nums}" +
    ".ct-up{color:#FF8A8A}.ct-down{color:#2FD47E}.ct-f{display:flex;gap:8px;flex-wrap:wrap;align-items:flex-end;margin-top:12px}" +
    ".ct-f label{display:flex;flex-direction:column;gap:4px;margin:0;font-weight:600;font-size:12.5px;color:var(--muted,#8C9AB3);flex:1;min-width:120px}" +
    ".ct-f input,.ct-f select{font:inherit;font-size:14px;padding:8px 10px;border-radius:10px;border:1px solid rgba(140,154,179,.3);background:rgba(140,154,179,.08);color:inherit;min-width:0;width:100%}" +
    ".ct-list{list-style:none;margin:10px 0 0;padding:0}.ct-list li{display:flex;gap:10px;align-items:center;justify-content:space-between;padding:9px 0;border-top:1px solid rgba(140,154,179,.18);flex-wrap:wrap}" +
    ".ct-list li:first-child{border-top:0}.ct-list .tx{flex:1;min-width:0;overflow-wrap:anywhere}.ct-list .tx small{display:block;color:var(--muted,#8C9AB3)}" +
    ".ct-x{border:0;background:transparent;color:var(--muted,#8C9AB3);cursor:pointer;font:inherit;font-size:13px;padding:4px 8px;border-radius:8px}.ct-x:hover{color:#FF8A8A}" +
    ".ct-x.conf{color:#FF6B6B;font-weight:600}.ct-vazio{color:var(--muted,#8C9AB3);margin:8px 0 0;line-height:1.5}.ct-vazio code{font:inherit;font-weight:600;color:inherit}" +
    ".ct-trava{margin:0 0 18px;padding:12px 16px;border-radius:14px;border:1px solid rgba(242,181,68,.45);background:rgba(242,181,68,.08);line-height:1.5}" +
    ".ct-sem li{display:grid;grid-template-columns:1fr;gap:8px}.ct-sem .ct-f{margin-top:0}.ct-chk{flex-direction:row!important;align-items:center;gap:6px!important;flex:none!important;min-width:0!important}.ct-chk input{width:auto}";
  document.head.appendChild(st);

  function opcoes(sel) {
    return (D && D.sugestoes || []).map(function (c) { return '<option value="' + esc(c) + '"' + (c === sel ? " selected" : "") + ">" + esc(nome(c)) + "</option>"; }).join("");
  }
  function lista() { return '<datalist id="ct-cats">' + (D && D.sugestoes || []).map(function (c) { return '<option value="' + esc(nome(c)) + '">'; }).join("") + "</datalist>"; }

  function render() {
    var s = $("p-cats");
    if (!s) return;
    if (!D) { s.innerHTML = '<div class="skeleton"></div>'; return; }
    var b = D.bloqueios || {}, cats = D.categorias || [], max = 0;
    cats.forEach(function (c) { max = Math.max(max, Number(c.valor) || 0, Number(c.limite) || 0); });
    var h = "";
    if (b.regras || b.limites) h += '<div class="ct-trava">🔒 Ver os gastos por categoria vale para todos os planos. <b>Regras e limites</b> fazem parte do plano <b>Completo</b>. Para trocar de plano, use a aba Minha conta.</div>';
    h += '<div class="ct-top"><div><h2>Gastos por categoria</h2><small>' + esc(D.rotulo || "") + " · " + esc(brl(D.total)) + '</small></div><div class="ct-per" role="group" aria-label="Período">' +
      [["mes", "Este mês"], ["mes_passado", "Mês passado"], ["3meses", "3 meses"]].map(function (o) { return '<button type="button" data-per="' + o[0] + '" aria-pressed="' + (PER === o[0]) + '">' + o[1] + "</button>"; }).join("") + "</div></div>";

    // 1) Gastos por categoria
    var hc = cats.length ? '<ul class="ct-rows">' + cats.map(function (c) {
      var v = Number(c.valor) || 0, lim = Number(c.limite) || 0, a = Number(c.anterior) || 0;
      var pct = lim ? Math.round(v / lim * 100) : 0, cls = lim ? (pct >= 100 ? "x" : pct >= 80 ? "w" : "") : "";
      var w = lim ? Math.min(100, pct) : (max ? Math.round(v / max * 100) : 0);
      var dif = a > 0 ? Math.round((v - a) / a * 100) : null;
      var partes = [c.qtd ? c.qtd + (c.qtd === 1 ? " lançamento" : " lançamentos") : "sem gastos"];
      if (dif !== null && PER !== "3meses" && v > 0) partes.push('<span class="' + (dif > 0 ? "ct-up" : "ct-down") + '">' + (dif > 0 ? "▲ " : "▼ ") + Math.abs(dif) + "% vs. período anterior</span>");
      if (lim) partes.push("limite " + esc(brl(lim)) + " (" + pct + "%)");
      var meta = partes.join(" · ");
      return '<li><div class="ct-l1"><b>' + esc(nome(c.categoria)) + "</b><span>" + esc(brl(v)) + '</span></div><div class="ct-bar" aria-hidden="true"><i class="' + cls + '" style="width:' + w + '%"></i></div><div class="ct-meta">' + meta + "</div></li>";
    }).join("") + "</ul>" : '<p class="ct-vazio">Nenhum gasto neste período. Mande no WhatsApp algo como <code>mercado 120</code> que ele aparece aqui na categoria certa.</p>';

    // 2) Sem categoria
    var sem = D.sem_categoria || [];
    var hs = sem.length ? '<ul class="ct-list ct-sem">' + sem.map(function (t) {
      var PULA = ["pix", "para", "compra", "pagamento", "pagto", "pgto", "transferencia", "transferência", "debito", "débito", "credito", "crédito", "cartao", "cartão", "com", "dos", "das", "pedido"];
      var pal = String(t.descricao || "").toLowerCase().split(/[\s\-\/*]+/).filter(function (x) { return x.length > 2 && !/^\d+$/.test(x) && PULA.indexOf(x) < 0; })[0] || "";
      return '<li data-tid="' + esc(t.id) + '"><div class="tx">' + esc(t.descricao || "Sem descrição") + "<small>" + esc(dataBR(t.data)) + " · " + esc(brl(t.valor)) + "</small></div>" +
        '<form class="ct-f" data-form="tx"><label>Categoria<select name="cat" required><option value="">Escolher…</option>' + opcoes("") + "</select></label>" +
        (b.regras ? "" : '<label class="ct-chk"><input type="checkbox" name="regra"> Usar sempre para</label><label>Palavra<input name="pad" maxlength="60" value="' + esc(pal) + '"></label>') +
        '<button class="btn btn-primary btn-sm" type="submit">Salvar</button></form></li>';
    }).join("") + "</ul>" : '<p class="ct-vazio">Tudo categorizado neste período. 👏</p>';

    // 3) Regras
    var rg = D.regras || [];
    var hr = (rg.length ? '<ul class="ct-list">' + rg.map(function (r) {
      return '<li><div class="tx"><b>' + esc(r.padrao) + "</b> → " + esc(nome(r.categoria)) + '</div><button class="ct-x" type="button" data-apagar="regra" data-id="' + esc(r.id) + '">Remover</button></li>';
    }).join("") + "</ul>" : '<p class="ct-vazio">Nenhuma regra ainda. Ensine pelo WhatsApp (<code>padaria é alimentação</code>) ou aqui embaixo. Quando você corrige a categoria de um gasto, o Dyno também aprende.</p>') +
      (b.regras ? "" : '<form class="ct-f" data-form="regra"><label>Quando o gasto tiver<input name="pad" maxlength="60" placeholder="ex.: padaria" required></label><label>Usar a categoria<input name="cat" maxlength="30" list="ct-cats" placeholder="ex.: Alimentação" required></label><button class="btn btn-primary btn-sm" type="submit">Adicionar</button></form>');

    // 4) Limites
    var lm = D.limites || [], tot = D.limite_total;
    var hl = '<ul class="ct-list">' + (tot ? '<li><div class="tx"><b>Orçamento do mês inteiro</b><small>' + esc(brl(tot.limite)) + '</small></div><button class="ct-x" type="button" data-apagar="limite" data-id="' + esc(tot.id) + '">Remover</button></li>' : "") +
      lm.map(function (l) { return '<li><div class="tx"><b>' + esc(nome(l.categoria)) + "</b><small>" + esc(brl(l.limite)) + ' por mês</small></div><button class="ct-x" type="button" data-apagar="limite" data-id="' + esc(l.id) + '">Remover</button></li>'; }).join("") + "</ul>";
    if (!tot && !lm.length) hl = '<p class="ct-vazio">Nenhum limite ainda. O Dyno avisa quando um gasto chega a 80% e a 100% do limite.</p>';
    if (!b.limites) hl += '<form class="ct-f" data-form="limite"><label>Categoria<select name="cat" required><option value="">Escolher…</option><option value="__total">Mês inteiro (todas)</option>' + opcoes("") + '</select></label><label>Limite por mês (R$)<input name="val" inputmode="decimal" placeholder="ex.: 800" required></label><button class="btn btn-primary btn-sm" type="submit">Salvar</button></form>';

    h += '<div class="ct-grid"><div class="box">' + hc + '</div><div class="box"><h2>Sem categoria</h2><p class="ct-vazio" style="margin-top:0">Gastos que ficaram em Outros. Escolha a categoria certa.</p>' + hs + "</div>" +
      '<div class="box"><h2>Regras que o Dyno aprendeu</h2>' + hr + '</div><div class="box"><h2>Limites</h2>' + hl + "</div></div>" + lista() +
      '<p class="ct-vazio" style="margin-top:18px">Tudo o que você muda aqui vale também no WhatsApp, e o contrário também.</p>';
    s.innerHTML = h;
    ligar(s);
  }

  function aplicar(r, msg) {
    ocupado = false;
    if (r && r.ok) { D = r; render(); if (msg) toast(msg); }
    else toast(ERRO[r && r.erro] || "Não consegui salvar agora. Tente de novo em instantes.");
  }
  function enviar(corpo, msg) { if (ocupado) return; ocupado = true; corpo.periodo = PER; api(corpo).then(function (r) { aplicar(r, msg); }); }

  function ligar(s) {
    s.querySelectorAll("[data-per]").forEach(function (x) { x.addEventListener("click", function () { PER = x.getAttribute("data-per"); D = null; render(); carregar(); }); });
    s.querySelectorAll("[data-apagar]").forEach(function (x) {
      x.addEventListener("click", function () {
        if (!x.classList.contains("conf")) { x.classList.add("conf"); x.textContent = "Confirmar"; setTimeout(function () { if (x.isConnected) { x.classList.remove("conf"); x.textContent = "Remover"; } }, 4000); return; }
        var tipo = x.getAttribute("data-apagar");
        enviar({ op: tipo + "_apagar", id: x.getAttribute("data-id") }, tipo === "regra" ? "Regra removida." : "Limite removido.");
      });
    });
    s.querySelectorAll("form[data-form]").forEach(function (f) {
      f.addEventListener("submit", function (ev) {
        ev.preventDefault();
        var t = f.getAttribute("data-form"), e = f.elements;
        if (t === "regra") enviar({ op: "regra_salvar", padrao: e.pad.value.trim(), categoria: e.cat.value.trim() }, "Regra salva. O Dyno já usa nos próximos gastos.");
        else if (t === "limite") {
          var c = e.cat.value, v = e.val.value.trim();
          enviar(c === "__total" ? { op: "limite_salvar", total: true, limite: v } : { op: "limite_salvar", categoria: c, limite: v }, "Limite salvo.");
        } else if (t === "tx") {
          var li = f.closest("[data-tid]"), cr = { op: "transacao_categoria", id: li.getAttribute("data-tid"), categoria: e.cat.value };
          if (e.regra && e.regra.checked) { cr.regra = true; cr.padrao = e.pad.value.trim(); }
          enviar(cr, cr.regra ? "Categoria trocada e regra criada." : "Categoria trocada.");
        }
      });
    });
  }

  function carregar() { api({ op: "ver", periodo: PER }).then(function (r) { if (r && r.ok) { D = r; render(); } else { var s = $("p-cats"); if (s) s.innerHTML = '<div class="box"><p>Não consegui carregar agora. Tente de novo em instantes.</p></div>'; } }); }

  function aba() {
    if (montou) return;
    var tc = $("t-comp") || $("t-conta"), pp = $("p-painel");
    if (!tc || !pp) return;
    montou = true;
    var b = document.createElement("button");
    b.className = "tab"; b.id = "t-cats"; b.type = "button"; b.textContent = "Categorias";
    b.setAttribute("role", "tab"); b.setAttribute("aria-selected", "false"); b.setAttribute("aria-controls", "p-cats");
    tc.parentNode.insertBefore(b, tc.nextSibling);
    var s = document.createElement("section");
    s.className = "panel"; s.id = "p-cats"; s.hidden = true; s.setAttribute("role", "tabpanel"); s.setAttribute("aria-labelledby", "t-cats");
    pp.parentNode.appendChild(s);
    b.addEventListener("click", function () {
      document.querySelectorAll('[role="tab"]').forEach(function (t) { t.setAttribute("aria-selected", String(t === b)); });
      document.querySelectorAll('[role="tabpanel"]').forEach(function (x) { x.hidden = x !== s; });
      try { sessionStorage.setItem("dyno_aba", "cats"); } catch (e) {}
      try { if (/^\/minhaconta/.test(location.pathname)) history.replaceState(null, "", "/minhaconta/categorias"); } catch (e) {}
      render(); if (!D) carregar();
    });
    document.addEventListener("click", function (ev) {
      var t = ev.target && ev.target.closest ? ev.target.closest('[role="tab"]') : null;
      if (t && t !== b) { s.hidden = true; b.setAttribute("aria-selected", "false"); try { if (sessionStorage.getItem("dyno_aba") === "cats") sessionStorage.removeItem("dyno_aba"); } catch (e) {} }
    }, true);
    var quer = /\/minhaconta\/categorias/.test(location.pathname) || location.hash === "#categorias";
    if (!quer) { try { quer = sessionStorage.getItem("dyno_aba") === "cats"; } catch (e) {} }
    if (quer) setTimeout(function () { b.click(); }, 600);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", aba); else aba();
}();