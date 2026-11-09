# V2 Scene 1 — complete dashboard composite r1

User approved the one-second phone-turn test and authorized completion. Original source and approved POC media remain untouched; no existing assembly or Scene 2 render was changed.

## Outputs

All review files are under `out/v2-scene1-dashboard-full-r1/review/`:

- `scene-01-dashboard-720p-r1.mp4`: review master, 1280×720, 24fps, 505 frames / 21.041667 seconds.
- `scene-01-dashboard-native-r1.mp4`: native 1284×724 master, same timeline.
- `scene-01-to-02-boundary-r1.mp4`: final second followed by two seconds of accepted Scene 2 r4.
- `scene-01-dashboard-contact-r1.jpg`: paired phone crops across retrieval, rotation and hold.
- `scene-01-dashboard-wide-r1.jpg`: wider checkpoints.
- `scene-01-to-02-endpoint-comparison.jpg`: final Scene 1 / approved Scene 2 opening comparison.
- `scene-01-dashboard-full-r1-report.json`: metadata, diagnostics, hashes and audio verification.

## Implementation

`manifests/v2-scene1-dashboard-full-r1.json` and `scripts/composite_scene1_full.py` reuse the accepted POC compositor. Reviewed native-coordinate corners 426–443 are preserved exactly. Reviewed edge-fit proposals extend the track through frame 504; adjacent-frame flow is diagnostic only. Before frame 426 the source is unchanged before encoding/output sizing. Original dashboard, rounded antialiased aperture and source finger holdouts are reused. No notch is added. No tracking interpolation or blanket smoothing replaces the measured motion.

A smooth subpixel aperture-definition correction after the POC (maximum 0.993 native pixel) brings the final screen to the approved reference geometry. Fixed proportional output alignment measured from 1106 feature inliers matches the supplied 720p reference; it does not stretch the image. Native output is also retained. The 720p last frame and Scene 2 opening align closely; minor resampling/encoding differences remain (outside-phone mean absolute RGB difference 2.33/255; inside 5.52/255), so the handoff is not pixel-identical.

Original full-length AAC is stream-copied into both masters. Decoded PCM bytes match the original exactly. Source SHA256 remains `0260e671fd1757db2b030a22cfa82642ded971f7debe59f32faa3420a73b67af`. Both masters decode and retain 505 frames at 24fps. `npm run verify` passes (22 assets, 1349 approved baseline frames); `git diff --check` passes. No browser render is involved.

The brief blurred rotation at frames 426–429 retains the accepted manual geometry and original hand blur. Small source-screen detail remains limited by the original shot resolution. No sharpening or finger reconstruction is applied.

## Reproduce

With the existing OpenCV/NumPy environment:

```sh
out/scene04-notch/venv/bin/python scripts/composite_scene1_full.py manifests/v2-scene1-dashboard-full-r1.json
```

Renderer refuses to overwrite outputs. Use a fresh configured output directory for another run. No commit or integration was requested; stop for review.
