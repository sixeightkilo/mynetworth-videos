"""Apply a specified local chroma correction in a new review export.
Supports the Scene 4–5 matrix repair or the separately reviewed Scene 8/9 matches.
No source regeneration, timing changes or source overwrites.
Lossless H.264 preserves unaffected decoded pixels. FFmpeg/FFprobe and stdlib only.
"""
import argparse, hashlib, json, subprocess
from fractions import Fraction
from pathlib import Path

def call(args):
    return subprocess.check_output(args)

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def hashes(path):
    text = call(['ffmpeg', '-v', 'error', '-i', str(path), '-map', '0:v:0',
                 '-an', '-f', 'framemd5', '-']).decode()
    return [line.split(',')[-1].strip() for line in text.splitlines() if not line.startswith('#')]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('manifest', nargs='?', default='manifests/scene01-10-color-fixed-v3.json')
    args = parser.parse_args()
    c = json.loads(Path(args.manifest).read_text())
    if 'warmChromaScale' in c:
        factor = c['warmChromaScale']
        assert 0 < factor <= 1
        effect = f"lutyuv=y=val:u='if(lt(val,128),128+(val-128)*{factor},val)':v=val"
    else:
        assert (c['inputMatrix'], c['outputMatrix'], c['range']) == ('bt601', 'bt709', 'tv')
        effect = ('colorspace=ispace=bt470bg:iprimaries=bt709:itrc=bt709:irange=tv:'
                  'space=bt709:primaries=bt709:trc=bt709:range=tv:format=yuv420p')
    source, dest = Path(c['source']), Path(c['output'])
    assert not dest.exists(), dest
    before = sha(source)
    start, end, total = c['correctionStartFrame'], c['correctionEndFrameExclusive'], c['frames']
    work = Path(c['workDir']); work.mkdir(parents=True, exist_ok=True)
    graph = (
        '[0:v]split=3[a][b][c];'
        f'[a]trim=end_frame={start},setpts=PTS-STARTPTS[a0];'
        f'[b]trim=start_frame={start}:end_frame={end},setpts=PTS-STARTPTS,'
        f'{effect}[b0];'
        f'[c]trim=start_frame={end},setpts=PTS-STARTPTS[c0];'
        '[a0][b0][c0]concat=n=3:v=1:a=0,'
        'setparams=range=limited:color_primaries=bt709:color_trc=bt709:colorspace=bt709[v]'
    )
    subprocess.run(['ffmpeg', '-v', 'warning', '-n', '-filter_complex_threads', '2',
        '-i', str(source), '-filter_complex', graph, '-map', '[v]', '-map', '0:a:0',
        '-c:v', 'libx264', '-crf', '0', '-preset', 'fast', '-threads', '4',
        '-pix_fmt', 'yuv420p', '-colorspace', 'bt709', '-color_primaries', 'bt709',
        '-color_trc', 'bt709', '-color_range', 'tv', '-video_track_timescale', '12288',
        '-c:a', 'copy', '-movflags', '+faststart', str(dest)], check=True)
    v = json.loads(call(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                         '-show_streams', '-of', 'json', str(dest)]))['streams'][0]
    assert (v['width'], v['height'], int(v['nb_frames']), Fraction(v['avg_frame_rate'])) == (c['width'], c['height'], total, c['fps'])
    assert abs(float(v['duration']) - total / c['fps']) < 1 / 12288
    original, corrected = hashes(source), hashes(dest)
    assert len(original) == len(corrected) == total
    assert original[:start] == corrected[:start]
    assert original[end:] == corrected[end:]
    if 'warmChromaScale' in c:
        def plane_hash(path, plane):
            return call(['ffmpeg', '-v', 'error', '-i', str(path), '-an', '-vf',
                         f'extractplanes={plane}', '-f', 'hash', '-hash', 'sha256', '-'])
        for plane in ['y', 'v']:
            assert plane_hash(source, plane) == plane_hash(dest, plane), plane
    changes = sum(a != b for a, b in zip(original[start:end], corrected[start:end]))
    assert c.get('minimumChangedFrames', end - start) <= changes <= end - start, changes
    def pcm(path):
        return call(['ffmpeg', '-v', 'error', '-i', str(path), '-vn', '-f', 's16le', '-'])
    assert pcm(source) == pcm(dest)
    subprocess.run(['ffmpeg', '-v', 'error', '-i', str(dest), '-f', 'null', '-'], check=True)
    assert sha(source) == before
    report = {**c, 'durationSeconds': total / c['fps'], 'sourceSHA256': before,
              'outputSHA256': sha(dest), 'changedFrames': changes,
              'unaffectedVideoFramesIdentical': total - changes,
              'outsideCorrectionRangeIdentical': True,
              'lumaAndVPreserved': 'warmChromaScale' in c,
              'decodedAudioIdentical': True, 'sourceUnchanged': True,
              'fullDecode': 'passed', 'videoMetadata': v}
    dest.with_suffix('.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: report[k] for k in ['output', 'durationSeconds', 'changedFrames',
          'unaffectedVideoFramesIdentical', 'decodedAudioIdentical', 'fullDecode']}, indent=2))

if __name__ == '__main__':
    main()
