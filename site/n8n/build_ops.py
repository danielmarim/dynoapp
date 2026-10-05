import re, json
src = open('api.js').read()
secret = open('/home/claude/dyno-site/.proxy_secret').read().strip()
codes = {}
for m in re.finditer(r"name: '([^']+)',\s*parameters: \{\s*mode: 'runOnceForAllItems',\s*language: 'javaScript',\s*jsCode: `(.*?)`\s*\}", src, re.S):
    codes[m.group(1)] = m.group(2).replace('\\\\', '\\').replace('__SEGREDO__', secret)
assert set(codes) == {'Preparar','Decidir','Depois do Asaas','Montar painel','Montar resposta'}, codes.keys()
SB = 'https://xvekgnbneeokihtjpbts.supabase.co/rest/v1/rpc/'
AS = 'https://api.asaas.com/v3'
SUPA = {'httpHeaderAuth': {'id': 'qgXgW9Cfnyoli06W', 'name': 'Supabase_Dyno'}}
ASAAS = {'httpHeaderAuth': {'id': 'l3GO5H4hRL8ca2k3', 'name': 'asaas-prod'}}
EVO = {'httpHeaderAuth': {'id': 'l2BZVdQJowvQuT6M', 'name': 'evolution-dyno'}}
UA = {'parameters': [{'name': 'User-Agent', 'value': 'Dyno-Site'}]}
nodes = []
def add(name, typ, ver, params, pos, cred=None, **settings):
    n = {'name': name, 'type': typ, 'typeVersion': ver, 'parameters': params, 'position': pos}
    if cred: n['credentials'] = cred
    nodes.append((n, settings))
def code(name, pos): add(name, 'n8n-nodes-base.code', 2, {'mode': 'runOnceForAllItems', 'language': 'javaScript', 'jsCode': codes[name]}, pos)
def cond(left, val): return {'conditions': {'options': {'caseSensitive': True, 'leftValue': '', 'typeValidation': 'loose'}, 'conditions': [{'leftValue': left, 'operator': {'type': 'string', 'operation': 'equals'}, 'rightValue': val}], 'combinator': 'and'}}
def http(name, method, url, pos, cred, body=None, ua=False):
    p = {'method': method, 'url': url, 'authentication': 'genericCredentialType', 'genericAuthType': 'httpHeaderAuth', 'options': {'timeout': 20000}}
    if ua: p.update({'sendHeaders': True, 'specifyHeaders': 'keypair', 'headerParameters': UA})
    if body: p.update({'sendBody': True, 'contentType': 'json', 'specifyBody': 'json', 'jsonBody': body})
    add(name, 'n8n-nodes-base.httpRequest', 4.3, p, pos, cred, onError='continueRegularOutput')
code('Preparar', [240, 300])
add('Precisa do banco?', 'n8n-nodes-base.if', 2.2, cond('={{ $json.proximo }}', 'rpc'), [480, 300])
http('Supabase: RPC', 'POST', '={{ "' + SB + '" + $json.rpc }}', [720, 200], SUPA, '={{ JSON.stringify($json.args) }}')
code('Decidir', [960, 200])
keys = ['whatsapp', 'asaas_get', 'asaas_put', 'asaas_delete', 'dados', 'rpc2']
add('Próximo passo', 'n8n-nodes-base.switch', 3.2, {'rules': {'values': [dict(outputKey=k, renameOutput=True, conditions=cond('={{ $json.proximo }}', k)['conditions']) for k in keys]}, 'options': {'fallbackOutput': 'extra', 'renameFallbackOutput': 'responder'}}, [1200, 200])
http('Enviar código (Dyno)', 'POST', 'https://wa.dynoapp.com.br/message/sendText/dyno', [1500, -100], EVO, '={{ JSON.stringify($json.corpo) }}')
http('Asaas: faturas', 'GET', '={{ "' + AS + '" + $json.caminho }}', [1500, 40], ASAAS, ua=True)
http('Asaas: trocar plano', 'PUT', '={{ "' + AS + '" + $json.caminho }}', [1500, 180], ASAAS, '={{ JSON.stringify($json.corpo) }}', ua=True)
http('Asaas: cancelar assinatura', 'DELETE', '={{ "' + AS + '" + $json.caminho }}', [1500, 320], ASAAS, ua=True)
code('Depois do Asaas', [1740, 250])
add('Confirmar no banco?', 'n8n-nodes-base.if', 2.2, cond('={{ $json.proximo }}', 'rpc2'), [1980, 250])
http('Supabase: confirmar', 'POST', '={{ "' + SB + '" + $json.rpc }}', [2220, 400], SUPA, '={{ JSON.stringify($json.args) }}')
add('Foi cancelamento?', 'n8n-nodes-base.if', 2.2, cond("={{ $('Preparar').first().json.acao }}", 'cancelar'), [2460, 560])
http('Avisar Daniel (cancelamento)', 'POST', 'https://wa.dynoapp.com.br/message/sendText/dyno', [2700, 560], EVO,
     "={{ JSON.stringify({ number: '5511930851325', text: String.fromCharCode(8203) + '*Dyno (site):* ' + ($('Decidir').first().json.nome || 'um cliente') + ' cancelou a assinatura pela área do cliente.', delay: 300 }) }}")
