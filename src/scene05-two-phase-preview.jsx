import React from 'react';
import {Composition,registerRoot} from 'remotion';
import {Scene5TwoPhase} from './scenes/Scene5TwoPhase';
import c from '../manifests/scene05-two-phase-v5.json';
registerRoot(()=><Composition id="Scene05TwoPhasePreview" component={Scene5TwoPhase}
 width={c.width} height={c.height} fps={c.fps} durationInFrames={c.durationInFrames}/>);
