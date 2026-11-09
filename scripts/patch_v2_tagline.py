"""Apply the Remotion-rendered tagline region to the accepted full film."""
import argparse,json,subprocess
from pathlib import Path
from mix_v2_soundtrack import sha,probe

p=argparse.ArgumentParser();p.add_argument('manifest');a=p.parse_args()
c=json.loads(Path(a.manifest).read_text());out=Path(c['output']);assert not out.exists(),out
checks={path:sha(path) for path in [c['source'],c['patch']]}
patch_video=next(s for s in probe(c['patch']) if s['codec_type']=='video')
assert int(patch_video['nb_frames'])==c['patchFrames']
x,y,w,h=c['rectangle'];start=c['patchStartGlobalFrame'];end=start+c['patchFrames']
f=f"[1:v]crop={w}:{h}:{x}:{y},setpts=PTS-STARTPTS+{start}/{c['fps']}/TB[p];[0:v][p]overlay=x={x}:y={y}:enable='gte(n,{start})*lt(n,{end})':eof_action=pass:repeatlast=0[v]"
subprocess.run(['ffmpeg','-v','error','-n','-i',c['source'],'-i',c['patch'],'-filter_complex',f,
                '-map','[v]','-map','0:a:0','-c:v','libx264','-crf','12','-preset','slow','-threads','4',
                '-pix_fmt','yuv420p','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709',
                '-color_range','tv','-c:a','copy','-movflags','+faststart',str(out)],check=True)
def pcm(path):return subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-vn','-f','s16le','-'])
assert pcm(c['source'])==pcm(out)
v0=next(s for s in probe(c['source']) if s['codec_type']=='video');v1=next(s for s in probe(out) if s['codec_type']=='video')
for k in ['width','height','nb_frames','avg_frame_rate','duration','start_time']:assert v0[k]==v1[k],k
assert checks=={path:sha(path) for path in checks}
subprocess.run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'],check=True)
report={'output':str(out),'sourceSHA256':checks,'outputSHA256':sha(out),'frames':int(v1['nb_frames']),
        'resolution':[v1['width'],v1['height']],'durationSeconds':float(v1['duration']),
        'decodedAudioIdentical':True,'patchGlobalFrameRange':[start,end],'patchRectangle':c['rectangle'],
        'fullDecode':'passed','sourcesUnchanged':True,'note':'Only the tagline region is replaced; H264 CRF12 recompression introduces minor differences elsewhere.'}
out.with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
