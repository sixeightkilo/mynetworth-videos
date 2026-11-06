import React from 'react';
import {AbsoluteFill, Audio, OffthreadVideo, Sequence, staticFile, useCurrentFrame} from 'remotion';
import config from '../../manifests/scene6-7.json';
import transition from '../../manifests/phone-transition.json';
import showcase from '../../manifests/scene7.json';
import {Scene6Transition} from '../scenes/Scene6Transition';
import {Scene7ProductShowcase} from '../scenes/Scene7ProductShowcase';
import {combinedPlan,combinedOffset} from '../transitions/combined-plan.mjs';
export const ApprovedScene6And7 = () => <AbsoluteFill>
  <Sequence durationInFrames={config.takeoverFrame}><OffthreadVideo muted src={staticFile(config.source)} style={{width:'100%',height:'100%',objectFit:'contain'}} /></Sequence>
  <Sequence durationInFrames={config.sourceFrameCount}><Audio src={staticFile(config.source)} volume={f=>Math.max(0,Math.min(1,(config.sourceFrameCount-f)/config.audioFadeFrames))} /></Sequence>
  <Sequence from={config.takeoverFrame} durationInFrames={config.approvedFrameCount-config.approvedStartFrame}>
    <OffthreadVideo muted src={staticFile(config.approved)} trimBefore={config.approvedStartFrame} style={{width:'100%',height:'100%',objectFit:'contain'}} />
  </Sequence>
</AbsoluteFill>;
const plan=combinedPlan(transition,showcase);
// Editable reconstruction is available separately; baked approved media remains the baseline.
export const EditableScene6And7 = () => {
  const f=useCurrentFrame(),[dx,dy]=combinedOffset(f,plan),t=Math.max(0,Math.min(1,(f-plan.joinFrame)/plan.crossfadeFrames));
  return <AbsoluteFill style={{background:transition.mockup.background}}>
    <Sequence durationInFrames={plan.joinFrame+plan.crossfadeFrames+1} layout="none"><AbsoluteFill style={{transform:`translate(${dx}px,${dy}px)`}}><Scene6Transition /></AbsoluteFill></Sequence>
    <Sequence from={plan.joinFrame} durationInFrames={showcase.durationInFrames} layout="none"><AbsoluteFill style={{opacity:t*t*(3-2*t)}}><Scene7ProductShowcase /></AbsoluteFill></Sequence>
  </AbsoluteFill>;
};
