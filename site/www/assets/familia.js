(function () {
  'use strict';
  // Aba "Família" da área do cliente (Modo família do plano Premium) e acerto do texto do plano/preço em "Minha conta".
  var WA_NUM = '5511939497178';
  var WA = 'https://wa.me/' + WA_NUM;
  var PRECOS = { essencial: [19.9, 199.9], beta: [19.9, 199.9], completo: [29.9, 299.9], premium: [39.9, 399.9] };
  var usr = null, dados = null, carregando = false, msg = null, pedindoRemover = null;
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };
  var brl = function (v) { return (Number(v) || 0).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }); };
  function fone(n) {
    var d = String(n || '').replace(/\D/g, '');
    if (d.length === 13) return '+' + d.slice(0, 2) + ' ' + d.slice(2, 4) + ' ' + d.slice(4, 9) + '-' + d.slice(9);
    if (d.length === 12) return '+' + d.slice(0, 2) + ' ' + d.slice(2, 4) + ' ' + d.slice(4, 8) + '-' + d.slice(8);
    return d ? '+' + d : '';
  }
  function api(corpo) {
    return fetch('/api', {
      method: 'POST', credentials: 'same-origin',
      headers: { 'Content-Type': 'application/json', 'X-Requested-With': 'dyno' },
      body: JSON.stringify(corpo)
    }).then(function (r) {
      return r.json().catch(function () { return {}; }).then(function (j) { j._status = r.status; return j; });
    }).catch(function () { return { ok: false, erro: 'indisponivel' }; });
  }

  /* ---------- plano e preço em "Minha conta" ---------- */
  function precoDe(u) {
    var n = String(u && (u.nivel_preco || u.nivel) || 'completo').toLowerCase();
    return PRECOS[n] || PRECOS.completo;
  }
  function fixPlano() {
    if (!usr || usr.plano === 'familia') return;
    var p = precoDe(usr), anual = usr.ciclo === 'YEARLY', nome = (usr.nivel_nome || 'Completo') + (usr.nivel_preco === 'beta' ? ' (preço do Beta)' : usr.nivel_preco && usr.nivel && usr.nivel_preco !== usr.nivel ? ' (cortesia)' : '');
    var cont = document.getElementById('p-conta'); if (!cont) return;
    [].slice.call(cont.querySelectorAll('dt')).forEach(function (dt) {
      if (dt.textContent.trim() !== 'Plano') return;
      var dd = dt.nextElementSibling; if (!dd) return;
      var t = nome + ' · ' + (anual ? brl(p[1]) + ' por ano' : brl(p[0]) + ' por mês');
      if (dd.textContent !== t) dd.textContent = t;
    });
    var bt = document.getElementById('trocar');
    if (bt) {
      var t2 = anual ? 'Mudar para o mensal' : 'Mudar para o anual (economize ' + brl(p[0] * 12 - p[1]) + ')';
      if (bt.textContent !== t2) bt.textContent = t2;
    }
  }
  function fixDialogo() {
    var el = document.getElementById('dlg-p'); if (!el || !usr) return;
    var p = precoDe(usr), t = el.textContent, novo = t;
    if (/passa a ser anual/.test(t)) novo = 'Sua assinatura passa a ser anual, de ' + brl(p[1]) + ' por ano (equivale a ' + brl(p[1] / 12) + ' por mês). A próxima cobrança já vem no novo valor.';
    else if (/passa a ser mensal/.test(t)) novo = 'Sua assinatura passa a ser mensal, de ' + brl(p[0]) + ' por mês. A próxima cobrança já vem no novo valor.';
    if (novo !== t) el.textContent = novo;
  }
  function observar() {
    if (!window.MutationObserver) return;
    var c = document.getElementById('p-conta'), d = document.getElementById('dlg-p');
    if (c) new MutationObserver(fixPlano).observe(c, { childList: true, subtree: true });
    if (d) new MutationObserver(fixDialogo).observe(d, { childList: true, characterData: true, subtree: true });
  }
  var of = window.fetch;
  window.fetch = function (u, o) {
    var p = of.apply(this, arguments);
    try {
      if (String(u) === '/api' && o && typeof o.body === 'string' && o.body.indexOf('"conta"') > -1) {
        p.then(function (r) { return r.clone().json(); }).then(function (j) {
          if (j && j.ok && j.usuario) { usr = j.usuario; setTimeout(fixPlano, 0); setTimeout(fixPlano, 300); }
        }).catch(function () { });
      }
    } catch (e) { }
    return p;
  };

  /* ---------- aba Família ---------- */
  function aba() { return document.getElementById('t-familia'); }
  function painel() { return document.getElementById('p-familia'); }
  function montar() {
    var ref = document.getElementById('t-conta'), pref = document.getElementById('p-conta');
    if (!ref || !pref || aba()) return;
    var b = document.createElement('button');
    b.className = 'tab'; b.id = 't-familia'; b.type = 'button'; b.textContent = 'Família';
    b.setAttribute('role', 'tab'); b.setAttribute('aria-selected', 'false'); b.setAttribute('aria-controls', 'p-familia');
    ref.parentNode.insertBefore(b, ref);
    var s = document.createElement('section');
    s.className = 'panel'; s.id = 'p-familia'; s.hidden = true;
    s.setAttribute('role', 'tabpanel'); s.setAttribute('aria-labelledby', 't-familia');
    pref.parentNode.insertBefore(s, pref);
    b.addEventListener('click', abrir);
    document.querySelectorAll('[role="tab"]').forEach(function (t) {
      if (t !== b) t.addEventListener('click', function () { s.hidden = true; b.setAttribute('aria-selected', 'false'); });
    });
  }
  function abrir() {
    var b = aba(), s = painel(); if (!b || !s) return;
    document.querySelectorAll('[role="tab"]').forEach(function (t) { t.setAttribute('aria-selected', String(t === b)); });
    document.querySelectorAll('[role="tabpanel"]').forEach(function (p) { p.hidden = p !== s; });
    carregar();
  }
  function carregar() {
    if (carregando) return; carregando = true;
    var s = painel(); if (s && dados === null) s.innerHTML = '<div class="skeleton"></div>';
    api({ acao: 'familia' }).then(function (r) { dados = r; carregando = false; render(); });
  }

  var ERROS = {
    nome_invalido: 'Informe o nome da pessoa (de 2 a 60 letras).',
    numero_invalido: 'O WhatsApp não parece válido. Use o DDD e o número, por exemplo (11) 91234-5678.',
    limite: 'O grupo já está completo. Remova alguém para adicionar outra pessoa.',
    proprio_numero: 'Esse é o seu próprio número, que já faz parte do grupo.',
    ja_cliente: 'Esse número já é cliente do Dyno e não pode entrar no seu grupo.',
    ja_membro: 'Esse número já faz parte de um grupo família.',
    nao_encontrado: 'Não encontramos essa pessoa no grupo. Atualize a página.',
    plano: 'O Modo família é exclusivo do plano Premium.',
    status: 'Seu acesso está pausado, por isso o grupo não pode ser alterado agora.',
    sessao: 'Sua sessão expirou. Entre novamente.',
    indisponivel: 'Não foi possível falar com o servidor. Tente de novo em instantes.'
  };

  function render() {
    var s = painel(); if (!s) return;
    var d = dados;
    if (!d) { s.innerHTML = '<div class="skeleton"></div>'; return; }
    if (d.ok === false && (d.erro === 'plano' || d.erro === 'bloqueado')) { s.innerHTML = upsell(d.nivel); return; }
    if (d.ok === false) { s.innerHTML = '<div class="box"><h2>Família</h2><p class="fam-msg err">' + esc(ERROS[d.erro] || 'Não foi possível carregar agora.') + '</p></div>'; return; }
    var mem = d.membros || [], max = Number(d.max) || 4, vagas = Number(d.vagas);
    if (isNaN(vagas)) vagas = Math.max(0, max - 1 - mem.length);
    var total = mem.length + 1;
    var lista = '<li class="fam-item"><div><b>' + esc(d.titular || 'Você') + ' (você)</b><small>Titular do plano</small></div></li>' +
      mem.map(function (m) {
        var conf = pedindoRemover === m.id;
        return '<li class="fam-item"><div><b>' + esc(m.nome) + '</b><small>' + esc(fone(m.whatsapp)) + '</small></div>' +
          (conf ? '<div class="actions" style="margin:0"><button class="btn btn-danger btn-sm" type="button" data-conf="' + esc(m.id) + '">Confirmar remoção</button><button class="btn btn-ghost btn-sm" type="button" data-cancela="1">Cancelar</button></div>'
            : '<button class="btn btn-ghost btn-sm" type="button" data-rem="' + esc(m.id) + '">Remover</button>') + '</li>';
      }).join('');
    var form = vagas > 0
      ? '<form class="box fam-form" id="fam-form" novalidate><h3 style="margin:0">Adicionar pessoa</h3>' +
        '<div class="row"><label>Nome<input class="input" id="fam-nome" maxlength="60" autocomplete="off" placeholder="Ex.: Maria"></label>' +
        '<label>WhatsApp com DDD<input class="input" id="fam-fone" inputmode="tel" maxlength="20" autocomplete="off" placeholder="(11) 91234-5678"></label></div>' +
        '<label class="fam-check"><input type="checkbox" id="fam-ok"><span>Essa pessoa sabe e está de acordo em compartilhar comigo os gastos, contas e lembretes.</span></label>' +
        '<div class="actions" style="margin:0"><button class="btn btn-primary btn-sm" type="submit">Adicionar</button></div></form>'
      : '<div class="box"><p class="fam-msg">O grupo está completo (' + max + ' pessoas). Para adicionar outra pessoa, remova uma antes.</p></div>';
    s.innerHTML = '<div class="fam-wrap">' +
      '<div class="fam-top"><div><h2 style="margin:0">Família</h2><p class="fam-count">' + total + ' de ' + max + ' pessoas no grupo · ' + vagas + (vagas === 1 ? ' vaga livre' : ' vagas livres') + '</p></div></div>' +
      '<ul class="fam-list">' + lista + '</ul>' +
      (msg ? '<p class="fam-msg ' + msg.t + '" role="status">' + esc(msg.m) + '</p>' : '') +
      form +
      '<div class="box"><h3 style="margin:0 0 6px">Como a pessoa começa</h3><p class="fam-howto">Depois de adicionar, peça para ela mandar um <b>“oi”</b> para o número do Dyno, <a href="' + WA + '" rel="noopener">+55 11 93949-7178</a>. A partir daí ela fala com o Dyno e a Dina no próprio WhatsApp, vendo e lançando nos mesmos gastos, contas e lembretes que os seus. Quem entra no grupo não tem acesso a esta área do cliente, e você pode remover a pessoa quando quiser.</p></div>' +
      '</div>';
    ligar(s);
  }
  function upsell(nivel) {
    var link = WA + '?text=' + encodeURIComponent('Quero ativar o Modo família');
    return '<div class="fam-wrap"><div class="box fam-up"><span class="tier t-prem">Premium</span><h2 style="margin:10px 0 6px">Modo família</h2>' +
      '<p>Cadastre até 3 pessoas para usar o Dyno e a Dina no próprio WhatsApp, com os mesmos gastos, contas e lembretes que os seus. É ideal para casais e para a casa toda.</p>' +
      '<h3 style="margin:16px 0 6px">Integrantes do seu plano</h3><ul class="fam-list"><li class="fam-item"><div><b>' + esc((usr && usr.nome ? String(usr.nome).split(' ')[0] : 'Você')) + ' (você)</b><small>Titular do plano · 1 de 4 pessoas</small></div></li></ul>' +
      '<p class="fam-howto"><b>Recurso em liberação.</b> O Modo família é ativado pela nossa equipe. Para pedir a ativação, fale com a gente no WhatsApp.</p>' +
      '<div class="actions"><a class="btn btn-primary btn-sm" href="' + link + '" rel="noopener">Pedir ativação</a><a class="btn btn-ghost btn-sm" href="/precos">Ver os planos</a></div></div></div>';
  }
  function ligar(s) {
    var f = s.querySelector('#fam-form');
    if (f) f.addEventListener('submit', function (e) {
      e.preventDefault();
      var nome = s.querySelector('#fam-nome').value.trim(), tel = s.querySelector('#fam-fone').value.trim(), ok = s.querySelector('#fam-ok').checked;
      if (!ok) { msg = { t: 'err', m: 'Confirme que a pessoa está de acordo com o compartilhamento.' }; render(); return; }
      var bt = f.querySelector('button[type=submit]'); bt.disabled = true;
      api({ acao: 'familia_add', nome: nome, whatsapp: tel }).then(function (r) {
        if (r.ok) { msg = { t: 'ok', m: 'Pronto! ' + nome + ' foi adicionada. Peça para ela mandar um “oi” ao número do Dyno.' }; dados = r; }
        else { msg = { t: 'err', m: ERROS[r.erro] || 'Não foi possível adicionar agora.' }; if (r.erro === 'sessao') setTimeout(function () { location.href = '/entrar'; }, 1500); }
        render();
      });
    });
    [].slice.call(s.querySelectorAll('[data-rem]')).forEach(function (b) { b.addEventListener('click', function () { pedindoRemover = b.getAttribute('data-rem'); msg = null; render(); }); });
    [].slice.call(s.querySelectorAll('[data-cancela]')).forEach(function (b) { b.addEventListener('click', function () { pedindoRemover = null; render(); }); });
    [].slice.call(s.querySelectorAll('[data-conf]')).forEach(function (b) {
      b.addEventListener('click', function () {
        b.disabled = true;
        api({ acao: 'familia_del', id: b.getAttribute('data-conf') }).then(function (r) {
          pedindoRemover = null;
          if (r.ok) { msg = { t: 'ok', m: 'Pessoa removida do grupo.' }; dados = r; }
          else msg = { t: 'err', m: ERROS[r.erro] || 'Não foi possível remover agora.' };
          render();
        });
      });
    });
  }

  function iniciar() {
    montar(); observar();
    setTimeout(function () {
      if (usr) return;
      api({ acao: 'conta' }).then(function (j) { if (j && j.ok && j.usuario) { usr = j.usuario; fixPlano(); } });
    }, 2500);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', iniciar); else iniciar();
})();
