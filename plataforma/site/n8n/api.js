import { workflow, node, trigger, ifElse, switchCase, expr } from '@n8n/workflow-sdk';

const SB = 'https://xvekgnbneeokihtjpbts.supabase.co/rest/v1/rpc/';
const ASAAS = 'https://api.asaas.com/v3';

const entrada = trigger({
  type: 'n8n-nodes-base.webhook',
  version: 2.1,
  config: {
    name: 'Site: requisição',
    parameters: { httpMethod: 'POST', path: 'dyno-site-api', responseMode: 'responseNode', options: { allowedOrigins: 'https://dynoapp.com.br,https://www.dynoapp.com.br' } }
  }
});

const preparar = node({
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {
    name: 'Preparar',
    parameters: {
      mode: 'runOnceForAllItems',
      language: 'javaScript',
      jsCode: `const SEGREDO = '__SEGREDO__';
const req = $input.first().json || {};
const h = req.headers || {};
const b = req.body || {};
const m = String(h.cookie || '').match(/(?:^|;\\s*)dyno_sess=([a-f0-9]{64})/);
const token = m ? m[1] : '';
const ip = String(h['x-real-ip'] || String(h['x-forwarded-for'] || '').split(',')[0] || '').trim().slice(0, 64);
const acao = String(b.acao || '');
const responder = (status, resposta) => [{ json: { proximo: 'responder', acao, status, resposta } }];
if (String(h['x-dyno-site'] || '') !== SEGREDO) return responder(403, { ok: false, erro: 'proibido' });
const rpc = (nome, args) => [{ json: { proximo: 'rpc', acao, rpc: nome, args, token, ip, ciclo: b.ciclo === 'YEARLY' ? 'YEARLY' : 'MONTHLY' } }];
switch (acao) {
  case 'codigo': return rpc('dyno_site_codigo_pedir', { p_whatsapp: String(b.whatsapp || '').slice(0, 30), p_ip: ip });
  case 'entrar': return rpc('dyno_site_codigo_validar', { p_whatsapp: String(b.whatsapp || '').slice(0, 30), p_codigo: String(b.codigo || '').slice(0, 10), p_ip: ip });
  case 'conta':
  case 'painel':
    if (!token) return responder(401, { ok: false, erro: 'sessao' });
    return rpc('dyno_site_conta', { p_token: token });
  case 'plano':
    if (!token) return responder(401, { ok: false, erro: 'sessao' });
    return rpc('dyno_site_plano', { p_token: token, p_ciclo: b.ciclo === 'YEARLY' ? 'YEARLY' : 'MONTHLY' });
  case 'cancelar':
    if (!token) return responder(401, { ok: false, erro: 'sessao' });
    return rpc('dyno_site_cancelar', { p_token: token });
  case 'sair':
    return rpc('dyno_site_sair', { p_token: token });
  default:
    return responder(400, { ok: false, erro: 'acao_invalida' });
}`
    }
  }
});

const precisaBanco = ifElse({
  version: 2.2,
  config: {
    name: 'Precisa do banco?',
    parameters: {
      conditions: {
        options: { caseSensitive: true, leftValue: '', typeValidation: 'loose' },
        conditions: [{ leftValue: expr('{{ $json.proximo }}'), operator: { type: 'string', operation: 'equals' }, rightValue: 'rpc' }],
        combinator: 'and'
      }
    }
  }
});

const supabaseRpc = node({
  type: 'n8n-nodes-base.httpRequest',
  version: 4.3,
  config: {
    name: 'Supabase: RPC',
    onError: 'continueRegularOutput',
    parameters: {
      method: 'POST',
      url: expr('{{ "' + SB + '" + $json.rpc }}'),
      authentication: 'genericCredentialType',
      genericAuthType: 'httpHeaderAuth',
      sendBody: true,
      contentType: 'json',
      specifyBody: 'json',
      jsonBody: expr('{{ JSON.stringify($json.args) }}'),
      options: { timeout: 15000 }
    }
  }
});

