import sherpa_onnx, soundfile as sf, json, re
D="/tmp/claude-0/sherpa/sherpa-onnx-whisper-small/"
r=sherpa_onnx.OfflineRecognizer.from_whisper(encoder=D+"small-encoder.int8.onnx",decoder=D+"small-decoder.int8.onnx",tokens=D+"small-tokens.txt",language="fr",task="transcribe",num_threads=4)
a,sr=sf.read("/tmp/claude-0/el16.wav")
ev=[(l.split(':')[0],float(l.split(': ')[1])) for l in open("sil.txt")]
# intervalles de parole
sp=[];cur=0.0
for k,v in ev:
    if k=='silence_start': 
        if v-cur>0.05: sp.append((cur,v))
    else: cur=v
if len(a)/sr-cur>0.1: sp.append((cur,len(a)/sr))
out=[]
for s,e in sp:
    st=r.create_stream(); st.accept_waveform(sr,a[int(s*sr):int(e*sr)]); r.decode_stream(st)
    out.append({"s":round(s,2),"e":round(e,2),"txt":st.result.text.strip()}); print(out[-1])
json.dump(out,open("asr.json","w"),ensure_ascii=False,indent=1)
