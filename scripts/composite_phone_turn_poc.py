"""One-second native-coordinate phone-screen POC; no source modification.
Reviewed per-frame geometry with independent flow checks, supersampled aperture,
original-pixel finger holdouts, explicit BT.709 and normalized original audio excerpt.
"""
import argparse,hashlib,json,subprocess
from pathlib import Path
import cv2
import numpy as np

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read_frames(source,start,end):
    cap=cv2.VideoCapture(source);cap.set(cv2.CAP_PROP_POS_FRAMES,start);frames=[]
    for _ in range(start,end):
        ok,im=cap.read();assert ok;frames.append(im)
    cap.release();return frames

def aperture(w,h,r):
    a=np.zeros((h,w),np.uint8)
    cv2.rectangle(a,(r,0),(w-r-1,h-1),255,-1);cv2.rectangle(a,(0,r),(w-1,h-r-1),255,-1)
    for x in [r,w-r-1]:
        for y in [r,h-r-1]:cv2.circle(a,(x,y),r,255,-1)
    return a

def flow_check(previous,current,q0,q1):
    g0=cv2.cvtColor(previous,cv2.COLOR_BGR2GRAY);g1=cv2.cvtColor(current,cv2.COLOR_BGR2GRAY)
    mask=np.zeros_like(g0);cv2.fillConvexPoly(mask,np.rint(q0).astype('int32'),255)
    mask=cv2.erode(mask,np.ones((3,3),np.uint8))
    pts=cv2.goodFeaturesToTrack(g0,120,.01,2,mask=mask)
    if pts is None or len(pts)<4:return {'status':'manual geometry; too few features','features':0 if pts is None else len(pts)}
    nxt,st,_=cv2.calcOpticalFlowPyrLK(g0,g1,pts,None,winSize=(25,25),maxLevel=3)
    back,bs,_=cv2.calcOpticalFlowPyrLK(g1,g0,nxt,None,winSize=(25,25),maxLevel=3)
    valid=(st[:,0]>0)&(bs[:,0]>0)&(np.linalg.norm(back-pts,axis=2)[:,0]<.5)
    if valid.sum()<4:return {'status':'manual geometry; flow rejected','features':len(pts),'valid':int(valid.sum())}
    H,inside=cv2.findHomography(pts[valid],nxt[valid],cv2.RANSAC,.7)
    if H is None:return {'status':'manual geometry; homography rejected','valid':int(valid.sum())}
    if inside.sum()<8:
        return {'status':'weak check rejected; manual geometry retained','features':len(pts),
                'valid':int(valid.sum()),'inliers':int(inside.sum()),'estimateRejected':True}
    pred=cv2.perspectiveTransform(q0[None],H)[0]
    return {'status':'independent motion check','features':len(pts),'valid':int(valid.sum()),
            'inliers':int(inside.sum()),'maxCornerDisagreementPixels':float(np.linalg.norm(pred-q1,axis=1).max())}

def composite_frame(original,shot,cap,q,supersampling,opacity):
    h,w=original.shape[:2];sh,sw=shot.shape[:2]
    srcquad=np.float32([[0,0],[sw-1,0],[sw-1,sh-1],[0,sh-1]])
    H=cv2.getPerspectiveTransform(srcquad,q)
    lo=np.maximum(np.floor(q.min(axis=0)-3).astype(int),0);hi=np.minimum(np.ceil(q.max(axis=0)+4).astype(int),[w,h]);x,y=lo;rw,rh=hi-lo
    sampling=supersampling;T=np.array([[sampling,0,-x*sampling],[0,sampling,-y*sampling],[0,0,1]],float)
    warped=cv2.warpPerspective(shot,T@H,(rw*sampling,rh*sampling),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)
    matte=cv2.warpPerspective(cap,T@H,(rw*sampling,rh*sampling),flags=cv2.INTER_LINEAR)
    warped=cv2.resize(warped,(rw,rh),interpolation=cv2.INTER_AREA)
    alpha=cv2.resize(matte,(rw,rh),interpolation=cv2.INTER_AREA).astype(np.float32)/255
    local=original[y:y+rh,x:x+rw];hsv=cv2.cvtColor(local,cv2.COLOR_BGR2HSV)
    skin=cv2.inRange(hsv,np.array([0,48,65]),np.array([27,255,255]))
    skin_count=int(((skin>0)&(alpha>.01)).sum())
    skin=cv2.dilate(skin,np.ones((3,3),np.uint8));skin=cv2.GaussianBlur(skin.astype(np.float32)/255,(3,3),.35)
    alpha*=1-skin;alpha*=opacity
    composite=np.rint(warped*alpha[:,:,None]+local*(1-alpha[:,:,None])).astype('uint8')
    assert np.array_equal(composite[alpha==0],local[alpha==0])
    result=original.copy();result[y:y+rh,x:x+rw]=composite
    return result,skin_count

