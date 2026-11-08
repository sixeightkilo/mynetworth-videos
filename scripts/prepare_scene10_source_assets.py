"""Derive the held source frame and transparent actual-logo assets conventionally.
Strip PNG colour-profile metadata without changing encoded pixel data so browser
colour management does not shift the frozen video frame. Never overwrite assets.
"""
import argparse,json,struct,subprocess,tempfile
from pathlib import Path

def strip_colour_metadata(source,destination):
 data=source.read_bytes();result=data[:8];pos=8
 assert result==b'\x89PNG\r\n\x1a\n'
 while pos<len(data):
  length=struct.unpack('>I',data[pos:pos+4])[0];kind=data[pos+4:pos+8]
  if kind not in (b'gAMA',b'cHRM',b'iCCP',b'sRGB',b'cICP'):result+=data[pos:pos+length+12]
  pos+=length+12
 destination.write_bytes(result)

parser=argparse.ArgumentParser();parser.add_argument('manifest',nargs='?',default='manifests/scene10-end-card-v2.json');args=parser.parse_args()
c=json.loads(Path(args.manifest).read_text())
frame=Path(c['startImageSource']);logo=Path(c['logoDisplaySource'])
for p in (frame,logo):assert not p.exists(),p;p.parent.mkdir(parents=True,exist_ok=True)
work=Path(c['workDir']);work.mkdir(parents=True,exist_ok=True)
with tempfile.TemporaryDirectory(prefix='source-assets-',dir=work) as folder:
 folder=Path(folder);raw_frame=folder/'frame.png';raw_logo=folder/'logo.png'
 subprocess.run(['ffmpeg','-v','error','-n','-i',c['prefixSource'],'-vf',f'select=eq(n\\,{c["prefixFrames"]-1})','-frames:v','1',str(raw_frame)],check=True)
 subprocess.run(['ffmpeg','-v','error','-n','-i',c['logoOriginal'],'-vf','colorkey=0xFFFFFF:0.10:0.04,format=rgba','-frames:v','1',str(raw_logo)],check=True)
 strip_colour_metadata(raw_frame,frame);strip_colour_metadata(raw_logo,logo)
print('Prepared lossless held-frame pixels and background-keyed original logo.')
