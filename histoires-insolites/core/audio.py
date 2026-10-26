# Bande son : musique maison + bruitages synthétisés (sfx.json) + voix optionnelle.
# Usage : python3 audio.py timeline.json sfx.json out.wav [voix.wav lead_s]
import sys,json,numpy as np,soundfile as sf
SR=44100; tl=json.load(open(sys.argv[1])); ev=json.load(open(sys.argv[2])); total=tl["total"]; N=int(total*SR)
rng=np.random.default_rng(7); tt=np.arange(N)/SR
v=np.zeros(N)
if len(sys.argv)>4:
    a,sr=sf.read(sys.argv[4]); a=a if a.ndim==1 else a.mean(1); assert sr==SR; i=int(float(sys.argv[5])*SR); v[i:i+len(a)]=a[:N-i]
# musique : nappe Am-F-C-G + kick doux, 96 BPM (fluide)
beat=60/96; bar=beat*4; f=lambda m:440*2**((m-69)/12); mus=np.zeros(N)
chords=[[57,60,64,69],[53,57,60,65],[48,55,60,64],[55,59,62,67]]
for ci in range(int(total/bar)+1):
    c=chords[ci%4]; i0=int(ci*bar*SR); i1=min(N,int((ci+1)*bar*SR)+SR//2)
    if i0>=N: break
    s=tt[i0:i1]-ci*bar; env=np.minimum(1,s/0.6)*np.exp(-s*0.25)
    for m in c:
        for det in (1,1.003): mus[i0:i1]+=0.035*env*np.sin(2*np.pi*f(m)*det*s)
    mus[i0:i1]+=0.09*np.exp(-s*1.2)*np.sin(2*np.pi*f(c[0]-12)*s)
for bi in range(int(total/beat)):
    i0=int(bi*beat*SR); s=np.arange(min(int(.25*SR),N-i0))/SR
    mus[i0:i0+len(s)]+=np.sin(2*np.pi*(50+90*np.exp(-s*30))*s)*np.exp(-s*14)*0.22
    j=int((bi+.5)*beat*SR); L=int(.05*SR)
    if j+L<N: mus[j:j+L]+=rng.standard_normal(L)*np.exp(-np.arange(L)/(L/8))*0.025
# bruitages
def sfx(kind):
    if kind=='whoosh':
        L=int(.45*SR); s=np.arange(L)/SR; n=rng.standard_normal(L); n=np.convolve(n,np.ones(18)/18,'same')
        return n*np.sin(np.pi*s/.45)**2*0.5
    if kind=='thump':
        L=int(.5*SR); s=np.arange(L)/SR; return (np.sin(2*np.pi*(45+120*np.exp(-s*25))*s)*np.exp(-s*7)+rng.standard_normal(L)*np.exp(-s*40)*.25)*0.9
    if kind=='kick':
        L=int(.12*SR); s=np.arange(L)/SR; return (np.sin(2*np.pi*(180+300*np.exp(-s*60))*s)*np.exp(-s*45)+rng.standard_normal(L)*np.exp(-s*80)*.4)*0.5
    if kind=='stamp':
        L=int(.3*SR); s=np.arange(L)/SR; return (rng.standard_normal(L)*np.exp(-s*30)*.7+np.sin(2*np.pi*90*s)*np.exp(-s*18))*0.6
    if kind=='pop':
        L=int(.12*SR); s=np.arange(L)/SR; return np.sin(2*np.pi*(500+700*s/.12)*s)*np.exp(-s*35)*0.35
    if kind=='tick':
        L=int(.05*SR); s=np.arange(L)/SR; return np.sin(2*np.pi*2200*s)*np.exp(-s*120)*0.3
    return np.zeros(1)
fx=np.zeros(N)
for t,k in ev:
    x=sfx(k); i=int(max(0,t)*SR); n=min(len(x),N-i)
    if n>0: fx[i:i+n]+=x[:n]
# ducking : musique −9 dB sous la voix, bruitages −4 dB
envv=np.convolve(np.abs(v),np.ones(SR//5)/(SR//5),mode="same"); on=np.convolve((envv>0.005).astype(float),np.ones(SR//4)/(SR//4),mode="same")
duck=1-on*(1-0.355); fduck=1-on*(1-0.63)
fade=np.minimum(1,np.minimum(tt/1.0,(total-tt)/1.5))
out=v+mus*duck*fade*0.7+fx*fduck*0.55; out/=np.max(np.abs(out))*1.05
sf.write(sys.argv[3],out,SR)
