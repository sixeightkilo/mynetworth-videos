import React from 'react';
import {Composition,registerRoot} from 'remotion';
import {V2Segment2,V2Segments1And2} from './Segment2';
import config from '../../manifests/v2-segment2-r4.json';
registerRoot(()=><>
  <Composition id="V2Segment2Preview" component={V2Segment2} width={config.width} height={config.height}
    fps={config.fps} durationInFrames={config.durationInFrames}/>
  <Composition id="V2Segments1And2Preview" component={V2Segments1And2} width={config.width} height={config.height}
    fps={config.fps} durationInFrames={config.segment1.frames+config.durationInFrames}/>
  <Composition id="V2Segment1To2BoundaryPreview" component={V2Segments1And2} width={config.width} height={config.height}
    fps={config.fps} durationInFrames={48+config.durationInFrames}
    defaultProps={{sourceStartFrame:config.segment1.frames-48,sourceDurationInFrames:48}}/>
</>);
