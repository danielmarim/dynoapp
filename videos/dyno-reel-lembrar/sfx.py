exec(open('/home/claude/videos/_dark/sfx_base.py').read())
EV=[(0.3,pop,0.7),(1.0,pop,0.7),(2.4,thump,0.8)]+[(2.9+k*0.16,flick,0.5) for k in range(8)]
EV+=[(4.1,sent,0.8),(5.2,sent,1),(6.6,ping,1),(7.7,pop,0.9)]
EV+=[(9.8,thump,0.9),(11.3,ping,1.1),(11.3,thump,0.8)]
EV+=[(12.5,sent,0.8),(13.4,ping,1.2),(14.7,pop,0.6),(15.9,sent,1),(16.8,ping,1),(17.4,pop,0.8)]
EV+=[(18.6,sent,0.8),(19.0,thump,1),(20.0,pop,0.8),(22.9,ping,0.7)]
TOTAL=23.6
out=np.zeros(int(SR*TOTAL))
for t0,fn,g in EV:
    s=fn()*g; i=int(t0*SR)
    if i<len(out): out[i:i+len(s)]+=s[:len(out)-i]
out=np.clip(out*0.7,-1,1)
w=wave.open('assets/sfx/sfx-mix.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((out*32767).astype(np.int16).tobytes()); w.close()
