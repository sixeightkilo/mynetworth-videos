import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const checks=JSON.parse(fs.readFileSync(path.join(root,'manifests/asset-checksums.json')));
for(const [name,record] of Object.entries(checks)) {
 const sum=createHash('sha256').update(fs.readFileSync(path.join(root,name))).digest('hex');
 if(sum!==record.sha256)throw new Error(`Approved asset changed: ${name}`);
}
const film=JSON.parse(fs.readFileSync(path.join(root,'manifests/approved-720p.json')));
let end=0;
for(const clip of film.clips){if(clip.fromFrame!==end)throw Error(`Gap or overlap at ${clip.file}`);end+=clip.durationInFrames;}
if(film.endCard.fromFrame!==end-film.endCard.fadeFrames || film.durationInFrames!==end+film.endCard.holdFrames)throw Error('End card timing mismatch');
console.log(`Verified ${Object.keys(checks).length} approved assets and ${film.durationInFrames} timeline frames.`);
