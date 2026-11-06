# Approved MyNetWorth rough-cut milestone — 6 November 2026

User approval: “this looks good and all the work that has gone into should be bookmarked/preserved.”

This is the approved baseline. Make future changes in new revision folders; keep these renders and this archive intact. Prior experiments, references, tracking data, reports and render scripts are preserved too.

Approved outputs, relative to project root:

- Full film: assets/kling-video/full-rough-cut/revision-integrated-dashboard/mynetworth-rough-cut-720p.mp4 — 1280×720, 24 fps, 1349 frames / 56.208333 seconds.
- Scene 6–7: assets/kling-video/scene-6-7-preview/revision-integrated-dashboard/scene-6-7-preview.mp4 — 1280×720, 24 fps, 418 frames / 17.416667 seconds.
- Timing: assets/kling-video/full-rough-cut/revision-integrated-dashboard/scene-timing-report.md and .csv.

Baseline decisions:

- Scenes 1–5, 8 and 9 use the existing cleaned clips, with original dialogue as temporary audio.
- Scene 6 uses cleaned/6-zoom-on-app.mp4 with the dashboard already integrated. Its frame 120 matches the approved transition takeover pose at old frame 90; 120 new-source frames are followed by approved combined clip frames 90–387. No additional screen overlay is applied to the new source.
- The approved zoom, perspective settle and rightward phone handoff remain intact. The new approach adds 30 frames / 1.25 seconds.
- Scene 7 retains the stationary smartphone, four demonstrations, branding and feature captions. CAS shows import starting, holds Secure Local Import longer, then ends on the original opening dashboard still labelled Demo portfolio. No PAN, file picker, personal holdings, or repeated dashboard scroll.
- Scene 10: MyNetWorth / All Your Investments. One Clean Dashboard. / Available on Android. Crossfade 17 frames (0.708333 seconds), then full-opacity hold 84 frames (3.5 seconds).
- Rendering uses FFmpeg assembly of approved existing media; prior browser launches failed in this restricted runtime. Separate Remotion preview compositions and native render scripts are preserved.

Rebuild commands, from project root:

```sh
npm run render:scene6-7:integrated
npm run render:full-rough-cut:integrated
```

Remotion preview commands:

```sh
npm run preview:scene6-7:integrated
npm run preview:full-rough-cut:integrated
```

Preservation:

- project-snapshot.tar.gz contains assets (all scenes, experiments, source recordings, reports and outputs), remotion, scripts, package files and main project files. The milestones folder itself is excluded to avoid recursive archiving.
- source-checksums.json records regular-file SHA-256 hashes before archiving. Symlinks are retained as links; some public-directory links use the original absolute project path. If restoring elsewhere, recreate those links for the new root before previewing/bundling.
- snapshot.sha256 verifies the archive. archive-validation.json records file-by-file verification of the archive against source-checksums.json.
- environment.json records runtime versions. Installed node_modules and .python-deps are left intact in the current workspace but excluded from the archive; package-lock.json pins npm dependencies.
- This is a local filesystem milestone, not a Git commit or off-machine backup. This workspace has no usable Git repository.
