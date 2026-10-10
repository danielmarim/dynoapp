/* 10/10/2026: painel "ao vivo". Confere o painel a cada 30 s (só com a página visível) e
   ao voltar para a aba do navegador. Se chegou lançamento, tarefa, lembrete ou conta nova,
   recarrega a página sozinho quando o Painel estiver aberto; nas outras abas, recarrega ao voltar para o Painel. */
!function () {
  "use strict";
  var ultimo = "", conferido = 0, pendente = false, rodando = false, of = window.fetch;
  var $ = function (id) { return document.getElementById(id); };
  function marca(j) {
    var r = j.resumo || {}, u = (j.ultimos || [])[0] || {};
    return JSON.stringify([r.gastos, r.receitas, r.lancamentos, u.data, u.descricao, u.valor, (j.tarefas || []).length, (j.lembretes || []).length, (j.contas || []).length, (j.agenda || []).length]);
  }
  function hora() { return new Date().toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit", timeZone: "America/Sao_Paulo" }); }
  function selo(txt) {
    var s = $("pv-at");
    if (!s) {
      var sub = $("sub"); if (!sub) return;
      s = document.createElement("small"); s.id = "pv-at";
      s.style.cssText = "display:block;margin-top:4px;font-size:12px;opacity:.75";
      sub.parentNode.insertBefore(s, sub.nextSibling);
    }
    s.textContent = txt;
  }
  function painelAberto() { var p = $("p-painel"); return !!p && !p.hidden; }
  function ocupada() {
    var a = document.activeElement;
    return !!(a && /^(INPUT|TEXTAREA|SELECT)$/.test(a.tagName)) || !!document.querySelector("dialog[open]");
  }
  function recarregar() { selo("Chegou coisa nova · atualizando…"); setTimeout(function () { location.reload(); }, 700); }
  function veio(j) {
    if (!j || !j.ok) return;
    var m = marca(j);
    conferido = Date.now();
    if (ultimo && m !== ultimo) {
      if (painelAberto() && !ocupada()) { recarregar(); return; }
      pendente = true;
    }
    if (!ultimo || !pendente) ultimo = m;
    selo("Atualiza sozinho · conferido às " + hora());
  }
  // escuta a resposta do painel feita pela própria página (carga inicial)
  window.fetch = function (u, o) {
    var p = of.apply(this, arguments);
    try {
      if (String(u) === "/api" && o && typeof o.body === "string" && o.body.indexOf('"painel"') > -1) {
        p.then(function (r) { return r.ok ? r.clone().json() : null; }).then(veio).catch(function () { });
      }
    } catch (e) { }
    return p;
  };
  function conferir(forcar) {
    if (rodando || document.hidden) return;
    if (!forcar && Date.now() - conferido < 25000) return;
    rodando = true;
    of("/api", { method: "POST", credentials: "same-origin", headers: { "Content-Type": "application/json", "X-Requested-With": "dyno" }, body: JSON.stringify({ acao: "painel" }) })
      .then(function (r) { if (r.status === 401) { location.replace("/entrar"); return null; } return r.ok ? r.json() : null; })
      .then(veio).catch(function () { }).then(function () { rodando = false; });
  }
  setInterval(function () { conferir(false); }, 30000);
  document.addEventListener("visibilitychange", function () { if (!document.hidden) conferir(Date.now() - conferido > 8000); });
  window.addEventListener("pageshow", function (e) { if (e.persisted) conferir(true); });
  window.addEventListener("focus", function () { conferir(false); });
  document.addEventListener("click", function (ev) {
    var t = ev.target && ev.target.closest ? ev.target.closest("#t-painel") : null;
    if (t && pendente) recarregar();
  }, true);
}();