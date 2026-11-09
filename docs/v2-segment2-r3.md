# V2 Scene 2 r3 — approved mask, native 720p, no notch

Review video: `out/v2-segment2-r3/review/segment-02-r3-preview-720p.mp4`.
Contact sheet: `out/v2-segment2-r3/review/segment-02-r3-contact.jpg`.
Validation: `out/v2-segment2-r3/review/segment-02-r3-validation.json`.

The user approved the OpenCV composited still generated from their matching 1280×720 reference and alpha mask, then authorized regeneration of Scene 2 at 720p with no notch anywhere. Approved inputs and fitted-corner metadata are snapshotted in `production/v2/scene-02/references/approved-phone-*`. The original Scene 1 video remains untouched at its actual 1284×724 native resolution; it is not used as a differently sized replacement plate in this scene.

R3 is a native 1280×720 composition. The unencoded browser-rendered opening frame matches the approved composite RGB pixel-for-pixel (maximum difference zero). The approved plate and original alpha mask are used at native size. A high-resolution layer of the original dashboard is projected through those fitted corners and clipped by that exact alpha during the camera push, preserving the physical bezel, fingers and scene outside the approved mask. The scene remains frozen; only the virtual camera moves. As the room clears, the existing shared display/bezel projective transform settles into the stationary front-facing showcase.

The phone mockup has `showNotch: false`, with zero notch dimensions. The entire notch, earpiece and camera subtree is omitted, rather than merely covered. Earlier V1/r1/r2 defaults remain unchanged. Sampled opening, zoom, transition and feature frames were visually checked; no hardware notch or camera cutout appears.

Timing remains 384 frames / 16 seconds at 24fps. The first 36 frames use the approved dashboard still so its contents stay consistent through the transition; the genuine dashboard recording then plays naturally for 6.5 seconds through the end of the eight-second aggregation section. SIP (8–9.5s), safe CAS (9.5–11s), Reports (11–12.5s), and privacy hold (12.5–16s) retain their prior content/timing. CAS shows only the real import-opening flow then Secure Local Import, with all 36 output frames visually audited. Reports ends on the real Custom-range frame.

No licensed music asset exists; the configurable music path remains null and the preview is digitally silent. The container includes approximately 43ms AAC padding, while video duration is exactly 16 seconds. Output is H.264 yuv420p, BT.709 limited-range matrix, 1280×720; no 1080p export or complete-film assembly was made. The source video, recordings, previous reviews and Segments 3/4 are unchanged.

Reproduce on fresh staging/output paths:

```sh
python3 scripts/prepare_v2_segment2.py manifests/v2-segment2-r3.json
npm run studio:v2
python3 scripts/render_v2_segment2_preview.py --manifest manifests/v2-segment2-r3.json
python3 scripts/validate_v2_segment2.py --manifest manifests/v2-segment2-r3.json
```

The helpers and separate V2 entry default to r3. Staging/rendering refuse overwrites. Masks and references are not resized in preparation. The layout grid scales typography from the existing design, while the composition and approved reference remain native 720p. Optional earlier revisions are reproducible with explicit manifest props. Chromium is required for rendering; asset preparation uses the standard library and FFmpeg. The existing optional OpenCV environment was used only for the approved still and visual inspection.

Actual Chromium render, original public-asset checks, main-project build, full decode, frame count/rate/geometry, silent audio and immutable-input SHA256 checks passed. All current code-dependency inventories validate. No commit requested; awaiting video review.
