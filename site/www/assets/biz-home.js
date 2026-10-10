(function () {
  'use strict';
  var reduz = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var tudo = function (sel, cls) { document.querySelectorAll(sel).forEach(function (e) { e.classList.add(cls); }); };

  // Revelar ao rolar
  if (!('IntersectionObserver' in window) || reduz) { tudo('.rv', 'in'); }
  else {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    document.querySelectorAll('.rv').forEach(function (el) { io.observe(el); });
  }

  // Conversa do hero em sequência
  var stage = document.querySelector('.stage');
  if (stage) {
    var seq = stage.querySelectorAll('.seq');
    var typing = stage.querySelector('.typing');
    if (reduz) { seq.forEach(function (e) { e.classList.add('on'); }); }
    else {
      var at = function (ms, fn) { setTimeout(fn, ms); };
      var on = function (i) { return function () { if (seq[i]) seq[i].classList.add('on'); }; };
      // ordem no HTML: 0 áudio, 1 resposta, 2 PDF, 3 lembrete, 4 toast venda, 5 toast mês
      at(350, on(0));
      at(1000, function () { if (typing) typing.classList.add('on'); });
      at(2100, function () { if (typing) typing.classList.remove('on'); on(1)(); on(4)(); });
      at(2900, on(2));
      at(3700, on(3));
      at(4300, on(5));
    }
  }

  // Preço mensal x anual
  var preco = document.getElementById('preco'), nota = document.getElementById('preco-nota');
  document.querySelectorAll('[data-ciclo]').forEach(function (b) {
    b.addEventListener('click', function () {
      var anual = b.getAttribute('data-ciclo') === 'a';
      document.querySelectorAll('[data-ciclo]').forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
      if (preco) preco.textContent = anual ? 'R$ 29,08' : 'R$ 34,90';
      if (nota) nota.textContent = anual ? 'R$ 349 cobrados uma vez por ano · economia de R$ 69,80' : 'ou R$ 349 por ano no plano anual';
    });
  });
})();