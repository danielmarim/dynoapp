const {cardSemana}=require('./tpl.js');const fs=require('fs');
const {chromium}=require('/opt/npm-tools/node_modules/playwright/index.js');
const d={nome:'Daniel',periodo:'28/09 a 04/10',gSem:1284.37,gAnt:1460,rSem:0,nLanc:23,
dias:[['seg',120],['ter',340.5],['qua',88],['qui',0],['sex',412.87],['sáb',230],['dom',93]].map(([lb,v],i)=>({lb,v,hoje:i==6})),
cats:[['Mercado',512.4],['Alimentação',301.2],['Transporte',188.5],['Lazer',140],['Saúde',92.27],['Outras',50]],
proximos:[{quando:'seg 09:00',texto:'Pagar a luz',valor:189.9},{quando:'ter 14:30',texto:'Dentista da Quézia'},{quando:'qui 08:00',texto:'Renovar VPS Hostinger',valor:59.99},{quando:'sex 19:00',texto:'Aniversário do Eliezer'}],
feitos:9,nTar:4,orcamentos:[{cat:'Mercado',g:1480,lim:1800},{cat:'Lazer',g:420,lim:400}]};
fs.writeFileSync('a.html',cardSemana(d));
const e={...d,nome:'Marcelo',gSem:0,gAnt:0,nLanc:0,dias:d.dias.map(x=>({...x,v:0})),cats:[],proximos:[],orcamentos:[],feitos:0,nTar:0};
fs.writeFileSync('b.html',cardSemana(e));
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1350}});
for(const f of ['a','b']){await p.goto('file://'+__dirname+'/'+f+'.html');await p.screenshot({path:f+'.png'});
const o=await p.evaluate(()=>[...document.querySelectorAll('.card')].map(c=>c.getBoundingClientRect().bottom));console.log(f,o);}
await b.close();})();
