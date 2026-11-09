"""Local edge extension of padded V2 film; preserve framing and audio packets."""
import argparse
import json
import subprocess
from pathlib import Path
from mix_v2_soundtrack import probe, sha

p=argparse.ArgumentParser();p.add_argument('manifest');a=p.parse_args()
c=json.loads(Path(a.manifest).read_text())
source=c['source'];out=Path(c['output']);work=Path(c['workDir'])
assert not out.exists(),out
work.mkdir(parents=True,exist_ok=True);out.parent.mkdir(parents=True,exist_ok=True)
before=sha(source)
vf=f"fillborders=left={c['leftPixels']}:right={c['rightPixels']}:mode=smear"
subprocess.run(['ffmpeg','-v','error','-n','-i',source,'-map','0:v:0','-map','0:a:0','-vf',vf,
                '-c:v','libx264','-crf',str(c['crf']),'-preset','slow','-threads','4','-pix_fmt','yuv420p',
                '-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709',
                '-c:a','copy','-movflags','+faststart',str(out)],check=True)
v0=next(s for s in probe(source) if s['codec_type']=='video')
v1=next(s for s in probe(out) if s['codec_type']=='video')
for key in ['width','height','nb_frames','avg_frame_rate','duration','start_time']:
    assert v0[key]==v1[key],key
def pcm(path):
    return subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-vn','-f','s16le','-'])
assert pcm(source)==pcm(out),'Audio changed'
subprocess.run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'],check=True)
assert before==sha(source)
report={'source':source,'sourceSHA256':before,'output':str(out),'outputSHA256':sha(out),
        'method':c['method'],'filter':vf,'frames':int(v1['nb_frames']),'fps':v1['avg_frame_rate'],
        'resolution':[v1['width'],v1['height']],'durationSeconds':float(v1['duration']),
        'noCropZoomOrReposition':True,'originalAudioStreamCopied':True,'decodedAudioIdentical':True,
        'sourceUnchanged':True,'fullDecode':'passed','encoding':'H264 CRF12; slight recompression differences beyond the corrected edge strips are possible.'}
out.with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
