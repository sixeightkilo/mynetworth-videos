# Production v1

This directory contains all scene production assets and work created through 8 November 2026: `scene-01/` through `scene-10/` and shared `references/`. Existing filenames and render revision suffixes are preserved. The media was moved without re-encoding or pixel changes.

The latest assembled review stays at `output/scene-01-10-preview-v5-scene8-9-color-match.mp4` relative to the repository root: 1920×1080, 24fps, 1250 frames / 52.083333s, with original audio. Comparison stills remain in `output/color-comparison-v5/`.

Reusable implementation stays in `src/` and `scripts/`; assembly/tracking configurations remain in `manifests/` with references updated to this version. Scene 5 rendering uses `--public-dir=production/v1`. The Scene 10 staging helper reads versioned assets from its existing manifest. The original 720p baseline in `public/` and baseline Git tags remain untouched.

For the latest color adjustments see `docs/scenes01-10-color-fixed-v3.md`, `docs/scenes01-10-scene8-color-match-v4.md`, and `docs/scenes01-10-scene9-color-match-v5.md`. Production folder version v1 is independent of render revisions such as v2/v5 in individual filenames.

Production checkpoint tag: `production-v1` (includes the latest v5 full-film review and the versioned production asset layout).
