/* Quiz "Qual é sua maior dor?" (preços) e filtro por plano (funcionalidades) */
(function () {
  'use strict';
  var PLANOS = {
    ess: { nome: 'Essencial', preco: 'R$ 19,90/mês' },
    comp: { nome: 'Completo', preco: 'R$ 29,90/mês' },
    prem: { nome: 'Premium', preco: 'R$ 39,90/mês' }
  };
  var DORES = {
    contas: ['ess', 'Para não esquecer contas e compromissos, o essencial basta: contas a pagar com aviso, lembretes que voltam se você não responder, tarefas e listas.'],
    dinheiro: ['comp', 'Para entender para onde vai o dinheiro, o Completo traz limites por categoria, importação de extrato, assinaturas, parcelados, resumo do dia e painel completo.'],
    parcelado: ['comp', 'Parcelados, quem te deve e clientes entram no Completo, junto com extrato, limites e relatórios.'],
    rotina: ['comp', 'Para colocar a rotina em ordem, o Completo inclui o bom dia das 7h30, os check-ins, a agenda de compromissos e a manutenção da casa e do carro.'],
    casa: ['prem', 'Para dividir as contas e a rotina da casa, o Premium tem o Modo família: até 4 pessoas no mesmo grupo, cada uma falando com o Dyno no próprio WhatsApp.']
  };

  function quiz() {
    var q = document.getElementById('quiz'); if (!q) return;
    var res = q.querySelector('.qres'), btns = [].slice.call(q.querySelectorAll('.qopt'));
    btns.forEach(function (b) {
      b.addEventListener('click', function () {
        var d = DORES[b.getAttribute('data-d')]; if (!d) return;
        var p = PLANOS[d[0]];
        btns.forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
        res.hidden = false;
        res.querySelector('h3').textContent = 'Recomendado para você: ' + p.nome + ' (' + p.preco + ')';
        res.querySelector('p').textContent = d[1];
        [].slice.call(document.querySelectorAll('.plan[data-plano]')).forEach(function (el) {
          el.classList.toggle('rec', el.getAttribute('data-plano') === d[0]);
        });
      });
    });
  }

  function filtroPlano() {
    var bar = document.getElementById('tierbar'); if (!bar) return;
    var chips = [].slice.call(bar.querySelectorAll('[data-t]')), cards = [].slice.call(document.querySelectorAll('.fcard[data-tier]'));
    var atual = 'tudo';
    function atualizar(t) {
      atual = t;
      chips.forEach(function (c) { var on = c.getAttribute('data-t') === t; c.classList.toggle('on', on); c.setAttribute('aria-pressed', on ? 'true' : 'false'); });
      cards.forEach(function (c) { c.hidden = !(t === 'tudo' || c.getAttribute('data-tier') === t); });
      [].slice.call(document.querySelectorAll('.fgrid')).forEach(function (g) { g.parentNode.setAttribute('data-vazio', g.querySelector('.fcard:not([hidden])') ? '0' : '1'); });
      [].slice.call(document.querySelectorAll('.fsec')).forEach(function (s) { s.classList.toggle('vazio', s.getAttribute('data-vazio') === '1'); s.style.display = s.getAttribute('data-vazio') === '1' ? 'none' : ''; });
      [].slice.call(document.querySelectorAll('.fgrupo')).forEach(function (g) {
        var tem = [].slice.call(g.querySelectorAll('.fsec')).some(function (s) { return !s.hidden && s.style.display !== 'none'; });
        g.style.display = tem ? '' : 'none';
      });
    }
    chips.forEach(function (c) { c.addEventListener('click', function () { atualizar(c.getAttribute('data-t')); }); });
    [].slice.call(document.querySelectorAll('.chips .chip[data-f]')).forEach(function (c) { c.addEventListener('click', function () { atualizar(atual); }); });
  }

  function iniciar() { quiz(); filtroPlano(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', iniciar); else iniciar();
})();
