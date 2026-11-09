"""Stage immutable production inputs and derive lossless held frames. No AI.
Usage: python3 scripts/prepare_v2_segment2.py [manifest]
"""
import argparse,hashlib,json,shutil,struct,subprocess
from pathlib import Path

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def extract(source,dest,*,frame=None,seconds=None):
    temp=dest.with_suffix('.raw.png');dest.parent.mkdir(parents=True,exist_ok=True)
    args=['ffmpeg','-v','error','-n']
    if seconds is not None:args+=['-ss',str(seconds)]
    args+=['-i',str(source)]
    if frame is not None:args+=['-vf',f'select=eq(n\\,{frame})']
    subprocess.run(args+['-frames:v','1',str(temp)],check=True)
    data=temp.read_bytes();out=data[:8];pos=8
    while pos<len(data):
        n=struct.unpack('>I',data[pos:pos+4])[0];kind=data[pos+4:pos+8]
        if kind not in (b'gAMA',b'cHRM',b'iCCP',b'sRGB',b'cICP'):out+=data[pos:pos+n+12]
        pos+=n+12
    dest.write_bytes(out);temp.unlink()

p=argparse.ArgumentParser();p.add_argument('manifest',nargs='?',default='manifests/v2-segment2-r4.json')
c=json.loads(Path(p.parse_args().manifest).read_text());root=Path(c['publicDir']);assert not root.exists(),root
assert sha(c['segment1']['source'])==c['segment1']['sha256'],'Approved Segment 1 source changed'
inputs=[Path(c['segment1']['source']),Path(c['logoSource'])]+list(Path('public/app-recordings').glob('*.mp4'))+[Path('public/screenshots/import-local.png')]
ref=c.get('approvedReference')
if ref:
    for path,h in ref['expectedSHA256'].items():assert sha(path)==h,path
    inputs.extend(Path(ref[k]) for k in ['compositeSource','referenceSource','maskSource','mappingSource','dashboardSource'])
    for key in ['compositeSource','maskSource','referenceSource']:
        data=Path(ref[key]).read_bytes();assert data[:8]==b'\x89PNG\r\n\x1a\n'
        assert struct.unpack('>II',data[16:24])==(ref['width'],ref['height'])
checks={str(p):sha(p) for p in inputs}
shutil.copytree('public',root)
for relative,source in [(c['segment1']['file'],c['segment1']['source']),(c['logo'],c['logoSource'])]:
    dest=root/relative;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,dest)
if ref:
    for relative,source in [(c['segment1']['finalImage'],ref['compositeSource']),(ref['maskFile'],ref['maskSource']),(ref['dashboardFile'],ref['dashboardSource'])]:
        target=root/relative;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
else:
    extract(c['segment1']['source'],root/c['segment1']['finalImage'],frame=c['segment1']['frames']-1)
hold=c['recordings']['reportsHold'];extract(hold['sourceFile'],root/hold['image'],seconds=hold['sourceSeconds'])
for path,h in checks.items():assert sha(path)==h,path
Path(c['workDir'],'input-checksums.json').write_text(json.dumps(checks,indent=2)+'\n')
print(f'Staged Segment 1, real app media and held frames in {root}')
