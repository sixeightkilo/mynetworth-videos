# Codex handoff — approved MyNetWorth production project

Last updated: 8 November 2026. This document carries the decisions and validated state from the animation/rough-cut conversation into a new Codex session.

## Read this first

The user has approved the current integrated-dashboard rough cut. Do not redesign or regenerate it to recover context. The project has already been selectively migrated from `/home/dev/mynetworth-video-generator` to `/home/dev/mynetworth-videos`; the new project is the production workspace. Git branch `master`, baseline commit `69c1f74` (`Initialize MyNetWorth production project from approved rough cut`). At handoff preparation the new working tree was clean. This handoff and the AGENTS.md startup link are subsequent documentation changes.

Read README.md for setup and commands, AGENTS.md for working rules, manifests/production.json for all ten scenes and missing inputs, then docs/migration-validation.json for evidence. Filesystem permissions belong to each session: the previous session could read the destination but write only to the old project and /tmp, so the user moved the staged project. Start future Codex sessions from the production directory with that directory writable.

Latest user request: create this handoff so a fresh Codex session has context. There is no active request to alter the approved film, render a final 1080p export, regenerate footage, publish, or replace voices. Ask what the next production change should be after reading context rather than assuming it.

## Approved outputs and proof

- Full film: 1349 frames, 56.208333 seconds, 1280×720, 24fps, H.264 + AAC temporary dialogue.
- Scene 6–7 preview: 418 frames, 17.416667 seconds, same resolution/frame rate.
- `references/approved-rough-cut-720p.mp4` and `references/approved-scene6-7-720p.mp4` are approval comparison copies, ignored by Git.
- `public/composites/scene6-7-integrated-approved.mp4` is an actual production dependency, tracked by Git. Do not remove it as though it were a disposable render.
- Migration verification: both videos were rebuilt byte-for-byte identically to their approval references. Full-film decoded audio also matched exactly, video PSNR was infinite, full decode passed, no full black frames were detected, and all 22 migrated asset hashes passed.
- All five migrated Remotion compositions bundled successfully. Browser rendering was not validated: Chromium was blocked by the old environment (SIGTRAP / sandbox permission errors). Working approval/reproduction output came from FFmpeg assembly of existing media; older editable previews used Pillow/FFmpeg. Do not claim a successful browser render merely because bundling passed.
- Source footprint: 22 real copied production assets, approximately 70 MiB. No runtime symlinks or dependency on the original project location.

## Current scene ledger

Frame intervals are end-exclusive, measured globally at 24fps. Scene 10 intentionally overlaps Scene 9 for 17 frames.

| Scene | Frames | Runtime source / treatment |
|---|---|---|
| 1 Opening conversation | 0–121 | public/scenes/1-opening-clean.mp4 |
| 2 Notification received | 121–242 | public/scenes/2-notification-received-clean.mp4 |
| 3 Frustration | 242–363 | public/scenes/3-frustration-clean.mp4 |
| 4 Revelation | 363–484 | public/scenes/4-revelation-clean.mp4 |
| 5 Introduction | 484–605 | public/scenes/5-introduction-clean.mp4 |
| 6 MyNetWorth + phone transition | 605–759 | First 154 frames of approved integrated Scene 6–7 composite |
| 7 Product demonstration | 759–1023 | Remaining 264 frames of that same composite |
| 8 Vijay doubts | 1023–1144 | public/scenes/8-vijay-doubts.mp4 |
| 9 Conclusion | 1144–1265 | public/scenes/9-conclusion.mp4; outgoing end-card fade |
| 10 End card | 1248–1349 | public/branding/end-card-approved.png |

Scenes 1–5, 8 and 9 are 121-frame clips; some are 1284×724, so the assembly fits them into 1280×720 without stretching, adding tiny side margins. Do not crop or distort them to eliminate those margins.

End card text is exactly:

- MyNetWorth
- All Your Investments. One Clean Dashboard.
- Available on Android

Fade: 17 frames / 0.708333 seconds. Full-opacity hold: 84 frames / 3.5 seconds. Existing dialogue is temporary; no new music or voice replacement was requested. Scene 9 audio fades during the end-card crossfade.

## Critical Scene 6 → 7 decisions

