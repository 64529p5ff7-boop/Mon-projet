// node render.js stills 1.8 19.4 ...   -> still_<t>.jpg
// node render.js                       -> ../studio-motion-8-outils.mp4
const {chromium}=require('playwright');const fs=require('fs');const {spawn}=require('child_process');
(async()=>{
  const tl={...JSON.parse(fs.readFileSync('timeline.json')),captions:JSON.parse(fs.readFileSync('captions.json'))};
  const mode=process.argv[2];
  const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
  await p.goto('file://'+__dirname+'/scene.html');await p.evaluate(tl=>window.setup(tl),tl);
  const cv=await p.$('#c');
  if(mode==='stills'){for(const t of process.argv.slice(3)){await p.evaluate(t=>render(t),+t);await cv.screenshot({path:`still_${t}.jpg`,type:'jpeg',quality:85});}await b.close();return;}
  const fps=30,N=Math.round(tl.total*fps);
  const ff=spawn('ffmpeg',['-y','-v','error','-f','image2pipe','-framerate',''+fps,'-c:v','mjpeg','-i','-','-i','audio.flac','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart','../studio-motion-8-outils.mp4'],{stdio:['pipe','inherit','inherit']});
  for(let i=0;i<N;i++){
    const data=await p.evaluate(t=>{render(t);return document.getElementById('c').toDataURL('image/jpeg',.93).split(',')[1];},i/fps);
    if(!ff.stdin.write(Buffer.from(data,'base64')))await new Promise(r=>ff.stdin.once('drain',r));
    if(i%300===0)console.log(i,'/',N);
  }
  ff.stdin.end();await new Promise(r=>ff.on('close',r));await b.close();
})();
