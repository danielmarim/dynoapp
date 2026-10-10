/* Dyno · aba "Pedidos e funil" do /admin — 09/10/2026
   Funil (dyno_funil) e pedidos de função dos clientes (dyno_pedidos_funcao), com aprovar / arquivar / feito. */
(function () {
  'use strict';
  var A = window.DynoAdmin; if (!A) return;
  var api = A.api, esc = A.esc, toast = A.toast;
  var $ = function (id) { return document.getElementById(id); };
  var ST = { dias: 7, filtro: 'aberto', funil: null, ped: null, montado: false, ativo: false, timer: null, armado: null };
  var nf = function (v) { return (Number(v) || 0).toLocaleString('pt-BR'); };
  var pc = function (a, b) { return b ? Math.round(100 * a / b) + '%' : '—'; };
  var dataBR = function (s) { var d = new Date(s); return isNaN(d) ? '' : d.toLocaleString('pt-BR', { day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit', timeZone: 'America/Sao_Paulo' }); };
  var iso = function (d) { return new Date(d.getTime() - d.getTimezoneOffset() * 60000).toISOString().slice(0, 10); };

  var css = [
    '#tPedidos .pf-top{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;margin:18px 0 6px}',
    '#tPedidos h2{margin:0;font:600 13px var(--mono);letter-spacing:2px;color:var(--mut);text-transform:uppercase}',
    '#tPedidos .pf-sub{color:var(--dim);font-size:13px;margin:2px 0 0}',
    '.pf-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,420px),1fr));gap:14px;margin-top:12px}',
    '.pf-card{background:var(--panel);border:1px solid var(--line);border-radius:var(--r);padding:14px 16px;min-width:0}',
    '.pf-card h3{margin:0 0 10px;font:600 12px var(--mono);letter-spacing:1px;text-transform:uppercase;color:var(--mut)}',
    '.pf-fun{display:grid;gap:8px}',
    '.pf-row{display:grid;grid-template-columns:minmax(110px,150px) 1fr auto;gap:10px;align-items:center;font-size:13px}',
    '.pf-row .tr{height:16px;border-radius:5px;background:rgba(255,255,255,.04);overflow:hidden}',
    '.pf-row .tr i{display:block;height:100%;border-radius:5px;background:linear-gradient(90deg,var(--c,var(--cyan)),transparent 160%)}',
    '.pf-row b{font:600 14px var(--mono);font-variant-numeric:tabular-nums;text-align:right;min-width:72px}',
    '.pf-row b small{display:block;font:500 10px var(--mono);color:var(--dim)}',
    '.pf-list{list-style:none;margin:0;padding:0;display:grid;gap:6px;font-size:13px}',
    '.pf-list li{display:flex;justify-content:space-between;gap:10px;border-bottom:1px dashed var(--line);padding-bottom:5px}',
    '.pf-list li span:last-child{font-family:var(--mono);color:var(--mut)}',
    '.pf-tb{overflow-x:auto}.pf-tb table{min-width:520px}',
    '.pd-list{display:grid;gap:10px;margin-top:12px}',
    '.pd{background:var(--panel);border:1px solid var(--line);border-radius:var(--r);padding:14px 16px;display:grid;gap:8px;min-width:0}',
    '.pd-h{display:flex;gap:8px;align-items:center;flex-wrap:wrap;font:500 12px var(--mono);color:var(--mut)}',
    '.pd-h .st{border-radius:999px;padding:2px 9px;border:1px solid var(--line2);color:var(--fg)}',
    '.pd-h .st.avaliando,.pd-h .st.novo{border-color:var(--amber);color:var(--amber)}',
    '.pd-h .st.aprovado{border-color:var(--cyan);color:var(--cyan)}',
    '.pd-h .st.feito{border-color:var(--green);color:var(--green)}',
    '.pd-h .st.descartado{color:var(--dim)}',
    '.pd-t{font-size:16px;font-weight:600;overflow-wrap:anywhere}',
    '.pd-q{margin:0;color:var(--mut);font-size:13px;border-left:2px solid var(--line2);padding-left:10px;overflow-wrap:anywhere}',
    '.pd-av{display:grid;gap:4px;font-size:13px;background:rgba(255,255,255,.025);border-radius:10px;padding:10px 12px;overflow-wrap:anywhere}',
    '.pd-av .tags{display:flex;gap:6px;flex-wrap:wrap}',
    '.pd-av .tags span{font:500 11px var(--mono);border:1px solid var(--line2);border-radius:999px;padding:1px 8px;color:var(--mut)}',
    '.pd-av .tags span.v-sim{color:var(--green);border-color:rgba(47,227,160,.5)}',
    '.pd-av .tags span.v-nao{color:var(--rose);border-color:rgba(255,111,145,.45)}',
    '.pd-a{display:flex;gap:8px;flex-wrap:wrap;align-items:center}',
    '.pd-a small{color:var(--dim)}',
    '.pf-vazio{color:var(--dim);padding:18px 4px}'
  ].join('\n');
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

  function montar() {
    if (ST.montado) return; ST.montado = true;
    var tabs = $('tabs'), sec = $('tPedidos');
    if (!sec) { sec = document.createElement('section'); sec.id = 'tPedidos'; sec.hidden = true; var c = $('tCentral'); c.parentNode.insertBefore(sec, c.nextSibling); }
    sec.innerHTML =
      '<div class="pf-top"><div><h2>Funil</h2><p class="pf-sub" id="pfPer">Carregando…</p></div>' +
      '<div class="chips" id="pfDias"><button class="chip" data-d="7" aria-pressed="true">7 dias</button><button class="chip" data-d="30" aria-pressed="false">30 dias</button><button class="chip" data-d="90" aria-pressed="false">90 dias</button></div></div>' +
      '<div class="kpis" id="pfKpis"></div>' +
      '<div class="pf-grid"><div class="pf-card"><h3>Site → Beta</h3><div class="pf-fun" id="pfSite"></div></div>' +
      '<div class="pf-card"><h3>Convite → cliente pagante</h3><div class="pf-fun" id="pfConta"></div></div>' +
      '<div class="pf-card"><h3>De onde vêm os visitantes</h3><ul class="pf-list" id="pfOrig"></ul></div>' +
      '<div class="pf-card"><h3>Funções usadas (pessoas, desde o início)</h3><div class="pf-fun" id="pfFunc"></div></div></div>' +
      '<div class="pf-card" style="margin-top:14px"><h3>Coortes por semana de cadastro</h3><div class="pf-tb tbox" id="pfCoor"></div></div>' +
      '<div class="pf-top" style="margin-top:28px"><div><h2>Pedidos de função</h2><p class="pf-sub">O que os clientes pediram e o Dyno ainda não faz. A IA avalia; você decide.</p></div>' +
      '<div class="chips" id="pdFil"><button class="chip" data-f="aberto" aria-pressed="true">Em aberto <span class="n" id="pdNa"></span></button><button class="chip" data-f="aprovado" aria-pressed="false">Aprovados <span class="n" id="pdNp"></span></button><button class="chip" data-f="feito" aria-pressed="false">Feitos <span class="n" id="pdNf"></span></button><button class="chip" data-f="descartado" aria-pressed="false">Arquivados <span class="n" id="pdNd"></span></button><button class="chip" data-f="todos" aria-pressed="false">Todos</button></div></div>' +
      '<div class="pd-list" id="pdList"><p class="pf-vazio">Carregando…</p></div>';
    $('pfDias').addEventListener('click', function (e) { var b = e.target.closest('[data-d]'); if (!b) return; ST.dias = +b.dataset.d; [].forEach.call(this.children, function (x) { x.setAttribute('aria-pressed', String(x === b)); }); funil(); });
    $('pdFil').addEventListener('click', function (e) { var b = e.target.closest('[data-f]'); if (!b) return; ST.filtro = b.dataset.f; [].forEach.call(this.children, function (x) { x.setAttribute('aria-pressed', String(x === b)); }); renderPed(); });
    $('pdList').addEventListener('click', acao);
  }

  /* ---------- funil ---------- */
  function funil() {
    var ate = new Date(), de = new Date(Date.now() - (ST.dias - 1) * 86400000);
    api({ acao: 'admin_funil', de: iso(de), ate: iso(ate) }).then(function (r) {
      if (!r || !r.ok) { $('pfPer').textContent = 'Não consegui carregar o funil' + (r && r._status ? ' (' + r._status + ')' : '') + '.'; return; }
      ST.funil = r; renderFunil();
    });
  }
  function barras(el, linhas, cor) {
    var max = Math.max.apply(null, linhas.map(function (x) { return x[1]; }).concat([1]));
    el.innerHTML = linhas.map(function (x, i) {
      var prev = i ? linhas[i - 1][1] : null;
      return '<div class="pf-row" style="--c:' + (x[2] || cor) + '"><span>' + esc(x[0]) + '</span><div class="tr"><i style="width:' + (100 * x[1] / max).toFixed(1) + '%"></i></div><b>' + nf(x[1]) + (prev != null ? '<small>' + pc(x[1], prev) + ' da etapa anterior</small>' : '') + '</b></div>';
    }).join('');
  }
  function renderFunil() {
    var f = ST.funil, d = function (s) { var p = String(s || '').split('-'); return p.length === 3 ? p[2] + '/' + p[1] : s; };
    $('pfPer').textContent = d(f.de) + ' a ' + d(f.ate) + (f.site_desde ? ' · site medido desde ' + d(f.site_desde) : '') + ' · sem robôs e sem a família';
    var k = [['Visitantes', f.visitantes, 'pessoas no site', 'var(--cyan)'], ['Pedidos Beta', f.beta_pedidos, 'pelo site', 'var(--violet)'], ['Convites enviados', f.convites_enviados, (f.convites_abertos || 0) + ' ainda abertos', 'var(--blue)'],
      ['Cadastros', f.cadastros, 'no período', 'var(--green)'], ['Ativados 24h', f.ativados_24h, pc(f.ativados_24h, f.cadastros) + ' dos cadastros', 'var(--green)'], ['Pagamentos', f.pagamentos, (f.cancelamentos || 0) + ' cancelamentos', 'var(--amber)']];
    $('pfKpis').innerHTML = k.map(function (x) { return '<div class="kpi" style="--c:' + x[3] + '"><div class="l">' + x[0] + '</div><div class="v">' + nf(x[1]) + '</div><div class="h">' + esc(x[2]) + '</div></div>'; }).join('');
    barras($('pfSite'), [['Visitantes', +f.visitantes || 0], ['Viram o Beta', +f.viu_beta || 0], ['Pediram vaga', +f.beta_pedidos || 0]], 'var(--cyan)');
    $('pfSite').insertAdjacentHTML('beforeend', '<p class="pf-sub" style="margin-top:4px">' + nf(f.viu_precos) + ' visitantes abriram a página de preços. Pedidos de vaga contam também quem entrou direto no link do Beta.</p>');
    barras($('pfConta'), [['Convites enviados', +f.convites_enviados || 0], ['Convites usados', +f.convites_usados || 0], ['Cadastros', +f.cadastros || 0], ['Ativados em 24h', +f.ativados_24h || 0], ['Pagaram', +f.pagamentos || 0]], 'var(--green)');
    var o = f.origens || [];
    $('pfOrig').innerHTML = o.length ? o.map(function (x) { return '<li><span>' + esc(x.fonte) + '</span><span>' + nf(x.pessoas) + '</span></li>'; }).join('') + ((f.beta_por_origem || []).length ? '<li><span><b>Pedidos Beta por origem</b></span><span>' + f.beta_por_origem.map(function (x) { return esc(x.fonte) + ' ' + nf(x.n); }).join(' · ') + '</span></li>' : '') : '<li><span>Sem visitas no período.</span><span></span></li>';
    var NOME = { gastos: 'Gastos', lembretes: 'Lembretes', audio: 'Áudio', compromissos: 'Compromissos', tarefas: 'Tarefas', contas: 'Contas', foto: 'Foto', assinaturas: 'Assinaturas' };
    var fu = Object.keys(f.funcoes || {}).map(function (k2) { return [NOME[k2] || k2, +f.funcoes[k2] || 0]; }).sort(function (a, b) { return b[1] - a[1]; });
    if (fu.length) { var mx = Math.max.apply(null, fu.map(function (x) { return x[1]; })); $('pfFunc').innerHTML = fu.map(function (x) { return '<div class="pf-row" style="--c:var(--violet)"><span>' + esc(x[0]) + '</span><div class="tr"><i style="width:' + (100 * x[1] / mx).toFixed(1) + '%"></i></div><b>' + nf(x[1]) + '</b></div>'; }).join(''); }
    else $('pfFunc').innerHTML = '<p class="pf-vazio">Sem uso registrado.</p>';
    var co = (f.coortes || []).slice().reverse();
    $('pfCoor').innerHTML = co.length ? '<table><thead><tr><th>Semana</th><th>Contas</th><th>Ativadas 24h</th><th>Hábito D7</th><th>Ativas 7d</th><th>Pagaram</th></tr></thead><tbody>' + co.map(function (c) {
      return '<tr><td class="mono">' + esc(d(c.semana)) + '</td><td class="mono">' + nf(c.contas) + '</td><td class="mono">' + nf(c.ativadas_24h) + ' <span style="color:var(--dim)">' + pc(c.ativadas_24h, c.contas) + '</span></td><td class="mono">' + (c.maduras_d7 ? nf(c.habito_d7) + ' de ' + nf(c.maduras_d7) : '<span style="color:var(--dim)">ainda sem 7 dias</span>') + '</td><td class="mono">' + nf(c.ativas_7d) + '</td><td class="mono">' + nf(c.pagaram) + '</td></tr>';
    }).join('') + '</tbody></table>' : '<p class="pf-vazio">Sem cadastros ainda.</p>';
  }

  /* ---------- pedidos ---------- */
  function pedidos() {
    api({ acao: 'admin_pedidos' }).then(function (r) {
      if (!r || !r.ok) { $('pdList').innerHTML = '<p class="pf-vazio">Não consegui carregar os pedidos' + (r && r._status ? ' (' + r._status + ')' : '') + '.</p>'; return; }
      ST.ped = r; renderPed();
    });
  }
  var ABERTO = ['novo', 'avaliando'];
  function renderPed() {
    if (!ST.ped) return;
    var ps = ST.ped.por_status || {}, L = ST.ped.pedidos || [];
    $('pdNa').textContent = (ps.novo || 0) + (ps.avaliando || 0); $('pdNp').textContent = ps.aprovado || 0; $('pdNf').textContent = ps.feito || 0; $('pdNd').textContent = ps.descartado || 0;
    var f = ST.filtro, V = L.filter(function (p) { return f === 'todos' || (f === 'aberto' ? ABERTO.indexOf(p.status) >= 0 : p.status === f); });
    if (!V.length) { $('pdList').innerHTML = '<p class="pf-vazio">Nenhum pedido aqui.</p>'; return; }
    var ROT = { novo: 'novo', avaliando: 'aguardando você', aprovado: 'aprovado · na fila', feito: 'feito', descartado: 'arquivado' };
    var VER = { vale: 'IA: vale fazer', sim: 'IA: vale fazer', talvez: 'IA: talvez', nao_agora: 'IA: não agora', nao: 'IA: não fazer' };
    $('pdList').innerHTML = V.map(function (p) {
      var a = p.avaliacao || {}, v = String(a.veredito || '');
      var av = (a.motivo || a.como) ? '<div class="pd-av"><div class="tags">' + (v ? '<span class="' + (/^(vale|sim)/.test(v) ? 'v-sim' : /^nao/.test(v) ? 'v-nao' : '') + '">' + esc(VER[v] || v) + '</span>' : '') + (a.esforco ? '<span>esforço ' + esc(a.esforco) + '</span>' : '') + (a.custo ? '<span>' + esc(a.custo) + '</span>' : '') + (p.categoria ? '<span>' + esc(p.categoria) + '</span>' : '') + '</div>' +
        (a.motivo ? '<div><b>Por quê:</b> ' + esc(a.motivo) + '</div>' : '') + (a.como ? '<div><b>Como:</b> ' + esc(a.como) + '</div>' : '') + '</div>' : '';
      var bt = '';
      if (p.status === 'novo' || p.status === 'avaliando') bt = '<button class="btn sm pri" data-op="sim" data-id="' + p.id + '">Aprovar</button><button class="btn sm" data-op="nao" data-id="' + p.id + '">Arquivar</button>';
      else if (p.status === 'aprovado') bt = '<button class="btn sm pri" data-op="feito" data-id="' + p.id + '">Marcar como feito</button><button class="btn sm" data-op="nao" data-id="' + p.id + '">Arquivar</button><small>"Feito" avisa o cliente no WhatsApp.</small>';
      else if (p.status === 'feito') bt = '<small>' + (p.cliente_avisado_em ? 'Cliente avisado em ' + esc(dataBR(p.cliente_avisado_em)) : 'Aviso ao cliente na fila') + '</small>';
      else if (p.status === 'descartado') bt = '<button class="btn sm" data-op="sim" data-id="' + p.id + '">Reabrir e aprovar</button>';
      return '<article class="pd"><div class="pd-h"><span>#' + p.id + '</span><span class="st ' + esc(p.status) + '">' + esc(ROT[p.status] || p.status) + '</span><span>' + esc(p.autor) + (p.grupo ? ' · grupo' : '') + '</span><span>' + esc(dataBR(p.criado_em)) + '</span></div>' +
        '<div class="pd-t">' + esc(p.pedido) + '</div>' + (p.texto_usuario ? '<p class="pd-q">“' + esc(p.texto_usuario) + '”</p>' : '') + av + (bt ? '<div class="pd-a">' + bt + '</div>' : '') + '</article>';
    }).join('');
  }
  function acao(e) {
    var b = e.target.closest('button[data-op]'); if (!b) return;
    var op = b.dataset.op, id = b.dataset.id;
    if (op === 'feito' && ST.armado !== b) {
      if (ST.armado) { ST.armado.classList.remove('armed'); ST.armado.classList.add('pri'); ST.armado.textContent = 'Marcar como feito'; }
      ST.armado = b; b.classList.remove('pri'); b.classList.add('armed'); b.textContent = 'Confirmar: avisar o cliente';
      setTimeout(function () { if (ST.armado === b) { b.classList.remove('armed'); b.classList.add('pri'); b.textContent = 'Marcar como feito'; ST.armado = null; } }, 6000);
      return;
    }
    ST.armado = null;
    [].forEach.call(document.querySelectorAll('#pdList button[data-id="' + id + '"]'), function (x) { x.disabled = true; });
    api({ acao: 'admin_pedido', id: id, op: op }).then(function (r) {
      if (!r || !r.ok) { toast('Não deu certo' + (r && r._status ? ' (' + r._status + ')' : '') + '.', true); renderPed(); return; }
      ST.ped = r; renderPed();
      toast(op === 'sim' ? 'Pedido #' + id + ' aprovado.' : op === 'feito' ? 'Pedido #' + id + ' feito. O cliente recebe o aviso em até 5 minutos.' : 'Pedido #' + id + ' arquivado.');
    });
  }

  function carregar() { funil(); pedidos(); }
  function abrir() { montar(); ST.ativo = true; carregar(); clearInterval(ST.timer); ST.timer = setInterval(function () { if (ST.ativo && !document.hidden) carregar(); }, 120000); }
  function pausar() { ST.ativo = false; clearInterval(ST.timer); }
  window.DynoPedidos = { abrir: abrir, pausar: pausar };
})();
