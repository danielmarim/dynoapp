exec(open('/home/claude/videos/_dark/sfx_base.py').read())
EV=[(0.3,pop,0.7),(0.5,thump,0.7)]+[(1.1+k*0.18,pop,0.7) for k in range(3)]
EV+=[(3.5,sent,0.8)]+[(4.1+k*0.22,flick,0.7) for k in range(5)]+[(6.65,click,1.0),(7.4,ping,1.1)]
EV+=[(10.6,thump,0.9)]+[(11.2+k*0.45,pop,0.8) for k in range(3)]+[(13.4,ping,0.8)]
EV+=[(17.9,sent,0.8)]+[(18.0+k*0.08,flick,0.5) for k in range(10)]+[(18.9,thump,1)]
EV+=[(21.4,sent,0.8),(22.4,thump,1),(25.0,ping,0.7)]
TOTAL=25.8
out=np.zeros(int(SR*TOTAL))
for t0,fn,g in EV:
    s=fn()*g; i=int(t0*SR)
    if i<len(out): out[i:i+len(s)]+=s[:len(out)-i]
out=np.clip(out*0.7,-1,1)
w=wave.open('assets/sfx/sfx-mix.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((out*32767).astype(np.int16).tobytes()); w.close()
