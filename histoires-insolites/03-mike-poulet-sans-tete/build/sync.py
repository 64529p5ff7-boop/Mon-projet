# Cale la timeline sur la voix ElevenLabs : regroupe les morceaux de parole (silences de sil.txt) par plan.
import json,soundfile as sf
segs=json.load(open("segments.json")); a,sr=sf.read("voix.wav"); D=len(a)/sr
ev=[(l.split(':')[0],float(l.split(': ')[1])) for l in open("sil.txt")]
sp=[];cur=0.0
for k,v in ev:
    if k=='silence_start':
        if v-cur>0.05: sp.append((cur,v))
    else: cur=v
if D-cur>0.1: sp.append((cur,D))
groups=[[0,1,2],[3,4,5,6],[7,8,9,10],[11,12,13,14],[15,16,17,18],[19,20,21],[22,23,24,25],[26,27,28,29],[30,31,32],[33,34]]
assert sum(map(len,groups))==len(sp)
LEAD=0.4
for s,gp in zip(segs,groups):
    parts=[[round(sp[i][0]+LEAD,3),round(sp[i][1]+LEAD,3)] for i in gp]
    s["start"]=parts[0][0]; s["dur"]=round(parts[-1][1]-parts[0][0],3); s["parts"]=parts
total=round(sp[-1][1]+LEAD+1.6,3)
json.dump({"total":total,"segs":segs},open("timeline.json","w"),ensure_ascii=False,indent=1); print(total)
