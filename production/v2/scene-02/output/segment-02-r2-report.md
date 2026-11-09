# Segment 2 r2 — screen fit and first-frame correction

Two checks confirmed the reported appearance:

- The recording already filled the mockup’s inner glass. Its aspect-ratio mismatch contributed less than one recording pixel of side padding; the dominant inset was the 56-unit geometric bezel (about 15 pixels per side in the 720p preview).
- Approved Segment 1 really ends on Kling’s placeholder display. R1 also deliberately started the screen overlay at opacity zero, leaving that placeholder visible on Segment 2’s first frame.

R2 uses a 24-unit bezel (about 6.7 pixels per side at 720p), with the outer corner radius matched to the inner radius plus bezel. Phone height and center stay unchanged; the actual visible display is slightly larger inside that outline. `objectFit: cover` removes the subpixel aspect-fit gap without stretching the interface; the aspect difference crops approximately one input pixel at the top and bottom. The app’s own internal whitespace/card padding remains part of the real recording.

The real dashboard is fully visible from Segment 2 frame 0, mapped to the manually measured source-screen corners. The original scene image remains behind it; only the screen contents change at the cut. The approved Segment 1 MP4, its audio and its final placeholder frame are unchanged. Making the dashboard appear inside the end of Segment 1 itself would require a separate derived edit; that was not done.

Current config: `manifests/v2-segment2-r2.json`. Existing r1 config and review videos are preserved. Text, timing, app-recording selections, privacy constraints, music configuration and 16-second duration remain unchanged. Only 720p previews were rendered; no final full-resolution video or commit.

Outputs:

- `segment-02-r2-preview-720p.mp4` — standalone.
- `segment-01-to-02-r2-boundary-720p.mp4` — approved final two seconds plus Segment 2.
- `segment-02-r2-fit-comparison.jpg` — old/new phone fit and first-frame proof.
- `segment-02-r2-validation.json` — actual geometry, full-decode, silence and source-hash checks.

The preparation, preview and validation helpers now default to r2. To reproduce r1, pass its manifest explicitly (and use fresh output/staging paths). The preview helper passes the chosen config to Remotion. `src/v2/index.jsx` defaults to r2; existing main-project compositions are unaffected. Music is still unavailable and configurable; the standalone preview is silent.

Validation passed: 384/432 video frames at 24fps, full decode, BT.709 matrix, unchanged input hashes, silent standalone audio and original boundary audio followed by silence. Measured straight side bezels are 14px in r1 and 6px in r2 at the sampled 720p row. The dashboard is present at frame 0 in both standalone and boundary playback. The first parallel boundary render timed out under contention; rendering it alone succeeded.
