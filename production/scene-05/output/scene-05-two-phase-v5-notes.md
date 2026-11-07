# Scene 05 — two-phase transition v5

Current review files:

- `scene-05-two-phase-v5.mp4`: standalone, 1920×1080, 24fps, 120 frames / 5 seconds. Its AAC track is digitally silent (decoded PCM peak 0).
- `scene-04-05-two-phase-preview-v5.mp4`: combined preview, 241 frames / 10.041667 seconds; original Scene 04 AAC copied unchanged and verified PCM-identical.
- `scene-05-two-phase-v5-contact.jpg`: rendered video contact sheet.
- `scene-05-two-phase-v5-validation-contact.jpg`: four validation stills rendered before the full video.
- `scene-05-two-phase-v5-edges-200pct.png`: native 1080p edge crops enlarged 200% without interpolation.
- `scene-05-two-phase-v5-report.json`: validation evidence and input/output details.

## Two phases

Phase A (frames 0–60): freeze the exact approved Scene 04 final frame and push toward the measured screen plane. Stop with an 840px display height. All four display corners and the outer reconstructed bezel remain inside the viewport. The original scene, hand and fingertips move only through the virtual camera transform.

Phase B (frames 60–108): clear the frozen room/hand over frames 60–72, holding the phone plane fixed. Then interpolate all four shared phone-plane corners over frames 72–108 to the final front-facing showcase pose. Bezel, notch and dashboard use one projective transform in `PhoneMockup`; there is no independent screen rotation. The entire original 864×1872 dashboard remains visible. Final hold: frames 108–119.

The final phone center is (1320,540), phone height 960, with the exact existing showcase model and original portrait screen aspect ratio. No isolated graph crop is introduced. The final frame matches the phone framing of the current app showcase, without adding its captions or branding.

## Geometry reconstruction

The source image's raster phone footprint is removed in a separate derived background using conventional OpenCV inpainting, then covered by clean geometric phone geometry. Foreground fingertips are held out from original RGB pixels using manual domains and conventional mattes; dark old-bezel pixels are rejected. No fingers are synthesized, reconstructed or sharpened. Background and finger layers share the frozen camera transform and fade together before the phone-plane morph.

The bezel, screen aperture, rounded corners and notch are mathematical geometry. Four validation frames (0,60,84,119) were rendered at 3840×2160 before rendering the full video. They were downsampled and inspected at native 1080p and at 200% edge magnification. Initial matte tests exposed old raster-bezel contamination; those pixels were excluded before the final validation and full render.

The full render was also produced at 3840×2160, then Lanczos downsampled to 1920×1080 for edge antialiasing. The entire phone was not blurred. This is supersampling of graphics, not a claim of native 4K source-footage detail.

## Passed checks

- Every display and outer-bezel corner remains in view across all 120 frames; minimum outer-bezel viewport margin is 60px.
- Phase A phone/display plane is unchanged relative to the camera. Phase B uses a single shared transform for phone frame and screen.
- No dashboard crop during Phase B; unchanged original screenshot used throughout.
- Final model, center, scale and 864:1872 screen ratio match the existing showcase.
- Both final videos fully decode. Geometry, 24fps and frame counts pass.
- Source, approved Scene 04 and POC checksums remain unchanged. Original baseline verification still passes.

## Remaining limits

The clean bezel uses the existing showcase design; it approximates the original physical bezel texture rather than recovering detail from the low-resolution phone region. Original fingers and room retain their source softness under magnification; small matte softness remains at fingertip overlaps. The Phase B room/hand removal is an intentional graphic handoff, not new physical motion.

## Implementation

- `src/scene05-two-phase-preview.jsx`: separate preview entry.
- `src/scenes/Scene5TwoPhase.jsx`: layer assembly.
- `src/transitions/scene05-two-phase.mjs`: shared camera/plane geometry.
- `manifests/scene05-two-phase-v5.json`: measured corners and phase timings.
- `scripts/prepare_scene05_two_phase.py`: derived plate/foreground preparation; refuses to overwrite its outputs.

No source assets, previous renders, approved film assembly or existing app showcase were changed. No Kling or generative AI tool was used. Stop for review before integration.
