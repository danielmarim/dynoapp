# --- Página Funcionalidades (incluída pelo build.py) ---
# (categoria, voz, título, descrição, mensagem da pessoa, resposta)
FUNC_CATS = [
    ("gastos", "Gastos", "dyno"),
    ("contas", "Contas e assinaturas", "dyno"),
    ("parcelas", "Parcelados e a receber", "dyno"),
    ("extratos", "Extratos e faturas", "dyno"),
    ("limites", "Limites e relatórios", "dyno"),
    ("cambio", "Dólar e euro", "dyno"),
    ("lembretes", "Lembretes", "dina"),
    ("tarefas", "Tarefas, listas e notas", "dina"),
    ("rotina", "Rotina do dia", "dina"),
    ("casa", "Casa, carro e lugares", "dina"),
    ("conversa", "Do seu jeito", "ambos"),
    ("site", "Área do cliente", "ambos"),
    ("dados", "Seus dados", "ambos"),
]

FUNCS = [
    # Dyno — gastos
    ("gastos", "dyno", "Anote gastos e receitas em segundos", "Mande um texto, um áudio ou a foto do cupom. O Dyno entende o valor, escolhe a categoria e a forma de pagamento.", "uber 23 pra casa", "Anotado: R$ 23,00 em transporte 🚗"),
    ("gastos", "dyno", "Foto do comprovante vira lançamento", "Fotografe o cupom ou mande o comprovante do Pix. O Dyno lê, registra e guarda o arquivo junto com o gasto.", "📷 [foto do cupom do mercado]", "R$ 187,40 no Mercado Bom Preço, em mercado. Comprovante guardado ✅"),
    ("gastos", "dyno", "Errou? Corrige ou desfaz", "Edite ou desfaça o último lançamento das últimas 24 horas, ou peça para apagar um gasto específico.", "na verdade foram 32, não 23", "Corrigido: o Uber agora é R$ 32,00."),
    ("gastos", "dyno", "Pergunte sobre o seu dinheiro", "Quanto gastou com mercado, onde mais gastou, cartão ou Pix: é só perguntar como se fosse para uma pessoa.", "quanto gastei com delivery esse mês?", "R$ 312,50 em 9 pedidos. É 18% a mais que no mês passado."),
    # Dyno — contas e assinaturas
    ("contas", "dyno", "Contas a pagar sem esquecer", "Cadastre a conta com valor e vencimento, ou mande a foto do boleto. O Dyno avisa antes e no dia, e insiste até você responder “paguei”.", "📄 [boleto da internet]", "Internet R$ 119,90, vence dia 15. Aviso no dia 12 e no dia 15 🔔"),
    ("contas", "dyno", "Pagou? É só avisar", "Responda “paguei” ou envie o comprovante: a conta é marcada como paga e os avisos param.", "paguei a luz", "Conta de luz marcada como paga ✅"),
    ("contas", "dyno", "Assinaturas sob controle", "Netflix, academia, streaming: veja quanto tudo soma por mês e receba aviso antes da próxima cobrança.", "quanto pago de assinaturas?", "4 assinaturas, R$ 118,60 por mês. A próxima é a academia, dia 20."),
    # Dyno — parcelados e a receber
    ("parcelas", "dyno", "Compras parceladas e gastos fixos", "Parcelado em até 60 vezes ou gasto que se repete todo mês: o Dyno lança cada parcela no dia certo, sozinho.", "notebook 12x de 250 no cartão", "Parcelado criado: 12x de R$ 250,00. Lanço uma por mês 💳"),
    ("parcelas", "dyno", "Quem te deve", "Anote o que emprestou ou vendeu fiado, dê baixa quando pagarem (até em partes) e pergunte quem ainda deve.", "o João me pagou 100 dos 300", "Baixa feita. O João ainda deve R$ 200,00."),
    ("parcelas", "dyno", "Clientes e fornecedores", "Para quem trabalha por conta: cadastre clientes e pergunte quanto recebeu de cada um no período.", "quanto recebi da Ótica Vieira esse mês?", "R$ 1.450,00 em 3 pagamentos da Ótica Vieira."),
    # Dyno — extratos
    ("extratos", "dyno", "Importe o extrato do banco", "Mande o extrato ou a fatura em PDF, CSV, OFX ou Excel com a legenda “extrato”. Funciona até com o print do app salvo como PDF.", "📎 Extrato setembro.pdf — extrato", "Achei 31 lançamentos: R$ 797,62 de gastos e R$ 203,55 de entradas. Responda IMPORTAR para salvar."),
    ("extratos", "dyno", "Sem lançamento repetido", "O Dyno marca o que você já tinha anotado e ignora saldo, pagamento de fatura e transferência entre suas contas. Só grava depois do seu ok.", "IMPORTAR", "Pronto! 28 lançamentos novos salvos e 3 duplicados ignorados."),
    # Dyno — limites e relatórios
    ("limites", "dyno", "Limite por categoria", "Defina quanto quer gastar em cada categoria. O Dyno avisa quando estiver chegando perto e quando passar.", "no máximo 800 em mercado por mês", "Limite criado. Hoje você está em R$ 496,00 (62%)."),
    ("limites", "dyno", "Resumo do dia às 21h", "Todo fim de dia chega o resumo: gastos com total, entradas, lembretes feitos e o que ficou pendente.", "", "Hoje: 4 gastos, R$ 126,30. Maior: mercado R$ 74,10. Faltou registrar algo?"),
    ("limites", "dyno", "Painel em imagem e planilha", "Peça um painel com gastos por categoria, cartão × Pix e assinaturas, ou a planilha Excel do período.", "me manda o painel do mês", "📊 [imagem do painel] Mercado lidera com 31% dos gastos."),
    # Dyno — câmbio
    ("cambio", "dyno", "Cotação na hora", "Pergunte o dólar ou o euro e receba a cotação atualizada, com a variação dos últimos 30 dias.", "quanto tá o dólar?", "R$ 4,98 agora. Nos últimos 30 dias variou de R$ 4,96 a R$ 5,24."),
    ("cambio", "dyno", "Alerta de dólar e euro", "Peça para ser avisado quando a moeda passar de um valor. A cotação é conferida a cada 15 minutos em dias úteis. Só informamos, não é recomendação de investimento.", "me avisa quando o dólar ficar abaixo de 4,90", "Combinado! Te aviso uma vez quando passar desse valor 💵"),
    # Dina — lembretes
    ("lembretes", "dina", "Lembretes que insistem", "Se você não responder “ok”, a Dina lembra de novo a cada 30 minutos e apaga o aviso anterior, para não lotar a sua conversa. Quer mais tempo? “adiar 60”.", "me lembra de ligar pro médico às 15h", "Combinado ⏰ Às 15h eu te lembro, e insisto até você confirmar."),
    ("lembretes", "dina", "Do jeito que você fala", "“Amanhã cedo”, “daqui 20 minutos”, “toda segunda às 7h”, “dia 10 de todo mês”: lembretes únicos ou que se repetem.", "toda segunda às 7h academia", "Feito! Toda segunda, às 7h, eu te chamo 💪"),
    ("lembretes", "dina", "Ela organiza o recado longo", "Cole uma confirmação de reserva ou um recado comprido. A Dina encontra as datas e sugere os lembretes.", "[mensagem da reserva do Airbnb]", "Quer que eu lembre do check-in dia 07/10 às 15h e do check-out dia 09/10 às 12h?"),
    # Dina — tarefas, listas, notas
    ("tarefas", "dina", "Tarefas com prazo e projeto", "Crie tarefas com prioridade, prazo e projeto. Pergunte o que está atrasado e receba aviso das pendências.", "tarefa: enviar orçamento pro cliente até sexta, projeto obra", "Anotado no projeto obra, prazo sexta 📋"),
    ("tarefas", "dina", "Listas de compras", "Monte listas e vá adicionando ou tirando itens pelo caminho. Peça a lista quando chegar no mercado.", "coloca leite, café e pão na lista", "Lista de mercado: leite, café, pão. Mais alguma coisa?"),
    ("tarefas", "dina", "Notas e ideias com busca", "Guarde ideias e anotações soltas e encontre depois pelo assunto.", "o que eu anotei sobre a viagem?", "2 notas: hotel em Gramado e a ideia de ir de carro."),
    # Dina — rotina
    ("rotina", "dina", "Bom dia com o seu dia", "Às 7h30 chega o resumo: lembretes de hoje, contas que vencem e tarefas do dia ou atrasadas.", "", "Bom dia! Hoje: dentista 14h, conta de água vence e 2 tarefas pendentes ☀️"),
    ("rotina", "dina", "Check-ins ao longo do dia", "No meio da manhã e da tarde a Dina pergunta se faltou registrar algo. Se você já falou com ela, ela não incomoda.", "", "Esqueceu de registrar algum gasto ou compromisso? 😉"),
    # Dina — casa, carro, lugares
    ("casa", "dina", "Manutenção da casa e do carro", "Troca de óleo, revisão, filtro de água, dedetização: a Dina avisa com antecedência e acompanha a quilometragem do carro.", "troquei o óleo hoje com 42.300 km", "Anotado! Próxima troca com 52.300 km ou em 6 meses 🚗"),
    ("casa", "dina", "Lugares perto de você", "Mande sua localização e pergunte por farmácia, posto ou restaurante aberto por perto.", "📍 [localização] farmácia aberta perto?", "Achei 3 farmácias perto. A mais próxima fica a 400 m 📍"),
    ("casa", "dina", "Pesquisa rápida", "Precisa de uma informação atual? Pergunte e a Dina pesquisa na internet e resume.", "que horas abre o Poupatempo amanhã?", "Abre às 8h e fecha às 17h. Precisa de agendamento."),
    # Ambos — conversa
    ("conversa", "ambos", "Texto, áudio ou foto", "Fale como preferir. Áudio é transcrito, foto e PDF são lidos. Tudo no WhatsApp, sem baixar aplicativo.", "🎤 [áudio de 15 segundos]", "Entendi: gasto de R$ 60 na farmácia e lembrete do remédio às 22h ✅"),
    ("conversa", "ambos", "Várias coisas numa mensagem", "Num recado só você registra um gasto, cria um lembrete e adiciona algo na lista.", "gastei 30 no almoço e me lembra de pagar a luz amanhã", "R$ 30 em alimentação 🍽️ e lembrete da luz amanhã às 9h ⏰"),
    ("conversa", "ambos", "Eles lembram de você", "Conte suas preferências uma vez (“sou vegetariano”, “recebo dia 5”) e eles levam isso em conta nas respostas.", "lembra que eu recebo todo dia 5", "Guardado! Vou considerar isso nos seus resumos do mês."),
    # Ambos — site
    ("site", "ambos", "Painel no site", "Entre em dynoapp.com.br com um código enviado pelo WhatsApp, sem senha: gastos do mês, categorias, limites, contas e lembretes.", "", ""),
    ("site", "ambos", "Extrato e comprovantes", "Filtre lançamentos por período, categoria e pagamento, exporte para planilha e baixe os comprovantes (até em .zip).", "", ""),
    # Ambos — dados
    ("dados", "ambos", "Baixe seus dados", "Peça uma cópia de tudo o que está guardado sobre você e receba pelo WhatsApp.", "quero baixar meus dados", "Estou preparando sua cópia. Te envio aqui em instantes 📦"),
    ("dados", "ambos", "Apague quando quiser", "Seus dados são seus: peça a exclusão a qualquer momento, com confirmação para evitar acidentes. O Dyno nunca acessa sua conta no banco nem faz pagamentos.", "apagar meus dados", "Para confirmar, responda exatamente: CONFIRMO APAGAR MEUS DADOS"),
]

