(function () {
  'use strict';
  var $ = function (id) { return document.getElementById(id); };
  var numero = '';
  var ERROS = {
    numero_invalido: 'Esse número não parece válido. Use o DDD e o número, por exemplo (11) 91234-5678.',
    muitas_tentativas: 'Muitas tentativas em pouco tempo. Espere alguns minutos e tente de novo.',
    whatsapp: 'Não conseguimos enviar o código agora. Tente de novo em instantes.',
    codigo_invalido: 'Código incorreto. Confira e tente de novo.',
    codigo_expirado: 'Esse código expirou. Peça um novo.',
    bloqueado: 'Muitas tentativas com esse código. Peça um novo código.',
    indisponivel: 'O serviço está instável agora. Tente de novo em instantes.'
  };

  function api(corpo) {
    return fetch('/api', {
      method: 'POST',
      credentials: 'same-origin',
      headers: { 'Content-Type': 'application/json', 'X-Requested-With': 'dyno' },
      body: JSON.stringify(corpo)
    }).then(function (r) {
      return r.json().catch(function () { return {}; }).then(function (j) { j._status = r.status; return j; });
    }).catch(function () { return { ok: false, erro: 'indisponivel' }; });
  }
  function msg(el, tipo, texto) { el.className = 'msg ' + tipo; el.textContent = texto; }
  function limpa(el) { el.className = 'msg'; el.textContent = ''; }
  function mascara(v) {
    var d = v.replace(/\D/g, '').replace(/^55(?=\d{10,11}$)/, '').slice(0, 11);
    if (d.length <= 2) return d;
    if (d.length <= 6) return '(' + d.slice(0, 2) + ') ' + d.slice(2);
    if (d.length <= 10) return '(' + d.slice(0, 2) + ') ' + d.slice(2, 6) + '-' + d.slice(6);
    return '(' + d.slice(0, 2) + ') ' + d.slice(2, 7) + '-' + d.slice(7);
  }

  $('tel').addEventListener('input', function (e) { e.target.value = mascara(e.target.value); });

  function pedir(botao, saida) {
    botao.disabled = true;
    return api({ acao: 'codigo', whatsapp: numero }).then(function (r) {
      botao.disabled = false;
      if (r.ok) return true;
      msg(saida, 'err', ERROS[r.erro] || ERROS.indisponivel);
      return false;
    });
  }

  $('f1').addEventListener('submit', function (e) {
    e.preventDefault();
    var m1 = $('m1'); limpa(m1);
    var d = $('tel').value.replace(/\D/g, '');
    if (d.length < 10 || d.length > 11) { msg(m1, 'err', ERROS.numero_invalido); return; }
    numero = d;
    pedir($('b1'), m1).then(function (ok) {
      if (!ok) return;
      $('numShow').textContent = $('tel').value;
      $('f1').hidden = true; $('f2').hidden = false;
      msg($('m2'), 'ok', 'Se esse número tiver cadastro, o código chega em alguns segundos.');
      $('cod').focus();
    });
  });

  $('cod').addEventListener('input', function (e) {
    e.target.value = e.target.value.replace(/\D/g, '').slice(0, 6);
    if (e.target.value.length === 6) $('f2').requestSubmit();
  });

  $('f2').addEventListener('submit', function (e) {
    e.preventDefault();
    var m2 = $('m2'); limpa(m2);
    var c = $('cod').value;
    if (c.length !== 6) { msg(m2, 'err', 'O código tem 6 dígitos.'); return; }
    $('b2').disabled = true;
    api({ acao: 'entrar', whatsapp: numero, codigo: c }).then(function (r) {
      $('b2').disabled = false;
      if (r.ok) { try { localStorage.setItem('dyno_nome', r.nome || ''); } catch (e) { } location.href = '/conta'; return; }
      msg(m2, 'err', ERROS[r.erro] || ERROS.codigo_invalido);
      $('cod').select();
    });
  });

  $('reenviar').addEventListener('click', function () {
    var m2 = $('m2'); limpa(m2);
    pedir($('reenviar'), m2).then(function (ok) { if (ok) msg(m2, 'ok', 'Enviamos um novo código.'); });
  });
  $('trocar').addEventListener('click', function () {
    $('f2').hidden = true; $('f1').hidden = false; limpa($('m1')); $('cod').value = ''; $('tel').focus();
  });

  // Já está logado? vai direto para a conta
  api({ acao: 'conta' }).then(function (r) { if (r.ok) location.replace('/conta'); });
})();
