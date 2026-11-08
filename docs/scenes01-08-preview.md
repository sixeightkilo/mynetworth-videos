# Scenes 01–08 preview checkpoint

On 8 November 2026 the user requested extending the current preview through the new production Scene 08, then committing all dependencies for this stage. The result is `output/scene-01-08-preview-v1.mp4`: 1920×1080, 24fps, 1009 frames / 42.041667 seconds, H.264 with AAC stereo audio.

## Inputs and cut

| Segment | Versioned source | Frames | Output start |
|---|---|---|---|
| Existing Scenes 01–07 | `output/scene-01-07-preview-v1.mp4` | All 888 frames | 0 / 0s |
| New Scene 08 | `production/scene-08/output/scene-8.mp4` | All 121 frames | 888 / 37s |

Scene 08 is native 1920×1080 at 24fps, with its original Kling dialogue. Its prompt and starting reference are preserved as `production/scene-08/prompt.md` and `production/scene-08/references/scene-08-start.jpg`. The older `public/scenes/8-vijay-doubts.mp4` belongs to the original ten-scene rough cut and remains unchanged.

Scene 08 is used in full, without trimming, a crossfade, source regeneration or scene redesign. The new boundary is a direct cut from the flat app showcase back to the living-room shot, where Nikhil lowers the phone and Vijay raises the privacy concern. The staging/framing change is intentionally retained without polishing.

The existing Scenes 01–07 source file remains unchanged. Its video packets are copied, and all 888 decoded output frames were checked against the prefix. Scene 08 video is encoded once to compatible H.264 settings before concatenation. Video timestamps are normalized to zero; the final video has an exact 24fps frame cadence and starts Scene 08 at 37 seconds.

The earlier prefix's audio track ends before its video because the appended app showcase is silent. The audio pipeline preserves that silence through the 37-second video boundary, then appends Scene 08's original soundtrack. The joined audio is re-encoded as AAC, not byte-identical compressed audio. Waveform checks found zero measured lag and correlation above 0.9997 for the existing soundtrack and above 0.9999 for Scene 08. No new voices, music or effects are added.

## Reproduction

Runtime dependencies: `scripts/append_preview_clip.py`, `manifests/scene01-08-preview-v1.json`, the two source videos above, Python's standard library, FFmpeg and FFprobe. No Chromium, OpenCV, Node or AI generation is required for this append. Upstream dependencies remain documented in `docs/scenes01-07-preview.md` and `docs/scenes01-05-preview.md`.

The script builds video-only segments separately from the padded audio and muxes them at the end. This avoids timestamp shifts caused by the shorter prefix audio track and AAC priming. It verifies output geometry, exact frame count/rate, zero video start time, duration, full decode, all decoded prefix frames, source hashes and audio alignment.

Outputs and intermediates are never overwritten. Reproduce with a disposable copied manifest and unused paths:

```sh
python3 - <<'PY'
import json
from pathlib import Path
folder = Path('out/scenes01-08-rebuild')
folder.mkdir(parents=True, exist_ok=True)
cfg = json.loads(Path('manifests/scene01-08-preview-v1.json').read_text())
cfg['output'] = str(folder / 'scene-01-08-preview-v1.mp4')
cfg['workDir'] = str(folder / 'work')
(folder / 'manifest.json').write_text(json.dumps(cfg, indent=2))
PY
python3 scripts/append_preview_clip.py out/scenes01-08-rebuild/manifest.json
```

The preview was reproduced byte-for-byte with the validated FFmpeg 4.4.2 environment. Different encoder/platform versions may produce different compressed bytes; the script still checks integer-frame timing and video preservation. Source videos, all previous renders, existing baseline tags, the approved rough cut and the app showcase remain untouched.

## Review evidence and remaining scope

- `output/scene-01-08-preview-v1.json`: source hashes, timing, frame preservation and audio validation.
- `output/scene-01-08-preview-v1-contact.jpg`: showcase/room boundary and Scene 08 samples.
- `docs/scenes01-08-preview-validation.json`: checkpoint reproduction results.
- `manifests/scenes01-08-preview-checksums.json`: required inputs, code, documentation and review artifacts.

Source-frame staging differences at the direct cut and previously documented wrinkles remain. The old app section still contains upscaled 720p detail; the new Scene 08 does not need upscaling. The priority remains assembling the remaining film before polishing. Scenes 09–10 have not been appended. Scratch work and a failed timing-check candidate are retained only under ignored `out/`; they are not dependencies.