def dt(name, id, tabela, conds, pos, match='allConditions'):
    add(name, 'n8n-nodes-base.dataTable', 1.1, {'resource': 'row', 'operation': 'get', 'dataTableId': {'__rl': True, 'mode': 'id', 'value': id, 'cachedResultName': tabela}, 'matchType': match, 'filters': {'conditions': conds}, 'returnAll': True}, pos, executeOnce=True, alwaysOutputData=True, onError='continueRegularOutput')
autor = {'keyName': 'autor', 'condition': 'eq', 'keyValue': "={{ $('Decidir').first().json.autor }}"}
dt('Dados: transações', 'czjKVg7HFjMKNpAq', 'assessor_transacoes', [autor, {'keyName': 'data', 'condition': 'gte', 'keyValue': '={{ $now.minus({ months: 7 }).startOf("month").toISO() }}'}], [1500, 520])
dt('Dados: tarefas', 'LnRebLLXT3hHXXVT', 'assessor_tarefas', [autor], [1700, 520])
dt('Dados: lembretes', 'bYVBca9uT849KhYP', 'assessor_lembretes', [autor, {'keyName': 'telefone', 'condition': 'eq', 'keyValue': "={{ $('Decidir').first().json.telefone }}"}], [1900, 520], 'anyCondition')
dt('Dados: contas', 'EMXP62JHcMJtClgT', 'assessor_contas', [autor], [2100, 520])
dt('Dados: assinaturas', 'BhTS13DGVIPZ39LS', 'assessor_assinaturas', [autor], [2300, 520])
code('Montar painel', [2500, 520])
code('Montar resposta', [2760, 200])
add('Responder ao site', 'n8n-nodes-base.respondToWebhook', 1.5, {'respondWith': 'json', 'responseBody': '={{ JSON.stringify($json.corpo) }}', 'options': {'responseCode': '={{ $json.status }}', 'responseHeaders': {'entries': [{'name': 'Set-Cookie', 'value': '={{ $json.cookie }}'}, {'name': 'Cache-Control', 'value': 'no-store'}]}}}, [3000, 200])
C = [('Site: requisição',0,'Preparar'),('Preparar',0,'Precisa do banco?'),('Precisa do banco?',0,'Supabase: RPC'),('Precisa do banco?',1,'Montar resposta'),
 ('Supabase: RPC',0,'Decidir'),('Decidir',0,'Próximo passo'),
 ('Próximo passo',0,'Enviar código (Dyno)'),('Próximo passo',1,'Asaas: faturas'),('Próximo passo',2,'Asaas: trocar plano'),('Próximo passo',3,'Asaas: cancelar assinatura'),('Próximo passo',4,'Dados: transações'),('Próximo passo',5,'Supabase: confirmar'),('Próximo passo',6,'Montar resposta'),
 ('Enviar código (Dyno)',0,'Montar resposta'),('Asaas: faturas',0,'Montar resposta'),('Asaas: trocar plano',0,'Depois do Asaas'),('Asaas: cancelar assinatura',0,'Depois do Asaas'),
 ('Depois do Asaas',0,'Confirmar no banco?'),('Confirmar no banco?',0,'Supabase: confirmar'),('Confirmar no banco?',1,'Montar resposta'),
 ('Supabase: confirmar',0,'Montar resposta'),('Supabase: confirmar',0,'Foi cancelamento?'),('Foi cancelamento?',0,'Avisar Daniel (cancelamento)'),
 ('Dados: transações',0,'Dados: tarefas'),('Dados: tarefas',0,'Dados: lembretes'),('Dados: lembretes',0,'Dados: contas'),('Dados: contas',0,'Dados: assinaturas'),('Dados: assinaturas',0,'Montar painel'),('Montar painel',0,'Montar resposta'),
 ('Montar resposta',0,'Responder ao site')]
ops = []
for n, s in nodes:
    ops.append({'type': 'addNode', 'node': n})
    if s: ops.append({'type': 'setNodeSettings', 'nodeName': n['name'], 'settings': s})
for a, i, b in C: ops.append({'type': 'addConnection', 'source': a, 'sourceIndex': i, 'target': b})
ops.append({'type': 'setWorkflowSettings', 'settings': {'saveDataSuccessExecution': 'none', 'saveDataErrorExecution': 'none', 'errorWorkflow': '5UUmuzItIYDsd3AG', 'executionOrder': 'v1'}})
json.dump(ops, open('/tmp/claude-0/-home-claude/1ea3cd61-3ac0-5c2a-b188-77899c5fc2c6/scratchpad/ops.json', 'w'), ensure_ascii=False)
print(len(ops), len(json.dumps(ops)))
