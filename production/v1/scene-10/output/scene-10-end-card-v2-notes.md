# Scene 10 review — v2

Standalone: `scene-10-end-card-v2.mp4`; final still: `scene-10-end-card-v2-final.png`; contact sheet: `scene-10-transition-v2-contact.jpg`.
Complete film: `output/scene-01-10-preview-v2.mp4` with validation report alongside it.

1920×1080, 24 fps, H.264. Scene 10 is 120 frames / 5 seconds. Its 12-frame (0.5-second) gentle fade starts on the exact held final frame of Scene 9. The complete stationary card holds for 108 frames / 4.5 seconds. Total film: 1250 frames / 52.083333 seconds. No new audio; Scenes 1–9 decoded video and audio are identical to the input preview.

Uses the actual `public/branding/logo.png` shield with its off-white background removed, DejaVu Sans typography and navy #0A172B. Original logo and all approved media remain untouched. Requested wording appears verbatim. No AI generation.

Implementation: `manifests/scene10-end-card-v2.json`, `src/scenes/Scene10EndCard.jsx` and `src/compositions/Scenes01To10Review.jsx`. Both new compositions are registered in `src/index.jsx`; the earlier approved compositions remain unchanged.

Reproduction on fresh paths: run `python3 scripts/prepare_scene10_source_assets.py`, then `python3 scripts/prepare_scene10_end_card.py`. Render `Scene10EndCard1080p` with Remotion using the staged public directory `out/scene10-end-card-v2/public`, H.264 CRF 14 and working Chromium. Preserve this raw render under a separate filename, then run `python3 scripts/normalize_scene10_video.py RAW_RENDER.mp4` and `python3 scripts/append_scene10_end_card.py`. Helpers refuse to overwrite outputs. Existing derivatives and staged files must not be overwritten; use a new manifest with fresh paths for another version.

PNG colour-profile metadata is stripped without changing pixels to prevent browser brightness changes at the held-frame boundary. Only the new card video is normalized to the prefix’s BT.709 limited-range H.264 format. The full preview copies existing Scenes 1–9 video and audio rather than re-encoding them. Original audio ends naturally at the card; the card is silent.

Validation: actual Chromium render, production build, all 22 approved asset checksums, 1250-frame full decode, exact decoded prefix video/audio comparison, exact browser starting-frame RGB comparison and stationary rendered hold checks passed. No new limitations in the static card; earlier footage retains its existing source-resolution/upscaling limitations. Awaiting user review; no commit or integration approval implied.
