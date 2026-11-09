import React from 'react';
import {Composition,registerRoot} from 'remotion';
import {V2EndCard} from './EndCard';
import config from '../../manifests/v2-scene4-end-card-r1.json';

registerRoot(()=><Composition id="V2Scene4EndCard" component={V2EndCard}
  width={config.width} height={config.height} fps={config.fps}
  durationInFrames={config.durationInFrames}/>);