const decidir = node({
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {
    name: 'Decidir',
    parameters: {
      mode: 'runOnceForAllItems',
      language: 'javaScript',
      jsCode: `const ZW = String.fromCharCode(8203);
const NL = String.fromCharCode(10);
const p = $('Preparar').first().json;
const r = $input.first().json || {};
const out = (o) => [{ json: Object.assign({ acao: p.acao }, o) }];
const responder = (status, resposta, cookie) => out({ proximo: 'responder', status, resposta, cookie: cookie || '' });
if (r.error || (r.code && r.message)) return responder(500, { ok: false, erro: 'indisponivel' });
const COOKIE = (t, idade) => 'dyno_sess=' + t + '; Path=/; Max-Age=' + idade + '; HttpOnly; Secure; SameSite=Lax';
switch (p.acao) {
  case 'codigo': {
    if (r.enviar) {
      const texto = 'Olá, ' + (r.nome || '') + '! Seu código para entrar no site do Dyno é:' + NL + NL + '*' + r.codigo + '*' + NL + NL + 'Ele vale por 10 minutos. Se não foi você que pediu, é só ignorar esta mensagem.';
      return out({ proximo: 'whatsapp', status: 200, resposta: { ok: true }, corpo: { number: r.numero, text: ZW + texto, delay: 300 } });
    }
    if (r.motivo === 'muitas_tentativas') return responder(429, { ok: false, erro: 'muitas_tentativas' });
    if (r.motivo === 'numero_invalido') return responder(400, { ok: false, erro: 'numero_invalido' });
    return responder(200, { ok: true });
  }
  case 'entrar':
    if (r.ok && r.token) return responder(200, { ok: true, nome: r.nome }, COOKIE(r.token, 2592000));
    return responder(400, { ok: false, erro: r.erro || 'codigo_invalido' });
  case 'conta': {
    if (!r.ok) return responder(401, { ok: false, erro: 'sessao' }, COOKIE('', 0));
    const resposta = { ok: true, usuario: r.usuario, pagamentos: r.pagamentos || [] };
    if (r.interno && r.interno.assinatura) return out({ proximo: 'asaas_get', status: 200, resposta, caminho: '/subscriptions/' + r.interno.assinatura + '/payments?limit=6' });
    return responder(200, resposta);
  }
  case 'painel': {
    if (!r.ok) return responder(401, { ok: false, erro: 'sessao' }, COOKIE('', 0));
    const i = r.interno || {};
    return out({ proximo: 'dados', status: 200, autor: i.autor || '__sem_autor__', telefone: i.whatsapp || '__sem__', nome: (r.usuario || {}).primeiro_nome || '' });
  }
  case 'plano': {
    if (!r.ok) return responder(r.erro === 'sessao' ? 401 : 400, { ok: false, erro: r.erro });
    const confirmar = { rpc: 'dyno_site_plano', args: { p_token: p.token, p_ciclo: r.ciclo, p_confirmar: true } };
    if (r.assinatura) return out({ proximo: 'asaas_put', status: 200, resposta: { ok: true, ciclo: r.ciclo }, caminho: '/subscriptions/' + r.assinatura, corpo: { value: r.valor, cycle: r.ciclo, description: r.descricao, updatePendingPayments: true }, confirmar });
    return out(Object.assign({ proximo: 'rpc2', status: 200, resposta: { ok: true, ciclo: r.ciclo } }, confirmar));
  }
  case 'cancelar': {
    if (!r.ok) return responder(r.erro === 'sessao' ? 401 : 400, { ok: false, erro: r.erro });
    const confirmar = { rpc: 'dyno_site_cancelar', args: { p_token: p.token, p_confirmar: true } };
    if (r.assinatura) return out({ proximo: 'asaas_delete', status: 200, resposta: { ok: true }, caminho: '/subscriptions/' + r.assinatura, nome: r.nome, confirmar });
    return out(Object.assign({ proximo: 'rpc2', status: 200, resposta: { ok: true }, nome: r.nome }, confirmar));
  }
  case 'sair':
    return responder(200, { ok: true }, COOKIE('', 0));
}
return responder(400, { ok: false, erro: 'acao_invalida' });`
    }
  }
});

