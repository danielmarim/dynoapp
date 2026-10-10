(function () {
  'use strict';
  var $ = function (id) { return document.getElementById(id); };
  var plano = 'essencial';
  var TXT = {
    essencial: { t: 'Quero ser piloto do Essencial', s: 'Deixe seu contato. Quando a sua vaga abrir, a gente chama no WhatsApp.', b: 'Enviar inscrição',
      dt: 'Recebemos sua inscrição!', dp: 'Vamos chamar você no WhatsApp quando a sua vaga no piloto abrir.' },
    business: { t: 'Fale com a gente sobre o Business', s: 'Conte sobre a sua empresa. Respondemos pelo WhatsApp.', b: 'Enviar contato',
      dt: 'Recebemos seu contato!', dp: 'Vamos chamar você no WhatsApp para conversar sobre a sua empresa.' }
  };
  var ERROS = {
    nome: 'Escreva o seu nome.', numero: 'Esse WhatsApp não parece válido. Use DDD e número, por exemplo (11) 91234-5678.',
    negocio: 'Escreva o nome do seu negócio.', aceite: 'Marque a concordância para podermos chamar você.',
    muitas_tentativas: 'Muitas tentativas em pouco tempo. Espere alguns minutos e tente de novo.',
    indisponivel: 'Não conseguimos enviar agora. Tente de novo em instantes.'
  };

  function setPlano(p) {
    plano = p === 'business' ? 'business' : 'essencial';
    var t = TXT[plano];
    $('f-titulo').textContent = t.t; $('f-sub').textContent = t.s; $('fb').textContent = t.b;
    $('g-ess').hidden = plano !== 'essencial'; $('g-biz').hidden = plano !== 'business';
    document.querySelectorAll('[data-seg]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-seg') === plano)); });
  }
  document.querySelectorAll('[data-seg]').forEach(function (b) {
    b.addEventListener('click', function () { setPlano(b.getAttribute('data-seg')); });
  });
  document.querySelectorAll('a[data-plano]').forEach(function (a) {
    a.addEventListener('click', function () { setPlano(a.getAttribute('data-plano')); });
  });

  function mascara(v) {
    var d = v.replace(/\D/g, '').replace(/^55(?=\d{10,11}$)/, '').slice(0, 11);
    if (d.length <= 2) return d;
    if (d.length <= 6) return '(' + d.slice(0, 2) + ') ' + d.slice(2);
    if (d.length <= 10) return '(' + d.slice(0, 2) + ') ' + d.slice(2, 6) + '-' + d.slice(6);
    return '(' + d.slice(0, 2) + ') ' + d.slice(2, 7) + '-' + d.slice(7);
  }
  $('tel').addEventListener('input', function (e) { e.target.value = mascara(e.target.value); });

  function msg(tipo, texto) { var m = $('fm'); m.className = 'msg ' + tipo; m.textContent = texto; }

  $('fl').addEventListener('submit', function (e) {
    e.preventDefault();
    msg('', '');
    var nome = $('nome').value.trim(), tel = $('tel').value.replace(/\D/g, ''), neg = $('negocio').value.trim();
    if (nome.length < 2) { msg('err', ERROS.nome); $('nome').focus(); return; }
    if (tel.length < 10 || tel.length > 11) { msg('err', ERROS.numero); $('tel').focus(); return; }
    if (neg.length < 2) { msg('err', ERROS.negocio); $('negocio').focus(); return; }
    if (!$('aceite').checked) { msg('err', ERROS.aceite); return; }
    var corpo = { acao: 'biz_lead', plano: plano, nome: nome, whatsapp: tel, negocio: neg, aceite: true, site: $('site').value };
    if (plano === 'essencial') corpo.nicho = $('nicho').value.trim();
    else { corpo.funcionarios = $('func').value; corpo.mensagem = $('mens').value.trim(); }
    $('fb').disabled = true;
    fetch('/api', { method: 'POST', credentials: 'same-origin', headers: { 'Content-Type': 'application/json', 'X-Requested-With': 'dyno' }, body: JSON.stringify(corpo) })
      .then(function (r) { return r.json().catch(function () { return {}; }); })
      .catch(function () { return { ok: false, erro: 'indisponivel' }; })
      .then(function (r) {
        $('fb').disabled = false;
        if (r && r.ok) {
          var t = TXT[plano];
          $('fd-t').textContent = r.situacao === 'ja_recebido' ? 'Já temos o seu contato!' : t.dt;
          $('fd-p').textContent = r.situacao === 'ja_recebido' ? 'Sua inscrição já está na fila. Vamos chamar você no WhatsApp.' : t.dp;
          $('fl').hidden = true; $('fd').hidden = false;
          document.querySelector('.seg').hidden = true;
          return;
        }
        msg('err', ERROS[(r && r.erro)] || ERROS.indisponivel);
      });
  });

  if (location.hash === '#contato') { setPlano('business'); var p = $('participar'); if (p) p.scrollIntoView(); }
})();