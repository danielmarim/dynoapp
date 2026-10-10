(function () {
  'use strict';
  // 07/10/2026: Open Finance pela Pluggy. O link do WhatsApp traz ?c=<código de uso único, 30 min>.
  var $ = function (id) { return document.getElementById(id); };
  var SDK = 'https://cdn.pluggy.ai/pluggy-connect/v2.7.0/pluggy-connect.js';
  var ERROS = {
    link_invalido: 'Link inválido. No WhatsApp, diga "conectar banco" para receber um link novo.',
    link_expirado: 'Esse link expirou (vale 30 minutos). No WhatsApp, diga "conectar banco" para receber um link novo.',
    conta_inativa: 'Sua conta do Dyno não está ativa. Fale com a gente no WhatsApp.',
    indisponivel: 'O serviço está instável agora. Tente de novo em instantes.',
    sdk: 'Não consegui abrir a tela do banco. Confira sua internet e tente de novo.',
    banco: 'O banco não concluiu a conexão. Você pode tentar de novo agora.'
  };
  var codigo = new URLSearchParams(location.search).get('c') || '';
  try { history.replaceState(null, '', '/conectar-banco'); } catch (e) {}

  function msg(tipo, texto) { var el = $('cb-msg'); el.className = 'msg ' + tipo; el.textContent = texto; }
  function voltar() { $('cb-volta').hidden = false; }
  function botao(ativo, texto) { var b = $('cb-btn'); b.disabled = !ativo; b.textContent = texto; }

  function pedirToken() {
    return fetch('/api/banco', {
      method: 'POST',
      credentials: 'same-origin',
      headers: { 'Content-Type': 'application/json', 'X-Requested-With': 'dyno' },
      body: JSON.stringify({ codigo: codigo })
    }).then(function (r) { return r.json().catch(function () { return {}; }); })
      .catch(function () { return { ok: false, erro: 'indisponivel' }; });
  }

  var sdkPromessa = null;
  function carregarSdk() {
    if (window.PluggyConnect) return Promise.resolve();
    if (sdkPromessa) return sdkPromessa;
    sdkPromessa = new Promise(function (ok, falha) {
      var s = document.createElement('script');
      s.src = SDK; s.async = true;
      s.onload = function () { window.PluggyConnect ? ok() : falha(); };
      s.onerror = function () { sdkPromessa = null; falha(); };
      document.head.appendChild(s);
    });
    return sdkPromessa;
  }

  function abrir() {
    msg('', '');
    botao(false, 'Abrindo…');
    Promise.all([pedirToken(), carregarSdk().then(function () { return true; }, function () { return false; })]).then(function (res) {
      var r = res[0] || {}, sdkOk = res[1];
      if (!r.ok || !r.token) {
        botao(true, 'Escolher meu banco');
        msg('err', ERROS[r.erro] || ERROS.indisponivel);
        if (r.erro === 'link_invalido' || r.erro === 'link_expirado' || r.erro === 'conta_inativa') { $('cb-inicio').hidden = true; voltar(); }
        return;
      }
      if (!sdkOk) { botao(true, 'Escolher meu banco'); msg('err', ERROS.sdk); return; }
      var concluido = false;
      var w = new window.PluggyConnect({
        connectToken: r.token,
        includeSandbox: r.sandbox === true,
        language: 'pt',
        countries: ['BR'],
        connectorTypes: ['PERSONAL_BANK'],
        onSuccess: function (d) {
          concluido = true;
          var banco = d && d.item && d.item.connector && d.item.connector.name;
          $('cb-inicio').hidden = true;
          $('cb-titulo').textContent = 'Banco conectado ✅';
          msg('ok', 'Pronto' + (r.nome ? ', ' + r.nome : '') + '! ' + (banco ? 'Sua conta ' + banco + ' está' : 'Sua conta está') +
            ' conectada. Nos próximos minutos eu trago seus lançamentos e te aviso no WhatsApp.');
          voltar();
        },
        onError: function (e) {
          botao(true, 'Tentar de novo');
          msg('err', (e && e.message) ? ERROS.banco + ' (' + e.message + ')' : ERROS.banco);
        },
        onClose: function () { if (!concluido) botao(true, 'Escolher meu banco'); }
      });
      w.init();
    });
  }

  if (!/^[0-9a-f]{32}$/.test(codigo)) { msg('err', ERROS.link_invalido); voltar(); return; }
  $('cb-inicio').hidden = false;
  $('cb-btn').addEventListener('click', abrir);
})();
