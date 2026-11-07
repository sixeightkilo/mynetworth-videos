# Accepted Scenes 01–05 preview

On 7 November 2026 the user accepted `output/scene-01-05-preview-v1.mp4` as a review preview, noting that some wrinkles remain. This checkpoint preserves everything required to reproduce it. It does not replace the approved ten-scene, 1349-frame 720p baseline, and no integration or publication is authorized by this checkpoint.

## Current preview

1920×1080, 24fps, 623 frames / 25.958333 seconds, H.264 with AAC stereo audio. Source clips at 1916×1080 receive two black pixels on each side; they are not stretched. Cuts between scenes are direct. The source dialogue and soundtracks are retained; Scene 05 is silent.

| Scene | Versioned input | Source frames, end-exclusive | Global start |
|---|---|---|---|
| 01 | `production/scene-01/output/scene-01.mp4` | [0,121) | 0 |
| 02 | `production/scene-02/output/scene-02.mp4` | [0,169) | 121 |
| 03 | `production/scene-03/output/scene-03.mp4` | [0,110) | 290 |
| 04 | `production/scene-04/output/scene-04-dashboard-tracked-full-v2.mp4` | [18,121) | 400 |
| 05 | `production/scene-05/output/scene-05-two-phase-v5.mp4` | [0,120) | 503 |

The Scene 03 endpoint includes frame 109, matching `scene-03-end.jpg`. Scene 04's opening 18 frames are removed to avoid the repeated pocket-reaching action. Scene 04 appears once; the standalone Scene 05 transition follows it.

The assembly manifest is `manifests/scene01-05-preview-v1.json`; implementation is `scripts/assemble_scene_preview.py` (Python standard library plus FFmpeg/FFprobe). `output/scene-01-05-preview-v1.json` records source hashes, timings and audio checks. `output/scene-01-05-preview-v1-boundaries.jpg` shows the actual scene cuts.

## Reproduce the accepted assembly

All five media inputs are versioned, so rebuilding the assembly does not require Chromium, OpenCV, AI tools or source regeneration. The assembler refuses to overwrite an existing output. From the project root, create a disposable manifest with a new output path:

```sh
python3 - <<'PY'
import json
from pathlib import Path
folder = Path('out/preview-rebuild')
folder.mkdir(parents=True, exist_ok=True)
cfg = json.loads(Path('manifests/scene01-05-preview-v1.json').read_text())
cfg['output'] = str(folder / 'scene-01-05-preview-v1.mp4')
(folder / 'assembly.json').write_text(json.dumps(cfg, indent=2))
PY
python3 scripts/assemble_scene_preview.py out/preview-rebuild/assembly.json
```

The accepted assembly was reproduced byte-for-byte with this workflow on the validated FFmpeg 4.4.2 environment. Different encoder versions or platforms may produce different compressed bytes; geometry and timing remain defined by the manifest.

## Rebuild Scene 05 upstream

The accepted Scene 05 is v5, not the superseded digital-zoom or graph-crop experiments. Its complete dependency chain is versioned:

- `src/scene05-two-phase-preview.jsx`: standalone Remotion entry.
- `src/scenes/Scene5TwoPhase.jsx`: frozen plate, geometric phone and original-finger layering.
- `src/transitions/scene05-two-phase.mjs`: shared phone/screen camera and perspective motion.
- `src/components/PhoneMockup.jsx` and `screenTransform.mjs`: existing projective phone model.
- `manifests/scene05-two-phase-v5.json`: measured corners, phase timings and foreground domains.
- `production/scene-05/output/scene-05-start-exact.png`: approved Scene 04 frame 120, padded to 1920×1080.
- `scene-05-v5c-background.png` and `scene-05-v5c-fingers.png`: accepted derived layers beside that start frame.
- `production/references/dashboard-original.png`: original 864×1872 screenshot.
- `scripts/prepare_scene05_two_phase.py`: optional OpenCV asset preparation from the v5 manifest, with no dependency on rejected v1–v4 manifests. It refuses to overwrite existing layers or modify the source/configuration.

The exact prepared v5 layers were reproduced byte-for-byte after making the preparation script read the final manifest directly. They are already supplied in Git, so normal rendering does not need OpenCV. Optional preparation uses the pinned packages in `scripts/requirements-screen-compositing.txt`; Python virtual environments remain under ignored `out/`.

Install the existing pinned npm dependencies with `npm ci` as described in README. Rendering requires working Chromium; bundling alone is insufficient. The successful render used the existing system Chrome executable:

```sh
npx remotion render src/scene05-two-phase-preview.jsx Scene05TwoPhasePreview out/preview-rebuild/scene05-2x.mp4 --public-dir=production --codec=h264 --crf=12 --scale=2 --browser-executable=/opt/google/chrome/chrome --concurrency=2
ffmpeg -n -i out/preview-rebuild/scene05-2x.mp4 -vf scale=1920:1080:flags=lanczos -c:v libx264 -crf 16 -preset fast -pix_fmt yuv420p -movflags +faststart out/preview-rebuild/scene05-v5.mp4
```

Select the local Chrome path for other systems. This is 2× graphics supersampling followed by downsampling, not native 4K footage. To use a newly rendered Scene 05 in a comparison assembly, change only the last source in the disposable assembly manifest; preserve the accepted media.

The four pre-render validation stills, 200% edge crops, contact sheets, v5 review report, standalone Scene 05 and combined Scene 04→05 preview are retained under `production/scene-05/output/` with `two-phase-v5` in their names. They establish that all display and outer-bezel corners stay in frame, screen and bezel share one transform, the complete dashboard remains visible, and the endpoint matches the existing app showcase. The background and original hand clear before the phone-plane morph. Original fingertip pixels remain soft; the reconstructed bezel follows the showcase design rather than recovering physical source texture.

Scene 04's source, dashboard replacement code and reports were preserved in the preceding checkpoint; see `docs/scene04-dashboard-compositing.md`. Its accepted v2 composite is the upstream input to Scene 05.

## Validation and remaining scope

`docs/scenes01-05-preview-validation.json` records the byte-identical assembly and preparation checks. `manifests/scenes01-05-preview-checksums.json` inventories the reproducible dependency chain and accepted review artifacts. Both use repository-relative paths.

Latest checks: 623 frames at 24fps, full decode passed, original-audio alignment passed, Scene 05 digitally silent, source hashes unchanged, and all 22 baseline assets verified. Earlier source-generated framing/posture shifts remain at some cuts; Scene 04's blurred phone rotation and source fingertip softness remain documented limitations. The user accepted the preview with these wrinkles, not as a declaration that the whole film is finished.

Superseded Scene 05 v1–v4 experiments, old multi-scene preview renders, caches, diagnostic scratch files, Python environments and 4K intermediate renders are not dependencies of this checkpoint. They are not removed from the working directory. The approved assembly, existing app showcase, source media and prior renders remain unchanged.