const rota = switchCase({
  version: 3.2,
  config: {
    name: 'Próximo passo',
    parameters: {
      rules: {
        values: [
          { outputKey: 'whatsapp', conditions: { options: { caseSensitive: true, leftValue: '', typeValidation: 'loose' }, conditions: [{ leftValue: expr('{{ $json.proximo }}'), operator: { type: 'string', operation: 'equals' }, rightValue: 'whatsapp' }], combinator: 'and' } },
          { outputKey: 'asaas_get', conditions: { options: { caseSensitive: true, leftValue: '', typeValidation: 'loose' }, conditions: [{ leftValue: expr('{{ $json.proximo }}'), operator: { type: 'string', operation: 'equals' }, rightValue: 'asaas_get' }], combinator: 'and' } },
          { outputKey: 'asaas_put', conditions: { options: { caseSensitive: true, leftValue: '', typeValidation: 'loose' }, conditions: [{ leftValue: expr('{{ $json.proximo }}'), operator: { type: 'string', operation: 'equals' }, rightValue: 'asaas_put' }], combinator: 'and' } },
          { outputKey: 'asaas_delete', conditions: { options: { caseSensitive: true, leftValue: '', typeValidation: 'loose' }, conditions: [{ leftValue: expr('{{ $json.proximo }}'), operator: { type: 'string', operation: 'equals' }, rightValue: 'asaas_delete' }], combinator: 'and' } },
          { outputKey: 'dados', conditions: { options: { caseSensitive: true, leftValue: '', typeValidation: 'loose' }, conditions: [{ leftValue: expr('{{ $json.proximo }}'), operator: { type: 'string', operation: 'equals' }, rightValue: 'dados' }], combinator: 'and' } },
          { outputKey: 'rpc2', conditions: { options: { caseSensitive: true, leftValue: '', typeValidation: 'loose' }, conditions: [{ leftValue: expr('{{ $json.proximo }}'), operator: { type: 'string', operation: 'equals' }, rightValue: 'rpc2' }], combinator: 'and' } }
        ]
      },
      options: { fallbackOutput: 'extra', renameFallbackOutput: 'responder' }
    }
  }
});

const enviarCodigo = node({
  type: 'n8n-nodes-base.httpRequest',
  version: 4.3,
  config: {
    name: 'Enviar código (Dyno)',
    onError: 'continueRegularOutput',
    parameters: {
      method: 'POST',
      url: 'https://wa.dynoapp.com.br/message/sendText/dyno',
      authentication: 'genericCredentialType',
      genericAuthType: 'httpHeaderAuth',
      sendBody: true,
      contentType: 'json',
      specifyBody: 'json',
      jsonBody: expr('{{ JSON.stringify($json.corpo) }}'),
      options: { timeout: 20000 }
    }
  }
});

const asaasHeaders = { parameters: [{ name: 'User-Agent', value: 'Dyno-Site' }] };

const asaasFaturas = node({
  type: 'n8n-nodes-base.httpRequest',
  version: 4.3,
  config: {
    name: 'Asaas: faturas',
    onError: 'continueRegularOutput',
    parameters: {
      method: 'GET',
      url: expr('{{ "' + ASAAS + '" + $json.caminho }}'),
      authentication: 'genericCredentialType',
      genericAuthType: 'httpHeaderAuth',
      sendHeaders: true,
      specifyHeaders: 'keypair',
      headerParameters: asaasHeaders,
      options: { timeout: 20000 }
    }
  }
});

const asaasPlano = node({
  type: 'n8n-nodes-base.httpRequest',
  version: 4.3,
  config: {
    name: 'Asaas: trocar plano',
    onError: 'continueRegularOutput',
    parameters: {
      method: 'PUT',
      url: expr('{{ "' + ASAAS + '" + $json.caminho }}'),
      authentication: 'genericCredentialType',
      genericAuthType: 'httpHeaderAuth',
      sendHeaders: true,
      specifyHeaders: 'keypair',
      headerParameters: asaasHeaders,
      sendBody: true,
      contentType: 'json',
      specifyBody: 'json',
      jsonBody: expr('{{ JSON.stringify($json.corpo) }}'),
      options: { timeout: 20000 }
    }
  }
});

const asaasCancelar = node({
  type: 'n8n-nodes-base.httpRequest',
  version: 4.3,
  config: {
    name: 'Asaas: cancelar assinatura',
    onError: 'continueRegularOutput',
    parameters: {
      method: 'DELETE',
      url: expr('{{ "' + ASAAS + '" + $json.caminho }}'),
      authentication: 'genericCredentialType',
      genericAuthType: 'httpHeaderAuth',
      sendHeaders: true,
      specifyHeaders: 'keypair',
      headerParameters: asaasHeaders,
      options: { timeout: 20000 }
    }
  }
});

