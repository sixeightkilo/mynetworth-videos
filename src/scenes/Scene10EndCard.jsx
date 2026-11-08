import React from 'react';
import {AbsoluteFill,Img,staticFile,useCurrentFrame} from 'remotion';
import config from '../../manifests/scene10-end-card-v2.json';

export const Scene10EndCard=()=>{
 const frame=useCurrentFrame();
 const t=Math.max(0,Math.min(1,frame/config.fadeFrames));
 const opacity=t*t*(3-2*t);
 return <AbsoluteFill>
  <Img src={staticFile(config.startImage)} style={{width:1920,height:1080}}/>
  <AbsoluteFill style={{backgroundColor:config.background,opacity}}/>
  <AbsoluteFill style={{opacity,color:'#F7FAFF',fontFamily:config.fontFamily,textAlign:'center'}}>
   <Img src={staticFile(config.logo)} style={{position:'absolute',top:142,left:901,width:118,height:140,objectFit:'contain'}}/>
   <div style={{position:'absolute',top:322,left:120,width:1680,fontSize:104,lineHeight:'126px',fontWeight:700,letterSpacing:-3}}>{config.text.product}</div>
   <div style={{position:'absolute',top:460,left:140,width:1640,fontSize:43,lineHeight:'58px',fontWeight:400,color:'#CAD5E5',letterSpacing:-.5}}>{config.text.tagline}</div>
   <div style={{position:'absolute',top:590,left:160,width:1600,fontSize:36,lineHeight:'48px',fontWeight:400,color:'#D6E0EE'}}>{config.text.platform}</div>
   <div style={{position:'absolute',top:673,left:160,width:1600,fontSize:66,lineHeight:'84px',fontWeight:700,color:'#69D1F2',letterSpacing:-1}}>{config.text.website}</div>
   <div style={{position:'absolute',top:798,left:160,width:1600,fontSize:30,lineHeight:'42px',fontWeight:400,color:'#A7B8D0'}}>{config.text.download}</div>
  </AbsoluteFill>
 </AbsoluteFill>;
};
