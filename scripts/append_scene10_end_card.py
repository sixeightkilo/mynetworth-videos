"""Append the rendered, silent Remotion end card while preserving Scenes 01–09.
All video packets and the original soundtrack of the prefix are copied.
"""
import argparse,array,hashlib,json,os,subprocess
from pathlib import Path
from fractions import Fraction

def probe(p):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(p)]))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pcm(p):return subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-map','0:a:0','-f','s16le','-'])
def frame_hashes(p,n):
 raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-map','0:v:0','-an','-frames:v',str(n),'-f','framemd5','-']).decode()
 return [x.split(',')[-1].strip() for x in raw.splitlines() if not x.startswith('#')]
def main():
 parser=argparse.ArgumentParser();parser.add_argument('manifest',nargs='?',default='manifests/scene10-end-card-v2.json')
 c=json.loads(Path(parser.parse_args().manifest).read_text());prefix=Path(c['prefixSource']);card=Path(c['standaloneOutput']);out=Path(c['completeOutput']);work=Path(c.get('workDir','out/scene10-end-card-v1'))/'mux'
 assert not out.exists(),out
 inputs={str(p):sha(p) for p in [prefix,card,Path(c['logoOriginal'])]}
 for p,n in [(prefix,c['prefixFrames']),(card,c['durationInFrames'])]:
  v=next(s for s in probe(p)['streams'] if s['codec_type']=='video')
  assert (v['width'],v['height'],int(v['nb_frames']),Fraction(v['avg_frame_rate']))==(1920,1080,n,c['fps'])
 if any(s['codec_type']=='audio' for s in probe(card)['streams']):
  assert max(map(abs,array.array('h',pcm(card))),default=0)==0,'End card is not silent'
 work.mkdir(parents=True,exist_ok=True)
 video_inputs=[]
 for p,n,name in [(prefix,c['prefixFrames'],'prefix'),(card,c['durationInFrames'],'card')]:
  v=work/f'{name}-video.mp4';assert not v.exists(),v
  subprocess.run(['ffmpeg','-v','error','-n','-i',str(p),'-map','0:v:0','-an','-c:v','copy',str(v)],check=True)
  video_inputs.append((v,n))
 lines=[]
 for p,n in video_inputs:
  relative=os.path.relpath(p,work).replace("'","'\\''");lines.extend([f"file '{relative}'",f'duration {n/c["fps"]:.12f}'])
 listing=work/'concat.txt';listing.write_text('\n'.join(lines)+'\n')
 subprocess.run(['ffmpeg','-v','error','-n','-f','concat','-safe','0','-i',str(listing),'-i',str(prefix),'-map','0:v:0','-map','1:a:0','-c','copy','-video_track_timescale','12288','-movflags','+faststart',str(out)],check=True)
 total=c['prefixFrames']+c['durationInFrames'];v=next(s for s in probe(out)['streams'] if s['codec_type']=='video')
 assert (int(v['nb_frames']),Fraction(v['avg_frame_rate']),float(v['start_time']))==(total,c['fps'],0)
 assert abs(float(v['duration'])-total/c['fps'])<1/12288
 subprocess.run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'],check=True)
 assert frame_hashes(prefix,c['prefixFrames'])==frame_hashes(out,c['prefixFrames'])
 assert pcm(prefix)==pcm(out)
 for p,h in inputs.items():assert sha(p)==h,p
 report={'output':str(out),'standalone':str(card),'finalStill':c['finalStill'],'frames':total,'fps':c['fps'],'resolution':[1920,1080],'durationSeconds':total/c['fps'],'scene10':{'frames':c['durationInFrames'],'durationSeconds':c['durationInFrames']/c['fps'],'fadeFrames':c['fadeFrames'],'completeHoldFrames':c['fullOpacityHoldFrames'],'completeHoldSeconds':c['fullOpacityHoldFrames']/c['fps'],'audio':'Silent; no new sound'},'prefix':{'frames':c['prefixFrames'],'decodedVideoIdentical':True,'decodedAudioIdentical':True,'sourceUnchanged':True},'logo':{'original':c['logoOriginal'],'derivative':'Off-white background keyed out for navy placement; original shield artwork retained'},'fullDecode':'passed','sourceSHA256':inputs,'remotionCompositions':['Scene10EndCard1080p','Scenes01To10Preview1080p']}
 out.with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
