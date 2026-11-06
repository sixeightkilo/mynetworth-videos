const clamp = (value) => Math.max(0, Math.min(1, value));
const ease = (value) => { const t = clamp(value); return t*t*(3-2*t); };
const settleEase = (value) => { const t = clamp(value); return t*t*t*(t*(t*6-15)+10); };

export const transitionSpec = (config) => {
  const handoffStart = config.takeoverFrame+config.pushFrames-1;
  const scale = config.scene7Height/config.screenBoundsHeight;
  const model = {height: 640, bezel: 56, outerRadius: 128, screenRadius: 80,
    notchWidth: 304, notchHeight: 72, notchRadius: 24, background: '#f7f7f7', ...config.mockup};
  const screenMatchFrames = config.screenMatchFrames ?? 4;
  const settleFrames = config.phoneSettleFrames ?? 15;
  const settleStart = handoffStart+screenMatchFrames-1;
  const settleEnd = settleStart+settleFrames-1;
  const [screenWidth, screenHeight] = config.dashboardSize;
  const phoneScale = model.height/(screenHeight+2*model.bezel);
  const [cx, cy] = config.targetCenter;
  const frontQuad = [[cx-screenWidth*phoneScale/2, cy-screenHeight*phoneScale/2],
    [cx+screenWidth*phoneScale/2, cy-screenHeight*phoneScale/2],
    [cx+screenWidth*phoneScale/2, cy+screenHeight*phoneScale/2],
    [cx-screenWidth*phoneScale/2, cy+screenHeight*phoneScale/2]];
  const tx = config.targetCenter[0]-scale*config.focalPoint[0];
  const ty = config.targetCenter[1]-scale*config.focalPoint[1];
  return {
    handoffStart, settleStart, settleEnd, screenMatchFrames, settleFrames, model,
    durationInFrames: settleEnd+1+config.scene7HoldFrames,
    scale,
    tx, ty, frontQuad, phoneScale,
    zoomEndQuad: config.screenQuad.map(([x,y]) => [x*scale+tx,y*scale+ty]),
  };
};

export const transitionState = (frame, config) => {
  const spec = transitionSpec(config);
  if (frame < config.takeoverFrame) return {frame, phase: 'scene6', sourceFrame: frame};
  const push = ease((frame-config.takeoverFrame)/(config.pushFrames-1));
  const camera = {scale: 1+(spec.scale-1)*push, tx: spec.tx*push, ty: spec.ty*push};
  const match = ease((frame-spec.handoffStart)/(spec.screenMatchFrames-1));
  const settle = settleEase((frame-spec.settleStart)/(spec.settleFrames-1));
  const background = settleEase((frame-spec.settleStart)/((config.backgroundFadeFrames ?? 6)-1));
  const quad = frame < spec.settleStart
    ? config.screenQuad.map(([x,y]) => [x*camera.scale+camera.tx,y*camera.scale+camera.ty])
    : spec.zoomEndQuad.map((point,i) => point.map((value,axis) => value+(spec.frontQuad[i][axis]-value)*settle));
  return {frame, phase: frame >= spec.settleEnd ? 'scene7' : frame >= spec.settleStart ? 'phone-settle' :
    frame > spec.handoffStart ? 'screen-match' : 'push', ...camera,
    screenQuad: quad, clearQuad: spec.zoomEndQuad, screenOpacity: match,
    chassisOpacity: background, photoOpacity: 1-background,
    eraseOriginalScreen: frame >= spec.settleStart && background < 1,
    settleProgress: settle};
};

export const transitionAudioVolume = (frame, config) =>
  clamp((config.sourceFrameCount-frame)/config.audioFadeFrames);
