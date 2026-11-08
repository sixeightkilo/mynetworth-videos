# Scene 04 full dashboard replacement — review render v2

Output: `production/v1/scene-04/output/scene-04-dashboard-tracked-full-v2.mp4`

Original first-pass video and approved POC preserved. Same manual-anchor/OpenCV/FFmpeg implementation extended to the full shot; Remotion unchanged.

- 1916 × 1080, 24fps, 121 frames, 5.041667s video.
- Original AAC copied without re-encoding. Decoded audio matches exactly.
- Dashboard hidden through frame 72; edge-on retrieval preserved. Reveal begins at frame 73 (3.041667s), settles to full opacity at 75.
- New per-frame manual screen corners at 73–76; additional rotation anchors 77–82 and final anchors 110/115/120. POC anchors 84–107 retained.
- Rounded screen aperture, notch cutout, original-frame fingertip holdout, minimal feather. No source frame regeneration.
- Both final videos fully decoded; no adjacent duplicate frames. Source and approved POC hashes unchanged.

## Interval to review

Frames 73–80 (3.042–3.375s): fast rotation, motion blur, and fingers covering the screen. Manual checks corrected initial bottom-edge overshoot. Peak optical-flow corner-motion disagreement is 5.78px near frame 78; this is a tracker consistency measure, not a measured visible sliding distance. Frames 84–120 remain below 0.86px by the same check.

A thin dark source rim remains intentionally around the inset screen mask, and low-resolution screen text can alias during movement. No claim of perfect tracking through the blurred rotation. Review the comparison at normal speed and the contact sheet before assembly use.

Stopped after full-scene rendering. No Remotion changes, publishing or source overwrites.
