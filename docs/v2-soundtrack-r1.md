# V2 original soundtrack review r1

Preview: `production/v2/output/scene-01-04-review-music-r1.mp4`. Existing approved silent-music film and original WAV are untouched. 1280×720, 24fps, 1418 frames / 59.083333 seconds. All decoded video frames match the input film exactly; video packets are copied, with no Remotion scene edits or rerendering of approved visuals.

## Timeline and gains

The separate Remotion entries `src/v2/index.jsx` and `src/v2/end-card-entry.jsx`, Scene 2 r4 configuration and successive accepted assembly manifests establish these boundaries:

| Scene | Frames (end exclusive) | Seconds | Music gain relative to WAV |
|---|---|---|---|
| 1 Conversation | 0–505 | 0–21.041667 | −10 dB |
| 2 App showcase | 505–889 | 21.041667–37.041667 | +4 dB |
| 3 Conversation | 889–1298 | 37.041667–54.083333 | −10 dB |
| 4 End card | 1298–1418 | 54.083333–59.083333 | +6 dB |

Music gains, fades, loop overlap and output paths are configurable in `manifests/v2-soundtrack-r1.json`. Volume rises over 0.6s **after** leaving dialogue; it falls over 0.6s **before** incoming dialogue. Cubic ramps are evaluated in 128-sample blocks. Music enters over 0.8s and fades out over the final 2s.

The supplied `production/v2/audio/mynetworth-theme.wav` is stereo PCM16 at 44.1kHz, exactly 1,924,416 source samples / 43.6375510204 seconds. No nominal bar/loop length is assumed. Two complete copies use a one-second complementary half-sine crossfade from 42.637551 to 43.637551s; the resulting continuous layer is trimmed to film duration. No silence was detected at −60dB for intervals of 50ms or longer in the source. Original source mean level is −30.5dBFS, hence positive music gains in silent scenes are intentional.

## Mixing and preservation

`scripts/mix_v2_soundtrack.py` builds `out/v2-soundtrack-r1-review/music-stem.wav` separately, then adds it to the complete original dialogue/notification track at unity gain, with automatic amix normalization disabled. A shared configurable **−0.5dB master trim** leaves headroom: original AAC already has a few decoded peaks above 0dBFS, and the untrimmed mix peaks near +0.10dBFS. This small fixed trim affects both layers equally; no limiter, ducking compressor or time shift is applied. Final audio is AAC256kbps/48kHz. Dialogue and notification content/timing remain intact; compressed audio bytes change during mixing.

Validation checks every video frame, input hashes, duration/frame count and full decode. The float mix is also checked against the sample-aligned original plus separate music stem, including master gain, with maximum numerical residual below 1e−6. Sample discontinuities at the two crossfade endpoints are below normal surrounding waveform differences. The final music sample is near zero; decoded final mix peak is approximately −0.39dBFS. These are technical checks; musical balance and the loop join remain for the user's listening review.

## Reproduce / adjust

```sh
python3 scripts/mix_v2_soundtrack.py manifests/v2-soundtrack-r1.json
```

For another listening revision, copy the manifest, change `musicGainDb` and choose fresh `output` and `workDir` paths. Rendering refuses to overwrite outputs/intermediates and aborts if the float mix exceeds full scale. Only Python standard library and FFmpeg/FFprobe are required. No source music processing is destructive. Remotion content and earlier scene configurations remain untouched; the final assembly retains independent music preparation rather than baking it into individual scenes.

Source SHA256 and full verification results are in the JSON alongside the review MP4. Approved asset verification and whitespace checks pass. No commit requested.