def run(manifest):
    c=json.loads(Path(manifest).read_text());source=c['source'];assert sha(source)==c['sourceSHA256']
    assert c['endFrameExclusive']-c['startFrame']==c['fps'],'One-second POC only'
    root=Path(c['outputDir']);root.mkdir(parents=True,exist_ok=True)
    dest=root/'scene-01-turn-dashboard-native-r1.mp4';assert not dest.exists(),dest
    frames=read_frames(source,c['startFrame'],c['endFrameExclusive']);h,w=frames[0].shape[:2]
    shot=cv2.imread(c['dashboard']);sh,sw=shot.shape[:2];original_hashes={p:sha(p) for p in [source,c['dashboard']]}
    corners={int(n):np.float32(q) for n,q in c['reviewedPerFrameCorners'].items()}
    cap=aperture(sw,sh,c['cornerRadius']);srcquad=np.float32([[0,0],[sw-1,0],[sw-1,sh-1],[0,sh-1]])
    ff=['ffmpeg','-v','error','-n','-f','rawvideo','-pix_fmt','bgr24','-s',f'{w}x{h}','-r',str(c['fps']),'-i','-',
        '-ss',str(c['startFrame']/c['fps']),'-i',source,'-t','1','-map','0:v:0','-map','1:a:0',
        '-vf','scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int',
        '-c:v','libx264','-crf','14','-preset','fast','-pix_fmt','yuv420p',
        '-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-color_range','tv',
        '-c:a','aac','-b:a','160k','-ar','48000','-ac','2','-movflags','+faststart',str(dest)]
    encoder=subprocess.Popen(ff,stdin=subprocess.PIPE);results=[];checks=[];skin_counts={}
    for offset,original in enumerate(frames):
        n=c['startFrame']+offset;result=original.copy()
        if n>=c['visibleStartFrame']:
            q=corners[n]
            keys=sorted(int(k) for k in c['visibilityOpacity'])
            opacity=np.interp(n,keys,[c['visibilityOpacity'][str(k)] for k in keys])
            result,skin_counts[str(n)]=composite_frame(original,shot,cap,q,c['supersampling'],opacity)
            if n>c['visibleStartFrame']:checks.append({'frame':n,**flow_check(frames[offset-1],original,corners[n-1],q)})
        else:assert np.array_equal(result,original)
        results.append(result);encoder.stdin.write(result.tobytes())
    encoder.stdin.close();assert encoder.wait()==0
    review=root/'scene-01-turn-dashboard-720p-r1.mp4'
    subprocess.run(['ffmpeg','-v','error','-n','-i',str(dest),'-vf','scale=1280:720:force_original_aspect_ratio=decrease:force_divisible_by=2,pad=1280:720:(ow-iw)/2:(oh-ih)/2:color=white',
                    '-c:v','libx264','-crf','14','-preset','fast','-pix_fmt','yuv420p','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-color_range','tv','-c:a','copy','-movflags','+faststart',str(review)],check=True)
    # Comparison has full context above paired enlarged phone views.
    comparison=root/'scene-01-turn-before-after-r1.mp4'
    args=['ffmpeg','-v','error','-n','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r',str(c['fps']),'-i','-',
          '-i',str(dest),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-crf','14','-preset','fast','-pix_fmt','yuv420p','-c:a','copy',
          '-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-color_range','tv','-vf','scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int','-movflags','+faststart',str(comparison)]
    proc=subprocess.Popen(args,stdin=subprocess.PIPE)
    for i,(a,b) in enumerate(zip(frames,results)):
        n=c['startFrame']+i;q=corners.get(n,corners[c['visibleStartFrame']]);cx,cy=q.mean(axis=0);x=int(np.clip(cx-160,0,w-320));y=int(np.clip(cy-90,0,h-180))
        top=np.hstack([cv2.resize(a,(640,360)),cv2.resize(b,(640,360))]);bottom=np.hstack([cv2.resize(a[y:y+180,x:x+320],(640,360)),cv2.resize(b[y:y+180,x:x+320],(640,360))])
        panel=np.vstack([top,bottom])
        for xx,label in [(12,'Original'),(652,'Dashboard POC')]:cv2.putText(panel,f'{label} / frame {n}',(xx,28),0,.7,(255,255,255),2)
        proc.stdin.write(panel.tobytes())
    proc.stdin.close();assert proc.wait()==0
    rows=[]
    for n in [420,425,426,427,428,430,436,443]:
        idx=n-c['startFrame'];q=corners.get(n,corners[c['visibleStartFrame']]);cx,cy=q.mean(axis=0);x=int(np.clip(cx-120,0,w-240));y=int(np.clip(cy-100,0,h-200));row=[]
        for label,im in [('Original',frames[idx]),('Dashboard',results[idx])]:
            a=cv2.resize(im[y:y+200,x:x+240],(480,400));tile=np.full((435,480,3),245,np.uint8);tile[:400]=a;cv2.putText(tile,f'{label} {n} / {n/c["fps"]:.3f}s',(10,427),0,.6,(20,20,20),1);row.append(tile)
        rows.append(np.hstack(row))
    cv2.imwrite(str(root/'scene-01-turn-contact-r1.jpg'),np.vstack(rows))
    for p,value in original_hashes.items():assert sha(p)==value,p
    for p in [dest,review,comparison]:subprocess.run(['ffmpeg','-v','error','-i',str(p),'-f','null','-'],check=True)
    report={'config':manifest,'sourceFrames':[c['startFrame'],c['endFrameExclusive']],'sourceSeconds':[c['startFrame']/c['fps'],c['endFrameExclusive']/c['fps']],
            'frames':len(frames),'fps':c['fps'],'videoSeconds':1,'nativeResolution':[w,h],'reviewResolution':[1280,720],
            'visibleStartFrame':c['visibleStartFrame'],'noAddedNotch':True,'supersampling':c['supersampling'],'geometry':c['geometryMethod'],
            'manualRotationFrames':c['manualRotationFrames'],'flowChecks':checks,'skinPixelsInsideDisplay':skin_counts,'inputSHA256':original_hashes,
            'sourceUnchanged':True,'backFacingFramesPixelIdenticalBeforeEncoding':True,'outsideMattePixelsIdenticalBeforeEncoding':True,
            'audio':'Original audio excerpt AAC-encoded at 48kHz for compatibility; original source untouched','fullDecode':'passed',
            'outputs':[str(dest),str(review),str(comparison)]}
    (root/'scene-01-turn-report-r1.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('manifest',nargs='?',default='manifests/v2-scene1-turn-poc-r1.json');run(p.parse_args().manifest)
