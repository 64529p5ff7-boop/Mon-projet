import json,numpy as np,soundfile as sf
segs=json.load(open("build/segments.json")); SR=24000
lead=0.5; gap={"s3":0.55,"s14":0.6,"s16":0.7}
t=lead; voice=[]
for s in segs:
    s["start"]=round(t,3); a,_=sf.read(f"build/voix/{s['id']}.wav"); voice.append((t,a))
    t+=s["dur"]+gap.get(s["id"],0.28)
total=t+1.6
N=int(total*SR); v=np.zeros(N)
for st,a in voice: i=int(st*SR); v[i:i+len(a)]+=a
# musique : nappe douce + pulsation légère (synthèse maison, libre de droits)
tt=np.arange(N)/SR; bpm=96; beat=60/bpm
chords=[[57,60,64,69],[53,57,60,65],[48,55,60,64],[55,59,62,67]]  # Am F C G
f=lambda m:440*2**((m-69)/12)
mus=np.zeros(N); bar=beat*4
for ci in range(int(total/bar)+1):
    c=chords[ci%4]; i0=int(ci*bar*SR); i1=min(N,int((ci+1)*bar*SR)+SR//2)
    seg=tt[i0:i1]-ci*bar; env=np.minimum(1,seg/0.6)*np.exp(-seg*0.25)
    for m in c:
        for det in (1,1.003):
            mus[i0:i1]+=0.035*env*np.sin(2*np.pi*f(m)*det*seg)
    bass=0.09*np.exp(-seg*1.2)*np.sin(2*np.pi*f(c[0]-12)*seg); mus[i0:i1]+=bass
for bi in range(int(total/beat)):
    i0=int(bi*beat*SR); L=int(0.25*SR); s_=np.arange(min(L,N-i0))/SR
    kick=np.sin(2*np.pi*(50+90*np.exp(-s_*30))*s_)*np.exp(-s_*14)*0.22
    mus[i0:i0+len(s_)]+=kick
    j=int((bi+0.5)*beat*SR); 
    if j+2400<N: mus[j:j+2400]+=np.random.randn(2400)*np.exp(-np.arange(2400)/300)*0.025
# ducking
envv=np.convolve(np.abs(v),np.ones(4800)/4800,mode="same"); duck=np.where(envv>0.005,0.35,1.0)
duck=np.convolve(duck,np.ones(6000)/6000,mode="same")
fade=np.minimum(1,np.minimum(tt/1.0,(total-tt)/1.5))
out=v*1.0+mus*duck*fade*0.8; out/=np.max(np.abs(out))*1.05
sf.write("build/mix.wav",out,SR); sf.write("build/voix-seule.wav",v/np.max(np.abs(v))*0.95,SR)
json.dump({"total":round(total,3),"segs":segs},open("build/timeline.json","w"),ensure_ascii=False,indent=1)
print(total)
