const {chromium}=require('playwright');const fs=require('fs');const {spawn}=require('child_process');
(async()=>{
  const tl=JSON.parse(fs.readFileSync('timeline.json'));const mode=process.argv[2];
  const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
  await p.goto('file://'+__dirname+'/scene.html');await p.evaluate(tl=>window.setup(tl),tl);
  const cv=await p.$('#c');
  if(mode==='stills'){for(const t of process.argv.slice(3)){await p.evaluate(t=>render(t),+t);await cv.screenshot({path:`still_${t}.jpg`,type:'jpeg',quality:80});}await b.close();return;}
  const fps=30,N=Math.ceil(tl.total*fps);
  const ff=spawn('ffmpeg',['-y','-v','error','-f','image2pipe','-framerate',''+fps,'-c:v','mjpeg','-i','-','-i','mix.wav','-c:v','libx264','-preset','medium','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart','../wake-up-smart-clasico.mp4'],{stdio:['pipe','inherit','inherit']});
  for(let i=0;i<N;i++){
    const data=await p.evaluate(t=>{render(t);return document.getElementById('c').toDataURL('image/jpeg',.92).split(',')[1];},i/fps);
    if(!ff.stdin.write(Buffer.from(data,'base64')))await new Promise(r=>ff.stdin.once('drain',r));
    if(i%300===0)console.log(i,'/',N);
  }
  ff.stdin.end();await new Promise(r=>ff.on('close',r));await b.close();
})();
