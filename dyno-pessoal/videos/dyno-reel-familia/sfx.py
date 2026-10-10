exec(open('/home/claude/videos/_dark/sfx_base.py').read())
EV=[(0.25,pop,0.7),(0.95,thump,0.8)]+[(1.25+k*0.18,pop,0.6) for k in range(4)]
EV+=[(4.3,sent,0.8)]+[(1.6+k+4.3-0.3,click,0.6) for k in range(3)]+[(1.6+k+4.3,pop,0.7) for k in range(3)]
EV+=[(10.0,sent,0.8),(11.1,sent,0.9),(12.1,ping,1),(13.4,sent,0.9),(14.5,ping,1)]
EV+=[(16.7,thump,0.9)]+[(17.3+k*0.32,pop,0.7) for k in range(4)]
EV+=[(21.2,sent,0.8),(21.5,pop,0.8),(22.5,thump,1),(24.9,ping,0.7)]
TOTAL=25.8
out=np.zeros(int(SR*TOTAL))
for t0,fn,g in EV:
    s=fn()*g; i=int(t0*SR)
    if i<len(out): out[i:i+len(s)]+=s[:len(out)-i]
out=np.clip(out*0.7,-1,1)
w=wave.open('assets/sfx/sfx-mix.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((out*32767).astype(np.int16).tobytes()); w.close()
