import React from 'react';
import {AbsoluteFill, Audio, Freeze, Img, OffthreadVideo, Sequence, staticFile, useCurrentFrame} from 'remotion';
import {PhoneMockup} from '../components/PhoneMockup';
import {screenTransform} from '../components/screenTransform.mjs';
import {scene05TwoPhaseState} from '../transitions/scene05-two-phase.mjs';
import defaults from '../../manifests/v2-segment2-r4.json';

const clamp=(v)=>Math.max(0,Math.min(1,v));
const ease=(v)=>{const t=clamp(v);return t*t*(3-2*t);};
const appear=(frame,from,duration)=>ease((frame-from)/duration);

const Recording=({clip,config})=>{
  const frame=useCurrentFrame();
  const [width,height]=config.dashboardSize;
  const opacity=clip.fromFrame===0?1:appear(frame,0,config.timeline.screenFadeFrames);
  return <div style={{position:'absolute',inset:0,opacity}}>
    {/* Only freeze the outgoing overlap. Remotion 4 Freeze resets sequence offsets;
        subtract this sequence start to keep the held media time local. */}
    <Freeze active={frame>=clip.durationInFrames} frame={clip.durationInFrames-1-clip.fromFrame}>
      {clip.image?<Img src={staticFile(clip.image)} style={{width,height,display:'block',objectFit:config.recordingFit ?? 'contain'}}/>:
        <OffthreadVideo src={staticFile(clip.file)} muted trimBefore={clip.sourceStartSeconds*config.fps}
          style={{width,height,display:'block',objectFit:config.recordingFit ?? 'contain'}}/>}
    </Freeze>
  </div>;
};

