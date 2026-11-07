"""Assemble already-rendered, native-CFR clips without changing their sources.
Usage: python3 scripts/assemble_scene_preview.py MANIFEST.json
Requires FFmpeg/FFprobe; Python standard library only. Output is never overwritten.
"""
import argparse,hashlib,json,subprocess
from pathlib import Path
from fractions import Fraction

def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(path)]))
def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def run(manifest):
    cfg=json.loads(Path(manifest).read_text());out=Path(cfg['output'])
    assert not out.exists(),f'Output exists: {out}'
    out.parent.mkdir(parents=True,exist_ok=True)
    args=['ffmpeg','-hide_banner','-v','error','-n'];filters=[];clips=[];from_frame=0
    for i,clip in enumerate(cfg['clips']):
        p=clip['source'];metadata=probe(p);v=next(s for s in metadata['streams'] if s['codec_type']=='video')
        assert Fraction(v['avg_frame_rate'])==cfg['fps'] and Fraction(v['r_frame_rate'])==cfg['fps'],p
        assert any(s['codec_type']=='audio' for s in metadata['streams']),p
        start,end=clip['startFrame'],clip['endFrameExclusive']
        assert 0<=start<end<=int(v['nb_frames']),p
        assert v['width']<=cfg['width'] and v['height']==cfg['height'],p
        args+=['-i',p]
        filters.append(f'[{i}:v:0]trim=start_frame={start}:end_frame={end},setpts=PTS-STARTPTS,pad={cfg["width"]}:{cfg["height"]}:(ow-iw)/2:(oh-ih)/2:black,setsar=1[v{i}]')
        filters.append(f'[{i}:a:0]aresample=44100,apad,atrim=start={start/cfg["fps"]:.12f}:end={end/cfg["fps"]:.12f},asetpts=PTS-STARTPTS[a{i}]')
        clips.append({**clip,'fromFrame':from_frame,'frames':end-start,'sha256':digest(p)})
        from_frame+=end-start
    n=len(clips)
    filters+=[''.join(f'[v{i}]' for i in range(n))+f'concat=n={n}:v=1:a=0[v]',''.join(f'[a{i}]' for i in range(n))+f'concat=n={n}:v=0:a=1[a]']
    args+=['-filter_complex',';'.join(filters),'-map','[v]','-map','[a]','-c:v','libx264','-crf','16','-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','44100','-movflags','+faststart',str(out)]
    subprocess.run(args,check=True)
    result=probe(out);v=next(s for s in result['streams'] if s['codec_type']=='video')
    assert (v['width'],v['height'],Fraction(v['avg_frame_rate']),int(v['nb_frames']))==(cfg['width'],cfg['height'],cfg['fps'],from_frame)
    subprocess.run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'],check=True)
    for clip in clips:assert digest(clip['source'])==clip['sha256'],clip['source']
    report={'output':str(out),'manifest':manifest,'frames':from_frame,'fps':cfg['fps'],'durationSeconds':from_frame/cfg['fps'],'resolution':[cfg['width'],cfg['height']],'clips':clips,'cuts':'Direct cuts; no overlaps or fades','audio':'Original clip soundtracks trimmed with video, sample-aligned and concatenated; AAC 44.1kHz stereo','sourceHashes':'unchanged','fullDecode':'passed'}
    out.with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('manifest');run(parser.parse_args().manifest)
