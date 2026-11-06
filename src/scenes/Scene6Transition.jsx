import React from 'react';
import {AbsoluteFill, Audio, Img, OffthreadVideo, Sequence, staticFile, useCurrentFrame} from 'remotion';
import config from '../../manifests/phone-transition.json';
import {transitionAudioVolume, transitionState} from '../transitions/phone-transition.mjs';
import {transitionSpec} from '../transitions/phone-transition.mjs';
import {PhoneMockup} from '../components/PhoneMockup';

export const Scene6Transition = () => {
  const frame = useCurrentFrame();
  const state = transitionState(frame, config);
  const spec = transitionSpec(config);
  return (
    <AbsoluteFill style={{backgroundColor: spec.model.background}}>
      <Sequence durationInFrames={config.sourceFrameCount} layout="none">
        <Audio src={staticFile(config.video)} volume={(audioFrame) => transitionAudioVolume(audioFrame, config)} />
      </Sequence>
      {state.phase === 'scene6' ? (
        <OffthreadVideo src={staticFile(config.video)} muted
          style={{width: config.width, height: config.height, objectFit: 'fill'}} />
      ) : (
        <>
          {state.photoOpacity > 0 ? <AbsoluteFill style={{opacity: state.photoOpacity}}>
            <Img src={staticFile(config.flattenedPng)} style={{
              position: 'absolute', left: 0, top: 0, width: config.width, height: config.height,
              transformOrigin: '0 0',
              transform: `matrix(${state.scale},0,0,${state.scale},${state.tx},${state.ty})`,
            }} />
            {/* Once the aligned high-resolution screen is opaque, clear the
                baked dashboard beneath it. No second UI can ghost as the new
                phone settles; the source PNG on disk remains unchanged. */}
            {state.eraseOriginalScreen ? <PhoneMockup quad={state.clearQuad} config={config}
              model={spec.model} blank chassisOpacity={0} /> : null}
          </AbsoluteFill> : null}
          <PhoneMockup quad={state.screenQuad} config={config} model={spec.model}
            screenOpacity={state.screenOpacity} chassisOpacity={state.chassisOpacity} />
        </>
      )}
    </AbsoluteFill>
  );
};
