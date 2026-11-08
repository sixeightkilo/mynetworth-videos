# Scene 8 restrained color match — v4 review

New full-film review: `output/scene-01-10-preview-v4-scene8-color-match.mp4`.
Based on the accepted-for-review matrix-corrected v3 export, retaining its Scene 4–5 fix. Earlier renders and source footage stay untouched.

The app showcase ends at frame 888 / 37 seconds. Scene 8 occupies [888,1009), ending at 42.041667 seconds. Its warmer yellow cast is baked into the original Scene 8 source; both source and assembly correctly signal BT.709. This is a scene-specific color match, distinct from the earlier matrix repair.

Reference: Scene 3 source frame 109, comparing clear static wall regions (1660,80)–(1800,160), (1650,300)–(1800,420), (850,80)–(1000,200), and (1660,480)–(1800,600). Scene 8 wall blue values were approximately 5–7 levels lower. Tested warm-chroma scales 0.85 and 0.80; 0.80 gave the closer background match without changing brightness or imposing an overall cool cast.

Correction: only for U below neutral 128, use `128 + (U-128)*0.8`. Leave Y, V and U at/above neutral untouched, explicitly using y=val and v=val to prevent the LUT filter’s default legal-range clipping. This restrains yellow chroma while preserving luminance, neutral chroma and blue tones. It is a constant scene-wide operation with no temporal adaptation, geometry edits, sharpening, tracking, AI generation or audio processing. Warm-colored pixels in the phone content are also subject to this small correction; there is no separate phone replacement. Original scene lighting and fine source differences are intentionally retained.

Manifest: `manifests/scene01-10-scene8-color-match-v4.json`.
Reproduce: `python3 scripts/correct_preview_color_matrix.py manifests/scene01-10-scene8-color-match-v4.json`.
The helper now supports either the v3 matrix repair or a separately specified warm-chroma scale. The v3 manifest and its conversion remain unchanged. Python standard library and FFmpeg/FFprobe only; no runtime dependence on scratch measurements or OpenCV.

Output remains 1920×1080, 24fps, 1250 frames / 52.083333s. Lossless H.264 review encoding preserves all decoded frames outside Scene 8; original AAC audio is copied. The High 4:4:4 Predictive profile uses actual yuv420p pixels, as in v3, and produces a larger review file than a distribution encode. The machine-readable report beside the MP4 records frame comparisons, audio identity, source hash and full-decode validation. No commit or approved-baseline replacement is implied; awaiting visual review.

Visual spot checks at 37.0, 39.5 and 42.0 seconds show a stable, reduced yellow cast. At the first Scene 8 frame, a wall sample changes from RGB (218.34,171.32,144.33) to (218.34,170.59,150.75), closer to reference (216.90,168.88,150.29). All 121 Scene 8 frames changed and all 1129 other decoded frames match v3 exactly; complete decoded audio and input SHA256 are unchanged, and full decode passed. The final review preserves the earlier matrix correction.

Final plane-level SHA256 comparisons confirm that Y (luminance) and V (red chroma) are identical across the entire film. Only the intended warm-side U chroma samples in Scene 8 differ. Neutral values and superwhite/superblack luma values are preserved.
