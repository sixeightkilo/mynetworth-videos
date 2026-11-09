# MyNetWorth videos

This is the production workspace for the approved MyNetWorth promotional film. Start here to reproduce the current state. The original experimental project is preserved separately.

The approved film is **56.208333 seconds / 1349 frames, 1280×720 at 24fps**, including all ten scenes. Source assets and the tested Scene 6→7 transition are already approved; no footage regeneration is needed.

## Setup

Requirements: Git LFS (for the large lossless review MP4s), Node.js 22+ (validated with Node 24), npm, Python 3.10+, FFmpeg and FFprobe on PATH. Python production scripts use only the standard library. No Python packages, external animation libraries or AI models are needed.

```sh
git lfs install
git lfs pull
npm ci
npm run verify
npm run build
```

If the restricted runtime blocks esbuild’s install-time subprocess check, use `npm ci --ignore-scripts`, then run `npm run build` to validate the installed toolchain. This was the successful migration-validation path.

Dependencies remain pinned to React 19.0.0 and Remotion 4.0.373 via package-lock.json. public includes all required assets as real copies. Nothing depends on the original project path.

## Reproduce the approved film

```sh
npm run render:rough-cut
npm run validate:rough-cut
```

Output: out/mynetworth-rough-cut-720p.mp4. This assembles existing approved footage with FFmpeg; it does not regenerate scenes. It verifies source checksums and preserves existing dialogue, phone overlays, app recordings and captions. The Scene 9→10 crossfade lasts 17 frames, followed by an 84-frame end-card hold.

The comparison command checks stream metadata, full decode, source hashes and frame alignment/PSNR against references/approved-rough-cut-720p.mp4 when that optional approval reference is present. Reference videos are copied for this migration but excluded from Git. Without a reference it reports comparison skipped explicitly.

To reproduce just the integrated Scene 6–7 preview:

```sh
npm run render:scene6-7
```

Output: out/scene-6-7-preview.mp4 — 418 frames / 17.416667s. It uses the integrated source followed by the approved transition/showcase. This command writes output only; it never updates the approved composite used by the main assembly.

## Preview and 1080p

```sh
npm run studio
```

Compositions:

- ApprovedRoughCut720p: authoritative approved-media assembly.
- Production1080p: same approved layout and timing at 1920×1080.
- ApprovedScene6And7: reproducible approved media join.
- EditableScene6And7 and EditableScene7: working editable transition, smartphone and recording code; keep separate from baked approval.

```sh
npm run render:1080p
# Optional browser render:
npm run render:1080p:remotion
```

Output: out/mynetworth-production-1080p.mp4. Existing scene footage and approved composites are approximately 720p and will be upscaled; native 1080p masters have not been supplied. No final 1080p export was rendered during migration.

Remotion browser rendering failed in the original restricted runtime with Chromium SIGTRAP/permission errors. npm run build validates the bundle, not browser playback. The tested FFmpeg assembly route works without a browser. Editable Arial text can vary if that font is not installed; approved text is already baked in the source media.

## Where to work

- manifests/production.json: ten-scene inventory, approval status and missing inputs.
- manifests/approved-720p.json: actual assembly source paths and frame timings.
- manifests/scene7.json: app segments, caption text, phone position and still holds.
- manifests/scene6-7.json: integrated clip/approved transition frame correspondence.
- manifests/phone-transition.json: zoom geometry and phone model.
- src/: reusable Remotion components, editable scenes and compositions.
- public/scenes/: individual approved footage; public/composites/: approved baked production dependencies.
- public/app-recordings/, screenshots/, branding/, phone/: required media for editable scenes.
- docs/approval-history/: approval notes and timing reports; historical paths are provenance only.
- docs/prompts/: existing relevant brief copied verbatim. Original Kling generation prompts were not located; none were invented.
- references/: optional approval comparisons, not needed to render.
- out/: generated renders, bundles and validation logs; ignored by Git.

Read AGENTS.md before changing scenes. Preserve approved assets; create reviewed revisions rather than replacing them. CAS must not display PAN, personal holdings or the file picker. Its ending is the static demo-dashboard opening frame, not another scroll.

## Preservation

manifests/asset-checksums.json records every migrated production asset and its original provenance. Migration checks are in docs/migration-validation.json. Git tracks code, configurations, documentation and required approved assets; renders, dependencies and reference videos are ignored. The original project's milestone archive remains in the original workspace and is deliberately not duplicated here.

## New Scenes 01–05 review preview

The user accepted a separate 1080p review preview on 7 November 2026, with some wrinkles remaining. `output/scene-01-05-preview-v1.mp4` is 623 frames / 25.958333 seconds at 24fps. Its exact source selections are in `manifests/scene01-05-preview-v1.json`; all runtime inputs and the Scene 05 v5 rendering workflow are versioned. See [reproduction and validation](docs/scenes01-05-preview.md). This partial preview does not replace the approved ten-scene 720p baseline or modify the existing app showcase.

