# Scene 9 same warm-chroma correction — v5 review

User request: apply Scene 8’s correction to Scene 9 too.

Input: `output/scene-01-10-preview-v4-scene8-color-match.mp4`.
New full-film output: `output/scene-01-10-preview-v5-scene8-9-color-match.mp4`.
Configuration: `manifests/scene01-10-scene9-color-match-v5.json`.
Reproduce with `python3 scripts/correct_preview_color_matrix.py manifests/scene01-10-scene9-color-match-v5.json`.

Exactly the same constant warm-chroma scale 0.8 is used: for U below neutral 128, use `128+(U-128)*0.8`; pass Y, V and all U values at/above neutral through unchanged. Explicit y=val/v=val preserve highlights, shadows and the other chroma plane. No retuning, geometry changes, tracking, AI generation, timing or audio changes.

Scene 9 is [1009,1130), 42.041667–47.083333 seconds at 24fps. The correction also carries through the held Scene 9 image during the end card’s initial 12-frame fade [1130,1142), preventing an uncorrected-color return on the frozen frame. The fully opaque end card [1142,1250) remains untouched. Some late fade frames may have no warm-side chroma samples left and thus remain identical despite being inside the processing interval.

The prior Scenes 4–5 matrix fix and Scene 8 color match are preserved. The new output retains 1920×1080, 24fps, 1250 frames / 52.083333 seconds, lossless H.264 yuv420p and copied AAC audio. Existing original and review files stay untouched. Source hashes, decoded frame identity outside the correction interval, identical full-film luminance/V planes, identical decoded audio, output geometry/timing and full decode are checked by the helper. Validation results are saved alongside the video. This is a review export, not a replacement of the tagged baseline, and no commit is implied.

Final validation passed: all 121 Scene 9 frames and nine held-image fade frames changed, totaling 130 frames; all 1120 other frames match v4 exactly. Entire-film Y and V plane hashes match, decoded audio matches, source SHA256 is unchanged, and full decode passed. The full-opacity end card remains pixel-identical. Before/after contact sheet: `output/scene-01-10-preview-v5-scene9-comparison.jpg`.
