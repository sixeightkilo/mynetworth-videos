"""Render only 720p v2 review media; never overwrite an existing render."""
import argparse,json,os,shutil,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--manifest',default='manifests/v2-segment2-r4.json');p.add_argument('--boundary',action='store_true');p.add_argument('--browser-executable');a=p.parse_args()
c=json.loads(Path(a.manifest).read_text())
r=c['revision']
name=f'segment-01-to-02-{r}-boundary-720p.mp4' if a.boundary else f'segment-02-{r}-preview-720p.mp4'
dest=Path(c['outputDir'])/name;assert not dest.exists(),f'Existing review render: {dest}'
dest.parent.mkdir(parents=True,exist_ok=True)
sampling=c.get('renderSupersampling',1)
render_dest=Path(c['workDir'])/(name.removesuffix('.mp4')+'-2x.mp4') if sampling>1 else dest
assert not render_dest.exists(),render_dest
assert Path(c['publicDir']).is_dir(),'Run npm run prepare:v2:segment2 first'
browser=a.browser_executable or os.environ.get('REMOTION_BROWSER_EXECUTABLE') or shutil.which('google-chrome') or shutil.which('chromium')
cmd=['npx','remotion','render','src/v2/index.jsx','V2Segment1To2BoundaryPreview' if a.boundary else 'V2Segment2Preview',str(render_dest),
     '--public-dir='+c['publicDir'],'--props='+json.dumps({'config':c}),f'--width={c["width"]}',f'--height={c["height"]}','--codec=h264',f'--crf={12 if sampling>1 else 16}','--pixel-format=yuv420p','--color-space=bt709','--image-format=png',
     f'--scale={1280/c["width"]*sampling}','--concurrency=2','--timeout=120000']
if browser:cmd+=['--browser-executable='+browser]
subprocess.run(cmd,check=True)

if sampling>1:
    subprocess.run(['ffmpeg','-v','error','-n','-i',str(render_dest),'-vf','scale=1280:720:flags=lanczos',
                    '-c:v','libx264','-crf','14','-preset','fast','-pix_fmt','yuv420p',
                    '-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-color_range','tv',
                    '-c:a','copy','-movflags','+faststart',str(dest)],check=True)
