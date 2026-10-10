(function () {
  'use strict';
  var $ = function (id) { return document.getElementById(id); };
  var ERROS = {
    seguir: 'Para entrar no Beta, siga o @dynoapp.ia no Instagram e marque a opção do passo 1.',
    aceite: 'Para enviar o pedido, marque que leu a Política de Privacidade.',
    nome: 'Digite seu nome completo (nome e sobrenome).',
    numero: 'Esse WhatsApp não parece válido. Use o DDD e o número, por exemplo (11) 91234-5678.',
    instagram: 'Digite o seu @ do Instagram, por exemplo @seuperfil.',
    muitas_tentativas: 'Muitos pedidos em pouco tempo. Espere alguns minutos e tente de novo.',
    indisponivel: 'O serviço está instável agora. Tente de novo em instantes.'
  };
  var SITUACAO = {
    ja_recebido: ['Já recebemos seu pedido 👍', 'Ele está em análise. Assim que aprovado, o convite chega pelo WhatsApp do Dyno: +55 (11) 93949-7178.'],
    ja_aprovado: ['Seu pedido já foi aprovado! 🎉', 'Confira o WhatsApp: o convite foi enviado pelo número do Dyno, +55 (11) 93949-7178. Responda QUERO para ativar.'],
    ja_cliente: ['Você já é cliente do Dyno 😉', 'É só falar com o Dyno pelo WhatsApp ou entrar na sua área do cliente.']
  };
  function msg(t) { var el = $('mb'); el.className = 'msg err'; el.textContent = t; }
  function limpa() { var el = $('mb'); el.className = 'msg'; el.textContent = ''; }
  function mascara(v) {
    var d = v.replace(/\D/g, '').replace(/^55(?=\d{10,11}$)/, '').slice(0, 11);
    if (d.length <= 2) return d;
    if (d.length <= 6) return '(' + d.slice(0, 2) + ') ' + d.slice(2);
    if (d.length <= 10) return '(' + d.slice(0, 2) + ') ' + d.slice(2, 6) + '-' + d.slice(6);
    return '(' + d.slice(0, 2) + ') ' + d.slice(2, 7) + '-' + d.slice(7);
  }
  $('tel').addEventListener('input', function (e) { e.target.value = mascara(e.target.value); });
  $('fb').addEventListener('submit', function (e) {
    e.preventDefault();
    limpa();
    var nome = $('nome').value.trim().replace(/\s+/g, ' ');
    var tel = $('tel').value.replace(/\D/g, '');
    if (nome.split(' ').length < 2 || nome.length < 5) { $('nome').focus(); return msg(ERROS.nome); }
    if (tel.length < 10 || tel.length > 11) { $('tel').focus(); return msg(ERROS.numero); }
    if (!$('aceite').checked) return msg(ERROS.aceite);
    var b = $('bb'); b.disabled = true; b.textContent = 'Enviando…';
    fetch('/api', {
      method: 'POST', credentials: 'same-origin',
      headers: { 'Content-Type': 'application/json', 'X-Requested-With': 'dyno' },
      body: JSON.stringify({ acao: 'beta', nome: nome, whatsapp: tel, instagram: '', segue: false, aceite: true, site: $('site').value })
    }).then(function (r) { return r.json().catch(function () { return {}; }); })
      .catch(function () { return { ok: false, erro: 'indisponivel' }; })
      .then(function (r) {
        b.disabled = false; b.textContent = 'Enviar pedido';
        if (!r.ok) return msg(ERROS[r.erro] || ERROS.indisponivel);
        var s = SITUACAO[r.situacao];
        if (s) { $('ok-t').textContent = s[0]; $('ok-p').textContent = s[1]; }
        $('fb').hidden = true; $('bh').hidden = true; $('ok').hidden = false;
        $('ok').scrollIntoView({ behavior: 'smooth', block: 'center' });
      });
  });
})();
