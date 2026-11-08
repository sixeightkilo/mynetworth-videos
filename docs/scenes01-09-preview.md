# Scenes 01–09 preview checkpoint

The user requested appending the new Scene 09 on 8 November 2026, then checking in and committing this stage. Current review output: `output/scene-01-09-preview-v1.mp4`, 1920×1080, 24fps, 1130 frames / 47.083333 seconds, H.264 with AAC stereo audio.

## Inputs and timing

- Existing prefix: `output/scene-01-08-preview-v1.mp4`, all 1009 frames. Its video packets are copied; every decoded prefix frame was verified identical.
- Append: `production/v1/scene-09/output/scene-09.mp4`, all 121 native 1920×1080 frames at 24fps, with its original soundtrack. No trimming or crossfade.
- Scene 09 starts at output frame 1009 / 42.041667 seconds. Its opening pose matches Scene 08's ending closely; small source expression/rasterization differences remain. No polishing was performed.

The actual source files and previous preview remain unchanged. Original soundtracks are retained, padded to their respective video durations and concatenated on the frame boundary. Joined AAC audio is re-encoded. Verification found zero measured sample lag, with correlations 0.999979 for the prefix and 0.998133 for Scene 09. Both video/audio timelines start at zero; full decode, dimensions, exact frame count and 24fps checks pass.

## Reproduction

The same versioned `scripts/append_preview_clip.py` used for Scene 08 implements this append. Its only runtime dependencies are the two versioned inputs above, `manifests/scene01-09-preview-v1.json`, Python's standard library and FFmpeg/FFprobe. No Chromium, OpenCV, source regeneration or AI tools are required. The upstream assembly is documented in `docs/scenes01-08-preview.md`.

The script refuses existing outputs and intermediates. Reproduce using a copied manifest and unused paths:

```sh
python3 - <<'PY'
import json
from pathlib import Path
folder = Path('out/scenes01-09-rebuild')
folder.mkdir(parents=True, exist_ok=True)
cfg = json.loads(Path('manifests/scene01-09-preview-v1.json').read_text())
cfg['output'] = str(folder / 'scene-01-09-preview-v1.mp4')
cfg['workDir'] = str(folder / 'work')
(folder / 'manifest.json').write_text(json.dumps(cfg, indent=2))
PY
python3 scripts/append_preview_clip.py out/scenes01-09-rebuild/manifest.json
```

`output/scene-01-09-preview-v1.json` records source hashes, timings, decoded-prefix checks and audio correlations. The contact sheet beside it shows the Scene 08→09 boundary and Scene 09 samples. `manifests/scenes01-09-preview-checksums.json` inventories the complete append dependency set and review artifacts. Intermediates under `out/` are disposable and recreated by the script.

All 22 original baseline asset hashes still pass. Prior renders, sources, baseline tags, the approved ten-scene rough cut and existing showcase are untouched. Previously documented wrinkles remain; this is an assembly checkpoint, not a polished final export. The end card / Scene 10 has not yet been appended.
