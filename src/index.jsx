import React from 'react';
import {Composition, registerRoot} from 'remotion';
import {Film,Film1080p} from './compositions/Film';
import {ApprovedScene6And7,EditableScene6And7} from './compositions/Scene6And7';
import {Scene7ProductShowcase} from './scenes/Scene7ProductShowcase';
import film from '../manifests/approved-720p.json';
import showcase from '../manifests/scene7.json';
import combined from '../manifests/scene6-7.json';
registerRoot(() => <>
  <Composition id="ApprovedRoughCut720p" component={Film} width={1280} height={720} fps={24} durationInFrames={film.durationInFrames} />
  <Composition id="Production1080p" component={Film1080p} width={1920} height={1080} fps={24} durationInFrames={film.durationInFrames} />
  <Composition id="ApprovedScene6And7" component={ApprovedScene6And7} width={1280} height={720} fps={24} durationInFrames={combined.durationInFrames} />
  <Composition id="EditableScene6And7" component={EditableScene6And7} width={1280} height={720} fps={24} durationInFrames={combined.durationInFrames} />
  <Composition id="EditableScene7" component={Scene7ProductShowcase} width={1280} height={720} fps={24} durationInFrames={showcase.durationInFrames} />
</>);
