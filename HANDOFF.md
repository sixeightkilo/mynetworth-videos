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

The first 888 decoded video frames are identical to `scene-01-07-preview-v1.mp4`. The complete new `production/v1/scene-08/output/scene-8.mp4` (121 native 1080p frames) begins at frame 888 / 37 seconds, with its original dialogue and no trimming. The older public Scene 08 stays with the original ten-scene baseline. The transition is a direct cut from the app showcase to the living room; no polishing or added transition was requested.

`scripts/append_preview_clip.py` uses Python standard library and FFmpeg/FFprobe. It copies prefix video frames, normalizes timestamps through video-only concatenation, pads the shorter prefix audio through its silent showcase to 37s, appends Scene 08 audio, then encodes the joined AAC track. Audio contents are retained and zero-lag correlation verified; compressed audio is re-encoded. The result was reproduced byte-for-byte. All source inputs, prompt/reference, code, manifests, preview and validation evidence are versioned. Disposable work stays under ignored `out/`. Previous previews, baseline tags and approved compositions are untouched. Scenes 09–10 remain to be appended; finish assembly before refining wrinkles.

## Latest checkpoint — Scenes 01–09 preview, 8 November 2026

The user requested appending the new Scene 09, then checking in and committing this stage. Current output is `output/scene-01-09-preview-v1.mp4`: 1920×1080, 24fps, 1130 frames / 47.083333 seconds. Read `docs/scenes01-09-preview.md` and `manifests/scene01-09-preview-v1.json` for the exact append and reproduction command.

The complete new `production/v1/scene-09/output/scene-09.mp4` (121 native 1080p frames) follows the unchanged 1009 video frames of the Scenes 01–08 preview, starting at frame 1009 / 42.041667s. There is a direct cut and no trimming. Scene 08's final pose and Scene 09's first pose match closely; small source differences remain. The existing `scripts/append_preview_clip.py` copies prefix video and re-encodes correctly padded/concatenated original audio. Decoded-prefix comparison, zero-lag audio correlation, geometry/frame-count/timestamp checks and full decode passed. Sources, older previews, baseline tags and approved compositions remain untouched. The end card / Scene 10 is still outstanding; complete the assembly before polishing.

## Latest checkpoint — Scenes 01–10 preview, 8 November 2026

The user requested checking in the completed Scene 10 stage. Latest film: `output/scene-01-10-preview-v2.mp4`, 1920×1080 at 24fps, 1250 frames / 52.083333 seconds. The original approved ten-scene baseline remains unchanged.

Read `production/v1/scene-10/output/scene-10-end-card-v2-notes.md` and `manifests/scene10-end-card-v2.json` for implementation and reproduction. The new Remotion end card uses the existing actual logo, navy background and requested text. It lasts 120 frames / 5 seconds: a 12-frame gentle fade from the held final Scene 9 frame followed by a 108-frame stationary hold. No new sound. The combined export copies the first 1130 video frames and original audio unchanged, verified by decoded comparisons. The standalone card is normalized to the prefix’s BT.709 limited-range H.264 format. Browser colour metadata correction preserves the exact starting-frame RGB pixels.

New compositions `Scene10EndCard1080p` and `Scenes01To10Preview1080p` are registered independently; earlier compositions and source assets stay untouched. Standalone, combined preview, final still, contact sheet, manifest, source derivatives and reusable Python/FFmpeg helpers are versioned. Actual Chromium rendering, npm build, approved asset verification, full decode, frame count, stationary hold and no-black-gap checks passed. Earlier footage retains its existing upscale limitations. Superseded Scene 10 drafts are retained under ignored `temp/scene10-superseded/`; intermediates remain under `out/`. No publishing or baseline tag requested.

## Latest checkpoint — production version 1 organization, 8 November 2026

At the user’s request, all existing contents of `production/` moved into `production/v1/`: the ten scene directories and shared references, including empty directories. This is a directory/version organization change, not a new render. All 50 moved media files are byte-identical. Active manifests, helper scripts, reproduction commands, reports and checksum inventories now use the versioned paths. Scene 5’s public asset root is `production/v1`; its staticFile paths remain relative to that root. Source code, `public/`, top-level `output/`, existing render revision names and baseline tags remain in place. Inventories have refreshed hashes for text dependencies whose path strings changed; media hashes are unchanged.