VOZ_NOME = {"dyno": "Dyno", "dina": "Dina", "ambos": "Dyno &amp; Dina"}


def func_card(c, voz, t, d, me, bot):
    chat = ""
    if me or bot:
        cls = "b dy dina" if voz == "dina" else "b dy"
        quem = "Dina" if voz == "dina" else "Dyno"
        chat = '<div class="mini">' + (f'<div class="b me">{me}</div>' if me else "") + (f'<div class="{cls}"><small>{quem}</small>{bot}</div>' if bot else "") + "</div>"
    return f'<article class="fcard" data-cat="{c}"><span class="tag tag-{voz}">{VOZ_NOME[voz]}</span><h3>{t}</h3><p>{d}</p>{chat}</article>'


def func_body():
    n = len(FUNCS)
    chips = '<button class="chip on" data-f="tudo" aria-pressed="true">Tudo <span>{}</span></button>'.format(n)
    for k, nome, voz in FUNC_CATS:
        q = sum(1 for f in FUNCS if f[0] == k)
        chips += f'<button class="chip chip-{voz}" data-f="{k}" aria-pressed="false">{nome} <span>{q}</span></button>'
    blocos = ""
    for grupo, titulo, sub in (("dyno", "💰 Dyno · o seu dinheiro", "Gastos, contas, extratos, limites e relatórios."), ("dina", "⏰ Dina · a sua agenda e rotina", "Lembretes, tarefas, listas e o dia organizado."), ("ambos", "Os dois · do seu jeito", "Como você conversa, o painel no site e os seus dados.")):
        secs = ""
        for k, nome, voz in FUNC_CATS:
            if voz != grupo:
                continue
            cards = "".join(func_card(*f) for f in FUNCS if f[0] == k)
            secs += f'<div class="fsec" data-sec="{k}"><h3 class="fsec-t">{nome}</h3><div class="fgrid">{cards}</div></div>'
        blocos += f'<div class="fgrupo" data-grupo="{grupo}"><div class="fg-head"><h2 class="h">{titulo}</h2><p>{sub}</p></div>{secs}</div>'
    return f"""<section class="hero-f"><div class="wrap">
  <span class="kicker">Funcionalidades</span>
  <h1 class="h">Tudo o que o Dyno e a Dina sabem fazer.</h1>
  <p class="lead">Dois assessores no mesmo WhatsApp: o Dyno cuida do dinheiro e a Dina, da agenda e da rotina. São {n} funcionalidades, organizadas por assunto. Filtre pelo que te interessa ou leia tudo.</p>
</div></section>
<div class="chips-bar"><div class="wrap"><div class="chips" role="toolbar" aria-label="Filtrar funcionalidades">{chips}</div></div></div>
<section style="padding-top:28px"><div class="wrap">{blocos}</div></section>
<section style="padding-top:0"><div class="wrap"><div class="card fcta">
  <div><h2 class="h" style="margin:0 0 8px">Quer testar tudo isso?</h2><p>Beta fechado: 60 dias grátis em troca do seu feedback. Depois, R$ 19,90 por mês, sem fidelidade.</p></div>
  <div class="cta-row"><a class="btn btn-primary" href="/beta">Começar agora →</a><a class="btn btn-ghost" href="/duvidas">Tirar dúvidas</a></div>
</div></div></section>"""


FUNCJS = """<script>
(function(){
  var chips=document.querySelectorAll('.chip'),secs=document.querySelectorAll('.fsec'),grupos=document.querySelectorAll('.fgrupo');
  function aplicar(f){
    chips.forEach(function(c){var on=c.getAttribute('data-f')===f;c.classList.toggle('on',on);c.setAttribute('aria-pressed',on);});
    secs.forEach(function(s){s.hidden=!(f==='tudo'||s.getAttribute('data-sec')===f);});
    grupos.forEach(function(g){g.hidden=!g.querySelector('.fsec:not([hidden])');});
    if(history.replaceState)history.replaceState(null,'',f==='tudo'?location.pathname:'#'+f);
  }
  chips.forEach(function(c){c.addEventListener('click',function(){aplicar(c.getAttribute('data-f'));var b=document.querySelector('.chips-bar');window.scrollTo({top:b.offsetTop-70,behavior:'smooth'});});});
  var h=location.hash.replace('#','');if(h&&document.querySelector('.fsec[data-sec="'+h+'"]'))aplicar(h);
})();
</script>"""
