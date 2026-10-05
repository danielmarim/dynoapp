(function () {
  'use strict';
  var $ = function (id) { return document.getElementById(id); };
  var WA = 'https://wa.me/5511939497178';
  var conta = null;

  function api(corpo) {
    return fetch('/api', {
      method: 'POST', credentials: 'same-origin',
      headers: { 'Content-Type': 'application/json', 'X-Requested-With': 'dyno' },
      body: JSON.stringify(corpo)
    }).then(function (r) {
      return r.json().catch(function () { return {}; }).then(function (j) { j._status = r.status; return j; });
    }).catch(function () { return { ok: false, erro: 'indisponivel' }; });
  }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function brl(v) { return (Number(v) || 0).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' }); }
  function data(s) { if (!s) return '—'; var p = String(s).slice(0, 10).split('-'); return p.length === 3 ? p[2] + '/' + p[1] + '/' + p[0] : s; }
  function dataHora(s) {
    var d = new Date(s); if (isNaN(d)) return data(s);
    return d.toLocaleString('pt-BR', { day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit', timeZone: 'America/Sao_Paulo' });
  }
  function toast(t) { var el = $('toast'); el.textContent = t; el.style.display = 'block'; clearTimeout(toast._t); toast._t = setTimeout(function () { el.style.display = 'none'; }, 3500); }
  function esquecer() { try { localStorage.removeItem('dyno_nome'); } catch (e) { } }
  function sairPara401(r) { if (r._status === 401) { esquecer(); location.replace('/entrar'); return true; } return false; }
  function confirmar(titulo, texto, botao) {
    return new Promise(function (ok) {
      var d = $('dlg'); $('dlg-t').textContent = titulo; $('dlg-p').textContent = texto; $('dlg-s').textContent = botao || 'Confirmar';
      var fim = function (v) { d.close(); $('dlg-s').onclick = null; $('dlg-n').onclick = null; ok(v); };
      $('dlg-s').onclick = function () { fim(true); }; $('dlg-n').onclick = function () { fim(false); };
      d.showModal();
    });
  }

  // ---------- abas ----------
  var ABAS = ['painel', 'extrato', 'comp', 'conta'];
  function aba(qual) {
    ABAS.forEach(function (k) {
      $('t-' + k).setAttribute('aria-selected', String(k === qual));
      $('p-' + k).hidden = k !== qual;
    });
    try { sessionStorage.setItem('dyno_aba', qual); } catch (e) { }
    if (qual === 'extrato' || qual === 'comp') abrirMov(qual);
  }
  ABAS.forEach(function (k) { $('t-' + k).onclick = function () { aba(k); }; });

  $('sair').onclick = function () { esquecer(); api({ acao: 'sair' }).then(function () { location.replace('/'); }); };

  // ---------- painel ----------
  function hbar(itens) {
    if (!itens.length) return '<p class="empty">Nenhum gasto registrado neste mês ainda.</p>';
    var max = Math.max.apply(null, itens.map(function (c) { return c.valor; })) || 1;
    return '<div class="hbar">' + itens.map(function (c) {
      if (c.limite) {
        var pct = c.valor / c.limite * 100;
        var cls = pct > 100 ? 'estourou' : pct >= 80 ? 'perto' : 'ok';
        var dica = pct > 100 ? 'passou ' + brl(c.valor - c.limite) : 'restam ' + brl(c.limite - c.valor);
        return '<div class="r lim ' + cls + '" tabindex="0"><span>' + esc(c.nome) + '</span><div class="t" role="img" aria-label="' + esc(c.nome) + ': ' + brl(c.valor) + ' de ' + brl(c.limite) + ', ' + dica + '"><div class="f" style="width:' + Math.min(100, Math.max(2, pct)) + '%"></div></div><span class="v">' + brl(c.valor) + '<small>de ' + brl(c.limite) + ' · ' + dica + '</small></span></div>';
      }
      return '<div class="r" tabindex="0"><span>' + esc(c.nome) + '</span><div class="t" role="img" aria-label="' + esc(c.nome) + ': ' + brl(c.valor) + '"><div class="f" style="width:' + Math.max(2, c.valor / max * 100) + '%"></div></div><span class="v">' + brl(c.valor) + '</span></div>';
    }).join('') + '</div>';
  }
  function colunas(meses) {
    var max = Math.max.apply(null, meses.map(function (m) { return m.gastos; })) || 1;
    return '<div class="cols-wrap"><div class="cols">' + meses.map(function (m) {
      var h = m.gastos > 0 ? Math.max(3, m.gastos / max * 100) : 0;
      return '<div class="col" tabindex="0" aria-label="' + esc(m.mes) + ' ' + m.ano + ': ' + brl(m.gastos) + '"><span class="tip">' + brl(m.gastos) + '</span><i style="height:' + h + '%"></i><em>' + esc(m.mes.replace('.', '')) + '</em></div>';
    }).join('') + '</div></div>';
  }
  function lista(itens, vazio, fn) { return itens.length ? '<ul class="list">' + itens.map(fn).join('') + '</ul>' : '<p class="empty">' + vazio + '</p>'; }

  function renderPainel(p) {
    var el = $('p-painel');
    if (!p.ok) { el.innerHTML = '<div class="box"><p>Não conseguimos carregar o painel agora. Tente atualizar a página em instantes.</p></div>'; return; }
    if (p.vazio) {
      el.innerHTML = '<div class="box" style="text-align:center;padding:40px 24px"><h2 style="justify-content:center">Seu painel começa na primeira mensagem</h2><p>Mande para o Dyno algo como <b>“gastei 30 no almoço”</b> ou <b>“me lembra amanhã às 9h”</b>. Os dados aparecem aqui automaticamente.</p><div class="actions" style="justify-content:center"><a class="btn btn-primary" href="' + WA + '" rel="noopener">Abrir conversa com o Dyno</a></div></div>';
      return;
    }
    var r = p.resumo || {};
    var html = '<div class="kpis">' +
      '<div class="kpi"><span>Gastos em ' + esc(p.mes) + '</span><b>' + brl(r.gastos) + '</b></div>' +
      '<div class="kpi"><span>Receitas</span><b>' + brl(r.receitas) + '</b></div>' +
      '<div class="kpi"><span>Saldo do mês</span><b class="' + (r.saldo < 0 ? 'neg' : '') + '">' + brl(r.saldo) + '</b></div>' +
      '<div class="kpi"><span>Assinaturas por mês</span><b>' + brl(r.assinaturas_mes) + '</b></div></div>';
    html += '<div class="dash">' +
      '<div class="box"><h2>Gastos por categoria <small>' + esc(p.mes) + '</small></h2>' + hbar(p.categorias || []) + '</div>' +
      '<div class="box"><h2>Gastos nos últimos 6 meses</h2>' + colunas(p.meses || []) + '</div></div>';
    html += '<div class="dash">' +
      '<div class="box"><h2>Últimos lançamentos</h2>' + lista(p.ultimos || [], 'Nenhum lançamento ainda.', function (t) {
        return '<li><div>' + esc(t.descricao || t.categoria) + '<div class="sub">' + data(t.data) + ' · ' + esc(t.categoria) + (t.forma ? ' · ' + esc(t.forma) : '') + '</div></div><span class="val ' + (t.tipo === 'receita' ? 'in' : '') + '">' + (t.tipo === 'receita' ? '+ ' : '− ') + brl(t.valor) + '</span></li>';
      }) + '</div>' +
      '<div style="display:grid;gap:20px;align-content:start">' +
      '<div class="box"><h2>Contas a pagar</h2>' + lista(p.contas || [], 'Nenhuma conta em aberto.', function (c) {
        return '<li><div>' + esc(c.descricao) + '<div class="sub">vence ' + data(c.vencimento) + '</div></div><span class="val">' + brl(c.valor) + '</span></li>';
      }) + '</div>' +
      '<div class="box"><h2>Próximos lembretes</h2>' + lista(p.lembretes || [], 'Nenhum lembrete agendado.', function (l) {
        return '<li><div>' + esc(l.texto) + '<div class="sub">' + dataHora(l.quando) + (l.recorrencia && l.recorrencia !== 'nenhuma' ? ' · ' + esc(l.recorrencia) : '') + '</div></div></li>';
      }) + '</div></div></div>';
    html += '<div class="dash">' +
      '<div class="box"><h2>Tarefas em aberto</h2>' + lista(p.tarefas || [], 'Nenhuma tarefa pendente.', function (t) {
        return '<li><div>' + esc(t.titulo) + '<div class="sub">' + (t.prazo ? 'até ' + data(t.prazo) : 'sem prazo') + (t.prioridade ? ' · prioridade ' + esc(t.prioridade) : '') + '</div></div></li>';
      }) + '</div>' +
      '<div class="box"><h2>Assinaturas</h2>' + lista(p.assinaturas || [], 'Nenhuma assinatura registrada.', function (s) {
        return '<li><div>' + esc(s.nome) + '<div class="sub">' + esc(s.ciclo) + (s.proxima ? ' · próxima ' + data(s.proxima) : '') + '</div></div><span class="val">' + brl(s.valor) + '</span></li>';
      }) + '</div></div>';
    html += '<p class="note">Os dados vêm das suas conversas com o Dyno. Para corrigir algo, é só falar com ele no WhatsApp.</p>';
    el.innerHTML = html;
  }

  // ---------- conta ----------
  var STATUS = { ativo: ['ok', 'Ativo'], pendente: ['info', 'Período grátis'], em_atraso: ['warn', 'Pagamento em atraso'], cancelado: ['bad', 'Cancelado'], espera: ['info', 'Lista de espera'] };
  var FAT = { PENDING: ['info', 'Aguardando'], OVERDUE: ['warn', 'Vencida'], RECEIVED: ['ok', 'Paga'], CONFIRMED: ['ok', 'Paga'], RECEIVED_IN_CASH: ['ok', 'Paga'], REFUNDED: ['info', 'Estornada'] };
  function badge(par) { return '<span class="badge ' + par[0] + '">' + esc(par[1]) + '</span>'; }
  function mascaraFone(w) { var d = String(w || '').replace(/^55/, ''); return d.length >= 10 ? '(' + d.slice(0, 2) + ') ' + d.slice(2, d.length - 4) + '-' + d.slice(-4) : w; }

  function renderConta(c) {
    var el = $('p-conta');
    if (!c.ok) { el.innerHTML = '<div class="box"><p>Não conseguimos carregar sua conta agora. Tente atualizar a página.</p></div>'; return; }
    var u = c.usuario || {};
    var familia = u.plano === 'familia';
    var anual = u.ciclo === 'YEARLY';
    var planoTxt = familia ? 'Família (cortesia)' : (anual ? 'Anual · R$ 199,90 por ano' : 'Mensal · R$ 19,90 por mês');
    var st = STATUS[u.status] || ['info', u.status || '—'];
    var html = '<div class="acc"><div class="box"><h2>Sua assinatura ' + badge(st) + '</h2><dl class="dl">' +
      '<dt>Plano</dt><dd>' + esc(planoTxt) + '</dd>';
    if (!familia && u.dias_gratis > 0) html += '<dt>Período grátis</dt><dd>' + u.dias_gratis + ' dias restantes (até ' + data(u.gratis_ate) + ')</dd>';
    if (u.proximo_vencimento) html += '<dt>Próxima cobrança</dt><dd>' + data(u.proximo_vencimento) + '</dd>';
    html += '<dt>Cliente desde</dt><dd>' + data(u.cliente_desde) + '</dd></dl>';
    if (!familia && u.status !== 'cancelado') {
      html += '<div class="actions"><button class="btn btn-ghost btn-sm" id="trocar">' + (anual ? 'Mudar para o mensal' : 'Mudar para o anual (economize R$ 38,90)') + '</button>' +
        '<button class="btn btn-danger btn-sm" id="cancelar">Cancelar assinatura</button></div>';
    } else if (familia) {
      html += '<p class="note">Seu acesso é uma cortesia do plano família, sem cobranças.</p>';
    } else {
      html += '<p class="note">Sua assinatura está cancelada. Quer voltar? Fale com a gente pelo <a href="https://ig.me/m/dynoapp.ia">Instagram</a>.</p>';
    }
    html += '</div><div class="box"><h2>Seus dados</h2><dl class="dl"><dt>Nome</dt><dd>' + esc(u.nome) + '</dd><dt>WhatsApp</dt><dd>' + esc(mascaraFone(u.whatsapp)) + '</dd><dt>E-mail</dt><dd>' + esc(u.email || '—') + '</dd></dl>' +
      '<p class="note">Para alterar seus dados, pedir uma cópia ou a exclusão da conta, fale com o Dyno no WhatsApp. Veja a <a href="/privacidade">Política de privacidade</a>.</p></div></div>';
    var faturas = c.faturas || [];
    var pags = (c.pagamentos || []).map(function (p) { return { valor: p.valor, status: String(p.status || '').toUpperCase(), vencimento: p.vencimento, link: p.link }; });
    var todas = faturas.length ? faturas : pags;
    if (!familia) {
      html += '<div class="box" style="margin-top:20px"><h2>Faturas</h2>' + (todas.length ? '<ul class="list">' + todas.map(function (f) {
        return '<li><div>' + brl(f.valor) + '<div class="sub">vencimento ' + data(f.vencimento) + '</div></div><div style="display:flex;gap:10px;align-items:center">' + badge(FAT[f.status] || ['info', f.status || '—']) + (f.link ? '<a class="btn btn-ghost btn-sm" href="' + esc(f.link) + '" target="_blank" rel="noopener">' + (/PENDING|OVERDUE/.test(f.status) ? 'Pagar' : 'Ver') + '</a>' : '') + '</div></li>';
      }).join('') + '</ul>' : '<p class="empty">Nenhuma fatura ainda. A primeira só vence no fim do período grátis.</p>') + '</div>';
    }
    el.innerHTML = html;

    var bt = $('trocar');
    if (bt) bt.onclick = function () {
      var novo = anual ? 'MONTHLY' : 'YEARLY';
      var txt = novo === 'YEARLY' ? 'Sua assinatura passa a ser anual, de R$ 199,90 por ano (equivale a R$ 16,66 por mês). A próxima cobrança já vem no novo valor.' : 'Sua assinatura passa a ser mensal, de R$ 19,90 por mês. A próxima cobrança já vem no novo valor.';
      confirmar('Trocar de plano?', txt, 'Trocar plano').then(function (sim) {
        if (!sim) return;
        bt.disabled = true;
        api({ acao: 'plano', ciclo: novo }).then(function (r) {
          bt.disabled = false;
          if (sairPara401(r)) return;
          if (r.ok) { toast('Plano atualizado.'); carregarConta(); } else toast(r.erro === 'cobranca' ? 'Não conseguimos alterar no sistema de cobrança. Tente de novo mais tarde.' : 'Não foi possível trocar o plano agora.');
        });
      });
    };
    var bc = $('cancelar');
    if (bc) bc.onclick = function () {
      confirmar('Cancelar a assinatura?', 'As cobranças futuras serão canceladas e o Dyno deixa de atender você ao fim do período. Você pode voltar quando quiser.', 'Sim, cancelar').then(function (sim) {
        if (!sim) return;
        bc.disabled = true;
        api({ acao: 'cancelar' }).then(function (r) {
          bc.disabled = false;
          if (sairPara401(r)) return;
          if (r.ok) { toast('Assinatura cancelada.'); carregarConta(); } else toast('Não foi possível cancelar agora. Tente de novo mais tarde.');
        });
      });
    };
  }

  function carregarConta() {
    return api({ acao: 'conta' }).then(function (c) {
      if (sairPara401(c)) return;
      conta = c;
      var u = c.usuario || {};
      if (u.primeiro_nome) { $('ola').textContent = 'Olá, ' + u.primeiro_nome + '!'; document.title = 'Olá, ' + u.primeiro_nome + ' · Dyno'; }
      try { localStorage.setItem('dyno_nome', u.primeiro_nome || ''); } catch (e) { }
      if (u.primeiro_nome) { $('u-nome').textContent = u.primeiro_nome; $('u-av').textContent = u.primeiro_nome.charAt(0).toUpperCase(); }
      $('sub').textContent = u.plano === 'familia' ? 'Plano família' : ((STATUS[u.status] || [0, ''])[1] || '');
      renderConta(c);
    });
  }


  // ---------- extrato e comprovantes ----------
  var MESES = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro'];
  var mov = { cache: {}, dados: null, chave: '', carregando: false };
  var filtros = {
    extrato: { periodo: 'mes', de: '', ate: '', categoria: '', forma: '', tipo: '', busca: '' },
    comp: { periodo: 'mes', de: '', ate: '', categoria: '', busca: '' }
  };
  var iniciado = { extrato: false, comp: false };
  var arquivos = {};

  function iso(d) { return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0'); }
  function intervalo(f) {
    var h = new Date(); var y = h.getFullYear(), m = h.getMonth();
    switch (f.periodo) {
      case 'mes_passado': return [iso(new Date(y, m - 1, 1)), iso(new Date(y, m, 0))];
      case '3meses': return [iso(new Date(y, m - 2, 1)), iso(h)];
      case 'ano': return [iso(new Date(y, 0, 1)), iso(h)];
      case 'custom': return [f.de || iso(new Date(y, m, 1)), f.ate || iso(h)];
      default: return [iso(new Date(y, m, 1)), iso(h)];
    }
  }
  function sem(s) { return String(s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, ''); }
  function opcoes(lista, atual, todas) {
    return '<option value="">' + todas + '</option>' + lista.map(function (v) { return '<option' + (v === atual ? ' selected' : '') + '>' + esc(v) + '</option>'; }).join('');
  }
  function unicos(itens, campo) {
    var o = {}; itens.forEach(function (i) { if (i[campo]) o[i[campo]] = 1; });
    return Object.keys(o).sort(function (a, b) { return a.localeCompare(b, 'pt-BR'); });
  }

  function carregarMov(qual) {
    var f = filtros[qual]; var iv = intervalo(f); var chave = iv.join('|');
    if (mov.cache[chave]) { mov.dados = mov.cache[chave]; desenhar(qual); return; }
    $('lista-' + qual).innerHTML = '<div class="skeleton"></div>';
    api({ acao: 'extrato', de: iv[0], ate: iv[1] }).then(function (r) {
      if (sairPara401(r)) return;
      if (!r.ok) { $('lista-' + qual).innerHTML = '<div class="box"><p>Não conseguimos carregar agora. Tente de novo em instantes.</p></div>'; return; }
      mov.cache[chave] = r; mov.dados = r; desenhar(qual);
    });
  }

  function barraFiltros(qual) {
    var f = filtros[qual];
    var h = '<div class="filtros box">' +
      '<label>Período<select data-k="periodo">' +
      [['mes', 'Este mês'], ['mes_passado', 'Mês passado'], ['3meses', 'Últimos 3 meses'], ['ano', 'Este ano'], ['custom', 'Escolher datas']].map(function (o) { return '<option value="' + o[0] + '"' + (f.periodo === o[0] ? ' selected' : '') + '>' + o[1] + '</option>'; }).join('') +
      '</select></label>' +
      '<label class="so-custom"' + (f.periodo === 'custom' ? '' : ' hidden') + '>De<input type="date" data-k="de" value="' + esc(f.de) + '"></label>' +
      '<label class="so-custom"' + (f.periodo === 'custom' ? '' : ' hidden') + '>Até<input type="date" data-k="ate" value="' + esc(f.ate) + '"></label>' +
      '<label>Categoria<select data-k="categoria" id="f-cat-' + qual + '"><option value="">Todas</option></select></label>';
    if (qual === 'extrato') {
      h += '<label>Pagamento<select data-k="forma" id="f-forma-' + qual + '"><option value="">Todas</option></select></label>' +
        '<label>Tipo<select data-k="tipo"><option value="">Tudo</option><option value="despesa"' + (f.tipo === 'despesa' ? ' selected' : '') + '>Gastos</option><option value="receita"' + (f.tipo === 'receita' ? ' selected' : '') + '>Entradas</option></select></label>';
    }
    h += '<label class="busca">Buscar<input type="search" data-k="busca" placeholder="ex.: farmácia" value="' + esc(f.busca) + '"></label></div>';
    return h;
  }

  function ligarFiltros(qual) {
    var el = $('p-' + qual); var f = filtros[qual]; var t = null;
    el.querySelectorAll('[data-k]').forEach(function (inp) {
      var ev = inp.tagName === 'INPUT' && inp.type === 'search' ? 'input' : 'change';
      inp.addEventListener(ev, function () {
        var k = inp.getAttribute('data-k'); f[k] = inp.value;
        if (k === 'periodo') {
          el.querySelectorAll('.so-custom').forEach(function (x) { x.hidden = f.periodo !== 'custom'; });
          if (f.periodo === 'custom') return;
        }
        if (k === 'periodo' || k === 'de' || k === 'ate') { carregarMov(qual); return; }
        clearTimeout(t); t = setTimeout(function () { desenhar(qual); }, k === 'busca' ? 250 : 0);
      });
    });
  }

  function abrirMov(qual) {
    if (!iniciado[qual]) {
      iniciado[qual] = true;
      $('p-' + qual).innerHTML = barraFiltros(qual) + '<div id="lista-' + qual + '"></div>';
      ligarFiltros(qual);
    }
    carregarMov(qual);
  }

  function filtrar(qual) {
    var f = filtros[qual]; var b = sem(f.busca).trim();
    return (mov.dados.itens || []).filter(function (i) {
      if (qual === 'comp' && !i.comprovante) return false;
      if (f.categoria && i.categoria !== f.categoria) return false;
      if (qual === 'extrato' && f.forma && i.forma !== f.forma) return false;
      if (qual === 'extrato' && f.tipo && i.tipo !== f.tipo) return false;
      if (b && sem(i.descricao + ' ' + i.categoria + ' ' + i.forma).indexOf(b) < 0) return false;
      return true;
    });
  }

  function preencherSelects(qual, base) {
    var f = filtros[qual];
    var sc = $('f-cat-' + qual); if (sc) sc.innerHTML = opcoes(unicos(base, 'categoria'), f.categoria, 'Todas');
    var sf = $('f-forma-' + qual); if (sf) sf.innerHTML = opcoes(unicos(base, 'forma'), f.forma, 'Todas');
  }

  function diaLabel(s) {
    var p = s.split('-'); var d = new Date(+p[0], +p[1] - 1, +p[2]);
    return d.toLocaleDateString('pt-BR', { weekday: 'long', day: '2-digit', month: 'long' });
  }

  function desenhar(qual) {
    if (!mov.dados) return;
    var base = (mov.dados.itens || []).filter(function (i) { return qual !== 'comp' || i.comprovante; });
    preencherSelects(qual, base);
    var itens = filtrar(qual);
    var el = $('lista-' + qual);
    if (qual === 'extrato') el.innerHTML = htmlExtrato(itens); else el.innerHTML = htmlComp(itens);
    el.querySelectorAll('[data-ver]').forEach(function (b) { b.onclick = function () { verArquivo(Number(b.getAttribute('data-ver'))); }; });
    var exp = $('exportar'); if (exp) exp.onclick = function () { exportar(itens); };
    var zp = $('baixar-zip'); if (zp) zp.onclick = function () { baixarZip(itens, zp); };
    if (qual === 'comp') miniaturas(el);
  }

  function htmlExtrato(itens) {
    var g = 0, e = 0; itens.forEach(function (i) { if (i.tipo === 'receita') e += i.valor; else g += i.valor; });
    var h = '<div class="mov-topo"><div class="mov-tot"><span>Gastos <b>' + brl(g) + '</b></span><span>Entradas <b class="in">' + brl(e) + '</b></span><span>' + itens.length + (itens.length === 1 ? ' lançamento' : ' lançamentos') + '</span></div>' +
      (itens.length ? '<button class="btn btn-ghost btn-sm" id="exportar">Exportar planilha</button>' : '') + '</div>';
    if (!itens.length) return h + '<div class="box"><p class="empty">Nenhum lançamento com esses filtros.</p></div>';
    var dia = '', blocos = '';
    itens.forEach(function (i) {
      if (i.data !== dia) { if (dia) blocos += '</ul>'; dia = i.data; blocos += '<h3 class="dia">' + esc(diaLabel(dia)) + '</h3><ul class="list">'; }
      blocos += '<li><div>' + esc(i.descricao || i.categoria) + '<div class="sub">' + esc(i.categoria) + (i.forma ? ' · ' + esc(i.forma) : '') + ' · ' + esc(i.hora) + '</div></div>' +
        '<div class="lado">' + (i.comprovante ? '<button class="clip" data-ver="' + i.id + '" aria-label="Ver comprovante" title="Ver comprovante">📎</button>' : '') +
        '<span class="val ' + (i.tipo === 'receita' ? 'in' : '') + '">' + (i.tipo === 'receita' ? '+ ' : '− ') + brl(i.valor) + '</span></div></li>';
    });
    blocos += '</ul>';
    return h + '<div class="box">' + blocos + '</div>' + (mov.dados.cortado ? '<p class="note">Mostrando os 1.000 lançamentos mais recentes do período.</p>' : '');
  }

  function htmlComp(itens) {
    var tot = itens.reduce(function (s, i) { return s + (i.tipo === 'receita' ? 0 : i.valor); }, 0);
    var h = '<div class="mov-topo"><div class="mov-tot"><span>' + itens.length + (itens.length === 1 ? ' comprovante' : ' comprovantes') + '</span><span>Total <b>' + brl(tot) + '</b></span></div>' +
      (itens.length ? '<button class="btn btn-ghost btn-sm" id="baixar-zip">Baixar todos (.zip)</button>' : '') + '</div>';
    if (!itens.length) return h + '<div class="box" style="text-align:center"><p class="empty">Nenhum comprovante com esses filtros.</p><p class="note">Mande a foto ou o PDF do comprovante para o Dyno no WhatsApp e ele aparece aqui.</p></div>';
    var mes = '', out = '';
    itens.forEach(function (i) {
      var m = i.data.slice(0, 7);
      if (m !== mes) { if (mes) out += '</div>'; mes = m; out += '<h3 class="dia">' + MESES[+m.slice(5, 7) - 1] + ' de ' + m.slice(0, 4) + '</h3><div class="gal">'; }
      out += '<button class="comp" data-ver="' + i.id + '"><span class="thumb" data-thumb="' + i.id + '"><i>🧾</i></span>' +
        '<span class="ct"><b>' + brl(i.valor) + '</b><span>' + esc(i.descricao || i.categoria) + '</span><small>' + data(i.data) + ' · ' + esc(i.categoria) + '</small></span></button>';
    });
    out += '</div>';
    return h + out + (itens.length > 40 ? '<p class="note">O .zip leva os 40 comprovantes mais recentes do filtro. Para os demais, ajuste o período.</p>' : '');
  }

  // ---------- arquivos (passam pela API, só do dono) ----------
  function pegarArquivo(id) {
    if (arquivos[id]) return arquivos[id];
    arquivos[id] = fetch('/api/arquivo', {
      method: 'POST', credentials: 'same-origin',
      headers: { 'Content-Type': 'application/json', 'X-Requested-With': 'dyno' },
      body: JSON.stringify({ acao: 'arquivo', id: id })
    }).then(function (r) {
      if (r.status === 401) { esquecer(); location.replace('/entrar'); throw new Error('sessao'); }
      if (!r.ok) throw new Error('arquivo');
      var cd = r.headers.get('content-disposition') || '';
      var m = cd.match(/filename="([^"]+)"/);
      return r.blob().then(function (b) { return { url: URL.createObjectURL(b), tipo: b.type || '', nome: m ? m[1] : 'comprovante' }; });
    }).catch(function (e) { delete arquivos[id]; throw e; });
    return arquivos[id];
  }

  var fila = [], ativos = 0;
  function proximaMini() {
    if (ativos >= 2 || !fila.length) return;
    var span = fila.shift(); ativos++;
    pegarArquivo(Number(span.getAttribute('data-thumb'))).then(function (a) {
      if (/^image\//.test(a.tipo)) span.innerHTML = '<img alt="" src="' + a.url + '">';
      else span.innerHTML = '<i>📄</i><em>PDF</em>';
    }).catch(function () { span.innerHTML = '<i>⚠️</i>'; }).then(function () { ativos--; proximaMini(); });
  }
  function miniaturas(el) {
    var spans = el.querySelectorAll('[data-thumb]');
    if (!('IntersectionObserver' in window)) { spans.forEach(function (s) { fila.push(s); }); proximaMini(); return; }
    var obs = new IntersectionObserver(function (ents) {
      ents.forEach(function (en) { if (en.isIntersecting) { obs.unobserve(en.target); fila.push(en.target); proximaMini(); } });
    }, { rootMargin: '200px' });
    spans.forEach(function (s) { obs.observe(s); });
  }

  function verArquivo(id) {
    var item = (mov.dados.itens || []).filter(function (i) { return i.id === id; })[0] || {};
    var d = $('viewer');
    $('v-t').textContent = (item.descricao || item.categoria || 'Comprovante');
    $('v-s').textContent = data(item.data) + ' · ' + (item.categoria || '') + ' · ' + brl(item.valor);
    $('v-c').innerHTML = '<div class="skeleton"></div>';
    $('v-b').removeAttribute('href');
    d.showModal();
    pegarArquivo(id).then(function (a) {
      $('v-c').innerHTML = /^image\//.test(a.tipo) ? '<img alt="Comprovante" src="' + a.url + '">' : '<iframe title="Comprovante em PDF" src="' + a.url + '"></iframe>';
      $('v-b').href = a.url; $('v-b').download = a.nome;
    }).catch(function () { $('v-c').innerHTML = '<p class="empty">Não conseguimos abrir este comprovante agora.</p>'; });
  }
  $('v-x').onclick = function () { $('viewer').close(); };
  $('viewer').addEventListener('click', function (e) { if (e.target === $('viewer')) $('viewer').close(); });

  function baixarZip(itens, bt) {
    var iv = intervalo(filtros.comp);
    var ids = itens.slice(0, 40).map(function (i) { return i.id; });
    bt.disabled = true; var txt = bt.textContent; bt.textContent = 'Preparando…';
    fetch('/api/arquivo', {
      method: 'POST', credentials: 'same-origin',
      headers: { 'Content-Type': 'application/json', 'X-Requested-With': 'dyno' },
      body: JSON.stringify({ acao: 'zip', de: iv[0], ate: iv[1], ids: ids })
    }).then(function (r) {
      if (r.status === 401) { esquecer(); location.replace('/entrar'); return; }
      if (!r.ok) throw new Error('zip');
      return r.blob().then(function (b) {
        var a = document.createElement('a'); a.href = URL.createObjectURL(b); a.download = 'comprovantes_' + iv[0] + '_a_' + iv[1] + '.zip';
        document.body.appendChild(a); a.click(); a.remove();
        setTimeout(function () { URL.revokeObjectURL(a.href); }, 60000);
      });
    }).catch(function () { toast('Não conseguimos gerar o .zip agora. Tente de novo.'); })
      .then(function () { bt.disabled = false; bt.textContent = txt; });
  }

  function exportar(itens) {
    var cel = function (v) { v = String(v == null ? '' : v); return /[;"\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v; };
    var linhas = [['Data', 'Hora', 'Descrição', 'Categoria', 'Forma de pagamento', 'Tipo', 'Valor (R$)', 'Comprovante']];
    itens.forEach(function (i) {
      linhas.push([data(i.data), i.hora, i.descricao, i.categoria, i.forma, i.tipo === 'receita' ? 'Entrada' : 'Gasto', (i.tipo === 'receita' ? '' : '-') + Number(i.valor).toFixed(2).replace('.', ','), i.comprovante ? 'Sim' : 'Não']);
    });
    var csv = '﻿' + linhas.map(function (l) { return l.map(cel).join(';'); }).join('\r\n');
    var iv = intervalo(filtros.extrato);
    var a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([csv], { type: 'text/csv;charset=utf-8' }));
    a.download = 'extrato_dyno_' + iv[0] + '_a_' + iv[1] + '.csv';
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function () { URL.revokeObjectURL(a.href); }, 60000);
  }

  carregarConta().then(function () {
    if (!conta || !conta.ok) return;
    var salva = null;
    try { salva = sessionStorage.getItem('dyno_aba'); } catch (e) { }
    if (salva && ABAS.indexOf(salva) > -1 && salva !== 'painel') aba(salva);
    api({ acao: 'painel' }).then(function (p) { if (!sairPara401(p)) renderPainel(p); });
  });
})();
