# Cale la timeline sur la voix ElevenLabs (un seul mp3 pour tout le texte).
# Usage : ffmpeg -i ../voix-elevenlabs.mp3 -ar 44100 -ac 1 voix.wav
#         ffmpeg -i voix.wav -af silencedetect=n=-35dB:d=0.25 -f null - 2>&1 | grep -oE 'silence_(start|end): [0-9.]+' > sil.txt
#         python3 sync.py
# Les 11 plans sont retrouvés automatiquement : on choisit les 10 silences dont la position colle le mieux
# aux proportions des plans de la voix témoin (durées « dur » de segments.json).
import json,soundfile as sf
segs=json.load(open("segments.json")); a,sr=sf.read("voix.wav"); D=len(a)/sr
ev=[(l.split(':')[0],float(l.split(': ')[1])) for l in open("sil.txt")]
sp=[];cur=0.0
for k,v in ev:
    if k=='silence_start':
        if v-cur>0.05: sp.append((cur,v))
    else: cur=v
if D-cur>0.1: sp.append((cur,D))
n=len(segs); w=[s["dur"] for s in segs]; tot=sum(w)
t0,t1=sp[0][0],sp[-1][1]; want=[t0+(t1-t0)*sum(w[:i+1])/tot for i in range(n-1)]
# programmation dynamique : coupure j après le morceau c(j), croissante
m=len(sp); INF=1e18; best=[[INF]*m for _ in range(n)]; prev=[[-1]*m for _ in range(n)]
for c in range(m-1): best[0][c]=(sp[c][1]-want[0])**2
for j in range(1,n-1):
    for c in range(j,m-1):
        for q in range(j-1,c):
            v=best[j-1][q]+(sp[c][1]-want[j])**2
            if v<best[j][c]: best[j][c]=v; prev[j][c]=q
c=min(range(n-2,m-1),key=lambda c:best[n-2][c]); cuts=[c]
for j in range(n-2,0,-1): c=prev[j][c]; cuts.append(c)
cuts=cuts[::-1]; bounds=[-1]+cuts+[m-1]
LEAD=0.4
for i,s in enumerate(segs):
    parts=[[round(sp[k][0]+LEAD,3),round(sp[k][1]+LEAD,3)] for k in range(bounds[i]+1,bounds[i+1]+1)]
    s["start"]=parts[0][0]; s["dur"]=round(parts[-1][1]-parts[0][0],3); s["parts"]=parts
    print(s["id"],s["start"],s["dur"],s["cap"][:40])
total=round(sp[-1][1]+LEAD+1.6,3)
json.dump({"total":total,"segs":segs},open("timeline.json","w"),ensure_ascii=False,indent=1); print(total)
