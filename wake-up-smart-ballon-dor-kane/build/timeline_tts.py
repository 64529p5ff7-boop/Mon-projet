# Aperçu avec voix temporaire (Kokoro) : enchaîne les plans avec une respiration de 0,45 s
# et monte la piste voix à 44,1 kHz. Remplacé par sync.py quand la voix ElevenLabs arrive.
import json,subprocess,numpy as np,soundfile as sf
segs=json.load(open("segments.json")); LEAD,GAP,SR=0.4,0.45,44100
t=LEAD
for s in segs: s["start"]=round(t,3); t+=s["dur"]+GAP
total=round(t-GAP+1.6,3)
json.dump({"total":total,"segs":segs},open("timeline.json","w"),ensure_ascii=False,indent=1)
v=np.zeros(int(total*SR))
for s in segs:
    a=subprocess.run(["ffmpeg","-v","error","-i",f"wav/{s['id']}.wav","-ar",str(SR),"-ac","1","-f","f32le","-"],capture_output=True).stdout
    a=np.frombuffer(a,np.float32); i=int(s["start"]*SR); v[i:i+len(a)]=a[:len(v)-i]
sf.write("voix.wav",v*0.95/np.max(np.abs(v)),SR); print(total)
