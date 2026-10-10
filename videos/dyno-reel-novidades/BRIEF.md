---
workflow: general-video
flow: automation
storyboard: no
message: "Cinco funções novas no Dyno: remédio com confirmação, fatura com parcelas, aviso de gasto fora do normal, personalidades e voz no mesmo tom."
destination: instagram-reels
aspect: 1080x1920
language: pt-BR
audience: "Seguidores do @dynoapp.ia e interessados no Beta"
length: 29s
angle: tour rápido das 5 novidades de 07/10, uma cena por função, em conversas de WhatsApp simuladas, fechando com CTA
narration: no
music: "nova trilha (HeyGen catálogo e664828c): synth-pop energético com guitarra elétrica, 30 s — diferente da trilha lo-fi usada nos reels anteriores"
---

## Intent

Reel de novidades (07/10/2026). Mostra as cinco funções lançadas hoje, cada uma como uma mini-conversa no WhatsApp: (1) lembrete de remédio que pergunta "já tomou?" e registra o "sim"; (2) fatura do cartão por foto ou PDF, com parcelas separadas e o que ainda falta pagar; (3) aviso quando um gasto foge do normal; (4) personalidades do assistente (padrão, zen, profissional, coach, extrovertido); (5) resposta por áudio no tom da personalidade. Fecha com "Tudo isso já está no seu WhatsApp" e o CTA dynoapp.com.br.

## Customizations

- Estilo do site dynoapp.com.br (tema escuro): fundo #060A13, verde #2FD47E, Bricolage Grotesque + Figtree + JetBrains Mono, grade de pontos verde, celular escuro — mesma base dos reels de 06/10 (`_dark/base_dark.py`).
- Trilha nova pedida pelo Daniel: não reutilizar `dyno-bgm.wav`.
- Efeitos sonoros sintetizados (`_dark/sfx_base.py`).

## Notes

- Nomes, valores e remédios são fictícios/ilustrativos. Nada de orientação médica: o Dyno só lembra e registra.
- Preços não aparecem (mudaram hoje); o CTA fala só em "Beta · 60 dias grátis".
- Usage do HyperFrames: `usage --json` devolveu status unknown (auth não suportada), então o consumo não foi verificado.
