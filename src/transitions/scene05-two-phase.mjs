const clamp=(v)=>Math.max(0,Math.min(1,v));
const ease=(v)=>{const t=clamp(v);return t*t*t*(t*(t*6-15)+10);};
export const scene05TwoPhaseState=(frame,c)=>{
  const [w,h]=c.dashboardSize;
  const focal=[0,1].map(a=>c.screenQuad.reduce((sum,p)=>sum+p[a],0)/4);
  const bounds=Math.max(...c.screenQuad.map(p=>p[1]))-Math.min(...c.screenQuad.map(p=>p[1]));
  const endScale=c.phaseADisplayHeight/bounds;
  const p=ease(frame/c.phaseAEndFrame);
  const scale=1+(endScale-1)*p;
  const tx=(c.cameraTargetCenter[0]-endScale*focal[0])*p;
  const ty=(c.cameraTargetCenter[1]-endScale*focal[1])*p;
  const cameraQuad=c.screenQuad.map(([x,y])=>[x*scale+tx,y*scale+ty]);
  const screenScale=c.model.height*c.designScale/(h+2*c.model.bezel);
  const [cx,cy]=c.targetCenter;
  const finalQuad=[[cx-w*screenScale/2,cy-h*screenScale/2],[cx+w*screenScale/2,cy-h*screenScale/2],
    [cx+w*screenScale/2,cy+h*screenScale/2],[cx-w*screenScale/2,cy+h*screenScale/2]];
  const morph=ease((frame-c.morphStartFrame)/(c.phaseBEndFrame-c.morphStartFrame));
  const quad=cameraQuad.map((p,i)=>p.map((v,a)=>v+(finalQuad[i][a]-v)*morph));
  return {scale,tx,ty,quad,cameraQuad,finalQuad,morph,takeover:ease(frame/c.takeoverFrames),
    photoOpacity:1-ease((frame-c.phaseAEndFrame)/(c.backdropClearEndFrame-c.phaseAEndFrame))};
};
