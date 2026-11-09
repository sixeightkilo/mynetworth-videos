"""Validate rendered v2 review geometry, silence, and immutable inputs."""
import argparse,array,hashlib,json,subprocess
from fractions import Fraction
from pathlib import Path
parser=argparse.ArgumentParser();parser.add_argument('--manifest',default='manifests/v2-segment2-r4.json');args=parser.parse_args()
c=json.loads(Path(args.manifest).read_text());folder=Path(c['outputDir']);r=c['revision']
checks=json.loads(Path(c['workDir'],'input-checksums.json').read_text())
for p,h in checks.items():assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h,p
results=[]
for name,frames in [(f'segment-02-{r}-preview-720p.mp4',384),(f'segment-01-to-02-{r}-boundary-720p.mp4',432)]:
 p=folder/name
 if not p.exists():continue
 d=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]));v=next(s for s in d['streams'] if s['codec_type']=='video')
 assert (v['width'],v['height'],int(v['nb_frames']),Fraction(v['avg_frame_rate']))==(1280,720,frames,c['fps'])
 assert v['pix_fmt']=='yuv420p' and v['color_space']=='bt709'
 assert abs(float(v['duration'])-frames/c['fps'])<1/12288
 subprocess.run(['ffmpeg','-v','error','-i',str(p),'-f','null','-'],check=True)
 pcm=subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vn','-ac','1','-ar','24000','-f','s16le','-'])
 samples=array.array('h',pcm)
 # AAC transform overlap from the original dialogue lasts at most two AAC blocks.
 # It is not new Segment 2 audio. The standalone must remain exactly silent.
 guard=1024 if frames==432 else 0
 segment2=samples[48000+guard:] if frames==432 else samples
 peak=max(map(abs,segment2),default=0)
 if not c['music']['file']:assert peak==0,(name,peak)
 results.append({'file':str(p),'frames':frames,'fps':c['fps'],'videoSeconds':frames/c['fps'],'containerSeconds':float(d['format']['duration']),'resolution':[1280,720],'audioPresent':True,'segment2AudioPeakAfterCodecGuard':peak,'audioCodecGuardSeconds':guard/24000,'fullDecode':'passed','sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
report={'inputsUnchanged':True,'inputSHA256':checks,'renders':results,'compositionResolution':[c['width'],c['height']],'renderedAbove720p':False,'music':'Missing licensed asset; configurable, preview silent','casSelection':'1.416667–2.541667 seconds, followed by static Secure Local Import; no file picker/PAN entry or personal import completion','reportsSelection':'4.0–5.5 seconds, then original Custom-range frame at 5.458333 seconds','transition':'Approved native 720p alpha-mask composite and fitted corners; mask-clipped high-resolution dashboard; existing two-phase projective transform; no moving-video tracking or source modification' if c.get('approvedReference') else 'Frozen Segment 1 final frame; existing two-phase transition'}
(folder/f'segment-02-{r}-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'inputsUnchanged':True,'renders':results},indent=2))
