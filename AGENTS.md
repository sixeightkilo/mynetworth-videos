# MyNetWorth production project

## Start here in a new Codex session

Read `HANDOFF.md` in full before planning changes. It records the approved film, migration, exact scene/transition timings, privacy constraints, validation evidence, missing inputs and user preferences from the previous conversation. Then read README.md and manifests/production.json. Do not recreate experiments or alter approved scenes merely to recover context.

## Architecture and approved baseline

Read README.md first, then manifests/production.json. The approved baseline is 1349 frames, 1280×720 at 24fps (56.208333s). src/index.jsx registers the approved assembly, 1080p assembly and editable scene previews. The same approved-720p.json drives Remotion and FFmpeg. public contains immutable, checksummed production inputs; source videos and approved composites ARE tracked in Git. out is disposable output. references contains optional comparison renders, never runtime dependencies.

src/components owns the reusable phone shell and proper projective transform. src/transitions owns approved zoom/settle motion and wrapper positioning. src/scenes owns editable Scene 6/7 implementations. src/compositions owns assembly only. Scene 6/7 approved baked media remains authoritative; editable reconstruction can differ slightly in font/rasterization and is not silently substituted.

## Workflow

Run npm ci, npm run verify, npm run build. Reproduce the current film with npm run render:rough-cut and compare with npm run validate:rough-cut. FFmpeg and FFprobe are required; production assembly needs only Python's standard library. Remotion browser renders require working Chromium; the original restricted environment blocked browser startup with SIGTRAP/permission errors. Bundling alone does not prove browser rendering. Keep that distinction in reports.

1920×1080 Production1080p and render:1080p preserve 24fps and approved geometry. Existing scene masters are ~720p; clearly report upscaling. Never claim native 1080p detail. Keep 720p approval verification separate from final 1080p export.

Do not overwrite approved public assets or earlier approval media. New edits need new files/manifests and review. Output goes only under out. Make scene changes independently from assembly changes. Do not regenerate source footage or invent missing prompts. Do not send files or publish without explicit authorization.

## Timing and continuity lessons

Use integer composition frames. App recordings are variable-frame-rate: trim timestamps are converted at COMPOSITION fps, not source frame indices. Do not apply a global frame-rate change; 24fps is the existing convention.

The integrated Scene 6 source reaches the approved takeover pose at frame 120; legacy transition frame 90 has that pose. Approved combined assembly uses new frames [0,120), then legacy combined frames [90,388), totaling 418 frames. Dialogue plays once from the new source; do not replay legacy audio. Scene 7 begins at combined frame 154 and runs 264 frames. The editable transition config shifts takeover by 30 frames without changing easing or geometry. The combined wrapper moves the phone right only after the photo background disappears. Preserve the screen, bezel, notch, position and scale at handoff.

CAS must not reveal personal data. Show import starting, hold Secure Local Import, and finish on the static opening demo-dashboard frame labelled Demo portfolio. Do not show the file picker, PAN dialog/entry, personal holdings, or imply a completed personal import. Approved source files can contain excluded portions: never expose those by widening trims without inspection.

Keep original app colours. Monochrome treatment must not affect child screenshot/recording layers. Preserve portrait aspect ratio and rounded screen masks. Tracking experiments showed manual-anchor jumps; do not resurrect linear interpolation or blanket smoothing. Tracking diagnostics and models were intentionally left in the original archive; approved compositing is already baked.

End card crossfades over 17 frames and holds fully opaque for 84 frames; overlap is intentional. Temporary dialogue is retained, with Scene 9 fading out during the end-card crossfade. No added music or new voice track.

## Portability and preservation

No absolute filesystem paths or symlinks to the original project. Asset-checksums records provenance strings for audit only. References and old milestone notes may name historical paths but are not executable dependencies. No OpenCV, NumPy, Pillow, automatic tracking, or AI models are required for production assembly. Never copy the whole experimental project back in.

Git ignores dependencies, caches, temporary files, references and renders. Public approved media is versioned. Verify checksums before and after rendering. Before completion, report actual build/render checks, duration, frame count, audio presence and any limitations. The original project and approved milestone remain untouched.
