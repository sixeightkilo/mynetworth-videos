"""Append an existing legacy graphic/showcase tail to a preserved review prefix.
Python standard library + FFmpeg/FFprobe only. Sources and outputs never overwritten.
"""
import argparse,array,hashlib,json,os,subprocess
from pathlib import Path
from fractions import Fraction

def probe(p):
 return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(p)]))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pcm(p):return subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-map','0:a:0','-f','s16le','-'])
def frame_hashes(p,limit):
 data=subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-map','0:v:0','-an','-frames:v',str(limit),'-f','framemd5','-']).decode()
 return [line.split(',')[-1].strip() for line in data.splitlines() if not line.startswith('#')]
def run(manifest):
 c=json.loads(Path(manifest).read_text());prefix=Path(c['prefix']);legacy=Path(c['legacy']);out=Path(c['output']);work=Path(c['workDir'])
 assert not out.exists(),out
 hashes={str(p):sha(p) for p in (prefix,legacy)}
 v0=next(s for s in probe(prefix)['streams'] if s['codec_type']=='video')
 v1=next(s for s in probe(legacy)['streams'] if s['codec_type']=='video')
 assert (v0['width'],v0['height'],int(v0['nb_frames']))==(c['width'],c['height'],c['prefixFrames'])
 assert Fraction(v0['avg_frame_rate'])==Fraction(v1['avg_frame_rate'])==c['fps']
 start,end=c['legacyStartFrame'],c['legacyEndFrameExclusive'];assert 0<=start<end<=int(v1['nb_frames'])
 # App-facing tail is silent in the approved baked source. Verify rather than
 # drop potentially audible material; a non-silent selection must be reviewed.
 audio=subprocess.check_output(['ffmpeg','-v','error','-i',str(legacy),'-af',f'atrim=start={start/c["fps"]}:end={end/c["fps"]}','-vn','-f','s16le','-'])
 assert max(map(abs,array.array('h',audio)),default=0)==0,'Legacy tail contains sound; review audio assembly'
 work.mkdir(parents=True,exist_ok=True);out.parent.mkdir(parents=True,exist_ok=True)
 tail=work/'legacy-tail-1080p.mp4';assert not tail.exists(),tail
 vf=f'trim=start_frame={start}:end_frame={end},setpts=PTS-STARTPTS,scale={c["width"]}:{c["height"]}:flags=lanczos,setsar=1'
 timescale=int(Fraction(v0['time_base']).denominator)
 subprocess.run(['ffmpeg','-v','error','-n','-i',str(legacy),'-vf',vf,'-an','-c:v','libx264','-profile:v','high','-level:v','4.0','-crf','16','-preset','fast','-pix_fmt','yuv420p','-video_track_timescale',str(timescale),str(tail)],check=True)
 lines=[]
 for path,frames in [(prefix,c['prefixFrames']),(tail,end-start)]:
  rel=os.path.relpath(path,work).replace("'","'\\''")
  lines += [f"file '{rel}'",f'duration {frames/c["fps"]:.12f}']
 listing=work/'concat.txt';listing.write_text('\n'.join(lines)+'\n')
 subprocess.run(['ffmpeg','-v','warning','-n','-f','concat','-safe','0','-i',str(listing),'-i',str(prefix),'-map','0:v:0','-map','1:a:0','-c','copy','-video_track_timescale',str(timescale),'-movflags','+faststart',str(out)],check=True)
 total=c['prefixFrames']+end-start
 result=next(s for s in probe(out)['streams'] if s['codec_type']=='video')
 assert (int(result['nb_frames']),Fraction(result['avg_frame_rate']))==(total,c['fps']),result
 subprocess.run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'],check=True)
 assert frame_hashes(prefix,c['prefixFrames'])==frame_hashes(out,c['prefixFrames']),'Prefix video changed'
 assert pcm(prefix)==pcm(out),'Prefix audio changed'
 for path,digest in hashes.items():assert sha(path)==digest,path
 report={'output':str(out),'manifest':manifest,'resolution':[c['width'],c['height']],'fps':c['fps'],'frames':total,'durationSeconds':total/c['fps'],'prefix':{'file':str(prefix),'frames':c['prefixFrames'],'decodedFramesIdentical':True,'decodedAudioIdentical':True},'legacy':{'file':str(legacy),'sourceResolution':[v1['width'],v1['height']],'range':[start,end],'scene6TailFrames':c['legacyScene7StartFrame']-start,'scene7Frames':end-c['legacyScene7StartFrame'],'upscale':'Lanczos 720p to 1080p; not native 1080p detail','originalRecordingsCaptionsTransitions':'Preserved baked media','audio':'Selected app-facing tail verified digitally silent'},'selectionNote':c['selectionNote'],'sourcesSHA256':hashes,'sourceHashes':'unchanged','fullDecode':'passed'}
 out.with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('manifest');run(p.parse_args().manifest)
