import React from 'react';
import {AbsoluteFill, Img, OffthreadVideo, Sequence, useCurrentFrame} from 'remotion';
import {staticFile} from 'remotion';
import config from '../../manifests/approved-720p.json';

const EndCard = () => {
  const frame = useCurrentFrame();
  return <AbsoluteFill style={{opacity:Math.min(1,frame/config.endCard.fadeFrames)}}>
    <Img src={staticFile(config.endCard.file)} style={{width:'100%',height:'100%'}} />
  </AbsoluteFill>;
};
export const Film = () => <AbsoluteFill style={{background:'#000'}}>
  {config.clips.map((clip,index) => <Sequence key={clip.file} from={clip.fromFrame} durationInFrames={clip.durationInFrames}>
    <OffthreadVideo src={staticFile(clip.file)}
      volume={index === config.clips.length-1 ? frame => Math.max(0,Math.min(1,(clip.durationInFrames-frame)/config.endCard.fadeFrames)) : 1}
      style={{width:'100%',height:'100%',objectFit:'contain'}} />
  </Sequence>)}
  <Sequence from={config.endCard.fromFrame} durationInFrames={config.endCard.durationInFrames}><EndCard /></Sequence>
</AbsoluteFill>;
// Same 720p design space; changing output dimensions does not rearrange approved content.
export const Film1080p = () => <AbsoluteFill style={{background:'#000'}}>
  <div style={{position:'absolute',width:1280,height:720,transform:'scale(1.5)',transformOrigin:'0 0'}}><Film /></div>
</AbsoluteFill>;
