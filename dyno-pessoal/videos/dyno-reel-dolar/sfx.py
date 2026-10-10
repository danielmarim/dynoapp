import numpy as np, wave
SR=48000
rng=np.random.default_rng(7)
def env(n,a=0.003,d=0.15):
    t=np.arange(n)/SR; e=np.minimum(1,t/a)*np.exp(-t/d); return e
def tone(f,dur,d=0.12,a=0.002):
    n=int(SR*dur); t=np.arange(n)/SR
    return np.sin(2*np.pi*f*t)*env(n,a,d)
def ping():
    a=tone(1046,0.18,0.07)*0.6; b=tone(1568,0.35,0.12)*0.6
    out=np.zeros(int(SR*0.45)); out[:len(a)]+=a; s=int(SR*0.08); out[s:s+len(b)]+=b
    out+=0.25*np.concatenate([tone(2093,0.2,0.05),np.zeros(len(out)-int(SR*0.2))])*0
    return out
def sent():
    n=int(SR*0.22); t=np.arange(n)/SR
    f=600+2400*(t/t[-1]); ph=2*np.pi*np.cumsum(f)/SR
    return 0.35*np.sin(ph)*np.sin(np.pi*t/t[-1])**2
def click():
    n=int(SR*0.06); c=rng.normal(0,1,n)*env(n,0.0005,0.006)*0.8
    th=tone(90,0.25,0.05)*0.9
    out=np.zeros(int(SR*0.3)); out[:n]+=c; out[:len(th)]+=th; return out
def powerdown():
    n=int(SR*0.9); t=np.arange(n)/SR
    f=220*np.exp(-3*t); ph=2*np.pi*np.cumsum(f)/SR
    buzz=np.sign(np.sin(2*np.pi*120*t))*0.15*np.exp(-4*t)
    return (0.5*np.sin(ph)+buzz)*np.exp(-2.5*t)
def flick():
    n=int(SR*0.04); return rng.normal(0,1,n)*env(n,0.0005,0.008)*0.5
def thump():
    n=int(SR*0.5); t=np.arange(n)/SR
    f=110*np.exp(-6*t)+45; ph=2*np.pi*np.cumsum(f)/SR
    return np.sin(ph)*np.exp(-6*t)*1.0
def pop():
    n=int(SR*0.12); t=np.arange(n)/SR
    f=400+900*t/t[-1]; ph=2*np.pi*np.cumsum(f)/SR
    return 0.45*np.sin(ph)*np.exp(-30*t)
EV=[(0.2,pop,0.8)]
EV+=[(1.1+k*0.75,flick,1.2) for k in range(4)]+[(1.1+k*0.75,pop,0.35) for k in range(4)]
EV+=[(4.4,sent,0.9),(5.3,sent,1),(6.4,ping,1),(7.4,pop,0.9)]
EV+=[(8.8,sent,0.9)]+[(9.6+k*0.24,flick,0.6) for k in range(10)]
EV+=[(12.0,pop,0.8),(12.2,ping,1.1),(12.5,ping,1.1),(12.25,thump,0.7)]
EV+=[(14.05,thump,1)]+[(14.8+k*0.22,pop,0.8) for k in range(5)]
EV+=[(17.6,sent,0.8),(17.85,pop,0.8),(18.1,thump,1),(18.75,pop,0.8),(21.4,ping,0.7)]
out=np.zeros(int(SR*22))
for t0,fn,g in EV:
    s=fn()*g; i=int(t0*SR); out[i:i+len(s)]+=s[:len(out)-i]
out=np.clip(out*0.7,-1,1)
w=wave.open('assets/sfx/sfx-mix.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((out*32767).astype(np.int16).tobytes()); w.close()
