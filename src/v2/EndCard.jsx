import React from 'react';
import {AbsoluteFill, Audio, Img, staticFile, useCurrentFrame} from 'remotion';
import defaults from '../../manifests/v2-scene4-end-card-r1.json';

const smooth=(v)=>{const t=Math.max(0,Math.min(1,v));return t*t*(3-2*t);};

export const V2EndCard=({config=defaults})=>{
  const frame=useCurrentFrame();
  const c=config;
  const reveal=(key)=>{const [a,b]=c.timing[key];return smooth((frame-a)/(b-a));};
  return <AbsoluteFill style={{background:c.background,color:c.ink,fontFamily:c.fontFamily,alignItems:'center'}}>
    <div style={{position:'absolute',top:112,height:90,display:'flex',alignItems:'center',gap:24,opacity:reveal('brand')}}>
      <Img src={staticFile(c.logo)} style={{width:70,height:84,objectFit:'contain'}}/>
      <div style={{fontSize:58,fontWeight:700,letterSpacing:-1.8}}>{c.text.brand}</div>
    </div>
    <div style={{position:'absolute',top:268,width:'100%',textAlign:'center',fontSize:38,fontWeight:700,letterSpacing:-.8,opacity:reveal('primary')}}>{c.text.primary}</div>
    <div style={{position:'absolute',top:360,display:'flex',flexDirection:'column',alignItems:'center',fontSize:31,color:c.blue,opacity:reveal('secondary')}}>
      <div>{c.text.secondary}</div>
      <div style={{marginTop:10,width:'100%',height:2,background:c.blue,transformOrigin:'left center',transform:`scaleX(${reveal('underline')})`}}/>
    </div>
    <div style={{position:'absolute',top:482,width:'100%',textAlign:'center',opacity:reveal('details')}}>
      <div style={{fontSize:43,fontWeight:700,letterSpacing:-.8}}>{c.text.website}</div>
      <div style={{marginTop:25,fontSize:23,color:c.ink}}>{c.text.instruction}</div>
    </div>
    {c.music.file?<Audio src={staticFile(c.music.file)} volume={(f)=>c.music.volume*smooth(f/10)*smooth((c.durationInFrames-1-f)/c.music.fadeOutFrames)}/>:null}
  </AbsoluteFill>;
};
