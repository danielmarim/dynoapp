(function () {
  'use strict';
  var $ = function (id) { return document.getElementById(id); };
  var q = new URLSearchParams(location.search);
  var ERROS = {
    expirado: 'Esse link expirou ou já foi usado. No WhatsApp, diga "conectar agenda" para receber um link novo.',
    invalido: 'Link inválido. No WhatsApp, diga "conectar agenda" para receber um link novo.',
    nao_configurado: 'A conexão com o Google Agenda ainda não está disponível. Tente de novo mais tarde.',
    codigo: 'O Google não devolveu a autorização. Tente de novo pelo link do WhatsApp.',
    sem_refresh: 'O Google não liberou o acesso contínuo à agenda. Diga "conectar agenda" no WhatsApp e tente de novo.',
    google: 'Não consegui falar com o Google agora. Diga "conectar agenda" no WhatsApp e tente de novo.',
    negado: 'Você não autorizou o acesso. Tudo bem: quando quiser, diga "conectar agenda" no WhatsApp.',
    indisponivel: 'O serviço está instável agora. Tente de novo em instantes.'
  };
  function api(corpo) {
    return fetch('/api', {
      method: 'POST',
      credentials: 'same-origin',
      headers: { 'Content-Type': 'application/json', 'X-Requested-With': 'dyno' },
      body: JSON.stringify(corpo)
    }).then(function (r) {
      return r.json().catch(function () { return {}; });
    }).catch(function () { return { ok: false, erro: 'indisponivel' }; });
  }
  function msg(tipo, texto) { var el = $('ca-msg'); el.className = 'msg ' + tipo; el.textContent = texto; }
  function erro(cod) {
    msg('err', ERROS[cod] || ERROS.google);
    $('ca-volta').hidden = false;
  }
  function limparUrl() { try { history.replaceState(null, '', '/conectar-agenda'); } catch (e) {} }

  var s = q.get('s');
  var state = q.get('state');
  var code = q.get('code');
  var gErro = q.get('error');

  if (state || gErro) {
    limparUrl();
    $('ca-titulo').textContent = 'Conectando sua agenda…';
    if (gErro || !code) { $('ca-titulo').textContent = 'Agenda não conectada'; erro(gErro === 'access_denied' ? 'negado' : 'codigo'); return; }
    msg('ok', 'Só um instante, estou confirmando com o Google…');
    api({ acao: 'agenda_callback', s: state, code: code }).then(function (r) {
      if (r && r.ok) {
        $('ca-titulo').textContent = 'Agenda conectada ✅';
        msg('ok', 'Pronto' + (r.nome ? ', ' + r.nome.split(' ')[0] : '') + '! Sua Google Agenda' + (r.email ? ' (' + r.email + ')' : '') + ' está conectada. A Dina já te mandou uma mensagem no WhatsApp.');
        $('ca-volta').hidden = false;
      } else {
        $('ca-titulo').textContent = 'Agenda não conectada';
        erro((r && r.erro) || 'google');
      }
    });
    return;
  }

  if (!s) { $('ca-titulo').textContent = 'Conectar sua agenda'; erro('invalido'); return; }
  $('ca-inicio').hidden = false;
  $('ca-btn').addEventListener('click', function () {
    var b = $('ca-btn');
    b.disabled = true; b.textContent = 'Abrindo o Google…';
    api({ acao: 'agenda_iniciar', s: s }).then(function (r) {
      if (r && r.ok && /^https:\/\/accounts\.google\.com\//.test(r.url || '')) { location.href = r.url; return; }
      b.disabled = false; b.textContent = 'Continuar com o Google';
      erro((r && r.erro) || 'google');
    });
  });
})();
