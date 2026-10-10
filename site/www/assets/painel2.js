(function () {
  'use strict';
  var P = null, busy = false;
  var lk = document.createElement('link'); lk.rel = 'stylesheet'; lk.href = '/assets/painel2.css?v=1'; document.head.appendChild(lk);
  var brl = function (v) { return (Number(v) || 0).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }); };
  var cur = function (v) { return Math.round(Number(v) || 0).toLocaleString('pt-BR'); };
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };
  var COR = ['#0E8A60', '#FF8A3D', '#6C7BFF', '#14B37D', '#E8A33D', '#7B6FD6', '#B3261E', '#A9ADC6'];
  var of = window.fetch;
  window.fetch = function (u, o) {
    var p = of.apply(this, arguments);
    try {
      if (String(u) === '/api' && o && typeof o.body === 'string' && o.body.indexOf('"painel"') > -1) {
        p.then(function (r) { return r.clone().json(); }).then(function (j) { if (j && j.ok && !j.vazio) { P = j; setTimeout(melhorar, 60); } }).catch(function () { });
      }
    } catch (e) { }
    return p;
  };
  function delta(atual, ant, ruimSeSobe) {
    if (!ant) return '<span class="dl nd">sem mês anterior</span>';
    var pc = (atual - ant) / ant * 100, sobe = pc >= 0;
    var ruim = ruimSeSobe ? sobe : !sobe;
    return '<span class="dl' + (ruim ? ' ruim' : '') + '">' + (sobe ? '▲' : '▼') + ' ' + Math.abs(pc).toFixed(0) + '% <small>vs mês anterior</small></span>';
  }
  function kpis(r) {
    var ks = document.querySelectorAll('#p-painel .kpi');
    if (ks.length < 3) return;
    var add = function (k, h) { if (!k.querySelector('.dl')) k.insertAdjacentHTML('beforeend', h); };
    add(ks[0], delta(r.gastos, r.gastos_ant, true));
    add(ks[1], delta(r.receitas, r.receitas_ant, false));
    var sa = r.receitas_ant - r.gastos_ant;
    add(ks[2], (r.receitas_ant || r.gastos_ant) ? '<span class="dl nd">mês anterior ' + brl(sa) + '</span>' : '<span class="dl nd">receitas − gastos</span>');
  }
  function fluxo(ms) {
    var max = 1; ms.forEach(function (m) { max = Math.max(max, m.gastos, m.receitas || 0); });
    return '<div class="leg"><span style="--c:var(--green-ink)">Entradas</span><span style="--c:var(--orange)">Saídas</span></div><div class="fx">' + ms.map(function (m) {
      var he = (m.receitas || 0) > 0 ? Math.max(3, m.receitas / max * 100) : 0, hs = m.gastos > 0 ? Math.max(3, m.gastos / max * 100) : 0;
      var sal = (m.receitas || 0) - m.gastos;
      return '<div class="m" tabindex="0" aria-label="' + esc(m.mes) + ': entradas ' + brl(m.receitas) + ', saídas ' + brl(m.gastos) + '"><span class="tip">Entradas ' + brl(m.receitas) + '<br>Saídas ' + brl(m.gastos) + '<br>Saldo ' + brl(sal) + '</span><i class="e" style="height:' + he + '%"></i><i class="s" style="height:' + hs + '%"></i><em>' + esc(String(m.mes).replace('.', '')) + '</em></div>';
    }).join('') + '</div><div style="height:24px"></div>';
  }
  function rosca(cs) {
    var tot = cs.reduce(function (s, c) { return s + c.valor; }, 0);
    if (!tot) return '<p class="empty">Nenhum gasto registrado neste mês ainda.</p>';
    var R = 62, C = 2 * Math.PI * R, off = 0, segs = '';
    cs.forEach(function (c, i) {
      var len = c.valor / tot * C;
      segs += '<circle cx="85" cy="85" r="' + R + '" fill="none" stroke="' + COR[i % COR.length] + '" stroke-width="26" stroke-dasharray="' + len.toFixed(2) + ' ' + (C - len).toFixed(2) + '" stroke-dashoffset="' + (-off).toFixed(2) + '" transform="rotate(-90 85 85)"><title>' + esc(c.nome) + ': ' + brl(c.valor) + '</title></circle>';
      off += len;
    });
    var svg = '<svg viewBox="0 0 170 170" role="img" aria-label="Gastos por categoria">' + segs + '<text class="ctr" x="85" y="86" text-anchor="middle" font-size="15">' + brl(tot).replace(/ /g, ' ') + '</text><text class="ctr2" x="85" y="102" text-anchor="middle">gasto no mês</text></svg>';
    var li = cs.slice(0, 6).map(function (c, i) { return '<li><i style="background:' + COR[i % COR.length] + '"></i><span>' + esc(c.nome) + '</span><b>' + brl(c.valor) + '</b><small>' + Math.round(c.valor / tot * 100) + '%</small></li>'; }).join('');
    return '<div class="rosca">' + svg + '<ul class="rl">' + li + '</ul></div>';
  }
  function limites(cs) {
    var l = cs.filter(function (c) { return c.limite; });
    if (!l.length) return '';
    return '<div class="box"><h2>Limites por categoria</h2><div class="hbar">' + l.map(function (c) {
      var pct = c.valor / c.limite * 100, cls = pct > 100 ? 'estourou' : pct >= 80 ? 'perto' : 'ok';
      var dica = pct > 100 ? 'passou ' + brl(c.valor - c.limite) : 'restam ' + brl(c.limite - c.valor);
      return '<div class="r lim ' + cls + '"><span>' + esc(c.nome) + '</span><div class="t"><div class="f" style="width:' + Math.min(100, Math.max(2, pct)) + '%"></div></div><span class="v">' + brl(c.valor) + '<small>de ' + brl(c.limite) + ' · ' + dica + '</small></span></div>';
    }).join('') + '</div></div>';
  }
  function dias(ds) {
    var max = 1, tot = 0, pico = ds[0] || { v: 0, d: '' };
    ds.forEach(function (x) { max = Math.max(max, x.v); tot += x.v; if (x.v > pico.v) pico = x; });
    var f = function (s) { var p = s.split('-'); return p[2] + '/' + p[1]; };
    var bars = ds.map(function (x, i) {
      var cls = 'd' + (i === ds.length - 1 ? ' hoje' : '') + (x.v ? '' : ' zero');
      var rot = (i % 7 === 0 && i < ds.length - 3) ? '<em>' + f(x.d) + '</em>' : '';
      return '<div class="' + cls + '" tabindex="0" aria-label="' + f(x.d) + ': ' + brl(x.v) + '"><span class="tip">' + f(x.d) + ' · ' + brl(x.v) + '</span><i style="height:' + (x.v ? Math.max(3, x.v / max * 100) : 0) + '%"></i>' + rot + '</div>';
    }).join('');
    return '<div class="dd-sum"><span>Total <b>' + brl(tot) + '</b></span><span>Média/dia <b>' + brl(tot / ds.length) + '</b></span>' + (pico.v ? '<span>Maior dia <b>' + f(pico.d) + ' · ' + brl(pico.v) + '</b></span>' : '') + '</div><div class="ddw"><div class="dd">' + bars + '</div></div>';
  }
  function melhorar() {
    if (!P || busy) return;
    var el = document.getElementById('p-painel');
    var d1 = el && el.querySelector('.dash');
    if (!d1 || el.querySelector('.fx')) return;
    busy = true;
    try {
      var cs = P.categorias || [], ms = P.meses || [];
      kpis(P.resumo || {});
      var h = '<div class="dash"><div class="box"><h2>Fluxo de caixa <small>6 meses</small></h2>' + fluxo(ms) + '</div>' +
        '<div class="box"><h2>Gastos por categoria <small>' + esc(P.mes) + '</small></h2>' + rosca(cs) + '</div></div>' +
        '<div class="dash"><div class="box"><h2>Gastos por dia <small>últimos 30 dias</small></h2>' + dias(P.dias || []) + '</div>' + (limites(cs) || '<div class="box"><h2>Dica</h2><p class="empty">Defina limites pelo WhatsApp (“limite de 800 em alimentação”) e acompanhe aqui.</p></div>') + '</div>';
      d1.outerHTML = h;
    } catch (e) { }
    busy = false;
  }
  new MutationObserver(function () { melhorar(); }).observe(document.documentElement, { childList: true, subtree: true });
})();
