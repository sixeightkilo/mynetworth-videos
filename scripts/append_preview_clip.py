"""Append one complete native-resolution clip, copying existing video packets.
Audio is padded to each video duration and concatenated on the exact frame cut.
Python standard library and FFmpeg/FFprobe only. No source/output overwrite.
"""
import argparse,array,hashlib,json,os,subprocess,math
from pathlib import Path
from fractions import Fraction

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def probe(p):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(p)]))
def hashes(p,n):
 data=subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-map','0:v:0','-an','-frames:v',str(n),'-f','framemd5','-']).decode()
 return [x.split(',')[-1].strip() for x in data.splitlines() if not x.startswith('#')]
def pcm(p):return array.array('h',subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vn','-ac','1','-ar','24000','-f','s16le','-']))
def run(manifest):
 c=json.loads(Path(manifest).read_text());prefix=Path(c['prefix']);clip=Path(c['append']);out=Path(c['output']);work=Path(c['workDir'])
 assert not out.exists(),out
 sources={str(p):sha(p) for p in (prefix,clip)}
 for p,n in [(prefix,c['prefixFrames']),(clip,c['appendFrames'])]:
  v=next(s for s in probe(p)['streams'] if s['codec_type']=='video')
  assert (v['width'],v['height'],int(v['nb_frames']),Fraction(v['avg_frame_rate']))==(c['width'],c['height'],n,c['fps'])
 work.mkdir(parents=True,exist_ok=True);out.parent.mkdir(parents=True,exist_ok=True)
 tail=work/'append-video.mp4';assert not tail.exists(),tail
 subprocess.run(['ffmpeg','-v','error','-n','-i',str(clip),'-map','0:v:0','-an','-c:v','libx264','-crf','16','-preset','fast','-profile:v','high','-level:v','4.0','-pix_fmt','yuv420p','-video_track_timescale','12288',str(tail)],check=True)
 prefix_video=work/'prefix-video.mp4'
 subprocess.run(['ffmpeg','-v','error','-n','-i',str(prefix),'-map','0:v:0','-an','-c:v','copy',str(prefix_video)],check=True)
 lines=[]
 for p,n in [(prefix_video,c['prefixFrames']),(tail,c['appendFrames'])]:
  name=os.path.relpath(p,work).replace("'","'\\''");lines.extend([f"file '{name}'",f'duration {n/c["fps"]:.12f}'])
 listing=work/'concat.txt';listing.write_text('\n'.join(lines)+'\n')
 d0=c['prefixFrames']/c['fps'];d1=c['appendFrames']/c['fps']
 af=f'[0:a:0]aresample=44100,apad,atrim=duration={d0:.12f},asetpts=PTS-STARTPTS[a0];[1:a:0]aresample=44100,apad,atrim=duration={d1:.12f},asetpts=PTS-STARTPTS[a1];[a0][a1]concat=n=2:v=0:a=1[a]'
 joined_video=work/'joined-video.mp4';joined_audio=work/'joined-audio.m4a'
 subprocess.run(['ffmpeg','-v','error','-n','-f','concat','-safe','0','-i',str(listing),'-map','0:v:0','-an','-c:v','copy','-video_track_timescale','12288',str(joined_video)],check=True)
 subprocess.run(['ffmpeg','-v','error','-n','-i',str(prefix),'-i',str(clip),'-filter_complex',af,'-map','[a]','-c:a','aac','-b:a','192k','-ar','44100',str(joined_audio)],check=True)
 subprocess.run(['ffmpeg','-v','error','-n','-i',str(joined_video),'-i',str(joined_audio),'-map','0:v:0','-map','1:a:0','-c','copy','-video_track_timescale','12288','-movflags','+faststart',str(out)],check=True)
 total=c['prefixFrames']+c['appendFrames'];v=next(s for s in probe(out)['streams'] if s['codec_type']=='video')
 assert (v['width'],v['height'],int(v['nb_frames']),Fraction(v['avg_frame_rate']))==(c['width'],c['height'],total,c['fps'])
 assert abs(float(v['start_time']))<1e-6
 assert abs(float(v['duration'])-total/c['fps'])<1/12288
 subprocess.run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'],check=True)
 assert hashes(prefix,c['prefixFrames'])==hashes(out,c['prefixFrames'])
 samples=pcm(out);audio_checks=[]
 for p,offset in [(prefix,0),(clip,round(d0*24000))]:
  a=pcm(p);n=min(len(a),len(samples)-offset)
  def corr(lag):
   aa=a[48:n-48];b=samples[offset+48+lag:offset+n-48+lag]
   return sum(x*y for x,y in zip(aa,b))/math.sqrt(sum(x*x for x in aa)*sum(y*y for y in b))
  lag=max(range(-2,3),key=corr);value=corr(lag);assert value>.98,(p,value)
  audio_checks.append({'source':str(p),'correlation':value,'lagSamplesAt24kHz':lag})
 for p,h in sources.items():assert sha(p)==h
 report={'output':str(out),'manifest':manifest,'frames':total,'fps':c['fps'],'durationSeconds':total/c['fps'],'resolution':[c['width'],c['height']],'prefixFramesCopiedAndDecodedIdentical':c['prefixFrames'],'append':{'source':str(clip),'frames':c['appendFrames'],'startSeconds':d0,'trim':'none'},'audio':'Original soundtracks retained; prefix padded with silence to its video duration; AAC re-encoded for the joined track','audioChecks':audio_checks,'fullDecode':'passed','sourceSHA256':sources,'sourcesUnchanged':True}
 out.with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('manifest');run(p.parse_args().manifest)
