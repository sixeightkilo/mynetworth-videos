import React from 'react';
import {AbsoluteFill,Img,staticFile,useCurrentFrame} from 'remotion';
import {PhoneMockup} from '../components/PhoneMockup';
import {scene05TwoPhaseState} from '../transitions/scene05-two-phase.mjs';
import config from '../../manifests/scene05-two-phase-v5.json';
export const Scene5TwoPhase=()=>{
 const s=scene05TwoPhaseState(useCurrentFrame(),config);
 const photoStyle={position:'absolute',left:0,top:0,width:config.width,height:config.height,
  transformOrigin:'0 0',transform:`matrix(${s.scale},0,0,${s.scale},${s.tx},${s.ty})`};
 return <AbsoluteFill style={{backgroundColor:config.model.background}}>
  <AbsoluteFill style={{opacity:s.photoOpacity}}>
   <Img src={staticFile(config.backgroundImage)} style={photoStyle}/>
   <Img src={staticFile(config.startImage)} style={{...photoStyle,opacity:1-s.takeover}}/>
  </AbsoluteFill>
  {/* One shared projective transform carries BOTH geometric bezel and dashboard. */}
  <AbsoluteFill style={{opacity:s.takeover}}>
   <PhoneMockup quad={s.quad} config={config} model={config.model}/>
  </AbsoluteFill>
  <AbsoluteFill style={{opacity:s.takeover*s.photoOpacity}}>
   <Img src={staticFile(config.fingerImage)} style={photoStyle}/>
  </AbsoluteFill>
 </AbsoluteFill>;
};
