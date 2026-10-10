exec(open('/home/claude/videos/_dark/sfx_base.py').read())
# 01 hook: marca + tags
EV = [(0.3, pop, 0.7), (0.6, thump, 0.6)] + [(1.35 + k * 0.16, pop, 0.7) for k in range(5)]
# 02 remédio: mensagens (sent = enviada pela pessoa, ping = chegou do Dyno)
EV += [(3.4, sent, 0.8), (4.3, sent, 0.9), (5.2, ping, 1.0), (6.2, ping, 1.0), (7.4, sent, 0.9), (8.1, ping, 1.0)]
# 03 fatura
EV += [(9.0, thump, 0.8), (9.9, sent, 0.9), (10.9, ping, 1.0), (12.9, sent, 0.9), (13.6, ping, 1.0)]
# 04 gasto: barras + alerta
EV += [(14.4, sent, 0.8), (15.4, pop, 0.6), (15.6, pop, 0.6), (16.6, ping, 1.1), (17.8, sent, 0.9), (18.4, ping, 1.0)]
# 05 personalidades: pills, toque, mensagem, áudio
EV += [(19.0, thump, 0.8)] + [(19.6 + k * 0.12, pop, 0.6) for k in range(5)] + [(21.1, click, 1.0), (21.7, ping, 1.0), (22.6, ping, 0.9)]
# 06 cta
EV += [(24.4, sent, 0.8), (25.4, thump, 1.0), (28.0, ping, 0.7)]
TOTAL = 29.0
out = np.zeros(int(SR * TOTAL))
for t0, fn, g in EV:
    s = fn() * g; i = int(t0 * SR)
    if i < len(out): out[i:i + len(s)] += s[:len(out) - i]
out = np.clip(out * 0.7, -1, 1)
w = wave.open('assets/sfx/sfx-mix.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((out * 32767).astype(np.int16).tobytes()); w.close()