## Scenes 01–07 continuity checkpoint

`output/scene-01-07-preview-v1.mp4` extends the accepted Scenes 01–05 preview without changing its decoded video or audio. It adds the final aligned frame of the old Scene 6 and all of Scene 7, upscaled from 720p: 888 frames / 37 seconds at 1920×1080, 24fps. The duplicate old Scene 6 approach/dialogue is skipped. See [selection, limitations and reproduction](docs/scenes01-07-preview.md). Tag: `baseline-scenes-01-07-v1`. This temporary assembly remains separate from the approved ten-scene rough cut.

## Scenes 01–08 preview

`output/scene-01-08-preview-v1.mp4` appends the complete new `production/v1/scene-08/output/scene-8.mp4` to the current Scenes 01–07 preview: 1009 frames / 42.041667 seconds at 1920×1080, 24fps. All 888 existing decoded video frames are preserved; original dialogue is retained with correctly timed silence through the app showcase. See [dependencies, timing and reproduction](docs/scenes01-08-preview.md). Prior baselines and the original ten-scene rough cut remain unchanged.

## Scenes 01–09 preview

`output/scene-01-09-preview-v1.mp4` adds the full new production Scene 09: 1130 frames / 47.083333 seconds at 1920×1080, 24fps. The earlier 1009 decoded video frames are unchanged; original dialogue is retained. See [dependencies, validation and reproduction](docs/scenes01-09-preview.md). The end card remains to be added.

## Production version 1

All scene production work to date is under `production/v1/`, including scene folders, prompts, reference images and rendered scene outputs. Use that root for source assets and Scene 5’s Remotion public directory (`--public-dir=production/v1`). Reusable code remains in `src/` and `scripts/`; manifests retain their existing names with updated asset paths. The original `public/` baseline and existing assembled previews under `output/` remain in place.

Latest full-film review: `output/scene-01-10-preview-v5-scene8-9-color-match.mp4` — 1920×1080, 24fps, 1250 frames / 52.083333 seconds. It includes the Scenes 4–5 color-matrix repair and the same restrained warm-chroma correction on Scenes 8 and 9, carried through Scene 9’s held-image end-card fade. Earlier render revision suffixes remain unchanged inside production version 1. See `production/v1/README.md`.

Production checkpoint tag: `production-v1` (includes the latest v5 full-film review and the versioned production asset layout).

The lossless v3/v4/v5 full-film review videos in `output/` are stored with Git LFS. Their media bytes and validation hashes are unchanged. Install Git LFS before cloning, or run `git lfs pull` after cloning to retrieve the videos.

## V2 Segment 2 review

V2 uses four segments/scenes. Approved Segment 1 is `production/v2/scene-01/output/scene-01.mp4`; do not alter it. Segment 2 uses a separate entry `src/v2/index.jsx`, configuration `manifests/v2-segment2-r4.json`, and real existing app recordings.

```sh
npm run prepare:v2:segment2
npm run studio:v2
npm run render:v2:segment2:preview
npm run render:v2:segment2:boundary
python3 scripts/validate_v2_segment2.py
```

Preparation and rendering refuse to overwrite existing output/staging paths. On this checkout the reviewed paths already exist; use Studio to inspect them. For a fresh revision, update the centralized manifest and render filenames before rendering. The browser can be selected with `REMOTION_BROWSER_EXECUTABLE` or the preview helper’s `--browser-executable` argument. Only 720p review videos are authorized so far. Music is configurable but no licensed music asset was found. Current r4 retains the approved 1280×720 reference but uses fitted geometric screen edges rendered at their final zoomed size, with 2× antialiasing and a notch-free phone. Final review output is 720p under `out/v2-segment2-r4/review/`; see `docs/v2-segment2-r4.md`. Earlier revisions remain preserved.

## Complete V2 checkpoint

Current V2 review: `production/v2/output/scene-01-04-review-music-r2.mp4`, 1418 frames / 59.083333s, 1280×720 at 24fps. Four scenes, original dialogue/notification and updated user-composed soundtrack. Accepted scene masters and required sources are versioned. Run `python3 scripts/reproduce_v2.py` to verify inputs and reproduce into a fresh out/ directory. See [V2 dependencies and authoring](production/v2/README.md). The small white edge padding is retained in this checkpoint; its correction is a separate review.

Latest approved V2 edge correction: `production/v2/output/scene-01-04-review-music-r3-edge-fixed.mp4`. See [method, validation and reproduction](docs/v2-edge-fix-r1.md). Duration, framing and soundtrack are retained; the earlier checkpoint remains preserved.

Latest V2 tagline revision: `production/v2/output/scene-01-04-review-music-r4-tagline.mp4`, with explicit two-line showcase text. See [validation and reproduction](docs/v2-tagline-r5.md).
