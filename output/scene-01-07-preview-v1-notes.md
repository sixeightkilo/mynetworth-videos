# Scenes 01–07 temporary assembly v1

Preview: `output/scene-01-07-preview-v1.mp4` — 1920×1080, 24fps, 888 frames / 37 seconds.

Scenes 01–05 are the existing accepted `scene-01-05-preview-v1.mp4` (623 frames). Its video packets are copied without re-encoding, and its original audio is copied. Decoded frame hashes for all 623 frames and decoded PCM audio match the accepted preview exactly. The source file is unchanged.

Appended media is `public/composites/scene6-7-integrated-approved.mp4`, frames [153,418): the final aligned app-facing frame of the earlier Scene 6, then the complete 264-frame Scene 7. The earlier Scene 6 approach, frames [0,153), and its temporary dialogue are skipped: the current Scene 5 already performs the room-to-phone transition. This continuity selection avoids replaying the zoom or cutting back to the older room footage. It is not a claim that the entire original Scene 6 runtime was retained.

The full Scene 7 timing, dashboard/SIP/reports/CAS recordings, captions, baked four-frame transitions, Secure Local Import hold and static Demo portfolio ending are unchanged. The selected legacy range was verified digitally silent; no new soundtrack was added. Existing audio ends with the accepted prefix and the appended segment is silent.

The legacy 1280×720 media is upscaled with Lanczos to 1920×1080 for this temporary preview; it does not contain native 1080p detail. No source regeneration, tracking reconstruction or scene redesign was performed.

## Quick continuity check

At the join, the dark phone bounds measure 960px high in the last Scene 5 frame and 959px in the first appended frame. Horizontal center is 1319.5px in both; vertical center differs by 0.5px. Dashboard source screenshot hashes match between the newer and older projects. The framing and scale therefore align closely.

Visible differences remain: the older section is softer, with small bezel/shadow/rasterization changes. The original showcase fade introduces the recording's status bar and slightly different displayed portfolio values. These have been left as-is for assembly review, not polished. Earlier source-clip discontinuities in Scenes 01–05 are preserved.

Both streams fully decode; the output contains exactly 888 frames at 24fps. Source checksums remain unchanged; all 22 baseline asset checks pass. The original approved ten-scene rough cut and the accepted Scenes 01–05 baseline are untouched.

Reproduction: `python3 scripts/extend_preview_with_legacy.py manifests/scene01-07-preview-v1.json`. The script refuses existing outputs/intermediates; use a copied manifest with unused `output` and `workDir` paths for another run. Python standard library, FFmpeg and FFprobe only. No dependency on the original experimental project path.
