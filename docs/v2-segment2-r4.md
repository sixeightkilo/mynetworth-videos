# V2 Scene 2 r4 — geometric screen edges during zoom

Output: `out/v2-segment2-r4/review/segment-02-r4-preview-720p.mp4`.
Before/after close-up: `out/v2-segment2-r4/review/frame20-before-after.jpg`.

The user’s mpv screenshot corresponds to r3 frame 20 (0.833s), at 3.568× digital magnification. R3 enlarged the original raster alpha boundary with the room plate, magnifying single-pixel steps. The source mask fit was correct; its raster edge was inappropriate as the magnified rendering boundary.

R4 retains the approved plate at frame 0. Over four frames, a clean rounded display and narrow geometric rim enter as one opacity group. The original high-resolution screenshot projects directly into the final camera-transformed quadrilateral, rather than being rendered into the tiny source screen and enlarged afterward. The rim locally covers the old raster fringe inside the original phone silhouette. Fingers, hand and room remain the original photo; no global blur, AI reconstruction, tracking change or color grade is applied. The original soft outer phone image can still soften during digital magnification; the screen boundary itself is analytic geometry.

The camera trajectory, fitted screen corners, screen size, phone position, subsequent perspective settle, caption timing, app-recording selections, CAS privacy trims, silent music-null setting and 16-second duration are unchanged from r3. The entire notch/earpiece/camera subtree remains disabled. The geometry fade is grouped so screen brightness does not dip as a black frame and partial screen overlap. Once the room clears, the same plane continues as the stationary showcase phone.

The browser samples at 2× dimensions solely for antialiasing. FFmpeg downsamples to the requested 1280×720 using Lanczos, H.264 CRF 14, yuv420p and BT.709 limited range. The 2× intermediate is disposable under out/ and is not a higher-resolution production deliverable. No source media was regenerated. Existing inputs, masks, approved reference still and earlier previews are preserved.

Configuration: `manifests/v2-segment2-r4.json`. The preview helper honors `renderSupersampling`, selected manifest dimensions and old revision configurations. Preparation, preview and validation now default to r4:

```sh
python3 scripts/prepare_v2_segment2.py
python3 scripts/render_v2_segment2_preview.py
python3 scripts/validate_v2_segment2.py
```

Use fresh revision paths to avoid overwriting existing staging or review files. The real music asset remains missing; the preview is silent. Original Scene 1 and Scenes 3/4 are untouched. No full-film assembly or commit requested.

Final checks passed: actual Chromium render, full decode, 1280×720 / 24fps / 384 frames (16.0 video seconds), zero standalone audio peak, preserved input hashes and previous r3 media. All code-dependency inventories and approved asset checks validate. The current native opening-frame RGB check is pixel-identical to the approved reference. Actual encoded frame 20 and the contact sheet were inspected; the high-contrast display boundary is smooth, with source outer-bezel softness retained. The final H.264 file has approximately 43ms silent AAC padding beyond the 16-second video track.
