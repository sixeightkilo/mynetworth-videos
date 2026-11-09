import React from 'react';
import {Img, staticFile} from 'remotion';
import {screenTransform} from './screenTransform.mjs';

// Everything uses the ORIGINAL screenshot's portrait coordinate system. The
// same projective plane carries glass, dashboard, rounded clipping and notch.
export const PhoneMockup = ({quad, config, model, screenOpacity = 1, chassisOpacity = 1, blank = false, children, flat = false}) => {
  const [width, height] = config.dashboardSize;
  const b = model.bezel;
  return <div style={{position: 'absolute', left: 0, top: 0, width, height,
    transformOrigin: '0 0', transform: screenTransform(quad, width, height), pointerEvents: 'none'}}>
    {chassisOpacity > 0 ? <div style={{position: 'absolute', left: -b, top: -b,
      width: width+2*b, height: height+2*b, borderRadius: model.outerRadius,
      background: flat ? '#11151a' : 'linear-gradient(90deg,#373a40 0%,#17191d 5%,#090a0d 48%,#1c1e23 94%,#454850 100%)',
      border: '3px solid #30333a', boxSizing: 'border-box',
      boxShadow: flat ? 'none' : '0 22px 40px rgba(0,0,0,0.16), inset 0 0 0 8px #101115',
      opacity: chassisOpacity}} /> : null}
    <div style={{position: 'absolute', inset: 0, width, height,
      overflow: 'hidden', borderRadius: model.screenRadius,
      background: blank ? '#e9f3fa' : '#090a0d', opacity: screenOpacity}}>
      {children ?? (!blank ? <Img src={staticFile(config.dashboard)} style={{width, height, display: 'block'}} /> : null)}
      {model.showNotch !== false ? <div style={{position: 'absolute', top: -1, left: (width-model.notchWidth)/2,
        width: model.notchWidth, height: model.notchHeight+1,
        background: '#090a0d', borderRadius: `0 0 ${model.notchRadius}px ${model.notchRadius}px`}}>
        <div style={{position: 'absolute', left: (model.notchWidth-104)/2, top: 17,
          width: 104, height: 8, background: '#25282e', borderRadius: 4}} />
        <div style={{position: 'absolute', left: model.notchWidth/2+94, top: 21,
          width: 18, height: 18, background: '#151b25', border: '2px solid #262d38',
          boxSizing: 'border-box', borderRadius: '50%'}} />
      </div> : null}
    </div>
  </div>;
};
