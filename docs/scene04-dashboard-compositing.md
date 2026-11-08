# Scene 04 dashboard compositing

The user accepted the full-scene v2 render on 7 November 2026. It remains separate from the existing approved rough-cut assembly; no Remotion substitution has been made.

## Accepted artifacts

All media is under `production/v1/scene-04/output/`:

- `scene-04-dashboard-tracked-full-v2.mp4`: accepted complete Scene 04.
- `scene-04-dashboard-tracked-full-v2-comparison.mp4`: original and composite side by side.
- `scene-04-dashboard-tracked-full-v2-contact.jpg`: retrieval, rotation, and final hold closeups with shot context.
- `scene-04-dashboard-tracked-full-v2-report.json` and `-notes.md`: resolved per-frame corners, tracking diagnostics, validation and limitations.
- `scene-04-dashboard-poc-v2*`: approved one-second proof of concept, retained unchanged.

The v1 POC and full-scene outputs are intermediate review history, not the accepted deliverables. In particular, full-scene v1 had bottom-edge overshoot during rotation; v2 corrected it with revised manual corners.

## Inputs and implementation

`scene-04.mp4` is the untouched first-pass source: 1916×1080, 24fps, 121 frames / 5.041667 seconds. The replacement is `production/v1/references/dashboard-original.png` (864×1872). The original source audio is copied to the full-scene output without re-encoding; decoded PCM was verified identical. The earlier `scene-04-with-dash.mp4` and dashboard keyframe references are preserved for comparison, not used as runtime dependencies.

`scripts/composite_phone_screen.py` uses OpenCV optical flow with forward/backward checks and RANSAC homographies, constrained by manual inner-display corners. Interpolated manual corrections retain the nonlinear tracked movement. The full-scene configuration is `manifests/scene04-dashboard-full.json`; the POC configuration is `manifests/scene04-dashboard-poc.json`.

Manual corners cover each frame 73–76 during rapid rotation; additional anchors cover 77–82 and the final hold. POC anchors 84–107 are retained. Original decoded frames 0–72 pass through unchanged before encoding, preserving the back/edge-on phone. Replacement opacity ramps 0.65 → 0.9 → 1 over frames 73–75. Rounded display masks include a notch hole, conservative fingertip holdouts from original-frame skin colour, and 0.35px feathering. Original fingers are neither reconstructed nor sharpened.

## Reproduction

Validated with Python 3.10, FFmpeg/FFprobe 4.4.2, and the exact optional dependencies in `scripts/requirements-screen-compositing.txt`. OpenCV and NumPy are needed only for this compositing tool, not production baseline assembly.

From the repository root:

```sh
python3 -m venv out/screen-compositing-venv
out/screen-compositing-venv/bin/pip install -r scripts/requirements-screen-compositing.txt
```

Copy the full-scene manifest to a new manifest and change `outputStem` to an unused revision name. Then run:

```sh
out/screen-compositing-venv/bin/python scripts/composite_phone_screen.py manifests/YOUR-NEW-MANIFEST.json
```

The script deliberately refuses to overwrite existing outputs. Keep accepted files and the original source intact. It creates a render, comparison, contact sheet and JSON report. Its `fullSceneApproved` option is enabled for this already-authorized full-scene workflow; the POC stays available independently.

`manifests/scene04-dashboard-checksums.json` inventories processing inputs, configuration, code, dependency specification and review artifacts. Validate with:

```sh
python3 - <<'PY'
import hashlib, json
from pathlib import Path
for item in json.loads(Path('manifests/scene04-dashboard-checksums.json').read_text())['files']:
    path = Path(item['path'])
    assert hashlib.sha256(path.read_bytes()).hexdigest() == item['sha256'], str(path)
print('Scene 04 processing checksums passed')
PY
```

Virtual environments, wheels, caches and diagnostic scratch files remain disposable under `out/` and are not versioned.

## Validation and review limits

The accepted full-scene render retains 1916×1080, 24fps, all 121 frames, source video duration and original AAC audio. Full decode passed for the render and comparison; no adjacent duplicate frames were found. Source and approved POC hashes remained unchanged. All 22 original baseline asset checks still pass.

Frames 73–80 (3.042–3.375s) remain the least certain interval due to rapid rotation and motion blur. Peak optical-flow corner-motion disagreement is 5.78px near frame 78; that diagnostic is not a measurement of visible sliding. The steady hold from frame 84 stays below 0.9px by the same check. A narrow dark source rim is intentionally retained around the inset mask. Fine text can alias because the phone display occupies only about 75×190 pixels in the shot. The user reviewed and accepted the result with these limits documented.