const depoisAsaas = node({
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {
    name: 'Depois do Asaas',
    parameters: {
      mode: 'runOnceForAllItems',
      language: 'javaScript',
      jsCode: `const d = $('Decidir').first().json;
const a = $input.first().json || {};
const ok = d.proximo === 'asaas_delete' ? a.deleted === true : (!!a.id && !a.errors && !a.error);
if (!ok) return [{ json: { proximo: 'responder', acao: d.acao, status: 502, resposta: { ok: false, erro: 'cobranca' } } }];
return [{ json: Object.assign({}, d.confirmar, { proximo: 'rpc2', acao: d.acao, status: 200, resposta: d.resposta, nome: d.nome }) }];`
    }
  }
});

const confirmarBanco = ifElse({
  version: 2.2,
  config: {
    name: 'Confirmar no banco?',
    parameters: {
      conditions: {
        options: { caseSensitive: true, leftValue: '', typeValidation: 'loose' },
        conditions: [{ leftValue: expr('{{ $json.proximo }}'), operator: { type: 'string', operation: 'equals' }, rightValue: 'rpc2' }],
        combinator: 'and'
      }
    }
  }
});

const supabaseConfirmar = node({
  type: 'n8n-nodes-base.httpRequest',
  version: 4.3,
  config: {
    name: 'Supabase: confirmar',
    onError: 'continueRegularOutput',
    parameters: {
      method: 'POST',
      url: expr('{{ "' + SB + '" + $json.rpc }}'),
      authentication: 'genericCredentialType',
      genericAuthType: 'httpHeaderAuth',
      sendBody: true,
      contentType: 'json',
      specifyBody: 'json',
      jsonBody: expr('{{ JSON.stringify($json.args) }}'),
      options: { timeout: 15000 }
    }
  }
});

const foiCancelamento = ifElse({
  version: 2.2,
  config: {
    name: 'Foi cancelamento?',
    parameters: {
      conditions: {
        options: { caseSensitive: true, leftValue: '', typeValidation: 'loose' },
        conditions: [{ leftValue: expr("{{ $('Preparar').first().json.acao }}"), operator: { type: 'string', operation: 'equals' }, rightValue: 'cancelar' }],
        combinator: 'and'
      }
    }
  }
});

const avisarDaniel = node({
  type: 'n8n-nodes-base.httpRequest',
  version: 4.3,
  config: {
    name: 'Avisar Daniel (cancelamento)',
    onError: 'continueRegularOutput',
    parameters: {
      method: 'POST',
      url: 'https://wa.dynoapp.com.br/message/sendText/dyno',
      authentication: 'genericCredentialType',
      genericAuthType: 'httpHeaderAuth',
      sendBody: true,
      contentType: 'json',
      specifyBody: 'json',
      jsonBody: expr("{{ JSON.stringify({ number: '5511930851325', text: String.fromCharCode(8203) + '*Dyno (site):* ' + ($('Decidir').first().json.nome || 'um cliente') + ' cancelou a assinatura pela área do cliente.', delay: 300 }) }}"),
      options: { timeout: 20000 }
    }
  }
});

const dtOpts = (nome, id, tabela, conds, match) => node({
  type: 'n8n-nodes-base.dataTable',
  version: 1.1,
  config: {
    name: nome,
    executeOnce: true,
    alwaysOutputData: true,
    onError: 'continueRegularOutput',
    parameters: {
      resource: 'row',
      operation: 'get',
      dataTableId: { __rl: true, mode: 'id', value: id, cachedResultName: tabela },
      matchType: match || 'allConditions',
      filters: { conditions: conds },
      returnAll: true
    }
  }
});
const autorEq = { keyName: 'autor', condition: 'eq', keyValue: expr("{{ $('Decidir').first().json.autor }}") };

const dtTransacoes = dtOpts('Dados: transações', 'czjKVg7HFjMKNpAq', 'assessor_transacoes', [autorEq, { keyName: 'data', condition: 'gte', keyValue: expr('{{ $now.minus({ months: 7 }).startOf("month").toISO() }}') }]);
const dtTarefas = dtOpts('Dados: tarefas', 'LnRebLLXT3hHXXVT', 'assessor_tarefas', [autorEq]);
const dtLembretes = dtOpts('Dados: lembretes', 'bYVBca9uT849KhYP', 'assessor_lembretes', [autorEq, { keyName: 'telefone', condition: 'eq', keyValue: expr("{{ $('Decidir').first().json.telefone }}") }], 'anyCondition');
const dtContas = dtOpts('Dados: contas', 'EMXP62JHcMJtClgT', 'assessor_contas', [autorEq]);
const dtAssinaturas = dtOpts('Dados: assinaturas', 'BhTS13DGVIPZ39LS', 'assessor_assinaturas', [autorEq]);

