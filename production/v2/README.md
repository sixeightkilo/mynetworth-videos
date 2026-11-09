# V2 full-film checkpoint

Current approved output: `output/scene-01-04-review-music-r3-edge-fixed.mp4`. The edge correction is documented in `docs/v2-edge-fix-r1.md` (repository root), including fresh-path reproduction commands and tracked before/after evidence. It retains the soundtrack and framing while extending four adjacent columns across each padded edge.

The preserved pre-correction checkpoint follows.

Four scenes, 1280×720 at 24fps, 1418 frames / 59.083333s. Pre-correction soundtrack review: `output/scene-01-04-review-music-r2.mp4`; before music: `output/scene-01-04-review-r1.mp4`. Approved source videos remain untouched. The thin white edge padding is part of this checkpoint and remains preserved for comparison.

`../../manifests/v2-production-checkpoint.json` lists authoritative scene masters. Scene 1 dashboard composite and Scene 2 r4 baked outputs have been promoted from disposable out/ into their scene output folders, alongside source footage, masks and references. Scene 3 fitted output and Scene 4 end card are also preserved. Assembly/reproduction no longer requires recovering those accepted masters from an ignored cache. Optional compositing dependencies are pinned in `scripts/requirements-screen-compositing.txt`; OpenCV is not required to reproduce the film from these baked inputs.

From the repository root, reproduce the exact latest video:

```sh
npm ci
npm run verify
python3 scripts/reproduce_v2.py --output-dir out/v2-reproduction
```

Python standard library, FFmpeg and FFprobe suffice for the final assembly/music reproduction. Inputs are checked against `manifests/v2-production-checksums.json`. The helper renders into a new directory, refuses overwrite and compares its result byte-for-byte with the committed review. Encoder versions can affect byte identity on other systems; frame count, geometry and decoded comparison remain the meaningful cross-version checks.

For edits, authoring implementations/manifests are retained in src/v2/, scripts/ and manifests/v2-*. Source app recordings, screenshots and logo are existing tracked public/ and production/v1/ dependencies. Scene 1 compositor uses reviewed native-coordinate geometry; Scene 2 Remotion r4 uses the approved reference geometry and no notch. Scene 4 has its separate Remotion entry. See docs/v2-*.md for authoring commands and privacy-safe media selections. Never widen CAS trims.

Music source `audio/mynetworth-theme.wav` is the user’s updated 32.002902s composition, with source MIDI retained beside it. Settings are in `manifests/v2-soundtrack-r2.json`; the script calculates actual duration and loops with a one-second overlap. Gain: dialogue −10dB, showcase +4dB, end card +6dB; shared master −0.5dB; 0.8s entrance and 2s exit fades. The previous 43.637551s WAV was replaced by the user and is not required by the current checkpoint; older r1 reports are historical. The original dialogue/notification mix remains in the pre-music assembly.

All earlier V1 production, scenes and tags remain separate. Output paths under production/v2/output/ follow explicit user direction. Nothing is published or pushed by this checkpoint.
