/* Dyno · Central (visão de TV, estilo NOC) — 09/10/2026 */
(function () {
  'use strict';
  var A = window.DynoAdmin; if (!A) return;
  var api = A.api, esc = A.esc;
  var $ = function (id) { return document.getElementById(id); };
  var ST = { d: null, timer: null, ativo: false, tv: false, rot: true, bloco: 0, rotTimer: null };
  var C = { hoje: '#14a876', ontem: '#6f84a8', erro: '#ff6f91', texto: '#14a876', audio: '#2196cf', foto: '#7f5ee6', novos: '#2196cf', beta: '#7f5ee6' };
  var nf = function (v, d) { return (Number(v) || 0).toLocaleString('pt-BR', { minimumFractionDigits: d || 0, maximumFractionDigits: d || 0 }); };
  var brl = function (v) { return 'R$ ' + nf(v, 2); };
  var usd = function (v) { v = Number(v) || 0; return 'US$ ' + nf(v, v < 10 ? 2 : 0); };
  var mseg = function (v) { return v == null ? '—' : (v >= 1000 ? nf(v / 1000, 1) + ' s' : nf(v) + ' ms'); };
  var pct = function (a, b) { if (!b) return a ? '+100%' : '—'; var p = Math.round((a / b - 1) * 100); return (p >= 0 ? '+' : '') + p + '%'; };

  var css = [
    '#tCentral{--tile1:#00a98f;--tile2:#0c8f55}',
    '.ct-top{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;margin:6px 0 14px}',
    '.ct-top h1{margin:0;font:600 13px var(--mono);letter-spacing:2px;color:var(--mut);text-transform:uppercase}',
    '.ct-clock{font:600 30px/1 var(--mono);font-variant-numeric:tabular-nums;color:var(--fg)}',
    '.ct-clock small{display:block;font:500 11px var(--mono);color:var(--dim);letter-spacing:1px;margin-top:4px}',
    '.ct-ctr{display:flex;gap:8px;align-items:center;flex-wrap:wrap}',
    '.ct-ctr button{border:1px solid var(--line2);background:none;color:var(--mut);border-radius:10px;padding:7px 12px;cursor:pointer}',
    '.ct-ctr button[aria-pressed=true]{color:var(--fg);border-color:rgba(47,227,160,.5);background:rgba(47,227,160,.08)}',
    '.ct-blk{background:var(--panel);border:1px solid var(--line);border-radius:18px;padding:16px 18px 18px;margin-bottom:16px}',
    '.ct-tt{display:flex;align-items:center;justify-content:center;gap:12px;margin:0 0 14px;text-align:center}',
    '.ct-tt h2{margin:0;font:700 clamp(18px,2.2vw,28px)/1.15 var(--sans);letter-spacing:.5px;color:#2fe3a0;text-transform:uppercase;text-wrap:balance}',
    '.ct-tt svg{flex:none}',
    '.ct-kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(168px,1fr));gap:10px;margin-bottom:14px}',
    '.ct-ref{display:grid;grid-template-rows:auto 1fr;gap:8px}',
    '.ct-h{background:rgba(255,255,255,.04);border:1px solid var(--line);border-radius:10px;padding:9px 10px;text-align:center;font:600 11px var(--mono);letter-spacing:1px;text-transform:uppercase;color:var(--mut);display:flex;align-items:center;justify-content:center;min-height:40px}',
    '.ct-ref .r{display:flex;align-items:center;justify-content:center;text-align:center;border:1px solid var(--line);border-radius:10px;font:700 clamp(16px,1.9vw,26px)/1.1 var(--sans);color:#2fe3a0;padding:8px}',
    '.ct-k{display:grid;grid-template-rows:auto 1fr;gap:8px;min-width:0}',
    '.ct-v{border-radius:10px;background:linear-gradient(90deg,var(--tile1),var(--tile2));color:#fff;text-align:center;padding:12px 8px 10px;display:flex;flex-direction:column;justify-content:center;min-height:68px}',
    '.ct-v b{font:600 clamp(20px,2.1vw,34px)/1.05 var(--mono);font-variant-numeric:tabular-nums;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}',
    '.ct-v small{font:500 11px/1.3 var(--mono);opacity:.88;margin-top:5px}',
    '.ct-v.warn{background:linear-gradient(90deg,#b98a16,#9a6b00)}.ct-v.crit{background:linear-gradient(90deg,#c43b5c,#9b1f3e)}',
    '.ct-g2{display:grid;grid-template-columns:1fr 1fr;gap:16px}',
    '.ct-ch{min-width:0}.ct-ch h3{margin:0 0 6px;font:600 11px var(--mono);letter-spacing:1px;color:var(--mut);text-transform:uppercase}',
    '.ct-svg{position:relative}.ct-svg svg{display:block;width:100%;overflow:visible}',
    '.ct-tip{position:absolute;pointer-events:none;background:#0b1426;border:1px solid var(--line2);border-radius:8px;padding:6px 9px;font:500 11.5px var(--mono);white-space:nowrap;z-index:3;box-shadow:0 6px 20px rgba(0,0,0,.4)}',
    '.ct-leg{width:100%;min-width:0;border-collapse:collapse;font:500 11px var(--mono);margin-top:4px}',
    '.ct-leg th{color:#46d2ff;font-weight:500;text-align:right;padding:2px 6px}.ct-leg th:first-child{text-align:left}',
    '.ct-leg td{border-top:1px solid var(--line);padding:3px 6px;text-align:right;color:var(--fg);font-variant-numeric:tabular-nums}.ct-leg td:first-child{text-align:left;color:var(--mut)}',
    '.ct-sw{display:inline-block;width:14px;height:3px;border-radius:2px;vertical-align:middle;margin-right:7px}',
    '.ct-tab{width:100%;min-width:760px;border-collapse:separate;border-spacing:8px;table-layout:fixed}',
    '.ct-tab td,.ct-tab th{padding:0}',
    '.ct-tab .c{border:1px solid var(--line);border-radius:10px;text-align:center;padding:10px 6px;font:600 clamp(16px,1.7vw,26px)/1.1 var(--mono);color:#2fe3a0;font-variant-numeric:tabular-nums;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}',
    '.ct-tab .c small{display:block;font:500 11px var(--mono);color:var(--dim);margin-top:3px}',
    '.ct-ov{overflow-x:auto}',
    '.ct-canais{display:grid;gap:8px}',
    '.ct-big{display:flex;align-items:center;justify-content:space-between;gap:10px;border-radius:10px;background:linear-gradient(90deg,var(--tile1),var(--tile2));color:#fff;padding:12px 16px}',
    '.ct-big span{font:600 15px var(--sans);text-transform:uppercase;letter-spacing:.5px}.ct-big b{font:600 22px var(--mono);font-variant-numeric:tabular-nums}',
    '.ct-big.hero{padding:18px 16px}.ct-big.hero b{font-size:clamp(34px,4vw,56px)}',
    '.ct-map{display:grid;grid-template-columns:repeat(7,1fr);gap:5px;max-width:420px;margin:0 auto}',
    '.ct-uf{aspect-ratio:1;border-radius:8px;display:flex;flex-direction:column;align-items:center;justify-content:center;font:600 11px var(--mono);color:var(--fg);border:1px solid var(--line)}',
    '.ct-uf b{font-size:13px}.ct-uf i{font-style:normal;font-size:10px;opacity:.85}',
    '.ct-bars .row{display:grid;grid-template-columns:110px 1fr 56px;gap:8px;align-items:center;font:500 12px var(--mono);margin:6px 0}',
    '.ct-bars .tr{position:relative;height:14px;border-radius:4px;background:rgba(255,255,255,.04)}',
    '.ct-bars .b1{position:absolute;left:0;top:0;bottom:0;border-radius:0 4px 4px 0;background:' + C.hoje + '}',
    '.ct-bars .b0{position:absolute;top:-3px;bottom:-3px;width:2px;background:' + C.ontem + '}',
    '.ct-bars .row span:last-child{text-align:right;font-variant-numeric:tabular-nums}',
    '.ct-note{font-size:12px;color:var(--dim);margin-top:8px}',
    '.ct-prog{height:3px;background:rgba(255,255,255,.06);border-radius:2px;overflow:hidden;margin-bottom:10px}.ct-prog i{display:block;height:100%;width:0;background:#2fe3a0}',
    '#tCentral.tv{position:fixed;inset:0;z-index:50;background:var(--bg);overflow:auto;padding:18px 24px;max-width:none}',
    '#tCentral.tv.rot .ct-blk{display:none}#tCentral.tv.rot .ct-blk.on{display:block}',
    '@media (max-width:900px){.ct-g2{grid-template-columns:1fr}.ct-kpis{grid-template-columns:repeat(2,minmax(0,1fr))}.ct-kpis>.ct-ref{grid-column:1/-1}.ct-kpis>.ct-ref .r{min-height:48px}}'
  ].join('\n');
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

  var LOGO = '<svg width="34" height="34" viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="16" fill="#0b1a33"/><circle cx="32" cy="32" r="22" fill="#2fe3a0"/><text x="32" y="42.5" text-anchor="middle" font-family="Georgia,serif" font-size="30" font-weight="700" fill="#0b1a33">D</text></svg>';

  /* ---------- gráficos (SVG) ---------- */
  var GR = {};
  function area(id, o) {
    // o: {pts: n por dia, series:[{n,c,d,area,dash}], rotulos: fn(i)->texto, unid}
    GR[id] = o;
    var el = $(id); if (!el) return;
    var W = Math.max(300, el.clientWidth || 600), H = o.h || 170, L = 38, R = 8, T = 10, B = 22;
    var max = 0; o.series.forEach(function (s) { s.d.forEach(function (v) { if (v != null && v > max) max = v; }); });
    max = nice(max || 1);
    var x = function (i) { return L + (W - L - R) * i / (o.pts - 1); }, y = function (v) { return T + (H - T - B) * (1 - v / max); };
    var g = '<svg viewBox="0 0 ' + W + ' ' + H + '" height="' + H + '" role="img" aria-label="' + esc(o.titulo || '') + '"><defs>';
    o.series.forEach(function (s, k) { if (s.area) g += '<linearGradient id="' + id + 'g' + k + '" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="' + s.c + '" stop-opacity=".55"/><stop offset="1" stop-color="' + s.c + '" stop-opacity=".02"/></linearGradient>'; });
    g += '</defs>';
    for (var t = 0; t <= 4; t++) { var v = max * t / 4, yy = y(v); g += '<line x1="' + L + '" x2="' + (W - R) + '" y1="' + yy + '" y2="' + yy + '" stroke="rgba(120,170,255,.10)"/><text x="' + (L - 6) + '" y="' + (yy + 3.5) + '" text-anchor="end" font-size="10" fill="#8ea3c4" font-family="var(--mono)">' + fmtEixo(v) + '</text>'; }
    var passo = (o.passoRot || Math.ceil(o.pts / 12)) * (W < 520 ? 2 : 1);
    for (var i = 0; i < o.pts; i += passo) g += '<text x="' + x(i) + '" y="' + (H - 6) + '" text-anchor="middle" font-size="10" fill="#8ea3c4" font-family="var(--mono)">' + o.rotulos(i) + '</text>';
    o.series.forEach(function (s, k) {
      var pts = []; s.d.forEach(function (v, i) { if (v != null) pts.push([x(i), y(v)]); });
      if (!pts.length) return;
      var dl = pts.map(function (p, j) { return (j ? 'L' : 'M') + p[0].toFixed(1) + ',' + p[1].toFixed(1); }).join('');
      if (s.area) g += '<path d="' + dl + 'L' + pts[pts.length - 1][0].toFixed(1) + ',' + y(0) + 'L' + pts[0][0].toFixed(1) + ',' + y(0) + 'Z" fill="url(#' + id + 'g' + k + ')"/>';
      g += '<path d="' + dl + '" fill="none" stroke="' + s.c + '" stroke-width="2" stroke-linejoin="round"' + (s.dash ? ' stroke-dasharray="5 4"' : '') + '/>';
    });
    g += '<line id="' + id + 'x" x1="0" x2="0" y1="' + T + '" y2="' + (H - B) + '" stroke="#8ea3c4" stroke-dasharray="3 3" visibility="hidden"/></svg>';
    var leg = '<table class="ct-leg"><tr><th>Série</th><th>Média</th><th>Última</th><th>Máx.</th></tr>' + o.series.map(function (s) {
      var vs = s.d.filter(function (v) { return v != null; }), soma = vs.reduce(function (a, b) { return a + b; }, 0);
      var ult = s.ultimo != null ? s.ultimo : (vs.length ? vs[vs.length - 1] : 0);
      return '<tr><td><span class="ct-sw" style="background:' + s.c + (s.dash ? ';background:repeating-linear-gradient(90deg,' + s.c + ' 0 5px,transparent 5px 8px)' : '') + '"></span>' + esc(s.n) + '</td><td>' + fmtV(vs.length ? soma / vs.length : 0, o.unid, 1) + '</td><td>' + fmtV(ult, o.unid) + '</td><td>' + fmtV(vs.length ? Math.max.apply(null, vs) : 0, o.unid) + '</td></tr>';
    }).join('') + '</table>';
    el.innerHTML = '<div class="ct-svg">' + g + '<div class="ct-tip" hidden></div></div>' + leg;
    var box = el.querySelector('.ct-svg'), sv = box.querySelector('svg'), tip = box.querySelector('.ct-tip'), ln = $(id + 'x');
    sv.addEventListener('mousemove', function (e) {
      var r = sv.getBoundingClientRect(), px = (e.clientX - r.left) * W / r.width;
      var i = Math.round((px - L) / (W - L - R) * (o.pts - 1)); if (i < 0 || i >= o.pts) { tip.hidden = true; return; }
      ln.setAttribute('x1', x(i)); ln.setAttribute('x2', x(i)); ln.setAttribute('visibility', 'visible');
      tip.innerHTML = '<b>' + o.rotulos(i, true) + '</b><br>' + o.series.map(function (s) { return '<span class="ct-sw" style="background:' + s.c + '"></span>' + esc(s.n) + ': ' + (s.d[i] == null ? '—' : fmtV(s.d[i], o.unid)); }).join('<br>');
      tip.hidden = false; var lx = x(i) * r.width / W; tip.style.left = Math.min(lx + 12, r.width - tip.offsetWidth - 4) + 'px'; tip.style.top = '6px';
    });
    sv.addEventListener('mouseleave', function () { tip.hidden = true; ln.setAttribute('visibility', 'hidden'); });
  }
  function nice(v) { var p = Math.pow(10, Math.floor(Math.log10(v))), m = v / p; return (m <= 1 ? 1 : m <= 2 ? 2 : m <= 2.5 ? 2.5 : m <= 5 ? 5 : 10) * p; }
  function fmtEixo(v) { return v >= 1000 ? nf(v / 1000, v >= 10000 ? 0 : 1) + 'k' : (v % 1 ? nf(v, v < 1 ? 2 : 1) : nf(v)); }
  function fmtV(v, u, d) { if (u === 'usd') return 'US$ ' + nf(v, 3); if (u === 'ms') return mseg(v); return nf(v, d && v % 1 ? 1 : 0); }
  var hm = function (min) { return ('0' + Math.floor(min / 60)).slice(-2) + ':' + ('0' + (min % 60)).slice(-2); };
  function corta(arr, ate) { return arr.map(function (v, i) { return i <= ate ? v : null; }); }

  /* ---------- montagem ---------- */
  function tiles(ref, ks) {
    return '<div class="ct-kpis"><div class="ct-ref"><div class="ct-h">Referência</div><div class="r">' + ref + '</div></div>' + ks.map(function (k) {
      return '<div class="ct-k"><div class="ct-h">' + esc(k[0]) + '</div><div class="ct-v ' + (k[3] || '') + '"><b>' + k[1] + '</b>' + (k[2] ? '<small>' + k[2] + '</small>' : '') + '</div></div>';
    }).join('') + '</div>';
  }
  function bloco(titulo, corpo, i) { return '<section class="ct-blk' + (i === ST.bloco ? ' on' : '') + '" data-b="' + i + '"><div class="ct-tt">' + LOGO + '<h2>' + titulo + '</h2></div>' + corpo + '</section>'; }

  function render() {
    var d = ST.d, el = $('tCentral'); if (!d || !el) return;
    var op = d.op || {}, cr = d.cres || {}, uso = d.uso || {}, ia = d.ia || {}, sv = op.serie || {};
    var b10 = Math.floor((d.minuto || 0) / 10), b30 = Math.floor((d.minuto || 0) / 30), h1 = Math.floor((d.minuto || 0) / 60);
    var agora = new Date(d.agora || Date.now());
    var cab = '<div class="ct-top"><div><h1>Dyno · Central</h1><div class="ct-note" id="ctAtu">Atualizado ' + agora.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' }) + ' · atualiza a cada minuto</div></div>' +
      '<div class="ct-clock" id="ctClock"></div><div class="ct-ctr"><button id="ctRot" aria-pressed="' + ST.rot + '" title="No modo TV, troca de bloco a cada 20 s">Rotação</button><button id="ctTv" aria-pressed="' + ST.tv + '">' + (ST.tv ? 'Sair da TV' : 'Modo TV') + '</button></div></div>' +
      (ST.tv && ST.rot ? '<div class="ct-prog"><i id="ctProg"></i></div>' : '');
    var vs = op.msgs_ontem_ate_agora;
    var b1 = tiles('Resumo<br>do dia', [
      ['Mensagens recebidas', nf(op.msgs_hoje), pct(op.msgs_hoje, vs) + ' vs ontem até agora'],
      ['Clientes que falaram', nf(op.clientes_hoje), 'ontem: ' + nf(op.clientes_ontem)],
      ['Lançamentos', nf(op.lanc_hoje), brl(op.gastos_valor_hoje) + ' em gastos'],
      ['Lembretes enviados', nf(op.lembretes_hoje), nf(op.respostas_hoje) + ' respostas do Dyno'],
      ['Erros nos fluxos', nf(op.erros_hoje), 'execuções com falha hoje', op.erros_hoje >= 5 ? 'crit' : op.erros_hoje ? 'warn' : '']
    ]) + '<div class="ct-g2"><div class="ct-ch"><h3>Mensagens recebidas · a cada 10 min</h3><div id="ctA1"></div></div><div class="ct-ch"><h3>Ações registradas (gastos, lembretes, tarefas, agenda) · a cada 10 min</h3><div id="ctA2"></div></div></div>';
    var v = cr.vagas || {};
    var b2 = '<div class="ct-ov"><table class="ct-tab"><colgroup><col style="width:18%"><col><col><col><col><col><col></colgroup><tr><th></th>' +
      ['Cadastros', 'Pedidos do Beta', 'Convites usados', 'Em teste', 'Pagantes', 'Receita mensal (MRR)'].map(function (t) { return '<th><div class="ct-h">' + t + '</div></th>'; }).join('') + '</tr>' +
      '<tr><td><div class="ct-ref"><div class="r" style="min-height:64px">Resumo do dia</div></div></td>' + [nf(cr.cad_dia) + '<small>ontem: ' + nf(cr.cad_ontem) + '</small>', nf(cr.beta_dia), nf(cr.conv_dia), nf(cr.em_teste) + '<small>' + nf(cr.fim_teste_30d) + ' terminam em 30 dias</small>', nf(cr.pagantes), brl(cr.mrr)].map(function (x) { return '<td><div class="c">' + x + '</div></td>'; }).join('') + '</tr>' +
      '<tr><td><div class="ct-ref"><div class="r" style="min-height:64px">Acumulado mês</div></div></td>' + [nf(cr.cad_mes), nf(cr.beta_mes), nf(cr.conv_mes) + '<small>' + nf(cr.conv_abertos) + ' em aberto</small>', nf(v.restantes) + '<small>vagas de ' + nf(v.total) + '</small>', brl(cr.receita_mes) + '<small>recebido no mês</small>', brl(cr.mrr_potencial) + '<small>se todos assinarem</small>'].map(function (x) { return '<td><div class="c">' + x + '</div></td>'; }).join('') + '</tr></table></div>' +
      '<div class="ct-ch" style="margin-top:10px"><h3>Evolução de clientes · últimos 30 dias</h3><div id="ctB1"></div></div>';
    var cn = uso.canal || {}, totMsg = (cn.texto || 0) + (cn.audio || 0) + (cn.foto || 0);
    var b3 = '<div class="ct-g2"><div class="ct-ch"><h3>Mensagens por canal · a cada 30 min</h3><div id="ctC1"></div>' + mapa(uso.uf || {}, uso.clientes_total) + '</div><div class="ct-canais">' +
      '<div class="ct-big hero"><span>Total de mensagens</span><b>' + nf(totMsg) + '</b></div>' +
      [['WhatsApp · texto', cn.texto], ['WhatsApp · áudio', cn.audio], ['WhatsApp · foto e PDF', cn.foto], ['Grupos (modo família)', cn.grupos], ['Chat do site', cn.site_chat], ['Área do cliente (acessos)', cn.area_cliente], ['Dyno Business', cn.business]].map(function (x) { return '<div class="ct-big"><span>' + x[0] + '</span><b>' + nf(x[1]) + '</b></div>'; }).join('') +
      '<div class="ct-ch ct-bars"><h3 style="margin-top:6px">Funções usadas hoje <span style="color:var(--dim)">(traço = ontem)</span></h3>' + barras(uso.funcoes || {}) + '</div></div></div>';
    var pv = ia.previsao || {}, pp = Number(pv.pct) || 0;
    var b4 = tiles('IA, custo<br>e saúde', [
      ['Chamadas de IA', nf(ia.chamadas_hoje), nf(ia.exec_hoje) + ' execuções nos fluxos'],
      ['Custo hoje', usd(ia.custo_hoje), 'ontem: ' + usd(ia.custo_ontem)],
      ['Custo no mês', usd(ia.custo_mes), 'previsão ' + usd(pv.previsao) + ' (' + nf(pp, 0) + '% do limite)', pp >= 100 ? 'crit' : pp >= 80 ? 'warn' : ''],
      ['Resposta do Dyno', mseg(ia.resp_p50), 'mediana · IA ' + mseg(ia.lat_p50) + ' (p95 ' + mseg(ia.lat_p95) + ')', ia.resp_p50 > 15000 ? 'warn' : ''],
      ['Disponibilidade', (ia.uptime_24h == null ? '—' : nf(ia.uptime_24h, 2) + '%'), 'site e serviços · 24 h', ia.uptime_24h != null && ia.uptime_24h < 99 ? 'warn' : ''],
      ['Erros hoje', nf(ia.exec_erros), 'de ' + nf(ia.exec_hoje) + ' execuções', ia.exec_erros >= 5 ? 'crit' : ia.exec_erros ? 'warn' : '']
    ]) + '<div class="ct-g2"><div class="ct-ch"><h3>Custo de IA por hora · hoje x ontem (US$)</h3><div id="ctD1"></div></div><div class="ct-ch"><h3>Tempo da IA no cérebro por hora (mediana)</h3><div id="ctD2"></div></div></div>';
    el.innerHTML = cab + bloco('Dyno · Operação do dia', b1, 0) + bloco('Dyno · Crescimento e receita', b2, 1) + bloco('Dyno · Uso por canal e função', b3, 2) + bloco('Dyno · IA, custo e saúde', b4, 3);
    el.classList.toggle('tv', ST.tv); el.classList.toggle('rot', ST.tv && ST.rot);
    var r10 = function (i, l) { var m = i * 10; return l ? hm(m) + '–' + hm(m + 10) : hm(m); };
    area('ctA1', { titulo: 'Mensagens a cada 10 min', pts: 144, passoRot: 12, rotulos: r10, series: [
      { n: 'Hoje', c: C.hoje, area: true, d: corta(sv.msgs || [], b10) },
      { n: 'Ontem', c: C.ontem, dash: true, d: sv.msgs_ontem || [] },
      { n: 'Erros nos fluxos', c: C.erro, d: corta(sv.erros || [], b10) }] });
    area('ctA2', { titulo: 'Ações registradas', pts: 144, passoRot: 12, rotulos: r10, series: [
      { n: 'Hoje', c: C.hoje, area: true, d: corta(sv.acoes || [], b10) },
      { n: 'Ontem', c: C.ontem, dash: true, d: sv.acoes_ontem || [] }] });
    var s30 = (cr.serie || []);
    area('ctB1', { titulo: 'Clientes 30 dias', pts: Math.max(2, s30.length), passoRot: 3, h: 190, rotulos: function (i) { return (s30[i] || {}).d || ''; }, series: [
      { n: 'Contas no total', c: C.hoje, area: true, d: s30.map(function (x) { return x.total; }) },
      { n: 'Cadastros no dia', c: C.novos, d: s30.map(function (x) { return x.novos; }) },
      { n: 'Pedidos do Beta', c: C.beta, d: s30.map(function (x) { return x.beta; }) }] });
    var us = uso.serie || {}, r30 = function (i, l) { var m = i * 30; return l ? hm(m) + '–' + hm(m + 30) : hm(m); };
    area('ctC1', { titulo: 'Mensagens por canal', pts: 48, passoRot: 4, rotulos: r30, series: [
      { n: 'Texto', c: C.texto, area: true, d: corta(us.texto || [], b30) },
      { n: 'Áudio', c: C.audio, d: corta(us.audio || [], b30) },
      { n: 'Foto e PDF', c: C.foto, d: corta(us.foto || [], b30) }] });
    var is = ia.serie || {}, rh = function (i, l) { return l ? hm(i * 60) + '–' + hm(i * 60 + 60) : hm(i * 60); };
    area('ctD1', { titulo: 'Custo por hora', pts: 24, passoRot: 2, unid: 'usd', rotulos: rh, series: [
      { n: 'Hoje', c: C.hoje, area: true, d: corta((is.custo || []).map(Number), h1) },
      { n: 'Ontem', c: C.ontem, dash: true, d: (is.custo_ontem || []).map(Number) }] });
    area('ctD2', { titulo: 'Tempo da IA', pts: 24, passoRot: 2, unid: 'ms', rotulos: rh, series: [
      { n: 'Mediana do cérebro', c: C.audio, area: true, d: corta(is.lat || [], h1) }] });
    $('ctTv').onclick = alternarTv; $('ctRot').onclick = function () { ST.rot = !ST.rot; render(); rotacao(); };
    relogio();
  }
  function mapa(uf, tot) {
    var G = [['RR', 2, 0], ['AP', 3, 0], ['AM', 1, 1], ['PA', 2, 1], ['MA', 3, 1], ['CE', 4, 1], ['RN', 5, 1], ['AC', 0, 2], ['RO', 1, 2], ['MT', 2, 2], ['TO', 3, 2], ['PI', 4, 2], ['PE', 5, 2], ['PB', 6, 2],
      ['MS', 2, 3], ['GO', 3, 3], ['DF', 4, 3], ['BA', 5, 3], ['AL', 6, 3], ['PR', 2, 4], ['SP', 3, 4], ['MG', 4, 4], ['ES', 5, 4], ['SE', 6, 4], ['SC', 2, 5], ['RJ', 4, 5], ['RS', 2, 6]];
    var max = 1; Object.keys(uf).forEach(function (k) { max = Math.max(max, uf[k]); });
    var cel = {}; G.forEach(function (g) { cel[g[1] + ',' + g[2]] = g[0]; });
    var h = '';
    for (var r = 0; r < 7; r++) for (var c = 0; c < 7; c++) {
      var s = cel[c + ',' + r];
      if (!s) { h += '<div></div>'; continue; }
      var n = uf[s] || 0, a = n ? 0.25 + 0.75 * n / max : 0;
      h += '<div class="ct-uf" title="' + s + ': ' + n + (n === 1 ? ' cliente' : ' clientes') + '" style="background:' + (n ? 'rgba(20,168,118,' + a.toFixed(2) + ')' : 'rgba(255,255,255,.03)') + '"><b>' + s + '</b>' + (n ? '<i>' + n + '</i>' : '') + '</div>';
    }
    return '<h3 style="margin:14px 0 6px;font:600 11px var(--mono);letter-spacing:1px;color:var(--mut)">CLIENTES POR ESTADO (DDD) · ' + nf(tot) + ' NO TOTAL</h3><div class="ct-map">' + h + '</div>';
  }
  function barras(f) {
    var N = { gastos: 'Gastos', receitas: 'Receitas', lembretes: 'Lembretes', tarefas: 'Tarefas', agenda: 'Agenda', contas: 'Contas a pagar', comprovantes: 'Comprovantes', rastreios: 'Rastreios', contatos: 'Envios a contatos', documentos: 'Documentos', promessas: 'Promessas cobradas', pedidos: 'Pedidos de função', oficial: 'Msgs no nº oficial (Meta)' };
    var max = 1; Object.keys(N).forEach(function (k) { var x = f[k] || [0, 0]; max = Math.max(max, x[0], x[1]); });
    return Object.keys(N).map(function (k) { var x = f[k] || [0, 0];
      return '<div class="row"><span>' + N[k] + '</span><div class="tr"><div class="b1" style="width:' + (100 * x[0] / max).toFixed(1) + '%"></div><div class="b0" style="left:' + (100 * x[1] / max).toFixed(1) + '%" title="ontem: ' + x[1] + '"></div></div><span>' + nf(x[0]) + '</span></div>'; }).join('');
  }
  function relogio() { var el = $('ctClock'); if (!el) return; var n = new Date(); el.innerHTML = n.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' }) + '<small>' + n.toLocaleDateString('pt-BR', { weekday: 'long', day: '2-digit', month: '2-digit' }) + '</small>'; }
  setInterval(function () { if (ST.ativo) relogio(); }, 15000);

  function alternarTv() {
    ST.tv = !ST.tv; var el = $('tCentral');
    try { if (ST.tv && el.requestFullscreen && !document.fullscreenElement) el.requestFullscreen().catch(function () {}); else if (!ST.tv && document.fullscreenElement) document.exitFullscreen(); } catch (e) {}
    render(); rotacao();
  }
  document.addEventListener('fullscreenchange', function () { if (!document.fullscreenElement && ST.tv) { ST.tv = false; render(); rotacao(); } else if (ST.d) render(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && ST.tv) { ST.tv = false; render(); rotacao(); } });
  function rotacao() {
    clearInterval(ST.rotTimer); if (!(ST.tv && ST.rot)) return;
    var t0 = Date.now(), DUR = 20000;
    ST.rotTimer = setInterval(function () {
      var p = $('ctProg'), f = (Date.now() - t0) / DUR; if (p) p.style.width = Math.min(100, f * 100) + '%';
      if (f >= 1) { t0 = Date.now(); ST.bloco = (ST.bloco + 1) % 4; [].forEach.call(document.querySelectorAll('#tCentral .ct-blk'), function (b) { b.classList.toggle('on', Number(b.dataset.b) === ST.bloco); }); var nb = document.querySelector('#tCentral .ct-blk.on'); if (nb) { Object.keys(GR).forEach(function (k) { if (nb.querySelector('#' + k)) area(k, GR[k]); }); } }
    }, 250);
  }

  function carregar() {
    api({ acao: 'admin_central' }).then(function (r) {
      if (!r || !r.ok) { if (!ST.d) $('tCentral').innerHTML = '<p class="sub" style="padding:24px">Não consegui carregar a central agora' + (r && r._status ? ' (' + r._status + ')' : '') + '. Tento de novo em 1 minuto.</p>'; return; }
      ST.d = r; render();
    });
  }
  var rz; window.addEventListener('resize', function () { if (!ST.ativo || !ST.d) return; clearTimeout(rz); rz = setTimeout(function () { Object.keys(GR).forEach(function (k) { area(k, GR[k]); }); }, 200); });

  window.DynoCentral = {
    abrir: function () { ST.ativo = true; if (!ST.d) $('tCentral').innerHTML = '<p class="sub" style="padding:24px"><span class="pulse"></span>Carregando a central…</p>'; carregar(); clearInterval(ST.timer); ST.timer = setInterval(carregar, 60000); rotacao(); },
    pausar: function () { ST.ativo = false; clearInterval(ST.timer); clearInterval(ST.rotTimer); if (ST.tv) { ST.tv = false; if (document.fullscreenElement) try { document.exitFullscreen(); } catch (e) {} } }
  };
})();
