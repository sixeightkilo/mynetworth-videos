# MyNetWorth videos

This is the production workspace for the approved MyNetWorth promotional film. Start here to reproduce the current state. The original experimental project is preserved separately.

The approved film is **56.208333 seconds / 1349 frames, 1280×720 at 24fps**, including all ten scenes. Source assets and the tested Scene 6→7 transition are already approved; no footage regeneration is needed.

## Setup

Requirements: Node.js 22+ (validated with Node 24), npm, Python 3.10+, FFmpeg and FFprobe on PATH. Python production scripts use only the standard library. No Python packages, external animation libraries or AI models are needed.

```sh
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