The latest review film is `output/scene-01-10-preview-v5-scene8-9-color-match.mp4` (1250 frames / 52.083333s, 1080p24). Since the tagged Scene 10 baseline, v3 repaired the BT.601/BT.709 interpretation in Scenes 4–5; v4 applied a constant warm-side U chroma scale of 0.8 to Scene 8; v5 applied exactly the same correction to Scene 9 and its held-image end-card fade. Luminance, V chroma, audio, timing and other scenes are verified unchanged for the scene-specific matches. The fully opaque end card stays identical. Midpoint stills for Scenes 1,2,3,8,9 are in `output/color-comparison-v5/`. Read the corresponding v3/v4/v5 notes and manifests for reproduction. The user requested committing these color-review changes, dependencies, outputs and the v1 reorganization together, with annotated tag `production-v1`. No push or publishing was requested.

## Git LFS repair for production-v1

The initial production-v1 tag push was rejected because the three lossless full-film v3/v4/v5 MP4s exceed the remote’s ordinary-file size limit. These three files now use Git LFS via explicit `.gitattributes` entries. Their bytes and all validation hashes remain unchanged. Git LFS is required to retrieve them (`git lfs install`, `git lfs pull`). The rejected checkpoint was unpublished, so only its local commit was amended and the local production-v1 tag recreated; earlier baseline history and tags remain intact. Do not restore the rejected ordinary-blob commit/tag.

## Latest work — V2 Segment 2 showcase preview

V2 has four scene/segment folders. Approved Segment 1 is `production/v2/scene-01/output/scene-01.mp4`: 1284×724, 24fps, 505 frames / 21.041667s; SHA256 `0260e671fd1757db2b030a22cfa82642ded971f7debe59f32faa3420a73b67af`. It must remain untouched.

Segment 2 is implemented separately in `src/v2/Segment2.jsx` / `src/v2/index.jsx`, with centralized `manifests/v2-segment2-r1.json`. It reuses the existing phone shell, projective transform and two-phase transition math, real dashboard/SIP/CAS/reports recordings and real logo. The phone shell gained optional recording children and a plain bezel style; old callers’ defaults stay unchanged. The current dependency inventory reflects those code/package changes. No approved media or existing composition entries were changed.

Review outputs and report live in `production/v2/scene-02/output/`. Duration is 384 frames / 16 seconds, including a 36-frame push/settle from the exact frozen final Segment 1 frame. A boundary preview adds the last 48 frames of Segment 1 before Segment 2. A complete Segments 1–2 composition is available but no full-resolution render is authorized. Segments 3–4 are untouched.

CAS is limited to the actual import-opening recording [1.416667,2.541667), then the actual Secure Local Import still. Reports uses [4,5.5), then its last Custom-range frame. Audit every CAS output frame: an internal draft exposed a nested Freeze offset issue, fixed by freezing only outgoing overlap frames and compensating for Remotion 4’s sequence offset reset. Final CAS contact sheet is the review evidence; drafts stay ignored under out/. No PAN/file picker/personal import completion may appear.

No licensed music asset exists. `music.file` remains null; the standalone preview is digitally silent. See the scene report for exact files and reproducible commands. Nothing has been committed for this V2 stage; wait for preview review before any full-resolution render.

### V2 Segment 2 r2 — fit review

The user reported an inset-looking dashboard and no dashboard on the opening frame. Inspection found that the recording filled the glass, but the 56-unit bezel was thick (~15px per side at 720p), and the r1 screen opacity began at zero. The approved Segment 1 endpoint contains a placeholder. R2 (`manifests/v2-segment2-r2.json`) reduces bezel to 24, matches the outer radius to 94, uses aspect-preserving cover for the negligible fit gap, and shows the dashboard from Segment 2 frame 0. Approved Segment 1 remains byte-identical and its original final frame is still a placeholder. No overlay was added inside Segment 1. Existing r1 media/config stay preserved.

The separate V2 entry and preparation/render/validation helpers now default to r2; the render helper accepts --manifest and passes it as config props, so r1 is reproducible explicitly. Timing, captions, recordings, CAS privacy selection and music-null setting are unchanged. Only low-resolution previews are authorized; see `production/v2/scene-02/output/segment-02-r2-report.md`.

