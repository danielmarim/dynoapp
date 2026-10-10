
(function(){
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- hero chat ---------- */
  var DY='<div class="who"><span class="av dyno">D</span>Dyno <span>finanças</span></div>';
  var DI='<div class="who"><span class="av dina">D</span>Dina <span>agenda</span></div>';
  var S=[
    [['me','gastei 62 na farmácia','12:31'],
     ['bot',DY+'Anotado ✅ <b>R$ 62,00</b> em Saúde.<div class="mini"><div class="row"><span class="k">Saúde em outubro</span><span class="v">R$ 312,00</span></div><div class="row"><span class="k">Total do mês</span><span class="v">R$ 2.418,40</span></div></div>','12:31']],
    [['me','me lembra de ligar pro dentista amanhã às 10','09:14'],
     ['bot',DI+'Marcado para <b>amanhã, 10h</b>. Se você não responder, eu aviso de novo às 10h15.','09:14'],
     ['me','feito ✔','10:03'],
     ['bot',DI+'Ótimo, lembrete encerrado.','10:03']],
    [['me','quais contas vencem essa semana?','08:02'],
     ['bot',DY+'Duas contas:<div class="mini"><div class="row"><span class="k">Luz · hoje</span><span class="v">R$ 184,30</span></div><div class="row"><span class="k">Internet · sex 10</span><span class="v">R$ 119,90</span></div></div>','08:02'],
     ['me','paguei a luz','08:40'],
     ['bot',DY+'Luz marcada como paga 👍','08:40']],
    [['me','põe na lista: leite, café e pão','17:48'],
     ['bot',DI+'Lista do mercado com <b>3 itens</b>.','17:48'],
     ['me','minhas tarefas','17:50'],
     ['bot',DI+'<div class="mini"><div class="row"><span class="k">Renovar CNH</span><span class="v">sex 10</span></div><div class="row"><span class="k">Pagar IPVA</span><span class="v">seg 13</span></div><div class="row"><span class="k">Lista do mercado</span><span class="v">3 itens</span></div></div>','17:50']]
  ];
  var box=document.getElementById('msgs'), tabs=[].slice.call(document.querySelectorAll('.scene-tabs button'));
  var timers=[], cur=0, cycle;
  function bub(m){var d=document.createElement('div');d.className='b '+m[0];d.innerHTML=m[1]+'<span class="t">'+m[2]+'</span>';return d}
  function clear(){timers.forEach(clearTimeout);timers=[]}
  function full(i){box.innerHTML='';S[i].forEach(function(m){var b=bub(m);b.style.animation='none';box.appendChild(b)})}
  function play(i){
    clear();cur=i;tabs.forEach(function(t,k){t.setAttribute('aria-pressed',k===i)});
    if(reduce){full(i);return}
    box.innerHTML='';var t=200;
    S[i].forEach(function(m){
      if(m[0]==='bot'){
        timers.push(setTimeout(function(){var ty=document.createElement('div');ty.className='b bot';ty.id='ty';ty.innerHTML='<div class="typing"><i></i><i></i><i></i></div>';box.appendChild(ty)},t));
        t+=1100;
        timers.push(setTimeout(function(){var ty=document.getElementById('ty');if(ty)ty.remove();box.appendChild(bub(m))},t));
      }else{timers.push(setTimeout(function(){box.appendChild(bub(m))},t))}
      t+=900;
    });
    timers.push(setTimeout(function(){play((i+1)%S.length)},t+2600));
  }
  tabs.forEach(function(b){b.addEventListener('click',function(){play(+b.dataset.s)})});
  full(0); setTimeout(function(){play(0)},900);

  /* ---------- day stage ---------- */
  var LOGO='<span class="logo">D</span>';
  var D=[
    {h:'07:40',m:[['n','Dyno','07:40','Conta de luz vence hoje: <b style="color:var(--fg)">R$ 184,30</b>. Responda "paguei" quando quitar.']]},
    {h:'09:15',m:[['me','<div class="audio"><i class="play"></i><span class="wave"></span><span style="font-family:var(--mono);font-size:11px">0:07</span></div><div style="margin-top:6px;color:var(--muted);font-size:13px">"Me lembra de buscar o terno na quinta às 18h"</div>','09:15'],['bot',DI+'Marcado: <b>quinta, 18h</b> 👔 Vou insistir até você confirmar.','09:15']]},
    {h:'12:30',m:[['me','<div style="height:86px;border-radius:10px;background:repeating-linear-gradient(0deg,rgba(233,238,247,.08) 0 6px,transparent 6px 12px),#E9EEF7;opacity:.85"></div><div style="margin-top:6px">comprovante do almoço</div>','12:31'],['bot',DY+'Li o comprovante: <b>R$ 38,90</b> em Restaurante.','12:31']]},
    {h:'18:00',m:[['me','lista do mercado','18:02'],['bot',DI+'Leite · Café · Pão · Detergente<br><span style="color:var(--muted);font-size:12px">Responda "comprei café" para riscar.</span>','18:02']]},
    {h:'22:00',m:[['n','Resumo do dia','22:00','Saíram <b style="color:var(--fg)">R$ 223,20</b> em 3 gastos. 1 conta paga, 1 lembrete amanhã às 10h e 2 tarefas abertas.']]}
  ];
  var stage=document.getElementById('stage'), clock=document.getElementById('clock');
  var items=[].slice.call(document.querySelectorAll('.day-item')), di=0, dt;
  function renderDay(i){
    di=i;clock.textContent=D[i].h;stage.innerHTML='';
    items.forEach(function(el,k){el.classList.toggle('on',k===i);var b=el.querySelector('.bar');b.style.animation='none';void b.offsetWidth;b.style.animation=''});
    D[i].m.forEach(function(m,k){
      var el;
      if(m[0]==='n'){el=document.createElement('div');el.className='notif';el.innerHTML=LOGO+'<div style="flex:1;min-width:0"><b>'+m[1]+'<small>'+m[2]+'</small></b><p>'+m[3]+'</p></div>'}
      else{el=bub(m)}
      el.style.animationDelay=(k*0.5)+'s';stage.appendChild(el);
    });
    clearTimeout(dt); if(!reduce) dt=setTimeout(function(){renderDay((di+1)%D.length)},6000);
  }
  items.forEach(function(el){el.addEventListener('click',function(){renderDay(+el.dataset.i)})});
  renderDay(0);

  /* ---------- dot field ---------- */
  var c=document.getElementById('dots'),x=c.getContext('2d'),W,H,dpr,t0=performance.now();
  function size(){dpr=Math.min(devicePixelRatio||1,2);W=c.clientWidth;H=c.clientHeight;c.width=W*dpr;c.height=H*dpr;x.setTransform(dpr,0,0,dpr,0,0)}
  function draw(now){
    var t=(now-t0)/1000, g=16;x.clearRect(0,0,W,H);
    for(var yy=g/2;yy<H;yy+=g){for(var xx=g/2;xx<W;xx+=g){
      var v=Math.sin(xx*.012+t*.6)*Math.cos(yy*.018-t*.4)+Math.sin((xx+yy)*.006+t*.3);
      var r=Math.max(.4,(v+2)*.75);
      var gr=v>.9; x.fillStyle=gr?'rgba(47,212,126,'+(.22+(v-.9)*.3)+')':'rgba(160,185,225,'+(.08+(v+2)*.03)+')';
      x.beginPath();x.arc(xx,yy,r,0,6.283);x.fill();
    }}
    if(!reduce) requestAnimationFrame(draw);
  }
  size();addEventListener('resize',size);requestAnimationFrame(draw);
})();

/* vagas reais do Beta */
(function(){
  fetch('/api',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({acao:'vagas'})})
  .then(function(r){return r.ok?r.json():null}).then(function(d){
    if(!d||!d.ok||typeof d.restantes!=='number')return;
    var n=d.restantes,tot=d.total||40;
    document.querySelectorAll('[data-vagas-pill]').forEach(function(e){e.textContent=n===0?' · vagas esgotadas':(n===1?' · resta 1 vaga':' · restam '+n+' vagas')});
    var box=document.getElementById('seats');if(box){box.innerHTML='';for(var i=0;i<tot;i++){var el=document.createElement('i');if(i>=n)el.className='t';box.appendChild(el)}}
    var nt=document.getElementById('seatnote');if(nt)nt.textContent=n===0?'Vagas esgotadas nesta rodada':n+(n===1?' vaga restante':' vagas restantes')+' de '+tot;
  }).catch(function(){});
})();
