import json,sys,numpy as np,soundfile as sf
from kokoro_onnx import Kokoro
K="/tmp/claude-0/kokoro/"
k=Kokoro(K+"kokoro-v1.0.onnx",K+"voices-v1.0.bin")
segs=json.load(open(sys.argv[1])); out=sys.argv[2]
for s in segs:
    a,sr=k.create(s["say"],voice="ff_siwis",speed=1.15,lang="fr-fr")
    # trim silence
    idx=np.where(np.abs(a)>0.01)[0]; a=a[max(0,idx[0]-600):idx[-1]+1200]
    sf.write(f"{out}/{s['id']}.wav",a,sr); s["dur"]=round(len(a)/sr,3); print(s["id"],s["dur"])
json.dump(segs,open(sys.argv[1],"w"),ensure_ascii=False,indent=1)