### V2 Scene 2 r3 — approved alpha mask, native 720p, no notch (9 November)

The user supplied a matching 1280×720 reference PNG and transparent white phone mask and approved the single OpenCV composite as fitting perfectly. `scripts/composite_reference_mask.py` extracts straight-side corner intersections, uses getPerspectiveTransform/warpPerspective, composites only through the original alpha, and preserves all outside-mask pixels. Inputs were not resized/cropped/moved. Approved snapshots and mapping are preserved in `production/v2/scene-02/references/approved-phone-*`. The source video itself remains 1284×724; do not confuse its native dimensions with the approved 1280×720 reference.

The user explicitly requested completion at 720p and NO NOTCH ANYWHERE in the regenerated Scene 2. R3 (`manifests/v2-segment2-r3.json`) is a native 1280×720 composition, starting pixel-identically on the approved composite. The opening push uses its exact alpha mask to clip a high-resolution dashboard layer; the established two-phase motion and shared display/bezel plane continue into a fully notch-free mockup. PhoneMockup’s new showNotch=false bypasses the entire notch/camera subtree; earlier caller defaults stay unchanged. Text layout is scaled from the established design grid, with the same timing and content.

The static approved dashboard stays during the 36-frame transition, then the genuine dashboard recording plays at natural speed for the remaining 6.5s of the aggregation slot. SIP/CAS/Reports/privacy timings and safe source selections are unchanged. Music remains unavailable/configurable. Scene 1 original video/audio and Scenes 3/4 are untouched. Do not add a notch to the physical transition or final showcase.

Preparation/render/validation helpers and the separate V2 entry now default to r3. Review outputs go under `out/v2-segment2-r3/review/`. The original r1/r2 files and manifests are retained and can be selected explicitly. No full-film assembly or commit was requested. See `docs/v2-segment2-r3.md` for results.

### V2 Scene 2 r4 — fix enlarged raster-mask edges

An mpv screenshot in the r3 review directory identified frame 20 / 0.833s. The native alpha boundary and frozen plate were magnified 3.568×, turning one-pixel edge steps into visible staircase artifacts. The screenshot matches the actual decoded video; mpv is not the cause.

User authorized the fix. R4 (`manifests/v2-segment2-r4.json`) does not enlarge the native mask during the zoom. After a four-frame entrance, the existing clean phone plane projects the original dashboard directly into the current zoomed/morphing quadrilateral. Its narrow geometric bezel covers the old raster fringe locally inside the original phone rim. The original photo/hand stay behind it; no finger synthesis or global blur. The same plane handles the later mockup. The approved composite remains the frame-0 starting plate. No notch/camera subtree is drawn.

R4 uses 2× render sampling as a disposable antialiasing intermediate, then downsamples to the only deliverable resolution, 1280×720. Helpers default to r4 and honor renderSupersampling while preserving old revision support. Source files, masks, reference geometry, text, timing and source recording selections remain unchanged. Review output: `out/v2-segment2-r4/review/`. No commit requested.

### V2 Scene 1 — one-second phone-turn POC (9 November)

The user accepted Scene 2 r4’s appearance and requested a report on using v1 Scene 4 compositing for the new Scene 1, then authorized a one-second turn test only. Source [420,444) = 17.5–18.5s is processed into `out/v2-scene1-turn-poc-r1/review/`. `manifests/v2-scene1-turn-poc-r1.json` stores native-coordinate per-frame reviewed corners; `scripts/composite_phone_turn_poc.py` uses perspective warps, 4× aperture sampling, original finger holdouts and independent adjacent-frame flow/RANSAC diagnostics. Back/edge-on frames 420–425 are unchanged before encoding; dashboard reveal is 426–428. No synthetic notch. The blurred 426–429 interval uses manual geometry; weak optical-flow candidates are rejected, not applied. Later checks around frame 435 onward agree to about one native pixel, a diagnostic rather than accuracy proof.

The source video remains byte-identical. Native working output is 1284×724; the 720p review is aspect-fitted with small side padding. Original AAC excerpt is stream-copied; zero-lag audio correlation is 1.0. All three outputs decode, with 24 video frames / exactly one second. The actual Scene 1 endpoint / Scene 2 reference handoff is outside this sample and still needs alignment during any authorized extension. No full-scene processing was requested yet. Read `docs/v2-scene1-turn-poc-r1.md` and review the before/after and contact sheet before continuing.

