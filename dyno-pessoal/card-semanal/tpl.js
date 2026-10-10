// Monta o HTML do card "Sua semana" (1080 x 1350). Mesmo código vai para o n8n.
function cardSemana(d) {
  const esc = s => String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  const brl = v => { const [i, c] = Math.abs(Number(v) || 0).toFixed(2).split('.'); return 'R$ ' + i.replace(/\B(?=(\d{3})+(?!\d))/g, '.') + ',' + c; };
  const brl0 = v => { const n = Math.round(Math.abs(Number(v) || 0)); return 'R$ ' + String(n).replace(/\B(?=(\d{3})+(?!\d))/g, '.'); };
  const CORES = ['#14B37D', '#FF8A3D', '#6C7BFF', '#F2B53A', '#E35D8F', '#8A8FA8'];
  const maxDia = Math.max(1, ...d.dias.map(x => x.v));
  d.cats = d.cats.slice(0, 5);
  const totCat = d.cats.reduce((s, c) => s + c[1], 0) || 1;

  let comp = '';
  if (d.gAnt > 0) {
    const p = Math.round((d.gSem - d.gAnt) / d.gAnt * 100);
    const menos = p < 0;
    comp = '<span class="chip ' + (menos ? 'ok' : p === 0 ? 'neu' : 'up') + '">' + (p === 0 ? '= igual' : (menos ? '▼ ' : '▲ ') + Math.abs(p) + '%') + ' vs semana passada</span>';
  } else if (d.gSem > 0) comp = '<span class="chip neu">primeira semana com gastos</span>';

  const barras = d.dias.map((x, i) => {
    const h = x.v > 0 ? Math.max(10, Math.round(x.v / maxDia * 130)) : 4;
    return '<div class="dia' + (x.hoje ? ' hoje' : '') + '"><div class="val">' + (x.v > 0 ? brl0(x.v) : '') + '</div><div class="bar" style="height:' + h + 'px"></div><div class="lb">' + esc(x.lb) + '</div></div>';
  }).join('');

  const stack = d.cats.map((c, i) => '<i style="flex:' + c[1].toFixed(2) + ';background:' + CORES[i % 6] + '"></i>').join('');
  const legenda = d.cats.map((c, i) => '<div class="lg"><b style="background:' + CORES[i % 6] + '"></b><span class="ln">' + esc(c[0]) + '</span><span class="lv">' + brl(c[1]) + '</span><span class="lp">' + Math.round(c[1] / totCat * 100) + '%</span></div>').join('');

  const agenda = d.proximos.length
    ? d.proximos.slice(0, 4).map(p => '<div class="ag"><span class="ad">' + esc(p.quando) + '</span><div class="ab"><div class="at">' + esc(p.texto) + '</div>' + (p.valor ? '<div class="amt">' + brl(p.valor) + '</div>' : '') + '</div></div>').join('')
    : '<div class="vazio">Nada agendado ainda. Me pede um lembrete que eu cuido 😉</div>';

  const orc = d.orcamentos.slice(0, 2).map(o => {
    const p = o.lim ? Math.round(o.g / o.lim * 100) : 0;
    const cor = p >= 100 ? '#E5484D' : p >= 80 ? '#FF8A3D' : '#14B37D';
    return '<div class="oc"><div class="ot"><span>' + esc(o.cat) + '</span><span>' + p + '%</span></div><div class="trk"><i style="width:' + Math.min(100, p) + '%;background:' + cor + '"></i></div></div>';
  }).join('');

  const semGastos = !d.gSem;
  return '<!doctype html><html><head><meta charset="utf-8"><style>' +
  '*{box-sizing:border-box;margin:0;padding:0}' +
  'html,body{width:1080px;height:1350px;background:#FFF6EA}' +
  'body{font-family:"Lato","Open Sans","Roboto","DejaVu Sans",sans-serif;color:#1B1F3B;-webkit-font-smoothing:antialiased}' +
  '.wrap{position:relative;width:1080px;height:1350px;overflow:hidden;padding:56px 60px}' +
  '.blob{position:absolute;border-radius:50%}' +
  '.top{position:relative;display:flex;align-items:center;justify-content:space-between}' +
  '.who{display:flex;align-items:center;gap:18px}' +
  '.av{width:76px;height:76px;border-radius:50%;background:#FF8A3D;color:#fff;display:grid;place-items:center;font-size:40px;box-shadow:0 0 0 6px #FFE2CC}' +
  '.who h1{font-size:44px;font-weight:900;letter-spacing:-.02em;line-height:1}' +
  '.who p{font-size:24px;color:#5E6280;margin-top:6px;font-weight:700}' +
  '.per{white-space:nowrap;flex:none;background:#1B1F3B;color:#fff;border-radius:999px;padding:14px 24px;font-size:24px;font-weight:700}' +
  '.hero{position:relative;margin-top:30px;background:#1B1F3B;color:#fff;border-radius:36px;padding:32px 44px;display:flex;justify-content:space-between;align-items:flex-end;overflow:hidden}' +
  '.hero .k{font-size:22px;letter-spacing:.12em;font-weight:800;color:#9AF4D5}' +
  '.hero .big{font-size:84px;font-weight:900;letter-spacing:-.03em;line-height:1;margin-top:12px}' +
  '.hero .sub{font-size:24px;color:#C9CCDD;margin-top:14px;font-weight:700}' +
  '.chip{display:inline-block;border-radius:999px;padding:10px 18px;font-size:22px;font-weight:800;margin-top:16px}' +
  '.chip.ok{background:#3EE9AF;color:#0B3D2C}.chip.up{background:#FFB98B;color:#5A2600}.chip.neu{background:#3A4070;color:#fff}' +
  '.mini{text-align:right}.mini div{font-size:22px;color:#C9CCDD;font-weight:700}.mini b{display:block;font-size:40px;color:#fff;margin-top:4px}' +
  '.grid{position:relative;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:22px;margin-top:22px}' +
  '.card{background:#fff;border-radius:30px;padding:30px 32px;border:3px solid #1B1F3B;box-shadow:8px 8px 0 #1B1F3B}' +
  '.card h3{font-size:20px;letter-spacing:.12em;font-weight:900;color:#0B6E4D;margin-bottom:18px}' +
  '.full{grid-column:1/3}' +
  '.dias{display:flex;align-items:flex-end;justify-content:space-between;height:180px;gap:14px}' +
  '.dia{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%}' +
  '.dia .bar{width:100%;border-radius:14px 14px 6px 6px;background:#BDEFD9}' +
  '.dia.hoje .bar{background:#14B37D}' +
  '.dia .val{font-size:19px;font-weight:800;color:#5E6280;margin-bottom:8px;white-space:nowrap}' +
  '.dia .lb{font-size:22px;font-weight:800;margin-top:10px;color:#1B1F3B;text-transform:capitalize}' +
  '.stack{display:flex;height:26px;border-radius:13px;overflow:hidden;gap:4px;margin-bottom:20px}.stack i{display:block;height:100%}' +
  '.lg{display:flex;align-items:center;gap:12px;font-size:23px;font-weight:700;padding:4px 0}' +
  '.lg b{width:16px;height:16px;border-radius:5px;flex:none}.lg .ln{flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.lg .lv{font-weight:900}.lg .lp{width:58px;text-align:right;color:#8A8FA8}' +
  '.ag{display:flex;align-items:center;gap:14px;padding:9px 0;border-bottom:2px dashed #EFE5D2;font-size:23px;font-weight:700}.ag:last-child{border-bottom:0}' +
  '.ad{flex:none;background:#FFE2CC;color:#8A3B00;border-radius:12px;padding:6px 12px;font-size:20px;font-weight:900}' +
  '.ab{flex:1;min-width:0}.at{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.amt{font-weight:900;font-size:20px;color:#C25A12;margin-top:2px}' +
  '.vazio{font-size:23px;color:#5E6280;font-weight:700;line-height:1.4}' +
  '.nums{display:flex;gap:14px;margin-top:18px}.num{flex:1;background:#FFF6EA;border-radius:18px;padding:14px 16px}.num b{display:block;font-size:40px;font-weight:900}.num span{font-size:19px;color:#5E6280;font-weight:800}' +
  '.oc{margin-top:10px}.ot{display:flex;justify-content:space-between;font-size:22px;font-weight:800}.trk{height:14px;background:#EFE5D2;border-radius:7px;margin-top:8px;overflow:hidden}.trk i{display:block;height:100%;border-radius:7px}' +
  '.foot{position:absolute;left:60px;right:60px;bottom:40px;display:flex;justify-content:space-between;align-items:center;font-size:22px;font-weight:800;color:#5E6280}' +
  '.duo{display:flex;align-items:center;gap:10px}.duo i{width:36px;height:36px;border-radius:50%;display:grid;place-items:center;font-style:normal;font-size:18px}' +
  '</style></head><body><div class="wrap">' +
  '<div class="blob" style="width:520px;height:520px;background:#FFE2CC;right:-180px;top:-220px"></div>' +
  '<div class="blob" style="width:380px;height:380px;background:#D9F7EA;left:-160px;bottom:-140px"></div>' +
  '<div class="top"><div class="who"><div class="av">⏰</div><div><h1>Sua semana, ' + esc(d.nome) + '</h1><p>Dina, com os números do Dyno</p></div></div><div class="per">' + esc(d.periodo) + '</div></div>' +
  '<div class="hero"><div><div class="k">VOCÊ GASTOU NA SEMANA</div><div class="big">' + (semGastos ? 'R$ 0' : brl(d.gSem)) + '</div>' + (comp || '<div class="sub">Nenhum gasto registrado. Semana zen? 🧘</div>') + '</div>' +
  '<div class="mini"><div>Lançamentos</div><b>' + d.nLanc + '</b>' + (d.rSem > 0 ? '<div style="margin-top:12px">Entradas</div><b style="color:#3EE9AF">' + brl(d.rSem) + '</b>' : '') + '</div></div>' +
  '<div class="grid">' +
  '<div class="card full"><h3>DIA A DIA</h3><div class="dias">' + barras + '</div></div>' +
  '<div class="card"><h3>ONDE FOI O DINHEIRO</h3>' + (d.cats.length ? '<div class="stack">' + stack + '</div>' + legenda : '<div class="vazio">Sem gastos nesta semana.</div>') + (orc ? '<h3 style="margin:22px 0 0">ORÇAMENTOS DO MÊS</h3>' + orc : '') + '</div>' +
  '<div class="card"><h3>PRÓXIMOS 7 DIAS</h3>' + agenda +
  '<div class="nums"><div class="num"><b>' + d.feitos + '</b><span>lembretes feitos</span></div><div class="num"><b>' + d.nTar + '</b><span>tarefas abertas</span></div></div>' +
  '</div></div>' +
  '<div class="foot"><div class="duo"><i style="background:#FF8A3D">⏰</i><i style="background:#14B37D">💰</i>Dina &amp; Dyno</div><div>dynoapp.com.br</div></div>' +
  '</div></body></html>';
}
if (typeof module !== 'undefined') module.exports = { cardSemana };