const montarPainel = node({
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {
    name: 'Montar painel',
    parameters: {
      mode: 'runOnceForAllItems',
      language: 'javaScript',
      jsCode: `const TZ = 'America/Sao_Paulo';
const d = $('Decidir').first().json;
const linhas = (n) => { try { return $(n).all().map((i) => i.json).filter((r) => r && r.id !== undefined && r.id !== null); } catch (e) { return []; } };
const agora = DateTime.now().setZone(TZ);
const ini = agora.startOf('month');
const dt = (v) => { const x = DateTime.fromISO(String(v || '')); return x.isValid ? x.setZone(TZ) : null; };
const num = (v) => Number(v) || 0;
const BONITO = { alimentacao: 'Alimentação', educacao: 'Educação', saude: 'Saúde', vestuario: 'Vestuário', servicos: 'Serviços' };
const cat = (c) => { const k = String(c || 'outros').toLowerCase().trim(); return BONITO[k] || (k.charAt(0).toUpperCase() + k.slice(1)); };
const tx = linhas('Dados: transações').map((t) => ({ t, quando: dt(t.data || t.createdAt), v: num(t.valor) })).filter((x) => x.quando);
const doMes = tx.filter((x) => x.quando >= ini);
const gastos = doMes.filter((x) => x.t.tipo !== 'receita').reduce((s, x) => s + x.v, 0);
const receitas = doMes.filter((x) => x.t.tipo === 'receita').reduce((s, x) => s + x.v, 0);
const porCat = {};
doMes.filter((x) => x.t.tipo !== 'receita').forEach((x) => { const k = cat(x.t.categoria); porCat[k] = (porCat[k] || 0) + x.v; });
let categorias = Object.entries(porCat).sort((a, b) => b[1] - a[1]).map(([nome, valor]) => ({ nome, valor: Math.round(valor * 100) / 100 }));
if (categorias.length > 7) { const resto = categorias.slice(6).reduce((s, c) => s + c.valor, 0); categorias = categorias.slice(0, 6).concat([{ nome: 'Outras', valor: Math.round(resto * 100) / 100 }]); }
const meses = [];
for (let i = 5; i >= 0; i--) {
  const m = agora.minus({ months: i }).startOf('month');
  const f = m.endOf('month');
  const g = tx.filter((x) => x.t.tipo !== 'receita' && x.quando >= m && x.quando <= f).reduce((s, x) => s + x.v, 0);
  meses.push({ mes: m.setLocale('pt-BR').toFormat('LLL'), ano: m.year, gastos: Math.round(g * 100) / 100 });
}
const ultimos = tx.slice().sort((a, b) => b.quando - a.quando).slice(0, 12).map((x) => ({ data: x.quando.toISODate(), descricao: String(x.t.descricao || '').slice(0, 80), categoria: cat(x.t.categoria), valor: x.v, tipo: x.t.tipo === 'receita' ? 'receita' : 'despesa', forma: String(x.t.forma_pagamento || '').slice(0, 30) }));
const feita = (s) => /conclu|feit|done|ok|finaliz|cancel/i.test(String(s || ''));
const tarefas = linhas('Dados: tarefas').filter((t) => !feita(t.status)).map((t) => ({ titulo: String(t.titulo || '').slice(0, 120), prazo: t.prazo ? String(t.prazo).slice(0, 10) : null, prioridade: String(t.prioridade || ''), projeto: String(t.projeto || '') }))
  .sort((a, b) => String(a.prazo || '9999').localeCompare(String(b.prazo || '9999'))).slice(0, 15);
const lembretes = linhas('Dados: lembretes').filter((l) => !/conclu|feit|cancel|ok|pago/i.test(String(l.status || ''))).map((l) => ({ texto: String(l.texto || '').slice(0, 140), quando: String(l.proxima || l.quando || ''), recorrencia: String(l.recorrencia || '') }))
  .filter((l) => l.quando && l.quando >= agora.minus({ hours: 1 }).toUTC().toISO()).sort((a, b) => a.quando.localeCompare(b.quando)).filter((l, i, arr) => arr.findIndex((x) => x.texto === l.texto) === i).slice(0, 12);
const contas = linhas('Dados: contas').filter((c) => !/pag/i.test(String(c.status || ''))).map((c) => ({ descricao: String(c.descricao || c.beneficiario || 'Conta').slice(0, 80), valor: num(c.valor), vencimento: c.vencimento ? String(c.vencimento).slice(0, 10) : null }))
  .sort((a, b) => String(a.vencimento || '9999').localeCompare(String(b.vencimento || '9999'))).slice(0, 12);
const assin = linhas('Dados: assinaturas').filter((s) => s.ativo !== false).map((s) => ({ nome: String(s.nome || 'Assinatura').slice(0, 60), valor: num(s.valor), ciclo: String(s.ciclo || 'mensal'), proxima: s.proxima_cobranca ? String(s.proxima_cobranca).slice(0, 10) : null }));
const assinMensal = assin.reduce((s, a) => s + (a.ciclo === 'anual' ? a.valor / 12 : a.valor), 0);
const resposta = { ok: true, nome: d.nome, mes: agora.setLocale('pt-BR').toFormat('LLLL yyyy'),
  resumo: { gastos: Math.round(gastos * 100) / 100, receitas: Math.round(receitas * 100) / 100, saldo: Math.round((receitas - gastos) * 100) / 100, lancamentos: doMes.length, assinaturas_mes: Math.round(assinMensal * 100) / 100 },
  categorias, meses, ultimos, tarefas, lembretes, contas, assinaturas: assin.slice(0, 12),
  vazio: !tx.length && !tarefas.length && !lembretes.length && !contas.length };
return [{ json: { proximo: 'responder', acao: 'painel', status: 200, resposta } }];`
    }
  }
});

