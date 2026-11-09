"""Composite a real dashboard into a user-supplied alpha mask, still only.
OpenCV/NumPy; no reference or mask resizing, cropping, moving, or overwriting.
"""
import argparse,hashlib,json
from pathlib import Path
import cv2
import numpy as np

def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def corners_from_alpha(alpha):
    contours,_=cv2.findContours((alpha>127).astype(np.uint8)*255,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    contour=max(contours,key=cv2.contourArea)
    approx=cv2.approxPolyDP(contour,.02*cv2.arcLength(contour,True),True).reshape(-1,2).astype(float)
    assert len(approx)==4,'Mask must have four dominant sides'
    center=approx.mean(axis=0)
    approx=approx[np.argsort(np.arctan2(approx[:,1]-center[1],approx[:,0]-center[0]))]
    approx=np.roll(approx,-np.argmin(approx.sum(axis=1)),axis=0)
    points=contour.reshape(-1,2).astype(float);lines=[]
    for i in range(4):
        a,b=approx[i],approx[(i+1)%4];v=b-a
        t=((points-a)@v)/(v@v)
        delta=points-a
        distance=np.abs(v[0]*delta[:,1]-v[1]*delta[:,0])/np.linalg.norm(v)
        selected=points[(t>.2)&(t<.8)&(distance<3)]
        assert len(selected)>=4
        vx,vy,x,y=cv2.fitLine(selected.astype(np.float32),cv2.DIST_HUBER,0,.01,.01).flatten()
        normal=np.array([-vy,vx],float);lines.append((normal,float(normal@[x,y])))
    # Intersect the straight sides rather than mapping to rounded corner pixels.
    return np.array([np.linalg.solve(np.stack([lines[(i-1)%4][0],lines[i][0]]),
                     [lines[(i-1)%4][1],lines[i][1]]) for i in range(4)],np.float32)

def main():
    p=argparse.ArgumentParser();p.add_argument('reference');p.add_argument('mask');p.add_argument('dashboard');p.add_argument('output');a=p.parse_args()
    output=Path(a.output);assert not output.exists(),output
    original=cv2.imread(a.reference,cv2.IMREAD_UNCHANGED);mask=cv2.imread(a.mask,cv2.IMREAD_UNCHANGED);dashboard=cv2.imread(a.dashboard,cv2.IMREAD_COLOR)
    assert original is not None and mask is not None and dashboard is not None
    assert original.shape[:2]==mask.shape[:2], 'Reference and mask dimensions must match exactly'
    assert mask.ndim==3 and mask.shape[2]==4,'Mask needs alpha'
    assert original.ndim==3 and original.shape[2] in (3,4)
    alpha=mask[:,:,3];corners=corners_from_alpha(alpha)
    sh,sw=dashboard.shape[:2];h,w=alpha.shape
    source=np.float32([[0,0],[sw-1,0],[sw-1,sh-1],[0,sh-1]])
    transform=cv2.getPerspectiveTransform(source,corners)
    # Supersample only the generated dashboard layer. Both supplied inputs stay native.
    scale=4;sampling=np.diag([scale,scale,1.])
    layer=cv2.warpPerspective(dashboard,sampling@transform,(w*scale,h*scale),
                              flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)
    layer=cv2.resize(layer,(w,h),interpolation=cv2.INTER_AREA)
    weight=alpha.astype(np.float32)[:,:,None]/255
    result=original.copy();result[:,:,:3]=np.rint(layer*weight+original[:,:,:3]*(1-weight)).astype(np.uint8)
    assert np.array_equal(result[alpha==0],original[alpha==0]),'Outside-mask pixels changed'
    if original.shape[2]==4:assert np.array_equal(result[:,:,3],original[:,:,3])
    before={p:digest(p) for p in [a.reference,a.mask,a.dashboard]}
    output.parent.mkdir(parents=True,exist_ok=True);assert cv2.imwrite(str(output),result)
    for p,value in before.items():assert digest(p)==value
    report={'reference':a.reference,'mask':a.mask,'dashboard':a.dashboard,'output':str(output),
            'resolution':[w,h],'cornersOrder':'top-left, top-right, bottom-right, bottom-left',
            'corners':corners.tolist(),'perspectiveTransform':transform.tolist(),
            'alphaUsedWithoutResizing':True,'referenceUsedWithoutResizingCroppingOrMoving':True,
            'outsideMaskPixelsIdentical':True,'originalAlphaPreserved':original.shape[2]==4,
            'dashboardLayerSupersampling':scale,'addedNotchOrBezel':False,'videoProcessed':False,
            'inputSHA256':before}
    output.with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
