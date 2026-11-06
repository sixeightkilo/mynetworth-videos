from pathlib import Path
import json,subprocess,hashlib
ROOT=Path(__file__).resolve().parents[1];W=ROOT/'out';W.mkdir(exist_ok=True);PUBLIC=ROOT/'public';c=json.loads((ROOT/'manifests/scene6-7.json').read_text())
subprocess.run(['node',str(ROOT/'scripts/verify-assets.mjs')],check=True)
filters=f'''[0:v]trim=end_frame={c['takeoverFrame']},setpts=PTS-STARTPTS,setsar=1[a];[1:v]trim=start_frame={c['approvedStartFrame']}:end_frame={c['approvedFrameCount']},setpts=PTS-STARTPTS,setsar=1[b];[a][b]concat=n=2:v=1:a=0[v];[0:a]afade=t=out:st={(c['sourceFrameCount']-c['audioFadeFrames'])/c['fps']}:d={c['audioFadeFrames']/c['fps']},apad,atrim=duration={c['durationInFrames']/c['fps']}[audio]'''
cmd=['ffmpeg','-hide_banner','-y','-filter_complex_threads','1','-i',str(PUBLIC/c['source']),'-i',str(PUBLIC/c['approved']),'-filter_complex',filters,'-map','[v]','-map','[audio]','-frames:v',str(c['durationInFrames']),'-r','24','-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(W/'scene-6-7-preview.mp4')]
with (W/'scene6-7-render-log.txt').open('w') as log:subprocess.run(cmd,stdout=log,stderr=log,check=True)
print(W/'scene-6-7-preview.mp4')
