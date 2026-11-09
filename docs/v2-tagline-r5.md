# V2 showcase tagline line break

The user requested an explicit line break after “All Your Investments.” so “One Clean Dashboard.” remains intact on the second line. `src/v2/Segment2.jsx` supports optional `text.taglineLines` (each line uses nowrap); earlier manifests still use their original tagline string unchanged. New config: `manifests/v2-segment2-r5.json`. Font size, positioning, colors and timings are unchanged.

The actual Remotion render uses the same 2× antialiasing as r4, rendering local frames 132–201 only (the complete text fade-in/hold/fade-out interval). Native 720p patch source: `production/v2/scene-02/output/tagline-r5-frames132-201-720p.mp4`. A checked still is under `docs/validation/v2-tagline-r5.png`.

`manifests/v2-tagline-patch-r1.json` and `scripts/patch_v2_tagline.py` replace only x=96..735, y=440..549 at global frames [637,707) in the accepted edge-fixed film. The recorded app content, captions outside this area, phone animation, edge fix, end card and soundtrack are retained. Final output: `production/v2/output/scene-01-04-review-music-r4-tagline.mp4`, 1418 frames / 59.083333s, 1280×720 at 24fps. Audio is stream-copied and decoded PCM verified identical. Video is re-encoded at CRF12, so small compression differences can occur outside the edited area. Previous renders remain untouched. User approved the change and requested check-in and commit. No push requested.

Reproduce the source patch: prepare r5 with `python3 scripts/prepare_v2_segment2.py manifests/v2-segment2-r5.json`, create a props JSON containing `{ "config": <r5 manifest> }`, then render `src/v2/index.jsx` / `V2Segment2Preview` with that props file, `--frames=132-201 --scale=2 --codec=h264 --crf=12 --pixel-format=yuv420p --color-space=bt709 --image-format=png`. Downsample to 1280×720 with Lanczos/CRF14. To reproduce the full-film application use `python3 scripts/patch_v2_tagline.py manifests/v2-tagline-patch-r1.json`, selecting fresh output paths to preserve existing media.

The pre-correction checkpoint checksum inventory acknowledges the backwards-compatible component change; its baked production inputs remain unchanged.
