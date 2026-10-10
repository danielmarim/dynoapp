exec(open('/home/claude/videos/_dark/sfx_base.py').read())
S={'02':4.1,'03':10.4,'04':17.5,'05':24.2,'06':31.9,'07':39.2}
EV=[(0.3,pop,0.7)]+[(1.5+k*0.2,pop,0.7) for k in range(3)]
EV+=[(S['02'],sent,0.8),(S['02']+1.2,ping,1),(S['02']+2.6,sent,1),(S['02']+3.8,ping,1)]
EV+=[(S['03'],sent,0.8)]+[(S['03']+2.3+k*0.6,pop,0.8) for k in range(3)]+[(S['03']+4.4,pop,0.7)]
EV+=[(S['04'],sent,0.8),(S['04']+2.9,click,1),(S['04']+3.3,ping,1)]
EV+=[(S['05'],sent,0.8),(S['05']+1.2,sent,1),(S['05']+2.4,ping,1.1)]
EV+=[(S['06'],sent,0.8),(S['06']+1.1,pop,0.7),(S['06']+2.1,ping,1),(S['06']+3.4,pop,0.7),(S['06']+4.6,ping,1)]
EV+=[(S['07'],thump,0.8)]+[(S['07']+0.6+k*0.25,pop,0.7) for k in range(4)]
TOTAL=44.8
out=np.zeros(int(SR*TOTAL))
for t0,fn,g in EV:
    s=fn()*g; i=int(t0*SR)
    if i<len(out): out[i:i+len(s)]+=s[:len(out)-i]
out=np.clip(out*0.7,-1,1)
w=wave.open('assets/sfx/sfx-mix.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((out*32767).astype(np.int16).tobytes()); w.close()
