// Moteur commun « Histoires insolites » (Wake up smart).
// Tout est calculé depuis le temps t : aucune minuterie, aucun état entre deux images.
const W=1080,H=1920,cv=document.getElementById('c'),g=cv.getContext('2d');
const C={night:'#0B0E1F',night2:'#141A3A',ink:'#F5F3EE',mute:'#8E93B5',sun:'#FFB648',sun2:'#FF6B3D',red:'#FF4D5E',paper:'#EFE6D2',panel:'rgba(16,21,48,.94)'};
const F=(w,s,fam)=>`${w} ${s}px "${fam||'Inter Display'}"`;
let TL=null;
const cl=(x,a,b)=>Math.max(a,Math.min(b,x));
const lerp=(a,b,u)=>a+(b-a)*u;
const ease=x=>x<0?0:x>1?1:1-Math.pow(1-x,3);
const eio=x=>x<0?0:x>1?1:x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2;
// Ressort amorti en forme fermée (masse 1). Presets : UI 320/30, caméra 170/26, typo 120/24.
function spring(tau,k=320,c=30){if(tau<=0)return 0;const w=Math.sqrt(k),z=c/(2*w);
  if(z>=1)return 1-Math.exp(-w*tau)*(1+w*tau);
  const wd=w*Math.sqrt(1-z*z);return 1-Math.exp(-z*w*tau)*(Math.cos(wd*tau)+z/Math.sqrt(1-z*z)*Math.sin(wd*tau));}
const UI=t=>spring(t,320,30),CAM=t=>spring(t,170,26),TYPO=t=>spring(t,120,24);
function rr(x,y,w,h,r){g.beginPath();g.roundRect(x,y,w,h,r);}
function txt(s,x,y,font,col,align='center',a=1){if(a<=0)return;g.globalAlpha=a;g.font=font;g.fillStyle=col;g.textAlign=align;g.textBaseline='alphabetic';g.fillText(s,x,y);g.globalAlpha=1;}

// Texte masqué qui monte, mot par mot (décalage 55 ms). lines = ['MOT MOT', ...]
function rise(lines,x,y,size,col,t0,lt,{align='center',lh=1.08,w=900,out=null}={}){
  g.font=F(w,size);let wi=0;
  lines.forEach((line,li)=>{const ws=line.split(' '),sp=g.measureText(' ').width,tw=ws.reduce((a,s)=>a+g.measureText(s).width,0)+sp*(ws.length-1);
    let cx=align==='center'?x-tw/2:align==='right'?x-tw:x;const by=y+li*size*lh;
    ws.forEach(s=>{const mw=g.measureText(s).width,p=TYPO(lt-t0-wi*.055),o=out!==null?ease((lt-out)/.25):0;
      g.save();g.beginPath();g.rect(cx-6,by-size*1.0,mw+12,size*1.28);g.clip();
      const dy=(1-p)*size*1.05-o*size*1.05;const col_=typeof col==='function'?col(wi,s):col;
      g.font=F(w,size);g.fillStyle=col_;g.textAlign='left';g.fillText(s,cx,by+dy);g.restore();cx+=mw+sp;wi++;});});
}
// Tampon : arrive par ressort (échelle 1.35 → 1), sans rebond cartoon.
function stamp(s,x,y,col,rot,tau,size=84){if(tau<=0)return;const p=UI(tau),sc=1.35-.35*p;g.save();g.translate(x,y);g.rotate(rot);g.scale(sc,sc);g.globalAlpha=cl(tau*6,0,1);
  g.font=F(900,size);const w=g.measureText(s).width+60;rr(-w/2,-size*.8,w,size*1.25,16);g.lineWidth=10;g.strokeStyle=col;g.stroke();
  g.fillStyle=col;g.textAlign='center';g.textBaseline='middle';g.fillText(s,0,size*-.01);g.restore();g.globalAlpha=1;}