export const V2Segment2=({config=defaults})=>{
  const frame=useCurrentFrame();
  const c=config,t=c.timeline;
  const sourceScale=c.height/(c.approvedReference?.height ?? c.segment1.height);
  const sourceOffset=(c.width-(c.approvedReference?.width ?? c.segment1.width)*sourceScale)/2;
  const screenQuad=c.segment1.screenQuad.map(([x,y])=>[x*sourceScale+sourceOffset,y*sourceScale]);
  const state=scene05TwoPhaseState(frame,{...c,...c.transition,model:c.phoneModel,screenQuad});
  const camera={position:'absolute',width:c.width,height:c.height,transformOrigin:'0 0',
    transform:`matrix(${state.scale},0,0,${state.scale},${state.tx},${state.ty})`};
  const brandOpacity=appear(frame,t.brandFromFrame,t.captionFadeFrames);
  const aggregationOpacity=1-appear(frame,t.aggregationEndFrame,t.captionFadeFrames);
  const featureOpacity=appear(frame,t.sipFromFrame,t.captionFadeFrames);
  const captionStyle=(from)=>({opacity:appear(frame,from,t.captionFadeFrames),
    transform:`translateY(${8*(1-appear(frame,from,t.captionFadeFrames))}px)`});
  return <AbsoluteFill style={{background:c.background,color:c.ink,fontFamily:c.fontFamily}}>
    <AbsoluteFill style={{opacity:state.photoOpacity}}>
      <Img src={staticFile(c.segment1.finalImage)} style={{...camera,objectFit:'contain'}}/>
      {c.approvedReference && !c.transition.cleanScreenGeometry ? <div style={{...camera,opacity:appear(frame,0,3),
        maskImage:`url(${staticFile(c.approvedReference.maskFile)})`,WebkitMaskImage:`url(${staticFile(c.approvedReference.maskFile)})`,
        maskSize:'100% 100%',WebkitMaskSize:'100% 100%',maskRepeat:'no-repeat',WebkitMaskRepeat:'no-repeat'}}>
        <div style={{position:'absolute',width:c.dashboardSize[0],height:c.dashboardSize[1],transformOrigin:'0 0',
          transform:screenTransform(screenQuad,...c.dashboardSize)}}>
          <Img src={staticFile(c.approvedReference.dashboardFile)} style={{width:c.dashboardSize[0],height:c.dashboardSize[1],display:'block'}}/>
        </div>
      </div> : null}
    </AbsoluteFill>
    <div style={{position:'absolute',inset:0,opacity:c.transition.cleanScreenGeometry?appear(frame,0,c.transition.cleanGeometryFadeFrames):1}}>
    <PhoneMockup quad={state.quad} config={c} model={c.phoneModel} flat
      chassisOpacity={c.transition.cleanScreenGeometry ? 1 : appear(frame,c.transition.phaseAEndFrame,c.transition.backdropClearEndFrame-c.transition.phaseAEndFrame)}
      screenOpacity={c.transition.cleanScreenGeometry ? 1 : c.transition.screenOverlayStartFrame!==undefined ? appear(frame,c.transition.screenOverlayStartFrame,c.transition.screenOverlayFadeFrames) : c.transition.dashboardFromFirstFrame?1:appear(frame,0,c.transition.takeoverFrames)}>
      {Object.entries(c.recordings).map(([id,clip])=><Sequence key={id} from={clip.fromFrame}
        durationInFrames={Math.min(clip.durationInFrames+t.screenFadeFrames,c.durationInFrames-clip.fromFrame)} layout="none">
        <Recording clip={clip} config={c}/>
      </Sequence>)}
    </PhoneMockup>
    </div>
    <div style={{position:'absolute',left:0,top:0,width:1920,height:1080,transformOrigin:'0 0',transform:`scale(${c.layoutScale ?? 1})`}}>
    <div style={{position:'absolute',left:150,top:94,display:'flex',alignItems:'center',gap:24,opacity:brandOpacity}}>
      <Img src={staticFile(c.logo)} style={{width:70,height:84,objectFit:'contain'}}/>
      <div style={{fontSize:64,fontWeight:700,letterSpacing:-1.8}}>{c.text.brand}</div>
    </div>
    <div style={{position:'absolute',left:160,top:285,width:900,opacity:aggregationOpacity}}>
      {c.text.investments.map((text,i)=><div key={text} style={{...captionStyle(t.investmentFrames[i]),fontSize:64,lineHeight:'88px',fontWeight:500,letterSpacing:-1}}>{text}</div>)}
      <div style={{...captionStyle(t.taglineFromFrame),marginTop:38,width:920,fontSize:52,lineHeight:1.22,fontWeight:700,letterSpacing:-1.3}}>{c.text.tagline}</div>
    </div>
    <div style={{position:'absolute',left:160,top:350,width:940,opacity:featureOpacity}}>
      {c.text.features.map((text,i)=><div key={text} style={{...captionStyle([t.sipFromFrame,t.casFromFrame,t.reportsFromFrame][i]),
        display:'flex',alignItems:'center',gap:25,fontSize:58,lineHeight:'110px',fontWeight:500,letterSpacing:-1}}>
        <span style={{color:c.green,fontSize:60,fontWeight:700}}>✓</span><span>{text}</span>
      </div>)}
    </div>
    <div style={{position:'absolute',left:100,right:100,top:920,textAlign:'center',opacity:appear(frame,t.privacyFromFrame,t.captionFadeFrames)}}>
      <div style={{fontSize:42,lineHeight:'57px',fontWeight:400}}>{c.text.privacyFirst}</div>
      <div style={{fontSize:48,lineHeight:'62px',fontWeight:700,letterSpacing:-.7}}>{c.text.privacySecond}</div>
    </div>
    </div>
    {c.music.file?<Audio src={staticFile(c.music.file)} volume={(f)=>c.music.volume*
      ease(f/c.music.fadeInFrames)*ease((c.durationInFrames-1-f)/c.music.fadeOutFrames)}/>:null}
  </AbsoluteFill>;
};

export const V2Segments1And2=({config=defaults,sourceStartFrame=0,sourceDurationInFrames=defaults.segment1.frames})=><AbsoluteFill style={{background:'#FFFFFF'}}>
  <Sequence durationInFrames={sourceDurationInFrames}>
    <OffthreadVideo src={staticFile(config.segment1.file)} trimBefore={sourceStartFrame}
      style={{width:config.width,height:config.height,objectFit:'contain'}}/>
  </Sequence>
  <Sequence from={sourceDurationInFrames} durationInFrames={config.durationInFrames}>
    <V2Segment2 config={config}/>
  </Sequence>
</AbsoluteFill>;
