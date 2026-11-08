# Scenes 01–10 color-matrix correction — v3

Review output: `output/scene-01-10-preview-v3-color-fixed.mp4`.
Input: `output/scene-01-10-preview-v2.mp4` (the tagged Scene 10 baseline).

At 24fps, global frame 400 / 16.666667s cuts from Scene 3 source frame 109 to Scene 4 source frame 18. The original Scene 4 source is BT.709. Its OpenCV RGB-to-YUV export used an implicit BT.601 matrix with no color tags. Scene 5 is explicitly tagged BT.470BG (BT.601). The Scenes 1–5 concat preserved those YUV values while signalling BT.709 for the assembled stream, causing a warmer tint. No Remotion parent filter causes the shift. Later BT.709 scenes and the end card do not inherit this mismatch.

User authorized the proposed fix: convert only global frames [400,623), covering the selected Scene 4 composite and all of Scene 5, from BT.601 limited-range YUV to BT.709 limited-range YUV. This new export applies that mathematical conversion directly to the existing assembly using FFmpeg’s colorspace filter, explicitly holding BT.709 primaries and transfer fixed while converting the BT.601 matrix. A preliminary default-scaler draft showed a small neutral brightness offset; the colorspace path avoids that offset and the draft stays under ignored out/. There is no creative grade, tracking rerun, regeneration, timing change or audio processing. Existing sources, compositions, approved renders and tags remain untouched. The small earlier RGB round-trip difference already baked into Scene 4 is retained.

Reproduce with `python3 scripts/correct_preview_color_matrix.py manifests/scene01-10-color-fixed-v3.json`. Requires Python standard library, FFmpeg and FFprobe only. Refuses to overwrite the output. Intermediate diagnostics belong under `out/scene01-10-color-fixed-v3/`.

The review uses lossless H.264 (High 4:4:4 Predictive profile, actual pixel format yuv420p) so unaffected decoded YUV frames remain exact. It is larger than a normal distribution encode, approximately 146 MiB. An ordinary delivery encode can follow approval. Original AAC audio is copied.

Validation: 1920×1080, 24fps, 1250 frames / 52.083333s, start timestamp zero; BT.709 primaries, transfer and matrix, limited range. Exactly 223 corrected frames changed. All 1027 other decoded video frames match the v2 input exactly; the complete decoded audio matches exactly. Source hash unchanged and full video/audio decode passed. The original 22 approved asset checks also passed. No new browser render is needed because the correction operates on the baked preview.

Before/after contact: `output/scene-01-10-preview-v3-color-comparison.jpg`. Machine-readable validation: `output/scene-01-10-preview-v3-color-fixed.json`. Awaiting visual review; no commit or replacement of the tagged baseline is implied.

Sampled source comparisons confirm removal of the channel bias. At frame 400, mean RGB shift relative to the standalone composite falls from (+3.759,+2.774,−1.510) to (−0.255,−0.065,+0.029) levels out of 255. At frame 560 it falls from (+3.510,+2.413,−1.508) to (−0.248,−0.174,+0.142). Minor chroma resampling and earlier source compression differences remain.
