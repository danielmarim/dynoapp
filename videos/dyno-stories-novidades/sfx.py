exec(open('/home/claude/videos/_dark/sfx_base.py').read())
EV = [(0.2, thump, 0.8), (0.7, pop, 0.7), (2.6, sent, 0.8)]
EV += [(3.3 + k * 1.5, pop, 0.7) for k in range(5)] + [(3.95 + k * 1.5, ping, 0.9) for k in range(5)]
EV += [(11.8, sent, 0.8), (12.8, thump, 1.0)]
TOTAL = 14.0
out = np.zeros(int(SR * TOTAL))
for t0, fn, g in EV:
    s = fn() * g; i = int(t0 * SR)
    if i < len(out): out[i:i + len(s)] += s[:len(out) - i]
out = np.clip(out * 0.7, -1, 1)
w = wave.open('assets/sfx/sfx-mix.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((out * 32767).astype(np.int16).tobytes()); w.close()
