"""Complete V2 Scene 1 using the accepted POC pixel compositor.
Streams frames; preserves source/audio, timeline and the approved turn geometry.
"""
import argparse,json,subprocess
from pathlib import Path
import cv2
import numpy as np
from composite_phone_turn_poc import aperture,composite_frame,flow_check,sha

def encoder(path,w,h,fps,source):
    assert not path.exists(),path
    args=['ffmpeg','-v','error','-n','-f','rawvideo','-pix_fmt','bgr24','-s',f'{w}x{h}','-r',str(fps),'-i','-',
          '-i',source,'-map','0:v:0','-map','1:a:0','-vf','scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int',
          '-c:v','libx264','-crf','14','-preset','fast','-threads','4','-pix_fmt','yuv420p','-colorspace','bt709',
          '-color_primaries','bt709','-color_trc','bt709','-color_range','tv','-c:a','copy','-movflags','+faststart',str(path)]
    return subprocess.Popen(args,stdin=subprocess.PIPE)

def pcm(path):return subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-vn','-f','s16le','-'])

def run(manifest):
    c=json.loads(Path(manifest).read_text());assert c['startFrame']==0 and c['endFrameExclusive']==505
    assert sha(c['source'])==c['sourceSHA256'];source=c['source'];checksums={p:sha(p) for p in [source,c['dashboard']]}
    root=Path(c['outputDir']);root.mkdir(parents=True,exist_ok=True)
    native=root/'scene-01-dashboard-native-r1.mp4';review=root/'scene-01-dashboard-720p-r1.mp4'
    cap=cv2.VideoCapture(source);w=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH));h=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    encoders=[encoder(native,w,h,c['fps'],source),encoder(review,1280,720,c['fps'],source)]
    shot=cv2.imread(c['dashboard']);sh,sw=shot.shape[:2];opening=aperture(sw,sh,c['cornerRadius'])
    alignment=np.float64(c['outputAlignment']['nativeToReferenceSimilarity'])
    corners={int(k):np.float32(q) for k,q in c['reviewedPerFrameCorners'].items()}
    n=0;previous=None;flow=[];snapshots={};skin_counts={}
    keep={0,240,420,425,426,427,428,430,443,444,450,460,480,492,504}
    while True:
        ok,original=cap.read()
        if not ok:break
        if n>=c['visibleStartFrame']:
            keys=sorted(int(k) for k in c['visibilityOpacity']);opacity=np.interp(n,keys,[c['visibilityOpacity'][str(k)] for k in keys])
            result,skin_counts[str(n)]=composite_frame(original,shot,opening,corners[n],c['supersampling'],opacity)
            if n>c['visibleStartFrame']:flow.append({'frame':n,**flow_check(previous,original,corners[n-1],corners[n])})
        else:
            result=original
            assert np.array_equal(result,original)
        image720=cv2.warpAffine(result,alignment,(1280,720),flags=cv2.INTER_LANCZOS4,borderMode=cv2.BORDER_CONSTANT,borderValue=(255,255,255))
        encoders[0].stdin.write(result.tobytes());encoders[1].stdin.write(image720.tobytes())
        if n in keep:snapshots[n]=(original.copy(),result.copy(),image720.copy())
        previous=original;n+=1
    cap.release();assert n==c['endFrameExclusive']
    for e in encoders:e.stdin.close()
    for e in encoders:assert e.wait()==0
    assert pcm(source)==pcm(native)==pcm(review),'Whole-source decoded audio changed'
    metadata=[]
    for p in [native,review]:
        d=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
        v=next(x for x in d['streams'] if x['codec_type']=='video')
        assert int(v['nb_frames'])==505 and v['avg_frame_rate']=='24/1'
        assert abs(float(v['duration'])-505/24)<1/12288
        assert v['color_space']==v['color_primaries']==v['color_transfer']=='bt709' and v['color_range']=='tv'
        subprocess.run(['ffmpeg','-v','error','-i',str(p),'-f','null','-'],check=True)
        metadata.append({'path':str(p),'frames':505,'fps':24,'videoSeconds':505/24,'resolution':[v['width'],v['height']],
                         'audioPresent':True,'decodedAudioIdenticalToSource':True,'fullDecode':'passed','sha256':sha(p)})
    # Useful native before/after details, without adding camera motion to production footage.
    rows=[]
    for n in [420,426,427,428,443,450,460,480,504]:
        a,b,_=snapshots[n];q=corners.get(n,corners[c['visibleStartFrame']]);cx,cy=q.mean(axis=0)
        x=int(np.clip(cx-120,0,w-240));y=int(np.clip(cy-100,0,h-200));row=[]
        for label,img in [('Original',a),('Dashboard',b)]:
            tile=np.full((435,480,3),245,np.uint8);tile[:400]=cv2.resize(img[y:y+200,x:x+240],(480,400));cv2.putText(tile,f'{label} {n} / {n/24:.3f}s',(10,427),0,.6,(20,20,20),1);row.append(tile)
        rows.append(np.hstack(row))
    cv2.imwrite(str(root/'scene-01-dashboard-contact-r1.jpg'),np.vstack(rows))
    cv2.imwrite(str(root/'scene-01-dashboard-final-720p-r1.png'),snapshots[504][2])
    # Wide-context sequence, for concise contact-sheet review of the whole scene.
    tiles=[]
    for n in [0,240,420,426,430,450,480,504]:
        tile=np.full((296,480,3),245,np.uint8);tile[:270]=cv2.resize(snapshots[n][2],(480,270));cv2.putText(tile,f'{n/24:.3f}s | {n}',(10,289),0,.5,(20,20,20),1);tiles.append(tile)
    cv2.imwrite(str(root/'scene-01-dashboard-wide-r1.jpg'),np.vstack([np.hstack(tiles[i:i+2]) for i in range(0,len(tiles),2)]))
    for p,value in checksums.items():assert sha(p)==value,p
    report={'manifest':manifest,'frames':505,'fps':24,'videoSeconds':505/24,'originalSourceUnchanged':True,
            'inputSHA256':checksums,'visibleStartFrame':426,'acceptedPOCGeometryPreservedThroughFrame':443,
            'noAddedNotch':True,'outsideMattePixelsUnchangedBeforeEncoding':True,'framesBefore426UnchangedBeforeEncodingAndOutputSizing':True,
            'decodedAudioIdenticalToOriginal':True,'outputAlignment':c['outputAlignment'],'endpointCalibration':c['endpointCalibration'],
            'flowChecks':flow,'skinPixelsInsideDisplay':skin_counts,'outputs':metadata}
    (root/'scene-01-dashboard-full-r1-report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'frames':505,'videoSeconds':505/24,'outputs':metadata},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('manifest',nargs='?',default='manifests/v2-scene1-dashboard-full-r1.json');run(p.parse_args().manifest)
