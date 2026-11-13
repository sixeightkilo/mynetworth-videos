# V2 approved audio-tail cleanup baseline

User approved the review candidate and requested a new baseline. Current output: `production/v2/output/scene-01-04-review-music-r5-audio-cleanup.mp4`.

A low-frequency burst at about 20.6–21.0 seconds originates in the original Kling Scene 1 soundtrack. Fade only the original soundtrack from 20.48 to 20.56 seconds, then mute it through the Scene 1 end at 505/24 = 21.041667 seconds. Later dialogue and the independently regenerated r2 music stem retain their existing timing and gains. The final AAC track is re-encoded at 256kbps/48kHz. The user accepted the listening review; no other noise removal or dialogue processing is applied.

All video packets are copied from r4-tagline, retaining the edge correction and two-line tagline. Output remains 1280×720, 24fps, 1418 frames / 59.083333 seconds. Earlier baselines and original sources remain untouched.

Reproduce using Python standard library, FFmpeg and FFprobe:

```sh
python3 scripts/fix_v2_audio_tail.py manifests/v2-audio-tail-fix-r1.json
```

Existing outputs/work directories are never overwritten. For another reproduction, copy the manifest and select fresh `output` and `workDir` paths. The helper regenerates the music from tracked WAV/configuration using the existing mixer; it does not require the disposable review stem. The intermediate original mix is retained only under out/.

The accompanying output JSON records input/output SHA256, video packet identity, frame count, geometry, audio presence and full-decode verification. The generated baseline is also compared byte-for-byte with the accepted review candidate. Dependency hashes are recorded in `manifests/v2-audio-tail-fix-checksums.json`. User requested committing, tagging and pushing this checkpoint as `production-v2.2`.

Release copy: `release/mynetworth-promo-v2.2-720p.mp4` (byte-identical). A fresh full reproduction matched the approved baseline byte-for-byte.
