"""Short, manifest-driven screen-compositing POC. OpenCV and NumPy required.
Manual inner-display anchors define geometry; LK/RANSAC independently checks
inter-frame drift. Outputs are exclusive: select a new stem for a new revision.
"""
import argparse, hashlib, json, subprocess
from pathlib import Path
import cv2
import numpy as np


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run(config):
    cfg = json.loads(Path(config).read_text())
    source, dashboard = cfg['source'], cfg['dashboard']
    hashes = {p: digest(p) for p in (source, dashboard)}
    first, end, fps = cfg['startFrame'], cfg['endFrameExclusive'], cfg['fps']
    assert 0 < end-first and (end-first <= fps*1.25 or cfg.get('fullSceneApproved')), 'Full-scene processing requires approval'
    visible = cfg.get('visibleStartFrame',first)
    track_start = cfg.get('trackingStartFrame',visible)
    reference = cfg.get('trackingReferenceFrame',visible)
    stem = Path(cfg['outputStem'])
    paths = {k: Path(str(stem)+suffix) for k,suffix in {
        'preview': '.mp4', 'comparison': '-comparison.mp4',
        'contact': '-contact.jpg', 'report': '-report.json'}.items()}
    assert not any(p.exists() for p in paths.values()), 'Choose an unused output stem'
    cap = cv2.VideoCapture(source)
    assert abs(cap.get(cv2.CAP_PROP_FPS)-fps) < .001
    cap.set(cv2.CAP_PROP_POS_FRAMES, first)
    originals = []
    for n in range(first, end):
        ok, frame = cap.read()
        assert ok, n
        originals.append(frame)
    cap.release()
    height, width = originals[0].shape[:2]
    shot = cv2.imread(dashboard)
    sh, sw = shot.shape[:2]
    source_quad = np.float32([[0,0],[sw-1,0],[sw-1,sh-1],[0,sh-1]])
    anchors = sorted((int(n),np.float32(q)) for n,q in cfg['anchors'].items())
    assert anchors[0][0] <= visible and anchors[-1][0] >= end-1
    # Dense automatic trajectory plus interpolated manual corrections. This
    # retains nonlinear rigid motion while meeting every reviewed anchor.
    gray_base = cv2.cvtColor(originals[reference-first],cv2.COLOR_BGR2GRAY)
    feature_mask = np.zeros_like(gray_base)
    cv2.fillConvexPoly(feature_mask,np.rint(dict(anchors)[reference]).astype(np.int32),255)
    feature_mask = cv2.erode(feature_mask,np.ones((9,9),np.uint8))
    pts = cv2.goodFeaturesToTrack(gray_base,120,.01,3,mask=feature_mask)
    auto = {}
    for offset,frame in enumerate(originals):
        if first+offset < track_start: continue
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        nxt,st,_ = cv2.calcOpticalFlowPyrLK(gray_base,gray,pts,None,winSize=(25,25),maxLevel=3)
        back,bs,_ = cv2.calcOpticalFlowPyrLK(gray,gray_base,nxt,None,winSize=(25,25),maxLevel=3)
        valid=(st[:,0]>0)&(bs[:,0]>0)&(np.linalg.norm(back-pts,axis=2)[:,0]<.5)
        motion,ins=cv2.findHomography(pts[valid],nxt[valid],cv2.RANSAC,.7)
        assert motion is not None and ins.sum()>=12, first+offset
        auto[first+offset] = cv2.perspectiveTransform(dict(anchors)[reference][None],motion)[0]
    tracked_anchors = [a for a in anchors if a[0] >= track_start]
    def corners(n):
        if n < track_start:
            return np.float32([[np.interp(n,[a[0] for a in anchors],[a[1][c,d] for a in anchors]) for d in range(2)] for c in range(4)])
        residual = np.float32([[np.interp(n,[a[0] for a in tracked_anchors],
                            [(a[1]-auto[a[0]])[c,d] for a in tracked_anchors])
                            for d in range(2)] for c in range(4)])
        return auto[n]+residual
    # Antialiased rounded display aperture, with a true hole for the notch.
    aperture = np.zeros((sh,sw),np.uint8)
    rx,ry = [round(a*b) for a,b in zip(cfg['roundedCornerRadiusNormalized'],(sw,sh))]
    cv2.rectangle(aperture,(rx,0),(sw-rx-1,sh-1),255,-1)
    cv2.rectangle(aperture,(0,ry),(sw-1,sh-ry-1),255,-1)
    for x in (rx,sw-rx-1):
        for y in (ry,sh-ry-1): cv2.ellipse(aperture,(x,y),(rx,ry),0,0,360,255,-1)
    notch = np.rint(np.array(cfg['notchPolygonNormalized'])*[sw-1,sh-1]).astype(np.int32)
    cv2.fillPoly(aperture,[notch],0)
    ff = ['ffmpeg','-v','error','-n','-f','rawvideo','-pix_fmt','bgr24',
          '-s',f'{width}x{height}','-r',str(fps),'-i','-',
          '-ss',str(first/fps),'-i',source,'-t',str((end-first)/fps),
          '-map','0:v','-map','1:a:0','-c:v','libx264','-crf','16',
          '-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k',
          '-ar','44100','-movflags','+faststart',str(paths['preview'])]
    if cfg.get('copyAudio'):
        k=ff.index('-c:a'); ff[k:k+2]=['-c:a','copy']
        k=ff.index('-b:a'); del ff[k:k+2]
        k=ff.index('-ar'); del ff[k:k+2]
    encoder = subprocess.Popen(ff,stdin=subprocess.PIPE)
    results=[]; diagnostics=[]
    for offset,frame in enumerate(originals):
        n=first+offset
        if n < visible:
            results.append(frame)
            encoder.stdin.write(frame.tobytes())
            continue
        q=corners(n)
        H=cv2.getPerspectiveTransform(source_quad,q)
        warped=cv2.warpPerspective(shot,H,(width,height),flags=cv2.INTER_AREA)
        alpha=cv2.warpPerspective(aperture,H,(width,height),flags=cv2.INTER_LINEAR)/255.
        opacity=cfg.get('visibilityOpacity')
        if opacity:
            keys=sorted(int(k) for k in opacity)
            alpha*=np.interp(n,keys,[opacity[str(k)] for k in keys])
        # Preserve the original blurred fingertips: colour-based holdout,
        # conservatively dilated 1px; never synthesize or sharpen the fingers.
        hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        skin=cv2.inRange(hsv,np.array([0,48,65]),np.array([27,255,255]))
        skin=cv2.dilate(skin,np.ones((3,3),np.uint8))
        skin=cv2.GaussianBlur(skin,(3,3),.4)/255.
        alpha *= 1-skin
        # Erode slightly before feathering to prevent a halo onto the bezel.
        alpha=cv2.erode(alpha.astype(np.float32),np.ones((2,2),np.uint8))
        alpha=cv2.GaussianBlur(alpha,(3,3),cfg['featherPixels'])
        result=np.rint(warped*alpha[:,:,None]+frame*(1-alpha[:,:,None])).astype(np.uint8)
        assert np.array_equal(result[alpha==0],frame[alpha==0])
        results.append(result)
        encoder.stdin.write(result.tobytes())
        if offset and n > track_start:
            prev=originals[offset-1]; gray0=cv2.cvtColor(prev,cv2.COLOR_BGR2GRAY)
            gray1=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            mask=np.zeros_like(gray0); cv2.fillConvexPoly(mask,np.rint(corners(n-1)).astype(np.int32),255)
            mask=cv2.erode(mask,np.ones((9,9),np.uint8))
            pts=cv2.goodFeaturesToTrack(gray0,100,.01,3,mask=mask)
            nxt,st,_=cv2.calcOpticalFlowPyrLK(gray0,gray1,pts,None,winSize=(21,21),maxLevel=3)
            back,bs,_=cv2.calcOpticalFlowPyrLK(gray1,gray0,nxt,None,winSize=(21,21),maxLevel=3)
            valid=(st[:,0]>0)&(bs[:,0]>0)&(np.linalg.norm(back-pts,axis=2)[:,0]<.5)
            motion,ins=cv2.findHomography(pts[valid],nxt[valid],cv2.RANSAC,.6)
            assert motion is not None and ins.sum()>=8, n
            predicted=cv2.perspectiveTransform(corners(n-1)[None],motion)[0]
            diagnostics.append({'frame':n,'inliers':int(ins.sum()),'maxCornerMotionResidualPixels':float(np.linalg.norm(predicted-q,axis=1).max())})
    encoder.stdin.close(); assert encoder.wait()==0
    # Four paired phone closeups plus wide context, without modifying sources.
    rows=[]
    for n in cfg.get('contactFrames',[first,first+6,first+12,first+23]):
        offset=n-first
        a=originals[offset]; b=results[offset]
        center=corners(max(n,visible)).mean(axis=0); x=int(center[0]-100); y=int(center[1]-125)
        views=[cv2.resize(f[y:y+250,x:x+200],(400,500)) for f in (a,b)]
        for v,label in zip(views,('Original','Dashboard')):
            cv2.putText(v,f'{label} frame {n}',(8,28),cv2.FONT_HERSHEY_SIMPLEX,.6,(0,0,255),1)
        wide=cv2.resize(b,(888,500))
        rows.append(np.hstack([*views,wide]))
    cv2.imwrite(str(paths['contact']),np.vstack(rows))
    filters="[0:v]trim=start_frame=%d:end_frame=%d,setpts=PTS-STARTPTS,scale=958:540,pad=960:540,drawtext=text='ORIGINAL':x=15:y=15:fontsize=24:fontcolor=white:box=1:boxcolor=black[a];[1:v]scale=958:540,pad=960:540,drawtext=text='TRACKED DASHBOARD':x=15:y=15:fontsize=24:fontcolor=white:box=1:boxcolor=black[b];[a][b]hstack[v]"%(first,end)
    subprocess.run(['ffmpeg','-v','error','-n','-i',source,'-i',str(paths['preview']),'-filter_complex',filters,'-map','[v]','-map','1:a:0','-c:v','libx264','-crf','18','-c:a','copy','-movflags','+faststart',str(paths['comparison'])],check=True)
    for p in hashes: assert digest(p)==hashes[p]
    report={'config':config,'inputHashes':hashes,'frames':[first,end],'durationSeconds':(end-first)/fps,'resolution':[width,height],'fps':fps,'tracking':'Manual reviewed inner-display anchors; LK/RANSAC rigid-screen trajectory with interpolated manual corner corrections at reviewed anchors; per-frame manual corners during edge-on rotation; independent inter-frame flow checks','mask':'Rounded display aperture, manual notch hole, original-frame skin holdout, 0.35px feather','resolvedCorners':{str(n):corners(n).tolist() for n in range(visible,end)},'visibleStartFrame':visible,'manualOnlyFrames':[visible,track_start-1],'trackingDiagnostics':diagnostics,'maxMotionResidualPixels':max(d['maxCornerMotionResidualPixels'] for d in diagnostics),'outputs':{k:str(v) for k,v in paths.items()}}
    paths['report'].write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('manifest');args=parser.parse_args();run(args.manifest)
