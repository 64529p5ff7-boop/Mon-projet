# Calcule l'instant d'apparition de chaque mot à partir de l'analyse image par image
# de la vidéo d'origine (largeur d'encre de la zone de sous-titres).
import json,re
cap=json.load(open('analyse_sous_titres.json'))
lines=[l.rstrip('\n') for l in open('captions.txt',encoding='utf-8') if l.strip()]
groups=[];cur=None
for t,dk,org,x0,x1 in cap:
    on=dk+org>60 and t<77.6
    if on and cur is None: cur={'s':t,'fr':[]}
    if on: cur['fr'].append((t,x0,x1)); cur['e']=t
    elif cur: groups.append(cur);cur=None
if cur: groups.append(cur)
assert len(groups)==len(lines),(len(groups),len(lines))
out=[]
for g,l in zip(groups,lines):
    toks=re.findall(r'\[[^\]]+\]|\S+',l)
    words=[{'w':x.strip('[]'),'hl':x.startswith('[')} for x in toks]
    x0=min(f[1] for f in g['fr']);x1=max(f[2] for f in g['fr'])
    L=lambda w:len(w['w'])+(2 if w['hl'] else 0)
    tot=sum(L(w) for w in words)+len(words)-1
    cum=0
    for k,w in enumerate(words):
        if k==0: w['t']=g['s']
        else:
            th=x0+(x1-x0)*(cum+0.5)/tot
            w['t']=next((f[0] for f in g['fr'] if f[2]>=th),g['e'])
        cum+=L(w)+1
    out.append({'s':g['s'],'e':round(g['e']+1/30,3),'words':words})
out[-1]['e']=77.6
json.dump(out,open('captions.json','w'),ensure_ascii=False,indent=0)
for o in out[:6]+out[-4:]:print(o['s'],o['e'],[(w['w'],w['t']) for w in o['words']])