The replacement `public/scenes/6-zoom-on-app.mp4` has the real dashboard integrated throughout. Do not add another tracked overlay on top. Inspection showed that its camera reaches the approved takeover pose at frame 120, while the old approved transition reaches it at frame 90. Background/people matching excluded the phone and confirmed frame 120 as the closest match; this is an observed correspondence, not guessed timing.

The tested assembly is:

1. New integrated source video frames [0,120).
2. `public/composites/scene6-7-approved-transition.mp4` frames [90,388).
3. New source dialogue plays once, through its original 121-frame duration, with a six-frame tail fade. Legacy composite audio is muted to avoid repeating dialogue.

Total: 120 + 298 = 418 frames. Scene 7 starts at combined frame 154. The new camera approach adds 30 frames / 1.25 seconds compared with the earlier preview; later scenes move accordingly. Preserve the approved digital zoom, perspective settling, rightward phone movement and four-frame handoff. The phone must not jump in scale/position/orientation or pause on a black frame.

For the main film, use the complete baked integrated composite. `ApprovedScene6And7` can reproduce the join independently. `EditableScene6And7` reconstructs the working phone transition and Scene 7 code for future changes; it is deliberately separate from the authoritative baked approval. Editable text/rasterization can differ slightly across machines.

## Scene 7 product showcase

Approved duration is 264 frames / 11 seconds. Phone frame stays stationary, slightly right of centre at (880,360), approximately 640px tall in the 720p design. Realistic black bezel, rounded screen mask and notch. Simple light background. Left-side real logo/product name and synchronized feature captions. App screens keep their original colours and portrait aspect ratio. Never apply a parent grayscale filter to app content.

Captions are exact:

- Dashboard: All investments. One dashboard.
- SIP: Track your SIPs
- Reports: Reports that make sense
- CAS: Import your CAS. Skip manual entry.

The user supplied LosslessCut exports and explicitly asked that they be used. Current selections are in manifests/scene7.json; timestamps refer to the exported clips, not original .llc source coordinates (stream-copy exports included preroll).

| Feature | Local start frame | Migrated recording | Selected content |
|---|---|---|---|
| Dashboard | 0 | app-recordings/dashboard.mp4 | Source 1.000–4.000s; 72 frames |
| SIP | 68 | app-recordings/sip.mp4 | Source 4.750–7.500s; 66 frames |
| Reports | 130 | app-recordings/reports.mp4 | Source 2.750–5.500s; 66 frames |
| CAS | 192 | app-recordings/cas-import.mp4 | Source 1.416667–2.541667s; 27 frames |

Features overlap for four-frame subtle fades. CAS then holds screenshots/import-local.png for 18 additional frames (0.75s), then screenshots/dashboard-opening.png for 27 frames (1.125s), labelled Demo portfolio. The final image is the original dashboard recording's opening frame: NO repeat scroll.

Privacy is a hard constraint from the user: their only CAS is personal. Do not show PAN entry, the PAN prompt, the file picker or personal imported holdings. Do not fake import completion. Show import starting, then clearly labelled demo portfolio. The edited source recording contains portions beyond approved trims; its presence on disk does not authorize showing those portions.

## Migration architecture and files

- src/index.jsx registers ApprovedRoughCut720p, Production1080p, ApprovedScene6And7, EditableScene6And7, EditableScene7.
- src/compositions: assembly and combined previews, separate from individual scenes.
- src/scenes: working editable phone transition and showcase implementations.
- src/transitions: original approved easing, perspective/camera motion and combined wrapper positioning.
- src/components: PhoneMockup and proper perspective screenTransform.
- manifests/production.json: ten-scene inventory and missing inputs.
- manifests/approved-720p.json: source order, frame starts/durations, end-card overlap.
- manifests/scene6-7.json: exact source/composite join and dialogue fade.
- manifests/phone-transition.json: geometry, original dashboard coordinates, phone model and editable takeover shifted to new frame 120.
- manifests/scene7.json: recordings, source timestamps, captions, phone position and still holds.
- manifests/asset-checksums.json: approved assets, hashes and original provenance (historical paths are not runtime dependencies).
- manifests/reference-checksums.json: approval reference hashes.
- public/scenes: production footage; public/composites: baked approved inputs; app-recordings/screenshots/branding/phone: editable media.
- docs/prompts/rough-cut-brief.txt: existing assembly instructions copied verbatim, NOT original Kling prompts.
- docs/approval-history: original milestone notes and timing reports; original absolute paths in historical notes are retained for provenance only.
- out: ignored generated videos/bundles/logs. references: ignored comparison videos, not needed to render. Source/composite MP4s under public are tracked.

