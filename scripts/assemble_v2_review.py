"""Join accepted V2 renders without re-encoding their video. FFmpeg only."""
import argparse,hashlib,json,subprocess
from pathlib import Path

def run(cmd):return subprocess.check_output(cmd)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def framehash(p):
    data=run(['ffmpeg','-v','error','-i',str(p),'-map','0:v','-f','framemd5','-']).decode()
    return [line.split(',')[-1].strip() for line in data.splitlines() if not line.startswith('#')]
def main(manifest):
    c=json.loads(Path(manifest).read_text());inputs=c['inputs'];out=Path(c['output']);work=Path(c['workDir']);work.mkdir(parents=True,exist_ok=True)
    assert not out.exists(),out
    before={p:sha(p) for p in inputs}
    for i,p in enumerate(inputs):
        run(['ffmpeg','-v','error','-n','-i',p,'-map','0:v:0','-an','-c:v','copy','-video_track_timescale','12288',str(work/f'video-{i}.mp4')])
    listing=work/'concat.txt';listing.write_text(''.join(f"file 'video-{i}.mp4'\nduration {n/c['fps']:.12f}\n" for i,n in enumerate(c['frames'])))
    video=work/'joined-video.mp4'
    run(['ffmpeg','-v','error','-n','-f','concat','-safe','0','-i',str(listing),'-an','-c:v','copy',str(video)])
    af=';'.join(f'[{i}:a]aresample=48000,apad,atrim=duration={n/c["fps"]:.12f},asetpts=PTS-STARTPTS[a{i}]' for i,n in enumerate(c['frames']))+';[a0][a1]concat=n=2:v=0:a=1[a]'
    audio=work/'joined-audio.m4a'
    run(['ffmpeg','-v','error','-n','-i',inputs[0],'-i',inputs[1],'-filter_complex',af,'-map','[a]','-c:a','aac','-b:a','192k',str(audio)])
    out.parent.mkdir(parents=True,exist_ok=True)
    run(['ffmpeg','-v','error','-n','-i',str(video),'-i',str(audio),'-map','0:v','-map','1:a','-c','copy','-movflags','+faststart',str(out)])
    expected=sum((framehash(p) for p in inputs),[]);assert framehash(out)==expected
    run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'])
    assert before=={p:sha(p) for p in inputs}
    report={'output':str(out),'sourceSHA256':before,'frames':len(expected),'fps':c['fps'],'durationSeconds':len(expected)/c['fps'],'resolution':[1280,720],'cutFrame':c['frames'][0],'cutSeconds':c['frames'][0]/c['fps'],'decodedVideoIdenticalToInputs':True,'fullDecode':'passed','audio':'Original soundtracks retained; each padded/trimmed to its exact video duration; AAC re-encoded at 48kHz/192kbps. No music added.','sourcesUnchanged':True}
    assert len(expected)==sum(c['frames'])
    out.with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('manifest');main(p.parse_args().manifest)