function pill(s,x,y,bg,fg,a=1,size=34){if(a<=0)return;g.font=F(800,size);const w=g.measureText(s).width+52;g.globalAlpha=a;rr(x-w/2,y-size-14,w,size+30,(size+30)/2);g.fillStyle=bg;g.fill();txt(s,x,y+4,F(800,size),fg,'center',a);g.globalAlpha=1;}
function chip(s,a=1){if(a<=0)return;g.globalAlpha=a;g.font=F(800,30);const w=g.measureText(s).width+56;rr(90,250,w,58,29);g.fillStyle='rgba(255,182,72,.14)';g.fill();g.strokeStyle='rgba(255,182,72,.55)';g.lineWidth=2;g.stroke();txt(s,118,290,F(800,30),C.sun,'left',a);g.globalAlpha=1;}
function glow(x,y,r,a,col='255,182,72'){if(a<=0)return;const gr=g.createRadialGradient(x,y,0,x,y,r);gr.addColorStop(0,`rgba(${col},${.5*a})`);gr.addColorStop(1,`rgba(${col},0)`);g.fillStyle=gr;g.fillRect(x-r,y-r,2*r,2*r);}
// Flood : cercle depuis un point qui couvre le coin le plus lointain en ~0,3 s.
function flood(x,y,tau,col){if(tau<=0)return;const R=Math.hypot(Math.max(x,W-x),Math.max(y,H-y))*1.05;g.beginPath();g.arc(x,y,R*UI(tau*1.4),0,7);g.fillStyle=col;g.fill();}

function background(t){
  const p=t/TL.total,gr=g.createLinearGradient(0,0,0,H);gr.addColorStop(0,C.night);gr.addColorStop(.7,C.night2);gr.addColorStop(1,`rgba(${60+90*p|0},${30+40*p|0},${60-10*p|0},1)`);
  g.fillStyle=gr;g.fillRect(0,0,W,H);
  const sy=H+260-380*eio(p),rad=g.createRadialGradient(W/2,sy,0,W/2,sy,900);
  rad.addColorStop(0,`rgba(255,182,72,${.30+.25*p})`);rad.addColorStop(.35,`rgba(255,107,61,${.12+.12*p})`);rad.addColorStop(1,'rgba(255,107,61,0)');
  g.fillStyle=rad;g.fillRect(0,0,W,H);
}
function brand(label){
  g.save();g.translate(90,150);g.beginPath();g.arc(0,0,26,Math.PI,0);g.fillStyle=C.sun;g.fill();g.fillRect(-40,4,80,5);
  for(let i=0;i<5;i++){const a=Math.PI+(i+1)*Math.PI/6;g.strokeStyle=C.sun;g.lineWidth=5;g.lineCap='round';g.beginPath();g.moveTo(Math.cos(a)*36,Math.sin(a)*36);g.lineTo(Math.cos(a)*48,Math.sin(a)*48);g.stroke();}
  g.restore();txt('WAKE UP SMART',158,166,F(900,40),C.ink,'left');txt(label,W-130,166,F(500,26,'JetBrains Mono'),C.mute,'right');
}
// Sous-titres karaoké (zone sûre : bas du texte au-dessus de y=1620).
function captions(t){
  const s=TL.segs.find(s=>t>=s.start&&t<s.start+s.dur+.25);if(!s)return;
  const words=s.cap.split(' '),wt=words.map(w=>w.replace(/[^\p{L}\p{N}]/gu,'').length+2),sum=wt.reduce((a,b)=>a+b,0);
  const chunks=[];let cur=[],n=0;words.forEach((w,i)=>{cur.push(i);n+=w.length+1;if(n>18||/[.,:?…»]$/.test(w)||i===words.length-1){chunks.push(cur);cur=[];n=0;}});
  const P=s.parts||[[s.start,s.start+s.dur]],tot=P.reduce((a,p)=>a+p[1]-p[0],0);
  let el=0;for(const p of P)el+=cl(t-p[0],0,p[1]-p[0]);
  const u=cl(el/tot,0,.999);let acc=0,wi=0;for(let i=0;i<words.length;i++){acc+=wt[i]/sum;if(u<acc){wi=i;break;}wi=i;}
  const ch=chunks.find(c=>c.includes(wi));const y=1560;
  g.font=F(900,64);const sp=g.measureText(' ').width;const ws=ch.map(i=>words[i].toUpperCase());const tw=ws.reduce((a,w)=>a+g.measureText(w).width,0)+sp*(ws.length-1);
  let x=W/2-tw/2;
  ch.forEach((i,j)=>{const w=ws[j],mw=g.measureText(w).width;
    if(i===wi){rr(x-12,y-60,mw+24,80,14);g.fillStyle=C.sun;g.fill();}
    g.lineWidth=10;g.strokeStyle='rgba(0,0,0,.55)';g.lineJoin='round';g.textAlign='left';g.font=F(900,64);if(i!==wi)g.strokeText(w,x,y);
    g.fillStyle=i===wi?C.night:(i<wi?C.ink:'rgba(245,243,238,.75)');g.fillText(w,x,y);x+=mw+sp;});
}
// Caméra : clés [t, zoom, x, y] triées (x,y = point visé). À partir de t, la caméra rejoint
// la clé par ressort depuis la clé précédente ; zoom interpolé en espace log.
function camera(keys,t){let i=0;while(i+1<keys.length&&keys[i+1][0]<=t)i++;
  if(i===0)return [keys[0][1],keys[0][2],keys[0][3]];
  const a=keys[i-1],b=keys[i],u=CAM(t-b[0]);
  return [Math.exp(lerp(Math.log(a[1]),Math.log(b[1]),u)),lerp(a[2],b[2],u),lerp(a[3],b[3],u)];}