Original assets/experiments/archive remain at `/home/dev/mynetworth-video-generator`; selectively migrate any additional item only if genuinely needed. Do not wholesale-copy the experimental project. In particular, old character/cat animations, obsolete test compositions, OpenCV diagnostics and tracking models were intentionally excluded.

## Commands and toolchain

From the production root:

```sh
npm ci
npm run verify
npm run build
npm run studio
npm run render:rough-cut
npm run validate:rough-cut
npm run render:scene6-7
```

Output files: out/mynetworth-rough-cut-720p.mp4 and out/scene-6-7-preview.mp4. validate:rough-cut reports reference comparison skipped if the optional reference is absent; do not claim fidelity in that case. It verifies source hashes, video geometry/frame count, audio presence, full decode, no black frames and reference video/audio when available.

Node 24 / Python 3.10 / FFmpeg were used. React 19.0.0 and Remotion 4.0.373 are pinned in package-lock.json. Production Python scripts need only the standard library. No OpenCV, NumPy or Pillow dependencies are needed in this project.

During migration npm's esbuild post-install subprocess check failed with sandbox EPERM. `npm ci --ignore-scripts` succeeded, and bundling then passed. Offline validation used a temporary npm cache under /tmp; it is not part of the project. The first install attempt accidentally ran in the old project and refreshed generated node_modules; those dependencies were restored from the unchanged original lockfile, and source/config/media files were not altered. This is documented in docs/migration-validation.json.

## 1080p and missing inputs

The project is prepared for 1920×1080 at the existing 24fps:

```sh
npm run render:1080p
# Optional browser route when Chromium works:
npm run render:1080p:remotion
```

These preserve the approved timing/layout, but current scene masters and composites are ~720p and will be upscaled. No final 1080p export was rendered or approved during migration. Native 1080p masters were not found. Original Kling generation prompts for Scenes 1–6, 8 and 9 were not found. Final replacement dialogue/voice tracks were not supplied. Exact redistributable Arial font files are not bundled; editable scenes use Arial with sans-serif fallback, while approval text is already baked.

Do not invent prompts, dialogue, high-resolution source detail or completed import states to fill these gaps. No source-footage regeneration is authorized by the migration request.

## Lessons from earlier experiments

Earlier phone-screen work tried manual Procreate keyframes, corner interpolation, then offline pyramidal LK/RANSAC tracking. Tracking was stable between anchors, but instantaneous anchor replacement at 79/96/120 introduced visible pose jumps; targeted correction windows were explored, and indiscriminate smoothing could reintroduce drift. Those experiments belong to the original archive and are not production dependencies. Do not restart tracking or introduce new AI models to reproduce an already-baked approved composite.

Keep image/source timestamp coordinates distinct from output frame indices, especially with VFR Android recordings. Use a proper projective transform, preserve bezel/finger occlusion, and do not change the fixed dashboard UI. Inspect assets and actual footage when a mapping is uncertain. Never infer successful screen alignment solely because stored reference coordinates match one another.

## Collaboration preferences and next session

The user prefers concrete work and few unnecessary confirmation loops. Inspect existing files and preserve approvals; keep changes minimal and independent. Use clear brief updates during sustained work. Do not ask again for permission already granted, but source regeneration, publishing and changes outside a newly requested scope require explicit direction.

The old request to keep intermediate files under kling-video applied to the experimental workspace. The approved production migration intentionally replaces it with the documented structure: generated production artifacts belong in out, tracked documentation in docs, immutable inputs in public. Do not nest the old project layout back inside the production repository.

On startup: read this document and AGENTS.md, inspect git status, and retain any user changes. Handoff documents may be uncommitted immediately after the user copies them into the new project; preserve and commit them when appropriate. The migration baseline is complete and proven. Continue from the user's next requested task rather than modifying approved scenes speculatively.

## Latest checkpoint — Scenes 01–05 preview, 7 November 2026