### V2 Scene 1 — full dashboard composite r1

User approved the one-second POC and authorized the complete Scene 1. Completed copies are `out/v2-scene1-dashboard-full-r1/review/scene-01-dashboard-720p-r1.mp4` and `scene-01-dashboard-native-r1.mp4`, 505 frames / 21.041667s at 24fps. Original source and POC media remain untouched. Accepted turn geometry 426–443 is retained; reviewed measured corners extend through frame 504, with a subpixel endpoint aperture correction after the POC. Original fingers/hand motion are preserved; no added notch. Full original AAC is stream-copied and decoded PCM is byte-identical.

Fixed proportional native-to-reference alignment makes the 720p endpoint match the approved Scene 2 opening geometry; minor resampling differences remain. A three-second boundary review joins the last second to Scene 2 r4’s first two seconds. No existing assembly or Scene 2 media changed. `scripts/composite_scene1_full.py` and `manifests/v2-scene1-dashboard-full-r1.json` reproduce the processing using the accepted POC compositor. See `docs/v2-scene1-dashboard-full-r1.md` and contact sheets. Asset verification and whitespace checks pass. Await review; no commit requested.

### V2 Scenes 01–02 full review

User accepted completed Scene 1 and requested a full join in `production/v2/output/` (explicit output-location exception). `scene-01-02-review-r1.mp4` joins the full accepted Scene 1 dashboard 720p r1 to Scene 2 r4: 889 frames, 37.041667s, 1280×720 at 24fps. Direct cut at frame 505 / 21.041667s; all decoded video frames match their inputs exactly. Original dialogue is retained, padded through the exact first-scene duration, then silent Scene 2; AAC is re-encoded at 48kHz/192kbps. No added music. Full decode passed and input checksums are unchanged. Reproduce with `python3 scripts/assemble_v2_review.py manifests/v2-scenes01-02-review-r1.json`; renderer refuses overwrites. Validation report accompanies the MP4. No commit requested.

### V2 Scenes 01–03 review

User requested appending Scene 03. `production/v2/output/scene-01-03-review-r1.mp4` appends the complete `production/v2/scene-03/output/scene-03.mp4` (409 frames, 17.041667s, native 1284×724 at 24fps) to the accepted 889-frame Scenes 01–02 preview. Output: 1298 frames / 54.083333s, 1280×720, 24fps. Direct cut at frame 889 / 37.041667s; no trimming or added transition/music. Scene 03 uses proportional Lanczos fit with tiny white side margins; original AAC copied to the fitting intermediate, then joined soundtracks encoded at 48kHz/192kbps. Previous media remain untouched. Manifest `manifests/v2-scenes01-03-review-r1.json` records original-source hash and preparation; assembly uses `scripts/assemble_v2_review.py`. Disposable fitted source and intermediates remain under `out/v2-scenes01-03-r1/`. No commit requested.

### V2 Scene 04 — white end card and complete review

User requested a five-second white Remotion end card and append to the accepted film. `src/v2/EndCard.jsx` / separate `src/v2/end-card-entry.jsx` and `manifests/v2-scene4-end-card-r1.json` implement the exact requested text, real showcase logo, matching DejaVu Sans/navy typography, blue privacy line and left-to-right underline. Full visibility from frame 36 through 119. No music asset is configured; current output is silent, with configurable music/end fade.

Standalone: `production/v2/scene-04/output/scene-04-end-card-r1-720p.mp4` (120 frames / 5s), final PNG alongside. Combined: `production/v2/output/scene-01-04-review-r1.mp4` (1418 frames / 59.083333s), 1280×720 at 24fps. Earlier 1298 decoded video frames are identical; direct append at 54.083333s, original dialogue retained in re-encoded AAC. Full decode/hash/asset checks pass. Actual Chrome render succeeded outside sandbox after restricted socket failure. No preceding scenes changed. Reproduction and timing details: `docs/v2-scene4-end-card-r1.md`. Stop for review; no commit requested.

### V2 original theme soundtrack r1

