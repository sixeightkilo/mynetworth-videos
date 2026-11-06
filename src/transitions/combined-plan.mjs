import {transitionSpec} from './phone-transition.mjs';

// Combined-preview positioning only; individual scene implementations stay intact.
export const combinedPlan = (transition, showcase) => {
  if (transition.fps !== showcase.fps) throw new Error('Scene frame rates must match');
  const spec = transitionSpec(transition);
  return {
    fps: transition.fps,
    joinFrame: spec.settleEnd + 1,
    moveStart: spec.settleStart + (transition.backgroundFadeFrames ?? 6) - 1,
    moveEnd: spec.settleEnd,
    dx: showcase.phoneCenter[0] - transition.targetCenter[0],
    dy: showcase.phoneCenter[1] - transition.targetCenter[1],
    crossfadeFrames: showcase.transitionFrames,
    durationInFrames: spec.settleEnd + 1 + showcase.durationInFrames,
  };
};

export const combinedOffset = (frame, plan) => {
  const t = Math.max(0, Math.min(1, (frame-plan.moveStart)/(plan.moveEnd-plan.moveStart)));
  const ease = t*t*t*(t*(t*6-15)+10);
  return [plan.dx*ease, plan.dy*ease];
};
