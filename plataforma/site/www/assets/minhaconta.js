!function(){"use strict";
// 07/10/2026: links diretos da área do cliente — dynoapp.com.br/minhaconta/<aba>[/<id>]
// Ex.: /minhaconta/comprovante/123 abre o comprovante do lançamento 123 (pede login se precisar).
var $=function(i){return document.getElementById(i)};
var ROTA={painel:"painel",extrato:"extrato",comprovantes:"comp",comprovante:"comp",conta:"conta","minha-conta":"conta",agenda:"agenda",listas:"listas"};
var SLUG={painel:"painel",extrato:"extrato",comp:"comprovantes",conta:"conta",agenda:"agenda",listas:"listas"};
var m=location.pathname.match(/^\/minhaconta(?:\/([a-z-]+))?(?:\/([0-9-]+))?\/?$/);
var rota=m?{aba:ROTA[m[1]||"painel"]||"painel",id:/^\d+$/.test(m[2]||"")?Number(m[2]):0,periodo:/^\d{4}-\d{2}(-\d{2})?$/.test(m[2]||"")?m[2]:""}:null;
// /minhaconta/comprovantes/2026-10-05 (um dia) ou /minhaconta/comprovantes/2026-10 (um mês): aplica o filtro de datas da aba
function filtrarPeriodo(aba,p){
  var de=p,ate=p;
  if(p.length===7){var y=+p.slice(0,4),mo=+p.slice(5,7),ult=new Date(y,mo,0).getDate();de=p+"-01";ate=p+"-"+(ult<10?"0":"")+ult}
  var n=0,t=setInterval(function(){n++;var el=$("p-"+aba);var sel=el&&el.querySelector('select[data-k="periodo"]');
    if(sel){clearInterval(t);sel.value="custom";sel.dispatchEvent(new Event("change",{bubbles:true}));
      var ide=el.querySelector('input[data-k="de"]'),iat=el.querySelector('input[data-k="ate"]');
      if(ide&&iat){ide.value=de;ide.dispatchEvent(new Event("change",{bubbles:true}));iat.value=ate;iat.dispatchEvent(new Event("change",{bubbles:true}))}
    }else if(n>40)clearInterval(t)},150);
}
function lembrar(v){try{sessionStorage.setItem("dyno_volta",v)}catch(e){}}
function esquecer(){try{sessionStorage.removeItem("dyno_volta")}catch(e){}}
function volta(){try{return sessionStorage.getItem("dyno_volta")||""}catch(e){return""}}
// veio do login (/conta) com um link pendente? volta para ele
if(!rota&&/^\/conta\/?$/.test(location.pathname)){var v=volta();if(/^\/minhaconta(\/|$)/.test(v)){esquecer();location.replace(v)}}
if(!rota)return;
lembrar(location.pathname);
// quando a conta carregar com sucesso, o link pendente já foi usado
var f0=window.fetch;window.fetch=function(u,o){var p=f0.apply(this,arguments);try{if(String(u)==="/api"&&o&&typeof o.body==="string"&&o.body.indexOf('"acao":"conta"')>-1)p.then(function(r){if(r.ok)esquecer()}).catch(function(){})}catch(e){}return p};
function url(k,id){try{history.replaceState(null,"","/minhaconta/"+(SLUG[k]||k)+(id?"/"+id:""))}catch(e){}}
function brl(v){return(Number(v)||0).toLocaleString("pt-BR",{style:"currency",currency:"BRL"})}
function abrirComprovante(id){
  var d=$("viewer");if(!d)return;
  $("v-t").textContent="Comprovante";$("v-s").textContent="Lançamento nº "+id;$("v-c").innerHTML='<div class="skeleton"></div>';$("v-b").removeAttribute("href");
  if(!d.open)d.showModal();url("comp",id);
  fetch("/api/arquivo",{method:"POST",credentials:"same-origin",headers:{"Content-Type":"application/json","X-Requested-With":"dyno"},body:JSON.stringify({acao:"arquivo",id:id})}).then(function(r){
    if(r.status===401){location.replace("/entrar");throw 0}
    if(!r.ok)throw 0;var cd=r.headers.get("content-disposition")||"",mm=cd.match(/filename="([^"]+)"/);
    return r.blob().then(function(b){var u=URL.createObjectURL(b);$("v-c").innerHTML=/^image\//.test(b.type)?'<img alt="Comprovante" src="'+u+'">':'<iframe title="Comprovante em PDF" src="'+u+'"></iframe>';$("v-b").href=u;$("v-b").download=mm?mm[1]:"comprovante"})
  }).catch(function(){if($("v-c"))$("v-c").innerHTML='<p class="empty">Não encontrei esse comprovante. Confira se o link está certo ou abra a aba Comprovantes.</p>'});
}
function ir(){
  var k=rota.aba,b=$("t-"+k);
  if(b){b.click();url(k,0)}
  if((k==="comp"||k==="extrato")&&rota.periodo){filtrarPeriodo(k,rota.periodo);url(k,0);try{history.replaceState(null,"","/minhaconta/"+SLUG[k]+"/"+rota.periodo)}catch(e){}}
  if(k==="comp"&&rota.id){
    var alvo=document.querySelector('[data-ver="'+rota.id+'"]');
    if(alvo){alvo.click();url("comp",rota.id)}else abrirComprovante(rota.id);
  }
}
document.addEventListener("click",function(e){var t=e.target.closest&&e.target.closest('[role="tab"]');if(t&&/^t-/.test(t.id)){var k=t.id.slice(2);if(SLUG[k])url(k,0)}});
var vw=$("viewer");if(vw)vw.addEventListener("close",function(){if(/\/minhaconta\/comprovantes\/\d+/.test(location.pathname))url("comp",0)});
// espera a página terminar de montar (o "Olá, nome" aparece quando a sessão é válida)
var n=0,t=setInterval(function(){n++;var ola=$("ola");if(ola&&/Olá, /.test(ola.textContent)){clearInterval(t);ir()}else if(n>60)clearInterval(t)},250);
}();
