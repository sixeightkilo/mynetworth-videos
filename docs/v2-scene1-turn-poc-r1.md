# V2 Scene 1 — one-second phone-turn POC

Review: `out/v2-scene1-turn-poc-r1/review/scene-01-turn-dashboard-720p-r1.mp4`.
Comparison: `out/v2-scene1-turn-poc-r1/review/scene-01-turn-before-after-r1.mp4` (wide context above paired phone close-ups).
Contact sheet: `out/v2-scene1-turn-poc-r1/review/scene-01-turn-contact-r1.jpg`.
Native-resolution master and JSON report are alongside these files.

The POC covers source frames [420,444), 17.5–18.5 seconds: exactly 24 video frames / one second at 24fps. Source remains the approved `production/v2/scene-01/output/scene-01.mp4`, 1284×724, SHA256 `0260e671fd1757db2b030a22cfa82642ded971f7debe59f32faa3420a73b67af`. The real dashboard is `public/screenshots/dashboard-original.png`, the same screenshot used for the approved end-frame composite and Scene 2 transition.

Frames 420–425 stay unchanged before encoding, preserving the back-facing and near-edge-on phone. The dashboard enters on frame 426 (17.75s), initially at 0.65 opacity, then 0.9 at 427 and fully opaque at 428. No synthetic notch/hole or camera cutout is added. Original blurred fingers use source-pixel skin holdouts; they are not reconstructed or sharpened. No blanket mask erosion introduces an inset border. The rounded aperture and dashboard are warped at 4× local sampling and downsampled for antialiasing; the original room/characters are not regenerated or recolored.

Geometry is hybrid: screen edge-fit proposals were manually reviewed frame by frame, with explicit manual corner annotations at 426–427 where the automatic proposals failed. Every visible frame has its own reviewed corners, retaining the nonlinear motion without linear corner interpolation or blanket smoothing. Adjacent-frame LK forward/backward tests and RANSAC independently check the motion. The optical-flow estimates at 427–429 are rejected for too few inliers; they are never used to move the dashboard. These earliest blurred frames remain the least certain. Checks become more useful once the display faces forward; from frame 435 onward, differences between independent motion predictions and annotations stay around one native pixel. These are consistency diagnostics, not ground-truth tracking accuracy.

Implementation: `scripts/composite_phone_turn_poc.py`, `manifests/v2-scene1-turn-poc-r1.json`, using the existing optional OpenCV/NumPy environment. The v1 technique is reused, adapted for the smaller screen, dense manual review, no notch, supersampled edges and explicit BT.709 encoding. The original input/reference assets and all previous scene renders remain unchanged.

Native working output preserves 1284×724. The 720p review fits proportionally into 1280×720 with small white side padding; there is no stretching of the original phone. Final endpoint alignment to the user’s separate 1280×720 reference still must be handled when the full visible interval is authorized. This one-second sample does not reach the Scene 1→2 boundary.

Original AAC audio is stream-copied into the excerpt. Decoded audio matches the original timestamp selection at zero lag (correlation 1.0). Video tracks are exactly one second; AAC edit-list/padding makes containers approximately 1.007 seconds. Full decode passed for native, 720p and comparison exports. Their range, primaries, transfer and matrix are explicitly BT.709 limited range to avoid the old RGB/YUV color-matrix problem.

Run only on fresh output paths:

```sh
out/scene04-notch/venv/bin/python scripts/composite_phone_turn_poc.py manifests/v2-scene1-turn-poc-r1.json
```

The program refuses to overwrite outputs and asserts unchanged source hashes and outside-matte pixels before encoding. Only the requested one-second POC was processed. No full-scene replacement, assembly modification or commit was performed. Stop for review before extension.

## Playback compatibility copies

The user reported a stream-format playback error. The initial files fully decode in FFmpeg, but stream-copied AAC contains unusual packet preroll/edit-list history for this short excerpt. Preferred review files now have suffix `-compatible.mp4`: the 720p preview and before/after comparison. Both preserve all 24 decoded video frames exactly, re-encode only the original 17.5–18.5s audio excerpt as AAC-LC stereo 48kHz, normalize timestamps, and have exactly 1.000s container duration. Full decode passed. Existing initial POC files and original source remain untouched. The helper now normalizes excerpt audio for future POCs.
