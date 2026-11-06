import React from 'react';
import {AbsoluteFill, Img, OffthreadVideo, Sequence, staticFile, useCurrentFrame} from 'remotion';
import {PhoneMockup} from '../components/PhoneMockup';
import {screenTransform} from '../components/screenTransform.mjs';
import transition from '../../manifests/phone-transition.json';
import config from '../../manifests/scene7.json';

const model = transition.mockup;
const [width, height] = transition.dashboardSize;
const scale = model.height / (height + 2 * model.bezel);
const [cx, cy] = config.phoneCenter;
const quad = [[cx-width*scale/2,cy-height*scale/2], [cx+width*scale/2,cy-height*scale/2],
  [cx+width*scale/2,cy+height*scale/2], [cx-width*scale/2,cy+height*scale/2]];

const Feature = ({feature}) => {
  const frame = useCurrentFrame();
  // Incoming layers fade over the outgoing feature. The chassis never moves.
  const progress = feature.fromFrame === 0 ? 1 : Math.min(1, frame/config.transitionFrames);
  const opacity = progress*progress*(3-2*progress);
  let clipEnd = 0;
  const activeClip = feature.clips.find(clip => {
    clipEnd += clip.durationInFrames;
    return frame < clipEnd;
  });
  let offset = 0;
  return <>
    <div style={{position:'absolute',left:96,top:290,width:510,minHeight:220,
      background:model.background,opacity,display:'flex',flexDirection:'column',justifyContent:'center',alignItems:'flex-start'}}>
      <div style={{fontSize:44,lineHeight:1.17,fontWeight:600,letterSpacing:-1.2}}>{feature.caption}</div>
      {activeClip?.label ? <div style={{fontSize:20,color:'#61656b',marginTop:20}}>{activeClip.label}</div> : null}
    </div>
    <div style={{position:'absolute',width,height,transformOrigin:'0 0',
      transform:screenTransform(quad,width,height),opacity}}>
      <div style={{position:'absolute',inset:0,borderRadius:model.screenRadius,overflow:'hidden',background:'#fff'}}>
        {feature.clips.map((clip,index) => {
          const from = offset;
          offset += clip.durationInFrames;
          return <Sequence key={index} from={from} durationInFrames={clip.durationInFrames} layout="none">
            {/* Remotion trim frames use composition fps: timestamp * 24, never the VFR source frame index. */}
            {clip.stillImage ? <Img src={staticFile(clip.stillImage)}
              style={{width,height,display:'block',objectFit:'contain'}} /> : <OffthreadVideo src={staticFile(clip.file ?? feature.file)} muted
              trimBefore={clip.sourceStartSeconds*config.fps}
              style={{width,height,display:'block',objectFit:'contain'}} />}
          </Sequence>;
        })}
      </div>
      <div style={{position:'absolute',top:-1,left:(width-model.notchWidth)/2,
        width:model.notchWidth,height:model.notchHeight+1,background:'#090a0d',
        borderRadius:`0 0 ${model.notchRadius}px ${model.notchRadius}px`}}>
        <div style={{position:'absolute',left:(model.notchWidth-104)/2,top:17,width:104,height:8,background:'#25282e',borderRadius:4}} />
        <div style={{position:'absolute',left:model.notchWidth/2+94,top:21,width:18,height:18,
          background:'#151b25',border:'2px solid #262d38',boxSizing:'border-box',borderRadius:'50%'}} />
      </div>
    </div>
  </>;
};

export const Scene7ProductShowcase = () => <AbsoluteFill style={{background:model.background,
  color:'#17191d',fontFamily:'Arial, sans-serif'}}>
  <div style={{position:'absolute',left:96,top:80,display:'flex',alignItems:'center',gap:20}}>
    <Img src={staticFile('branding/logo.png')} style={{width:64,height:76,objectFit:'contain'}} />
    <div style={{fontSize:40,fontWeight:700,letterSpacing:-1}}>MyNetWorth</div>
  </div>
  <PhoneMockup quad={quad} config={transition} model={model} blank screenOpacity={0} />
  {config.features.map(feature => <Sequence key={feature.id} from={feature.fromFrame}
    durationInFrames={feature.clips.reduce((sum,clip)=>sum+clip.durationInFrames,0)} layout="none">
    <Feature feature={feature} />
  </Sequence>)}
</AbsoluteFill>;
