# Recale la timeline sur la voix ElevenLabs (découpe aux pauses, voir asr.json).
import json,numpy as np,soundfile as sf
segs=json.load(open("segments.json")); asr=json.load(open("asr.json"))
groups=[[0],[1,2],[3,4,5],[6,7],[8,9,10],[11,12],[13,14],[15,16],[17,18],[19,20,21],[22,23,24],[25,26,27],[28,29,30,31],[32,33],[34,35,36],[37,38],[39,40]]
assert sum(map(len,groups))==len(asr)
LEAD=0.4
for s,gp in zip(segs,groups):
    parts=[[asr[i]["s"]+LEAD,asr[i]["e"]+LEAD] for i in gp]
    s["start"]=round(parts[0][0],3); s["dur"]=round(parts[-1][1]-parts[0][0],3); s["parts"]=parts
v,SR=sf.read("el.wav"); v=np.concatenate([np.zeros(int(LEAD*SR)),v])
total=len(v)/SR+1.4; N=int(total*SR); v=np.pad(v,(0,N-len(v)))
tt=np.arange(N)/SR; beat=60/96; bar=beat*4
chords=[[57,60,64,69],[53,57,60,65],[48,55,60,64],[55,59,62,67]]
f=lambda m:440*2**((m-69)/12); mus=np.zeros(N)
for ci in range(int(total/bar)+1):
    c=chords[ci%4]; i0=int(ci*bar*SR); i1=min(N,int((ci+1)*bar*SR)+SR//2)
    if i0>=N: break
    seg=tt[i0:i1]-ci*bar; env=np.minimum(1,seg/0.6)*np.exp(-seg*0.25)
    for m in c:
        for det in (1,1.003): mus[i0:i1]+=0.035*env*np.sin(2*np.pi*f(m)*det*seg)
    mus[i0:i1]+=0.09*np.exp(-seg*1.2)*np.sin(2*np.pi*f(c[0]-12)*seg)
rng=np.random.default_rng(1)
for bi in range(int(total/beat)):
    i0=int(bi*beat*SR); s_=np.arange(min(int(.25*SR),N-i0))/SR
    mus[i0:i0+len(s_)]+=np.sin(2*np.pi*(50+90*np.exp(-s_*30))*s_)*np.exp(-s_*14)*0.22
    j=int((bi+.5)*beat*SR); L=int(.05*SR)
    if j+L<N: mus[j:j+L]+=rng.standard_normal(L)*np.exp(-np.arange(L)/(L/8))*0.025
envv=np.convolve(np.abs(v),np.ones(SR//5)/(SR//5),mode="same"); duck=np.where(envv>0.005,0.3,1.0)
duck=np.convolve(duck,np.ones(SR//4)/(SR//4),mode="same")
fade=np.minimum(1,np.minimum(tt/1.0,(total-tt)/1.5))
out=v+mus*duck*fade*0.7; out/=np.max(np.abs(out))*1.05
sf.write("mix.wav",out,SR)
json.dump({"total":round(total,3),"segs":segs},open("timeline.json","w"),ensure_ascii=False,indent=1)
print(total)