The user reviewed `output/scene-01-05-preview-v1.mp4` and said it looks acceptable with a few wrinkles remaining. They requested a commit of everything required to reproduce it. This is a separate partial review preview: 1920×1080, 24fps, 623 frames / 25.958333 seconds, with original soundtracks and a silent Scene 05. The approved 1349-frame ten-scene baseline remains unchanged.

Read `docs/scenes01-05-preview.md` and `manifests/scene01-05-preview-v1.json` for the current source selections and reproduction commands. Scene 03 keeps [0,110); accepted dashboard Scene 04 v2 keeps [18,121); Scene 05 uses the complete `scene-05-two-phase-v5.mp4`. Scene 04 appears once. Scene 05 v5 stops its push-in while the entire display is visible, then transforms the full screenshot and geometric bezel together into the existing showcase pose. Its final entry/configuration are `src/scene05-two-phase-preview.jsx` and `manifests/scene05-two-phase-v5.json`. Earlier graph-crop and independent screen-rotation experiments are superseded and not required.

The latest assembly and both v5 preparation layers were reproduced byte-for-byte. Review stills, 200% edge checks and render reports are retained beside the v5 media. Pinned npm dependencies and optional OpenCV/NumPy requirements are versioned; environments/caches stay ignored. Nothing depends on the old experimental project or disposable `out/` files. Existing app showcase and approved Remotion assembly were not modified. No publishing, source regeneration or further integration was requested.

## Latest checkpoint — Scenes 01–07 continuity preview, 7 November 2026

The user requested committing and tagging `output/scene-01-07-preview-v1.mp4` as `baseline-scenes-01-07-v1`. Read `docs/scenes01-07-preview.md` and `manifests/scene01-07-preview-v1.json` for the exact assembly. It is 888 frames / 37 seconds, 1920×1080 at 24fps. All 623 frames and the original audio of the accepted Scenes 01–05 prefix are preserved exactly in decoded comparisons.

The appended legacy selection is `public/composites/scene6-7-integrated-approved.mp4` [153,418): one aligned final Scene 6 frame plus the full 264-frame Scene 7. Old Scene 6 [0,153) and its dialogue are intentionally skipped because the new Scene 5 already performs the room-to-phone zoom; the entire old Scene 6 was not appended. Scene 7 recordings, captions, transitions and privacy-safe ending remain baked and unchanged. The 720p tail is upscaled, not native 1080p detail. Small raster/bezel/status-bar differences remain and were not polished.

`scripts/extend_preview_with_legacy.py` reproduces this append with Python standard library and FFmpeg only. The output was reproduced byte-for-byte. Inputs, validation/contact/notes and checksum inventory are versioned; intermediate upscale/concat files remain disposable under `out/`. The original ten-scene baseline and previous Scenes 01–05 tag are untouched. Scenes 08–10 remain to be appended. The user's priority is completing the film before polishing individual scenes; do not redesign or regenerate approved material.

## Latest checkpoint — Scenes 01–08 preview, 8 November 2026

The user requested appending the new production Scene 08 and committing all dependencies for this stage. Current output: `output/scene-01-08-preview-v1.mp4`, 1920×1080, 24fps, 1009 frames / 42.041667 seconds. Read `docs/scenes01-08-preview.md` and `manifests/scene01-08-preview-v1.json` before further assembly work.

The first 888 decoded video frames are identical to `scene-01-07-preview-v1.mp4`. The complete new `production/scene-08/output/scene-8.mp4` (121 native 1080p frames) begins at frame 888 / 37 seconds, with its original dialogue and no trimming. The older public Scene 08 stays with the original ten-scene baseline. The transition is a direct cut from the app showcase to the living room; no polishing or added transition was requested.

`scripts/append_preview_clip.py` uses Python standard library and FFmpeg/FFprobe. It copies prefix video frames, normalizes timestamps through video-only concatenation, pads the shorter prefix audio through its silent showcase to 37s, appends Scene 08 audio, then encodes the joined AAC track. Audio contents are retained and zero-lag correlation verified; compressed audio is re-encoded. The result was reproduced byte-for-byte. All source inputs, prompt/reference, code, manifests, preview and validation evidence are versioned. Disposable work stays under ignored `out/`. Previous previews, baseline tags and approved compositions are untouched. Scenes 09–10 remain to be appended; finish assembly before refining wrinkles.
