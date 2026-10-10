const TZ = 'America/Sao_Paulo';
// Quem recebe o resumo semanal no privado (nome → número). Hoje: só a família.
const PESSOAS = { 'Daniel': '5511930851325', 'Quézia': '55119XXXXXXXX', 'Eliezer': '55119YYYYYYYY' };
const NL = String.fromCharCode(10);
const linhas = n => { try { return $(n).all().map(i => i.json).filter(r => r && r.id !== undefined && r.id !== null); } catch (e) { return []; } };
const de = r => r.autor || 'Daniel';
const brl = v => { const [i, c] = Math.abs(Number(v) || 0).toFixed(2).split('.'); return 'R$ ' + i.replace(/\B(?=(\d{3})+(?!\d))/g, '.') + ',' + c; };
const dt = v => { if (!v) return null; let d = DateTime.fromISO(String(v)); if (!d.isValid) d = DateTime.fromSQL(String(v)); return d.isValid ? d.setZone(TZ) : null; };
const BONITO = { alimentacao: 'Alimentação', educacao: 'Educação', saude: 'Saúde', vestuario: 'Vestuário', servicos: 'Serviços', transporte: 'Transporte', moradia: 'Moradia', lazer: 'Lazer', contas: 'Contas', assinaturas: 'Assinaturas', mercado: 'Mercado', outros: 'Outros', presentes: 'Presentes', viagem: 'Viagem', pets: 'Pets', beleza: 'Beleza', impostos: 'Impostos', investimentos: 'Investimentos' };
const nomeCat = c => { const k = String(c || 'outros').toLowerCase().trim(); return BONITO[k] || (k.charAt(0).toUpperCase() + k.slice(1)); };
const DIAS = ['seg', 'ter', 'qua', 'qui', 'sex', 'sáb', 'dom'];
const agora = DateTime.now().setZone(TZ).setLocale('pt-BR');
const iniSem = agora.startOf('week');
const fimSem = iniSem.plus({ days: 7 });
const iniAnt = iniSem.minus({ weeks: 1 });
const iniMes = agora.startOf('month');
const proxFim = agora.endOf('day').plus({ days: 7 });
const trans = linhas('Transações recentes').map(t => ({ ...t, d: dt(t.data || t.createdAt), v: Number(t.valor) || 0 })).filter(t => t.d);
const orc = linhas('Orçamentos ativos').filter(r => r.ativo !== false);
const tarefas = linhas('Tarefas abertas');
const lembretes = linhas('Lembretes').map(r => ({ ...r, d: dt(r.quando) }));
const contas = linhas('Contas').map(r => ({ ...r, d: dt(r.vencimento) }));

//__TPL__

const saida = [];
for (const [nome, numero] of Object.entries(PESSOAS)) {
  const minhas = trans.filter(t => de(t) === nome);
  const desp = l => l.filter(t => t.tipo !== 'receita');
  const soma = l => l.reduce((s, t) => s + t.v, 0);
  const semana = minhas.filter(t => t.d >= iniSem && t.d < fimSem);
  const anterior = minhas.filter(t => t.d >= iniAnt && t.d < iniSem);
  const gSem = soma(desp(semana)), gAnt = soma(desp(anterior));
  const rSem = soma(semana.filter(t => t.tipo === 'receita'));
  const porCat = {};
  for (const t of desp(semana)) { const k = nomeCat(t.categoria); porCat[k] = (porCat[k] || 0) + t.v; }
  let cats = Object.entries(porCat).sort((a, b) => b[1] - a[1]);
  if (cats.length > 5) cats = cats.slice(0, 4).concat([['Outras', cats.slice(4).reduce((s, c) => s + c[1], 0)]]);
  const dias = DIAS.map((lb, i) => { const a = iniSem.plus({ days: i }), b = a.plus({ days: 1 }); return { lb, v: soma(desp(semana.filter(t => t.d >= a && t.d < b))), hoje: a.hasSame(agora, 'day') }; });
  const gastoMes = {};
  for (const t of desp(minhas.filter(t => t.d >= iniMes))) { const k = nomeCat(t.categoria); gastoMes[k] = (gastoMes[k] || 0) + t.v; }
  const orcamentos = orc.filter(o => (o.pessoa || o.autor || 'Daniel') === nome).map(o => ({ cat: nomeCat(o.categoria), g: gastoMes[nomeCat(o.categoria)] || 0, lim: Number(o.limite) || 0 })).sort((a, b) => (b.lim ? b.g / b.lim : 0) - (a.lim ? a.g / a.lim : 0));
  const meusL = lembretes.filter(l => de(l) === nome);
  const feitos = meusL.filter(l => l.status === 'concluido' && dt(l.updatedAt) && dt(l.updatedAt) >= iniSem).length;
  const quando = d => DIAS[d.weekday - 1] + ' ' + d.toFormat('HH:mm');
  const proximos = meusL.filter(l => l.status === 'pendente' && l.d && l.d > agora && l.d <= proxFim).map(l => ({ d: l.d, quando: quando(l.d), texto: String(l.texto || '').split(NL)[0].slice(0, 60) }))
    .concat(contas.filter(c => de(c) === nome && c.d && c.d > agora.startOf('day') && c.d <= proxFim && !['paga', 'pago', 'cancelada', 'cancelado'].includes(String(c.status || '').toLowerCase()))
      .map(c => ({ d: c.d, quando: DIAS[c.d.weekday - 1] + ' ' + c.d.toFormat('dd/LL'), texto: 'Vence: ' + (c.descricao || c.beneficiario || 'conta'), valor: Number(c.valor) || 0 })))
    .sort((a, b) => a.d - b.d);
  const nTar = tarefas.filter(t => de(t) === nome).length;
  const d = { nome: String(nome).split(' ')[0], periodo: iniSem.toFormat('dd/LL') + ' a ' + fimSem.minus({ days: 1 }).toFormat('dd/LL'), gSem, gAnt, rSem, nLanc: semana.length, dias, cats, proximos, feitos, nTar, orcamentos };

  let comp = '';
  if (gAnt > 0) { const v = Math.round((gSem - gAnt) / gAnt * 100); comp = v === 0 ? ' (igual à semana passada)' : ' (' + (v < 0 ? '▼ ' : '▲ ') + Math.abs(v) + '% vs semana passada)'; }
  const c = ['*⏰ Dina*', 'Oi, ' + d.nome + '! Aqui está a sua semana (' + d.periodo + ') 👆', ''];
  c.push(semana.length ? '💸 Gastos: *' + brl(gSem) + '*' + comp : '💸 Nenhum gasto registrado nesta semana.');
  if (rSem > 0) c.push('💵 Entradas: ' + brl(rSem));
  const alerta = orcamentos.filter(o => o.lim && o.g / o.lim >= 0.8);
  if (alerta.length) c.push('🎯 De olho: ' + alerta.map(o => o.cat + ' ' + Math.round(o.g / o.lim * 100) + '%').join(' · '));
  c.push('📅 Próximos 7 dias: ' + (proximos.length ? proximos.length + (proximos.length === 1 ? ' compromisso' : ' compromissos') : 'nada agendado ainda'));
  c.push('', 'Boa semana! Quer o detalhe do mês? É só pedir "meu dashboard do mês".');
  const caption = c.join(NL);
  const html = cardSemana(d);
  const bin = await this.helpers.prepareBinaryData(Buffer.from(html, 'utf8'), 'index.html', 'text/html');
  saida.push({ json: { numero, nome, caption, temImagem: true }, binary: { files: bin } });
}
return saida;
