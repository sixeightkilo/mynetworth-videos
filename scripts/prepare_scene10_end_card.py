"""Stage only versioned production inputs plus end-card derivatives for Remotion.
Original assets are unchanged; no dependency on historical project locations.
"""
import argparse,json,shutil,hashlib
from pathlib import Path
parser=argparse.ArgumentParser();parser.add_argument('manifest',nargs='?',default='manifests/scene10-end-card-v2.json')
c=json.loads(Path(parser.parse_args().manifest).read_text())
root=Path(c['publicDir']);assert not root.exists(),root
shutil.copytree('public',root)
assets={c['prefixVideo']:c['prefixSource'],c['startImage']:c.get('startImageSource','production/scene-10/output/scene-09-final-frame-v1.png'),c['logo']:c.get('logoDisplaySource','production/scene-10/references/logo-transparent-v1.png')}
for relative,source in assets.items():
 target=root/relative;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
 assert hashlib.sha256(Path(source).read_bytes()).digest()==hashlib.sha256(target.read_bytes()).digest()
print(f'Remotion public inputs staged under {root}')
