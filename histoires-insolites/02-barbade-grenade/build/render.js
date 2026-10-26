// Rendu image par image (Playwright → ffmpeg). Modes : stills t1 t2… | sfx | full
const {chromium}=require('playwright');const fs=require('fs');const {spawn}=require('child_process');
(async()=>{
  const tl=JSON.parse(fs.readFileSync('timeline.json'));const mode=process.argv[2];
  const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
  await p.goto('file://'+__dirname+'/scene.html');await p.evaluate(tl=>window.setup(tl),tl);
  if(mode==='sfx'){fs.writeFileSync('sfx.json',JSON.stringify(await p.evaluate(()=>window.sfx())));await b.close();return;}
  const cv=await p.$('#c');
  if(mode==='stills'){for(const t of process.argv.slice(3)){await p.evaluate(t=>render(t),+t);await cv.screenshot({path:`still_${t}.jpg`,type:'jpeg',quality:80});}await b.close();return;}
  // flou de bougé : moyenne de 2 sous-images (obturateur 0,5)
  await p.evaluate(()=>{window.__off=document.createElement('canvas');__off.width=1080;__off.height=1920;});
  const fps=30,N=Math.ceil(tl.total*fps),out=process.env.OUT;
  const ff=spawn('ffmpeg',['-y','-v','error','-f','image2pipe','-framerate',''+fps,'-c:v','mjpeg','-i','-','-i','mix.wav',
    '-vf','scale=in_range=pc:out_range=tv:out_color_matrix=bt709,format=yuv420p','-c:v','libx264','-preset','medium','-crf','16',
    '-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-c:a','aac','-b:a','256k','-shortest','-movflags','+faststart',out],{stdio:['pipe','inherit','inherit']});
  for(let i=0;i<N;i++){
    const data=await p.evaluate(t=>{const c=document.getElementById('c'),x=__off.getContext('2d');
      render(Math.max(0,t-1/120));x.globalAlpha=1;x.drawImage(c,0,0);render(t);
      const g2=c.getContext('2d');g2.globalAlpha=.5;g2.drawImage(__off,0,0);g2.globalAlpha=1;
      return c.toDataURL('image/jpeg',.94).split(',')[1];},i/fps);
    if(!ff.stdin.write(Buffer.from(data,'base64')))await new Promise(r=>ff.stdin.once('drain',r));
    if(i%600===0)console.log(i,'/',N);
  }
  ff.stdin.end();await new Promise(r=>ff.on('close',r));await b.close();
})();
