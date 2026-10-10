(function () {
  // Conversa animada do topo
  var tela = document.querySelector('.screen');
  var reduz = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (tela && !reduz) {
    var bolhas = Array.prototype.slice.call(tela.querySelectorAll('.b'));
    var status = tela.querySelector('[data-status]');
    tela.classList.add('anim');
    var timers = [];
    var esperar = function (fn, ms) { timers.push(setTimeout(fn, ms)); };
    var rodar = function () {
      var t = 500;
      bolhas.forEach(function (b) {
        var doDyno = b.classList.contains('dy');
        if (doDyno) {
          esperar(function () { if (status) { status.textContent = 'digitando…'; status.classList.add('typing'); } }, t);
          t += 1100;
        }
        esperar(function () {
          if (status) { status.textContent = 'online'; status.classList.remove('typing'); }
          b.classList.add('on');
        }, t);
        t += doDyno ? 1300 : 900;
      });
      esperar(function () { bolhas.forEach(function (b) { b.classList.remove('on'); }); }, t + 3500);
      esperar(rodar, t + 4300);
    };
    rodar();
  }
  // Vagas reais do Beta
  var alvos = document.querySelectorAll('[data-vagas],[data-vagas-txt],[data-vagas-pill]');
  if (!alvos.length) return;
  fetch('/api', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ acao: 'vagas' }) })
    .then(function (r) { return r.ok ? r.json() : null; })
    .then(function (d) {
      if (!d || !d.ok || typeof d.restantes !== 'number') return;
      var n = d.restantes, tot = d.total;
      document.querySelectorAll('[data-vagas]').forEach(function (e) { e.textContent = String(n); });
      document.querySelectorAll('[data-vagas-txt]').forEach(function (e) {
        e.textContent = n === 0 ? 'vagas esgotadas nesta rodada' : (n === 1 ? 'vaga restante' : 'vagas restantes') + ' de ' + tot;
      });
      document.querySelectorAll('[data-vagas-pill]').forEach(function (e) {
        e.textContent = n === 0 ? ' · vagas esgotadas' : ' · ' + (n === 1 ? 'resta 1 vaga' : 'restam ' + n + ' vagas');
      });
    })
    .catch(function () {});
})();
