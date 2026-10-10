# Dyno e Dina — o que já temos e o que falta (06/10/2026)

Fonte: aba Funcionalidades do site (35 funções), documentação técnica e workflows ativos. Esta lista substitui a tabela de 13 ideias do documento "Dyno e Dina — o que fazem e o que falta".

## O que já está implementado

### Dyno 💰 (dinheiro)
- Gastos e receitas por texto, áudio, foto de comprovante ou PDF; várias ações numa só mensagem.
- Corrigir ou desfazer o último lançamento; perguntas sobre o dinheiro ("quanto gastei com mercado?").
- Contas a pagar com aviso 3 dias antes e no dia, com insistência; "paguei" ou comprovante dá baixa, lança a despesa e cria a conta do mês seguinte.
- Assinaturas: total mensal e anual, aviso 2 dias antes da renovação.
- Parcelados (até 60x) e gastos fixos, lançados sozinhos no dia certo.
- Recebíveis ("quem me deve", baixa parcial) e cadastro de clientes e fornecedores.
- Importação de extrato e fatura (PDF, CSV, OFX, Excel e print salvo em PDF), sem duplicar, só grava após IMPORTAR.
- Limite por categoria com alertas em 80% e 100%.
- Resumo das 21h, painel em imagem e planilha Excel por período.
- Câmbio: cotação do dólar e do euro na hora e alerta por valor (só informa, sem recomendação).

### Dina ⏰ (agenda e rotina)
- Lembretes em linguagem natural, únicos ou recorrentes; se não houver "ok", insiste a cada 30 min (até 6 vezes) e apaga o aviso anterior; "adiar 60", "paguei" e "ok" funcionam.
- Organiza um recado longo (reserva, convite) e sugere os lembretes.
- Tarefas com prazo, prioridade e projeto; aviso diário das atrasadas.
- Listas de compras, notas e ideias com busca por assunto.
- Bom dia às 7h30, check-ins às 10h e 14h12, relatórios das 12h e 18h; mensagem das 6h do grupo da família.
- Card semanal em imagem no domingo às 20h (hoje só a família).
- Manutenção da casa e do carro, com quilometragem; lugares perto (Google Places) e pesquisa rápida na web.

### Comum aos dois
- Memória das últimas 60 mensagens e de fatos salvos; isolamento por cliente (número do WhatsApp) no Supabase.
- Painel do cliente no site (extrato, comprovantes, limites), LGPD pelo WhatsApp (baixar e apagar meus dados).

### Plataforma
- Cadastro por convite, Beta de 10 vagas, cobrança no Asaas sem boleto no cadastro, área do cliente, modo administrador.
- Site com aba Funcionalidades e menu próprio para quem está logado.
- IA em camadas (OpenAI, Claude para documentos, Jev em modo sombra) com custo medido.
- Backup diário no Drive, monitor de saúde a cada 5 min, alertas de erro, 24 workflows exportados no git.

## Roadmap de funções (atualizado)

| Ordem | Ideia | Voz | Esforço | Situação |
| --- | --- | --- | --- | --- |
| 1 | Card semanal para todos os clientes | Dina | 2 horas | Não iniciado; a função existe, falta liberar além da família |
| 2 | Editar e apagar qualquer item pelo WhatsApp | Os dois | 1 dia | Parcial: desfazer e editar o último lançamento, editar e cancelar contas e assinaturas, adiar e confirmar lembretes. Falta lembrete, tarefa e nota |
| 3 | Previsão do mês | Dyno | 1 dia | Não iniciado |
| 4 | Cartão de crédito com fechamento e vencimento | Dyno | 1–2 dias | Não iniciado |
| 5 | Categorias próprias e aprender com correções | Dyno | 1 dia | Não iniciado |
| 6 | Metas de economia | Dyno | 1 dia | Não iniciado |
| 7 | Agenda simples no Supabase | Dina | 2 dias | Não iniciado |
| 8 | Boas-vindas guiadas nos 7 primeiros dias | Os dois | 1 dia | Não iniciado; o texto precisa de aprovação do Daniel |
| 9 | Editar no painel do site | Os dois | 1–2 dias | Não iniciado |
| 10 | Modo casal/família opcional | Os dois | 2–3 dias | Não iniciado |
| 11 | Memória por assunto (pgvector) | Os dois | 2 dias | Não iniciado |
| 12 | Google Agenda | Dina | 2 dias | Aguarda a autorização da conta Google de cada cliente |
| 13 | Áudio longo e arquivo de áudio (ata) | Dina | 2–3 dias | Adiado por decisão do Daniel (05/10) |

A ordem mudou: o card semanal sobe por custar 2 horas, e a edição pelo WhatsApp vem logo depois porque o erro corrigido na hora evita o cliente desistir.

## O que mudou desde o documento anterior
- Dados no Supabase: mensagens, memórias, transações, tarefas, lembretes, contas, orçamentos e assinaturas, ligados ao número do cliente. Faltam manutenções, veículos, rotina, extras e devocional (ainda no n8n).
- Lembretes: a cada 30 min, apagando o aviso anterior sem resposta.
- Extrato: lê print de app salvo como PDF (corta em fatias).
- Operação: workflows do Dyno exportados para o git; número pessoal do Daniel desligado do Assessor.
