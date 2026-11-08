import React from 'react';
import {AbsoluteFill,OffthreadVideo,Sequence,staticFile} from 'remotion';
import {Scene10EndCard} from '../scenes/Scene10EndCard';
import config from '../../manifests/scene10-end-card-v2.json';

// Separate current-production review composition; original approvals stay intact.
// Use the public directory prepared by scripts/prepare_scene10_end_card.py.
export const Scenes01To10Review=()=> <AbsoluteFill>
 <Sequence durationInFrames={config.prefixFrames}>
  <OffthreadVideo src={staticFile(config.prefixVideo)} style={{width:1920,height:1080}}/>
 </Sequence>
 <Sequence from={config.prefixFrames} durationInFrames={config.durationInFrames}>
  <Scene10EndCard/>
 </Sequence>
</AbsoluteFill>;
