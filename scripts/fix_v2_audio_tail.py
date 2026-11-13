"""Rebuild music from tracked inputs and remove the approved Scene 1 tail burst."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from mix_v2_soundtrack import main as mix_soundtrack


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main(manifest):
    c = json.loads(Path(manifest).read_text())
    work = Path(c['workDir'])
    work.mkdir(parents=True, exist_ok=False)
    output = Path(c['output'])
    assert not output.exists(), output
    music = json.loads(Path(c['musicManifest']).read_text())
    inputs = [c['videoSource'], music['sourceVideo'], music['musicSource']]
    before = {p: sha(p) for p in inputs}
    music['workDir'] = str(work / 'music')
    music['output'] = str(work / 'original-mix.mp4')
    music_manifest = work / 'music.json'
    music_manifest.write_text(json.dumps(music, indent=2) + '\n')
    mix_soundtrack(str(music_manifest))
    start = c['fadeStartSeconds']
    cut = c['sceneEndFrame'] / music['fps']
    filters = (
        '[1:a]aresample=48000,asplit=3[pre][tail][post];'
        f'[pre]atrim=end={start},asetpts=PTS-STARTPTS[a];'
        f'[tail]atrim=start={start}:end={cut:.12f},asetpts=PTS-STARTPTS,'
        f'afade=t=out:st=0:d={c["fadeDurationSeconds"]}[b];'
        f'[post]atrim=start={cut:.12f},asetpts=PTS-STARTPTS[c];'
        '[a][b][c]concat=n=3:v=0:a=1[dialogue];'
        '[dialogue][2:a]amix=inputs=2:duration=first:dropout_transition=0:normalize=0,'
        f'volume={music["masterGainDb"]}dB[mix]'
    )
    subprocess.run([
        'ffmpeg', '-v', 'error', '-n', '-i', c['videoSource'],
        '-i', music['sourceVideo'], '-i', str(work / 'music/music-stem.wav'),
        '-filter_complex', filters, '-map', '0:v:0', '-map', '[mix]',
        '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-ar', '48000',
        '-movflags', '+faststart', str(output),
    ], check=True)
    def video_hash(path):
        return subprocess.check_output([
            'ffmpeg', '-v', 'error', '-i', str(path), '-map', '0:v:0',
            '-c', 'copy', '-f', 'hash', '-hash', 'sha256', '-',
        ]).decode().strip()
    assert video_hash(output) == video_hash(c['videoSource'])
    subprocess.run(['ffmpeg', '-v', 'error', '-i', str(output), '-f', 'null', '-'], check=True)
    streams = json.loads(subprocess.check_output([
        'ffprobe', '-v', 'error', '-show_streams', '-of', 'json', str(output),
    ]))['streams']
    v = next(s for s in streams if s['codec_type'] == 'video')
    assert (v['width'], v['height'], int(v['nb_frames']), v['avg_frame_rate']) == (1280, 720, 1418, '24/1')
    assert any(s['codec_type'] == 'audio' for s in streams)
    assert before == {p: sha(p) for p in inputs}
    report = dict(output=str(output), inputSHA256=before, outputSHA256=sha(output),
                  videoPacketsIdentical=True, frames=1418, fps=24,
                  durationSeconds=1418/24, resolution=[1280, 720],
                  audioPresent=True, fullDecode='passed', sourcesUnchanged=True,
                  fadeStartSeconds=start, fadeEndSeconds=start+c['fadeDurationSeconds'],
                  muteEndSeconds=cut, manifest=manifest)
    output.with_suffix('.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('manifest')
    main(parser.parse_args().manifest)
