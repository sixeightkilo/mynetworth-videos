"""Normalize only the new card to the existing film's H.264 BT.709 TV range.
The Remotion raw render is retained. The five-second video has no audio track.
"""
import argparse,json,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('raw_render');p.add_argument('--manifest',default='manifests/scene10-end-card-v2.json');args=p.parse_args()
c=json.loads(Path(args.manifest).read_text());dest=Path(c['standaloneOutput']);assert not dest.exists(),dest
subprocess.run(['ffmpeg','-v','error','-n','-i',args.raw_render,'-map','0:v:0','-an','-vf','scale=in_color_matrix=bt601:out_color_matrix=bt709:in_range=pc:out_range=tv,format=yuv420p','-c:v','libx264','-profile:v','high','-level:v','4.0','-crf','14','-preset','fast','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-color_range','tv','-video_track_timescale','12288','-movflags','+faststart',str(dest)],check=True)
