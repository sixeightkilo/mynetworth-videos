"""Validate assembled output and compare it to the optional approval reference."""
from pathlib import Path
import hashlib,json,re,subprocess
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'out';video=OUT/'mynetworth-rough-cut-720p.mp4'
c=json.loads((ROOT/'manifests/approved-720p.json').read_text())
subprocess.run(['node',str(ROOT/'scripts/verify-assets.mjs')],check=True)
m=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(video)]))
v=next(s for s in m['streams'] if s['codec_type']=='video')
if (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))!=(1280,720,'24/1',c['durationInFrames']):raise RuntimeError('Unexpected output geometry/frame count')
if not any(s['codec_type']=='audio' for s in m['streams']):raise RuntimeError('Missing temporary dialogue audio')
decode=subprocess.run(['ffmpeg','-hide_banner','-i',str(video),'-vf','blackdetect=d=0:pix_th=0.02:pic_th=0.98','-f','null','-'],capture_output=True,text=True,check=True)
(OUT/'decode-validation.txt').write_text(decode.stderr)
if 'black_start:' in decode.stderr:raise RuntimeError('Full black frames detected; inspect decode-validation.txt')
result={'status':'passed','width':1280,'height':720,'fps':24,'frames':int(v['nb_frames']),'durationSeconds':int(v['nb_frames'])/24,'fullDecode':'passed','audio':'present','sourceChecksums':'passed'}
reference=ROOT/'references/approved-rough-cut-720p.mp4'
if reference.exists():
 compare=subprocess.run(['ffmpeg','-hide_banner','-i',str(video),'-i',str(reference),'-filter_complex_threads','1','-filter_complex','[0:v]setpts=PTS-STARTPTS[a];[1:v]setpts=PTS-STARTPTS[b];[a][b]psnr','-an','-f','null','-'],capture_output=True,text=True,check=True)
 (OUT/'reference-comparison.txt').write_text(compare.stderr)
 match=re.search(r'average:([\d.]+|inf)',compare.stderr)
 if match is None:raise RuntimeError('Missing PSNR comparison result')
 score=match.group(1)
 if score!='inf' and float(score)<40:raise RuntimeError(f'Approval comparison below threshold: {score}dB')
 result['referenceComparison']={'averagePSNRdB':score,'status':'passed','outputFileIdentical':hashlib.sha256(video.read_bytes()).hexdigest()==hashlib.sha256(reference.read_bytes()).hexdigest()}
 # Compare decoded audio; byte-identical PCM proves no dialogue timing/content change.
 def pcm_digest(path):
  raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-vn','-f','s16le','-ac','2','-ar','48000','pipe:1'])
  return hashlib.sha256(raw).hexdigest()
 result['referenceComparison']['decodedAudioIdentical']=pcm_digest(video)==pcm_digest(reference)
 if not result['referenceComparison']['decodedAudioIdentical']:raise RuntimeError('Decoded dialogue differs from approval reference')
else:result['referenceComparison']={'status':'skipped','reason':'Optional approval reference absent; no reference fidelity claim made'}
(OUT/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