User supplied `production/v2/audio/mynetworth-theme.wav` (FluidSynth/Let'sNotate composition) and authorized mixing across the full film. Preview: `production/v2/output/scene-01-04-review-music-r1.mp4`, unchanged 1418 visual frames / 59.083333s, 1280×720 at 24fps. Video is stream-copied and every decoded frame matches; approved film and WAV hashes are unchanged. Existing dialogue/notification track is retained sample-aligned.

`manifests/v2-soundtrack-r1.json` configures music gains (dialogue −10dB, showcase +4dB, end card +6dB), 0.6s gain ramps, 0.8s entrance and 2s final fade. Raise after dialogue ends; duck before incoming dialogue. Actual WAV duration is 43.6375510204s; two copies overlap for 1s at 42.637551–43.637551s. Independent music stem remains under `out/v2-soundtrack-r1-review/`. Original track is unity before a configurable shared −0.5dB headroom trim; no limiter or timing changes. AAC256kbps/48kHz mixed output.

`scripts/mix_v2_soundtrack.py` reproduces with standard Python/FFmpeg only. Technical checks cover video identity, source hashes, full decode, sample-aligned summation, loop endpoint continuity and end fade. Decoded peak approximately −0.39dBFS. See `docs/v2-soundtrack-r1.md`; balance and musical loop remain for listening review. Earlier no-music notes are historical. No commit requested.

### V2 updated theme soundtrack r2

User replaced the theme WAV and requested a rerender with the same settings. New preview: `production/v2/output/scene-01-04-review-music-r2.mp4`; config `manifests/v2-soundtrack-r2.json`. Updated audio SHA256 `62166abfe8c88404aaa311f26d5cbf023d5f759bc05df584ef75efefda88c654`, actual duration 32.0029024943s. Two copies now overlap at 31.002902–32.002902s. Existing gains, 0.5dB headroom trim, scene envelopes and end fade are unchanged. Output remains 1418 frames / 59.083333s, 1280×720 at 24fps. All decoded video frames identical, source hashes unchanged, full decode passed, audio sum residual below 1e−6 with no dialogue offset; decoded peak −0.459dBFS. Detailed report accompanies the MP4. No commit requested.

### V2 complete reproducible checkpoint before edge correction

User requested checking in everything required for the current full V2 video before attempting the white-edge fix. Accepted Scene 1 native/720 composites, Scene 2 r4, Scene 3 fitted media and review evidence are now preserved under production/v2/ scene folders. `manifests/v2-production-checkpoint.json` lists authoritative masters; `manifests/v2-production-checksums.json` inventories 104 files including inputs, code and outputs. `scripts/reproduce_v2.py` validates those dependencies and regenerates the latest music-r2 film from the tracked pre-music assembly and updated WAV. Fresh reproduction under out/v2-checkpoint-reproduction matched the current MP4 byte-for-byte. Documentation: production/v2/README.md. Existing V1 baseline/media remain untouched. Locked npm ci succeeded outside the sandbox after restricted esbuild EPERM; approved asset verification passes. Commit this state before any edge fix.

### V2 edge correction candidate after checkpoint

Full V2 checkpoint committed as `6bd17eb` before correction. New uncommitted review: `production/v2/output/scene-01-04-review-music-r3-edge-fixed.mp4`. FFmpeg fillborders extends adjacent image pixels over the outer four columns on both sides, removing white padding/chroma fringe without crop, zoom or changing the phone handoff. Config/script: `manifests/v2-edge-fix-r1.json`, `scripts/fix_v2_edges.py`. Frame count/timings unchanged (1418 frames / 59.083333s, 720p24), current soundtrack stream-copied and decoded audio identical. Interior PSNR 54.80dB from CRF12 recompression. Magnified checks at frames 240/505/1000 show lines removed; frame 1350 intentional end-card white remains white. Full decode passes. Original committed film and dependency hashes are unchanged. Await user review before treating this fix as approved; not pushed or tagged. See docs/v2-edge-fix-r1.md.

### V2 edge correction approved for commit

User requested documenting, checking in and committing the edge correction. The current V2 film is `production/v2/output/scene-01-04-review-music-r3-edge-fixed.mp4`. Method/verification remain as above; tracked comparison evidence is now `docs/validation/v2-edge-fix-r1-before-after.png`. Documentation and current-output pointers are updated; `manifests/v2-edge-fix-checksums.json` records the correction dependencies. Original pre-correction media remain preserved. No push or tag requested.