function CTA(lt,line){
  const a=TYPO(lt);g.save();g.translate(W/2,820);g.scale(.85+.15*a,.85+.15*a);g.globalAlpha=cl(a,0,1);
  g.beginPath();g.arc(0,40,120,Math.PI,0);g.fillStyle=C.sun;g.fill();g.fillRect(-170,48,340,12);
  for(let i=0;i<7;i++){const r=UI(lt-.2-i*.05),ang=Math.PI+(i+.5)*Math.PI/7;g.strokeStyle=C.sun;g.lineWidth=12;g.lineCap='round';g.beginPath();g.moveTo(Math.cos(ang)*150,40+Math.sin(ang)*150);g.lineTo(Math.cos(ang)*(150+40*r),40+Math.sin(ang)*(150+40*r));g.stroke();}
  g.restore();g.globalAlpha=1;
  rise(['WAKE UP SMART'],W/2,1010,96,C.ink,.25,lt);txt(line,W/2,1080,F(600,36),C.mute,'center',ease((lt-.6)/.4));
  const b=UI(lt-1);if(b>0){g.save();g.translate(W/2,1198);g.scale(.9+.1*b,.9+.1*b);g.globalAlpha=cl(b,0,1);rr(-210,-48,420,96,48);g.fillStyle=C.sun;g.fill();txt('+  ABONNE-TOI',0,15,F(900,40),C.night,'center',cl(b,0,1));g.restore();}
}
// Boucle principale commune. SCENE = {label, S:{id:(lt,d,t)=>{}}, cam(t)?, sfx()?}
function makeRender(SCENE){
  window.render=function(t){
    background(t);brand(SCENE.label);
    const cur=[...TL.segs].reverse().find(s=>t>=s.start)||TL.segs[0];
    const lt=t-cur.start;
    g.save();g.beginPath();g.rect(0,212,W,1298);g.clip();
    // poussée lente continue (rien d'immobile) + caméra de la scène
    const dr=1+.03*eio(cl(lt/Math.max(1,cur.dur+.4),0,1));g.translate(W/2,900);g.scale(dr,dr);g.translate(-W/2,-900);
    if(SCENE.cam){const [z,cx,cy]=SCENE.cam(t);g.translate(W/2,900);g.scale(z,z);g.translate(-cx,-cy);}
    SCENE.S[cur.id](lt,cur.dur,t);g.restore();
    captions(t);
    g.fillStyle='rgba(255,255,255,.12)';g.fillRect(0,H-8,W,8);g.fillStyle=C.sun;g.fillRect(0,H-8,W*t/TL.total,8);
  };
  window.sfx=()=>SCENE.sfx?SCENE.sfx():[];
  window.setup=async function(tl){TL=tl;if(SCENE.init)SCENE.init();await document.fonts.load(F(900,40));await document.fonts.load(F(500,20,'JetBrains Mono'));await document.fonts.load(F(800,20,'DejaVu Serif'));window.ready=true;return true;};
}
