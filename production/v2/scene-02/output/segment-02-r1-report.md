# V2 Segment 2 — r1 review

Implemented a separate, editable Remotion showcase. No full-resolution video was rendered.

## Review media

- `segment-02-r1-preview-720p.mp4`: 16 seconds / 384 frames, 1280×720 at 24fps, H.264, limited-range BT.709 matrix. Silent because no licensed music was found.
- `segment-01-to-02-r1-boundary-720p.mp4`: final two seconds of approved Segment 1 followed by the complete showcase, 18 seconds / 432 video frames.
- `segment-02-r1-contact.jpg`: transition, aggregation, features and final privacy layout.
- `segment-01-to-02-r1-contact.jpg`: the actual Segment 1 → 2 cut and push-in.
- `segment-02-r1-cas-audit.jpg`: all 36 CAS-slot frames, including incoming crossfade and Secure Local Import hold.
- `segment-02-r1-validation.json`: source hashes, output metadata, audio and full-decode checks.

Video durations are exactly 16/18 seconds. Containers include AAC padding: 16.043/18.048 seconds. The standalone audio is digitally silent. The boundary includes original dialogue from the final two seconds; AAC transform overlap decays within approximately 43ms after the cut, followed by silence. It is a low-resolution review encode, not a replacement for the approved source.

## Assets reused

- Approved Segment 1: `production/v2/scene-01/output/scene-01.mp4`, 1284×724, 24fps, 505 frames / 21.041667 seconds. Exact final frame 504 is the transition plate. SHA256 remains `0260e671fd1757db2b030a22cfa82642ded971f7debe59f32faa3420a73b67af`.
- `public/app-recordings/dashboard-original.mp4`, native-speed source 0–8 seconds, including its original scroll and natural holds. The shorter dashboard export was also inspected but is only about four seconds long.
- `public/app-recordings/sip.mp4`, 4.75–6.25 seconds.
- `public/app-recordings/cas-import.mp4`, 1.416667–2.541667 seconds, followed by the actual `public/screenshots/import-local.png` for 0.375 seconds. No picker, PAN entry, personal holdings or completed-import claim.
- `public/app-recordings/reports.mp4`, 4–5.5 seconds, then the original Custom-range frame at 5.458333 seconds through the end.
- Actual logo `public/branding/logo.png`, via the existing transparent derivative `production/v1/scene-10/references/logo-transparent-srgb-v2.png`. No logo redesign.
- Existing `PhoneMockup`, `screenTransform` and `scene05TwoPhaseState`. DejaVu Sans uses the project’s established end-card font convention.

## Timing and transition

The first 1.5 seconds are a deterministic push/settle from the frozen approved endpoint. Four manually measured screen corners are centralized in the manifest. The real dashboard fades onto that display over five frames; rounded clipping and the phone’s top notch are retained. The hand, characters and phone are frozen, so there is no invented tracking or animated finger reconstruction. The living-room plate clears before the perspective settle. The real recording, display and geometric bezel then share one projective plane.

At 1.5 seconds the phone reaches its fixed showcase position and stays there. Stocks, Mutual Funds, ETFs and Bonds accumulate at 1.5/2.5/3.5/4.5 seconds. The exact tagline enters at 5.5 seconds and is fully readable before the 8-second feature change. SIP is 8–9.5s, CAS 9.5–11s, Reports 11–12.5s, and privacy 12.5–16s. All three feature checks remain visible through the final hold. Header branding remains after its restrained transition entrance.

## Missing asset and compromises

No instrumental music asset or license was present. `music.file` is null; volume and fade timings are configurable for a supplied licensed track. No substitute, voice or sound effect was generated.

The transition uses a frozen final plate rather than modifying or tracking the moving approved video. The original room/hand become softer during the digital push, then leave; the replacement app layer stays sourced from the real high-resolution recording. The original physical bezel is replaced by the existing geometric shell as the room clears, before perspective correction. CAS intentionally demonstrates only the safe opening flow. Reports settles on a genuine held frame rather than looping or accelerating. These are deliberate controlled choices for review.

## Files and commands

New: `src/v2/Segment2.jsx`, `src/v2/index.jsx`, `manifests/v2-segment2-r1.json`, and the `prepare_v2_segment2.py`, `render_v2_segment2_preview.py`, `validate_v2_segment2.py` helpers. `production/v2/scene-02/prompt.md` preserves the supplied brief.

Updated: `PhoneMockup.jsx` accepts optional children and a plain, shadow-free bezel; old callers retain exactly their original defaults. Package scripts, README, AGENTS, HANDOFF and the current code-dependency checksum entries were updated. Existing composition registrations, approved videos, original recordings, and V2 Segments 3/4 were not changed. No additional dependencies were installed.

On a fresh staging/output revision:

```sh
npm run prepare:v2:segment2
npm run studio:v2
npm run render:v2:segment2:preview
npm run render:v2:segment2:boundary
python3 scripts/validate_v2_segment2.py
```

Helpers refuse to overwrite existing staging/renders. Text, paths, geometry and timing are in the central manifest; update revision paths before another render. Use `REMOTION_BROWSER_EXECUTABLE` or `--browser-executable` for system Chromium. Compositions: `V2Segment2Preview`, `V2Segment1To2BoundaryPreview`, and the available complete `V2Segments1And2Preview`.

Actual Chromium renders, production build, source checksum preservation, the 22 approved public asset checks, full video/audio decode, geometry/frame counts, standalone silence and frame-by-frame CAS visual audit passed. The nested Freeze timing issue caught in an internal draft was fixed before delivery; excluded drafts remain under ignored out/. Boundary samples after settling match standalone geometry/content, with mean RGB encode differences below 0.3/255. Awaiting review; no full-resolution render, commit or integration with Segments 3/4 is authorized yet.
