# V2 Scene 04 — white end card r1

Remotion entry: `src/v2/end-card-entry.jsx`; component: `src/v2/EndCard.jsx`; configuration: `manifests/v2-scene4-end-card-r1.json`.

The actual shield logo is the same asset used in Scene 02 r4: `production/v1/scene-10/references/logo-transparent-srgb-v2.png`. Product-name typography matches the existing showcase (DejaVu Sans, navy #142238). Background is pure white. No invented icon, extra claims, platform text, narration or effects.

At 24fps the brand fades over frames 0–10, primary tagline 8–18, privacy line 16–26, underline extends left-to-right 20–36, and website/instruction fade 26–36. All elements hold stationary at full visibility from frame 36 through 119 (3.5 seconds). No licensed/configured music asset exists in the showcase; music remains null/configurable, with a one-second end fade if later supplied. Current end card has a silent AAC track for compatible assembly.

## Outputs

- `production/v2/scene-04/output/scene-04-end-card-r1-720p.mp4`: 1280×720 H.264, 24fps, 120 frames / 5 seconds.
- `production/v2/scene-04/output/scene-04-end-card-r1.png`: final card still.
- `production/v2/output/scene-01-04-review-r1.mp4`: 1418 frames / 59.083333 seconds, same resolution/fps, direct append at frame 1298 / 54.083333 seconds.
- Accompanying full-film JSON records source checksums and verification.

All 1298 earlier decoded video frames and all 120 end-card frames match their inputs exactly. Original media remain unchanged. Existing dialogue is retained; the joined AAC soundtrack is re-encoded at 48kHz/192kbps. No added music. Full decode, source hash checks, approved-asset verification and whitespace checks pass. The actual Remotion browser render succeeded outside the sandbox; initial restricted Chrome startup failed with SIGTRAP/socket permissions. No preceding Remotion scenes were edited.

## Reproduce into fresh output paths

Stage the configured logo into `out/v2-scene4-end-card-r1/public/branding/logo.png` (copy the logoSource asset). Then:

```sh
npx remotion render src/v2/end-card-entry.jsx V2Scene4EndCard out/v2-scene4-end-card-r1/end-card-render.mp4 --public-dir=out/v2-scene4-end-card-r1/public --codec=h264 --crf=14 --pixel-format=yuv420p --color-space=bt709 --image-format=png --concurrency=2 --browser-executable=/usr/bin/google-chrome
ffmpeg -hide_banner -loglevel error -n -i out/v2-scene4-end-card-r1/end-card-render.mp4 -f lavfi -i anullsrc=r=48000:cl=stereo -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -t 5 -movflags +faststart production/v2/scene-04/output/scene-04-end-card-r1-720p.mp4
python3 scripts/assemble_v2_review.py manifests/v2-scenes01-04-review-r1.json
```

Select an installed Chrome using the CLI argument; no runtime asset uses an absolute path. Assembly refuses overwrites. Earlier approved renders remain preserved. Stop for review; no commit requested.
