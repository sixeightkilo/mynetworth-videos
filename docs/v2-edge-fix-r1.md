# V2 approved edge-padding correction

Reproducible baseline was committed first as `6bd17eb` (complete V2 film with soundtrack). A fresh reproduction matched the accepted music-r2 MP4 byte-for-byte. npm ci, npm run verify and npm run build passed; npm ci required execution outside the sandbox after esbuild EPERM. No push or tag was requested.

Thin white lines were measured in the living-room scenes: approximately two left pixels and one/two right pixels from aspect-preserving fitting of 1284×724 sources into 1280×720. Chroma encoding also slightly contaminates adjacent boundary pixels. White edges in the showcase/end card are the intended white background.

The new review uses `fillborders=left=4:right=4:mode=smear`: each outer four-pixel strip is replaced with its nearest interior picture column, covering padding plus chroma fringe. This is conventional edge extension, with no generated content, crop, zoom, stretch, scene movement, timing change or phone geometry change. Applying it across the film also keeps the frozen opening of Scene 2 consistent. Fully white showcase/end-card boundaries remain white. Interior areas have no intended edits; H.264 CRF12 introduces small recompression differences.

New output: `production/v2/output/scene-01-04-review-music-r3-edge-fixed.mp4`. Current soundtrack audio is stream-copied, not remixed or re-encoded. Original music-r2 preview remains untouched. Reproduce with:

```sh
python3 scripts/fix_v2_edges.py manifests/v2-edge-fix-r1.json
```

Use fresh output/work paths for further revisions. Decoder/metadata checks verify frame count, timing, 720p resolution, source immutability and exact decoded audio identity. Report is saved alongside the new MP4. The user requested documenting and committing this correction. The earlier checkpoint remains preserved as the pre-correction baseline.

Completed validation: 1418 frames / 59.083333s, 1280×720 at 24fps; full decode passed, decoded audio identical. Interior PSNR is 54.80dB versus the committed source (recompression only). Magnified edge comparisons at frames 240, 505, 1000 and 1350 show the padding removed from the picture and intentional white end-card background preserved. Comparison: `docs/validation/v2-edge-fix-r1-before-after.png`.

To reproduce without overwriting the committed output:

```sh
python3 - <<'PYCONFIG'
import json
from pathlib import Path
c = json.loads(Path('manifests/v2-edge-fix-r1.json').read_text())
c['output'] = 'out/v2-edge-reproduction/film.mp4'
c['workDir'] = 'out/v2-edge-reproduction/work'
Path('out').mkdir(exist_ok=True)
Path('out/v2-edge-reproduction.json').write_text(json.dumps(c))
PYCONFIG
python3 scripts/fix_v2_edges.py out/v2-edge-reproduction.json
```

`manifests/v2-edge-fix-checksums.json` records the source, corrected output, implementation and comparison evidence. The standard-library/FFmpeg correction requires no optional OpenCV dependencies. No push or tag is part of this commit.
