"""Render assembly directly from the same manifest as the separate Remotion composition.
Existing scene composites are decoded, fitted without stretching, and concatenated.
No source or individual scene is modified. No browser is required for assembly.
"""
from pathlib import Path
import subprocess,json,hashlib
ROOT=Path(__file__).resolve().parents[1];W=ROOT/'out';W.mkdir(exist_ok=True)
import sys
PUBLIC=ROOT/'public'
c=json.loads((ROOT/'manifests/approved-720p.json').read_text());fps=c['fps'];e=c['endCard']
subprocess.run(['node',str(ROOT/'scripts/verify-assets.mjs')],check=True)
width,height=(1920,1080) if '--1080p' in sys.argv else (1280,720)
cmd=['ffmpeg','-hide_banner','-y','-filter_complex_threads','1']
for clip in c['clips']:cmd+=['-i',str(PUBLIC/clip['source'])]
cmd+=['-loop','1','-framerate',str(fps),'-i',str(PUBLIC/e['file'])]
filters=[]
for i,clip in enumerate(c['clips']):
 n=clip['durationInFrames'];duration=n/fps
 filters.append(f'[{i}:v]trim=end_frame={n},setpts=PTS-STARTPTS,scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:black,setsar=1,fps={fps},settb=1/{fps},format=yuv420p[v{i}]')
 filters.append(f'[{i}:a]aresample=48000,apad,atrim=end_sample={n*2000},asetpts=PTS-STARTPTS,aformat=sample_fmts=fltp:channel_layouts=stereo[a{i}]')
filters.append(''.join(f'[v{i}][a{i}]' for i in range(len(c['clips'])))+f'concat=n={len(c["clips"])}:v=1:a=1[filmv][filma]')
filters.append(f'[filmv]settb=1/{fps},setpts=PTS-STARTPTS[base]')
filters.append(f'[{len(c["clips"])}:v]trim=end_frame={e["durationInFrames"]},setpts=PTS-STARTPTS,settb=1/{fps},scale={width}:{height},format=yuv420p,setsar=1[card]')
filters.append(f'[base][card]xfade=transition=fade:duration={e["fadeFrames"]/fps}:offset={e["fromFrame"]/fps},format=yuv420p[v]')
filters.append(f'[filma]afade=t=out:st={e["fromFrame"]/fps}:d={e["fadeFrames"]/fps},apad,atrim=end_sample={c["durationInFrames"]*2000}[a]')
script=W/'assembly-filter.txt';script.write_text(';\n'.join(filters))
out=W/('mynetworth-production-1080p.mp4' if '--1080p' in sys.argv else 'mynetworth-rough-cut-720p.mp4')
cmd+=['-filter_complex_script',str(script),'-map','[v]','-map','[a]','-frames:v',str(c['durationInFrames']),'-t',str(c['durationInFrames']/fps),'-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(out)]
with (W/'render-log.txt').open('w') as log:subprocess.run(cmd,stdout=log,stderr=log,check=True)
subprocess.run(['node',str(ROOT/'scripts/verify-assets.mjs')],check=True)
print(out,flush=True)