const montarResposta = node({
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {
    name: 'Montar resposta',
    parameters: {
      mode: 'runOnceForAllItems',
      language: 'javaScript',
      jsCode: `const pega = (n) => { try { return $(n).first().json; } catch (e) { return null; } };
let d = pega('Montar painel') || pega('Depois do Asaas') || pega('Decidir') || pega('Preparar') || {};
let status = d.status || 200;
let resposta = Object.assign({}, d.resposta || { ok: true });
let cookie = d.cookie || '';
const fat = pega('Asaas: faturas');
if (d.proximo === 'asaas_get' && fat) {
  resposta.faturas = (fat.data || []).map((x) => ({ valor: x.value, status: x.status, vencimento: x.dueDate, link: x.invoiceUrl }));
}
const conf = pega('Supabase: confirmar');
if (conf && (conf.ok === false || conf.code)) { status = 500; resposta = { ok: false, erro: 'indisponivel' }; }
if (d.proximo === 'whatsapp') { const w = pega('Enviar código (Dyno)') || {}; if (w.error) { status = 503; resposta = { ok: false, erro: 'whatsapp' }; } }
if (!cookie) cookie = 'dyno_v=1; Path=/; Max-Age=31536000; Secure; SameSite=Lax';
return [{ json: { status, corpo: resposta, cookie } }];`
    }
  }
});

const responder = node({
  type: 'n8n-nodes-base.respondToWebhook',
  version: 1.5,
  config: {
    name: 'Responder ao site',
    parameters: {
      respondWith: 'json',
      responseBody: expr('{{ JSON.stringify($json.corpo) }}'),
      options: {
        responseCode: expr('{{ $json.status }}'),
        responseHeaders: { entries: [ { name: 'Set-Cookie', value: expr('{{ $json.cookie }}') }, { name: 'Cache-Control', value: 'no-store' } ] }
      }
    }
  }
});

export default workflow('dyno-site-api', 'Dyno | API do site (área do cliente)')
  .add(entrada)
  .to(preparar)
  .to(precisaBanco
    .onTrue(supabaseRpc.to(decidir).to(rota
      .onCase(0, enviarCodigo.to(montarResposta))
      .onCase(1, asaasFaturas.to(montarResposta))
      .onCase(2, asaasPlano.to(depoisAsaas))
      .onCase(3, asaasCancelar.to(depoisAsaas))
      .onCase(4, dtTransacoes.to(dtTarefas).to(dtLembretes).to(dtContas).to(dtAssinaturas).to(montarPainel).to(montarResposta))
      .onCase(5, supabaseConfirmar)
      .onCase(6, montarResposta)))
    .onFalse(montarResposta))
  .add(depoisAsaas)
  .to(confirmarBanco.onTrue(supabaseConfirmar).onFalse(montarResposta))
  .add(supabaseConfirmar)
  .to(montarResposta)
  .add(supabaseConfirmar)
  .to(foiCancelamento.onTrue(avisarDaniel))
  .add(montarResposta)
  .to(responder);
