# Scenes 01–07 continuity preview checkpoint

The user requested committing and tagging this preview on 7 November 2026. The checkpoint tag is `baseline-scenes-01-07-v1`. This is a temporary 1080p assembly, not a polished final film or a replacement for the original ten-scene 720p baseline.

## Output and exact selection

`output/scene-01-07-preview-v1.mp4`: 1920×1080, 24fps, 888 frames / 37 seconds. The existing Scenes 01–05 preview occupies frames [0,623) and is copied without video re-encoding. All 623 decoded frames and the decoded audio match the accepted prefix exactly.

The only additional source is the versioned `public/composites/scene6-7-integrated-approved.mp4`, a 1280×720, 24fps, 418-frame baked approval. This assembly uses its frames [153,418):

| Material | Source frames, end-exclusive | Output frames | Duration |
|---|---|---|---|
| Accepted Scenes 01–05 | [0,623) in the accepted prefix | [0,623) | 25.958333s |
| Old Scene 6, final aligned app-facing frame | [153,154) | [623,624) | 0.041667s |
| Complete old Scene 7 | [154,418) | [624,888) | 11s |

The earlier Scene 6 approach, frames [0,153), and its temporary dialogue are deliberately omitted because the new Scene 5 already performs the room-to-phone transition. Appending the full old Scene 6 would cut back from the flat dashboard to the room and repeat the camera approach. This checkpoint retains only its aligned tail; it does not preserve the original complete Scene 6 duration or dialogue.

Scene 7's full 264-frame timing, recordings, dashboard/SIP/reports/CAS captions and baked transitions are retained. The Secure Local Import hold and final static Demo portfolio ending are unchanged. No raw CAS footage or excluded personal-data portions are exposed.

The legacy tail is upscaled to 1080p with Lanczos, then appended by stream-copying video packets. It is not native 1080p footage. Its audio was verified digitally silent. The accepted prefix's original AAC stream is copied unchanged; playback after its audio track ends is silent, matching the appended media. There is no added voice, music or sound effect.

## Continuity and remaining wrinkles

The matched boundary phone center is x=1319.5px in both frames. Heights are 960px and 959px, with only a 0.5px vertical-center difference. Thus the current Scene 5's final framing and scale align with the selected app-facing frame.

Visible changes remain: the older 720p raster is softer; bezel, shadow and rasterization differ slightly. The original showcase transition introduces recording status bars and slightly different displayed portfolio values. Existing source-generated framing/posture changes in Scenes 01–05 remain. No polishing or redesign was performed. The priority remains completing the film before refining individual scenes.

## Reproduction

The complete runtime dependency chain is the accepted prefix, the baked legacy composite, `manifests/scene01-07-preview-v1.json`, and `scripts/extend_preview_with_legacy.py`. All are versioned. FFmpeg/FFprobe and Python's standard library are sufficient; no Chromium, OpenCV or source regeneration is required for this append operation. The upstream Scenes 01–05 workflow remains documented in `docs/scenes01-05-preview.md`.

The script verifies the selected legacy audio is silent, upscales that selection, copies the prefix, checks full decode and frame count, and compares every decoded prefix frame and the original audio. It refuses to overwrite existing outputs or intermediate media. To reproduce into disposable output:

```sh
python3 - <<'PY'
import json
from pathlib import Path
folder = Path('out/scenes01-07-rebuild')
folder.mkdir(parents=True, exist_ok=True)
cfg = json.loads(Path('manifests/scene01-07-preview-v1.json').read_text())
cfg['output'] = str(folder / 'scene-01-07-preview-v1.mp4')
cfg['workDir'] = str(folder / 'work')
(folder / 'manifest.json').write_text(json.dumps(cfg, indent=2))
PY
python3 scripts/extend_preview_with_legacy.py out/scenes01-07-rebuild/manifest.json
```

The checkpoint was reproduced byte-for-byte on the validated FFmpeg 4.4.2 environment. Other encoder versions may produce different compressed bytes for the upscaled tail. Integer-frame selection and prefix preservation remain explicitly verified.

Review evidence is in `output/scene-01-07-preview-v1.json`, the contact sheet and notes beside it. `manifests/scenes01-07-preview-checksums.json` inventories the inputs, code and review artifacts. `docs/scenes01-07-preview-validation.json` records the reproduction check. Temporary upscaled media and concat lists live under ignored `out/` and are recreated by the script, not runtime dependencies of the committed video.

Sources, previous preview baselines, existing Remotion compositions and the original ten-scene approved film remain untouched. Scenes 08–10 have not yet been appended to this assembly. No publishing or pushing is included in this checkpoint.
