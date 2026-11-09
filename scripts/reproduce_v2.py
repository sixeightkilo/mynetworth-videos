"""Reproduce the accepted V2 soundtrack review from versioned production inputs."""
import argparse
import json
from pathlib import Path
from mix_v2_soundtrack import main, sha

p=argparse.ArgumentParser()
p.add_argument('--output-dir',default='out/v2-reproduction')
a=p.parse_args()
inventory=json.loads(Path('manifests/v2-production-checksums.json').read_text())
for item in inventory['files']:
    assert sha(item['path'])==item['sha256'],item['path']
root=Path(a.output_dir)
assert not root.exists(),root
root.mkdir(parents=True)
c=json.loads(Path('manifests/v2-soundtrack-r2.json').read_text())
c['output']=str(root/'scene-01-04-review-music-r2.mp4')
c['workDir']=str(root/'work')
manifest=root/'soundtrack.json'
manifest.write_text(json.dumps(c,indent=2)+'\n')
main(str(manifest))
reference='production/v2/output/scene-01-04-review-music-r2.mp4'
assert sha(c['output'])==sha(reference),'Output bytes differ; compare codec/tool versions.'
print('V2 reproduction matches the accepted music-r2 MP4 byte for byte.')
