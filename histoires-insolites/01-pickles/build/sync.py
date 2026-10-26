# Cale la timeline sur la voix ElevenLabs : regroupe les morceaux de parole (asr.json) par plan.
import json
segs=json.load(open("segments.json")); asr=json.load(open("asr.json"))
groups=[[0,1,2],[3,4,5],[6,7,8,9],[10,11,12,13,14],[15,16],[17,18,19],[20,21,22],[23,24,25,26],[27,28,29,30],[31,32,33,34],[35,36,37]]
assert sum(map(len,groups))==len(asr)
LEAD=0.4
for s,gp in zip(segs,groups):
    parts=[[asr[i]["s"]+LEAD,asr[i]["e"]+LEAD] for i in gp]
    s["start"]=round(parts[0][0],3); s["dur"]=round(parts[-1][1]-parts[0][0],3); s["parts"]=parts
total=round(asr[-1]["e"]+LEAD+1.6,3)
json.dump({"total":total,"segs":segs},open("timeline.json","w"),ensure_ascii=False,indent=1); print(total)
