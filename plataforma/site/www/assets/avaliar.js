!function(){"use strict";
// 07/10/2026: avaliação de 1 a 5 estrelas na área do cliente (aba Minha conta e rodapé do Painel).
var $=function(i){return document.getElementById(i)};
var st=document.createElement("style");st.textContent=".aval{margin-top:20px}.aval h2{margin-bottom:6px}.aval p.sub{margin:0 0 10px;color:var(--muted,#8C9AB3)}.stars{display:flex;gap:6px;margin:6px 0 10px}.stars button{font-size:30px;line-height:1;background:none;border:0;cursor:pointer;color:#3a4661;padding:2px 4px;border-radius:8px;transition:transform .1s}.stars button.on{color:#F5B301}.stars button:hover{transform:scale(1.15)}.stars button:focus-visible{outline:2px solid var(--green,#2FD47E)}.aval textarea{box-sizing:border-box;width:100%;min-height:72px;border:1px solid rgba(255,255,255,.14);background:rgba(255,255,255,.04);color:inherit;border-radius:10px;padding:8px 10px;font:inherit;resize:vertical}.aval .ok{color:var(--green,#2FD47E);margin-top:8px}.aval .err{color:#FF8A8A;margin-top:8px}";document.head.appendChild(st);
var ROT={1:"Muito ruim",2:"Ruim",3:"Regular",4:"Bom",5:"Excelente"};
function api(c){return fetch("/api",{method:"POST",credentials:"same-origin",headers:{"Content-Type":"application/json","X-Requested-With":"dyno"},body:JSON.stringify(c)}).then(function(r){return r.json().catch(function(){return{}}).then(function(j){j._status=r.status;return j})}).catch(function(){return{ok:false,erro:"indisponivel"}})}
function esc(s){return String(s==null?"":s).replace(/[&<>"']/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]})}
function montar(ultima){
  var nota=ultima&&ultima.estrelas?Number(ultima.estrelas):0;
  var box=document.createElement("div");box.className="box aval";box.id="aval";
  box.innerHTML='<h2>Como está sendo usar o Dyno e a Dina?</h2><p class="sub">'+(nota?'Sua última avaliação: '+nota+' de 5 ('+ROT[nota]+'). Pode avaliar de novo quando quiser.':'Dê uma nota de 1 a 5 estrelas. Leva 10 segundos e ajuda muito.')+'</p>'+
    '<div class="stars" role="radiogroup" aria-label="Nota de 1 a 5 estrelas">'+[1,2,3,4,5].map(function(n){return'<button type="button" role="radio" aria-checked="'+(n===nota)+'" aria-label="'+n+' estrela'+(n>1?'s':'')+'" data-n="'+n+'"'+(n<=nota?' class="on"':'')+'>★</button>'}).join('')+'</div>'+
    '<div id="aval-rot" class="sub" style="min-height:20px">'+(nota?ROT[nota]:'')+'</div>'+
    '<textarea id="aval-txt" maxlength="500" placeholder="Quer contar o motivo? (opcional)"></textarea>'+
    '<div class="actions" style="margin-top:10px"><button class="btn btn-primary btn-sm" id="aval-enviar" type="button" disabled>Enviar avaliação</button></div><div id="aval-msg" role="status"></div>';
  var sel=nota,bts=box.querySelectorAll(".stars button");
  function pintar(n){bts.forEach(function(b){var k=Number(b.getAttribute("data-n"));b.classList.toggle("on",k<=n);b.setAttribute("aria-checked",String(k===n))});$("aval-rot").textContent=n?ROT[n]:"";$("aval-enviar").disabled=!n}
  bts.forEach(function(b){b.onclick=function(){sel=Number(b.getAttribute("data-n"));pintar(sel)};b.onmouseenter=function(){var k=Number(b.getAttribute("data-n"));bts.forEach(function(x){x.classList.toggle("on",Number(x.getAttribute("data-n"))<=k)})};b.onmouseleave=function(){pintar(sel)}});
  box.querySelector("#aval-enviar").onclick=function(){
    if(!sel)return;var bt=this,msg=$("aval-msg");bt.disabled=true;msg.className="";msg.textContent="";
    api({acao:"avaliar",estrelas:sel,comentario:$("aval-txt").value}).then(function(r){
      if(r._status===401){location.replace("/entrar");return}
      if(r.ok){msg.className="ok";msg.textContent="Obrigado! Avaliação de "+sel+" estrela"+(sel>1?"s":"")+" registrada ⭐";$("aval-txt").value="";box.querySelector("p.sub").textContent="Sua última avaliação: "+sel+" de 5 ("+ROT[sel]+"). Pode avaliar de novo quando quiser."}
      else{msg.className="err";msg.textContent=r.erro==="limite"?"Você já avaliou várias vezes hoje. Tente amanhã.":"Não consegui registrar agora. Tente de novo em instantes.";bt.disabled=false}
    });
  };
  return box;
}
function colocar(){
  var alvo=$("p-conta");if(!alvo||$("aval"))return false;
  if(!alvo.querySelector(".acc"))return false; // ainda carregando
  api({acao:"avaliacao"}).then(function(r){if(!$("aval")&&$("p-conta"))$("p-conta").appendChild(montar(r&&r.ok?r:null))});
  return true;
}
var n=0,t=setInterval(function(){n++;if(colocar()||n>80)clearInterval(t)},300);
// re-insere se a aba Minha conta for redesenhada (troca de plano, cancelamento)
var obs=new MutationObserver(function(){if($("p-conta")&&!$("aval")&&$("p-conta").querySelector(".acc"))colocar()});
var pc=$("p-conta");if(pc)obs.observe(pc,{childList:true});
}();
