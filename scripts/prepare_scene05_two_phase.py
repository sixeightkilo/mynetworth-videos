"""Prepare separate background and original-finger layers for Scene 05 v5.
No source is changed. The local phone removal is conventional OpenCV inpainting;
the removed area is covered by the reconstructed geometric phone. Fingers are
copied from the original plate, never synthesized or sharpened.
"""
from pathlib import Path
import argparse,json,cv2,numpy as np
parser=argparse.ArgumentParser()
parser.add_argument('manifest',nargs='?',default='manifests/scene05-two-phase-v5.json')
args=parser.parse_args()
cfg=json.loads(Path(args.manifest).read_text())
root=Path('production')
outputs=[root/cfg['backgroundImage'],root/cfg['fingerImage']]
for p in outputs:assert not p.exists(),f'Output exists: {p}'
plate=cv2.imread(str(root/cfg['startImage']));assert plate is not None
height,width=plate.shape[:2]
q=np.float32(cfg['screenQuad']);w,h=cfg['dashboardSize'];b=cfg['model']['bezel']
H=cv2.getPerspectiveTransform(np.float32([[0,0],[w,0],[w,h],[0,h]]),q)
outer=cv2.perspectiveTransform(np.float32([[[-b-30,-b-30],[w+b+30,-b-30],[w+b+30,h+b+30],[-b-30,h+b+30]]]),H)[0]
erase=np.zeros((height,width),np.uint8);cv2.fillConvexPoly(erase,np.rint(outer).astype(np.int32),255)
erase=cv2.dilate(erase,np.ones((3,3),np.uint8))
# Manual occlusion domains keep warm wall/dashboard colours out of the matte.
polygons=cfg['foregroundPolygons']
hsv=cv2.cvtColor(plate,cv2.COLOR_BGR2HSV).astype(np.float32);hue,sat,val=cv2.split(hsv)
raw=np.clip((30-hue)/6,0,1)*np.clip((sat-35)/25,0,1)*np.clip((val-105)/40,0,1)
skin=np.zeros((height,width),np.float32)
# Fill fingernail holes within actual warm-finger contours, without copying
# dark phone-edge pixels into the matte. RGB always comes from the original.
for poly in polygons[:-1]:
 domain=np.zeros((height,width),np.uint8);cv2.fillPoly(domain,[np.int32(poly)],255)
 seed=((raw>.3)&(domain>0)).astype(np.uint8)*255
 contours,_=cv2.findContours(seed,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
 if contours:
  shape=np.zeros_like(seed);cv2.drawContours(shape,[max(contours,key=cv2.contourArea)],-1,255,-1)
  skin=np.maximum(skin,cv2.GaussianBlur(shape.astype(np.float32)/255,(3,3),.55))
hand=np.zeros((height,width),np.uint8);cv2.fillPoly(hand,[np.int32(polygons[-1])],255)
hand[:501]=0
skin=np.maximum(skin,raw*hand/255.)
skin*=np.clip((val-115)/45,0,1)
core=cv2.perspectiveTransform(np.float32([[[w*.20,h*.05],[w*.87,h*.05],[w*.87,h*.95],[w*.20,h*.95]]]),H)[0]
interior=np.zeros_like(erase);cv2.fillConvexPoly(interior,np.rint(core).astype(np.int32),255)
skin*=1-interior/255.
# Reject original bezel RGB around the analytically measured phone perimeter.
# Only unmistakable skin/highlights survive in this band; no black raster rim.
ring=np.zeros_like(erase)
cv2.fillConvexPoly(ring,np.rint(outer).astype(np.int32),255)
inside=cv2.perspectiveTransform(np.float32([[[12,12],[w-12,12],[w-12,h-12],[12,h-12]]]),H)[0]
cv2.fillConvexPoly(ring,np.rint(inside).astype(np.int32),0)
strong=np.clip((val-175)/25,0,1)*np.clip((sat-75)/25,0,1)
highlight=np.clip((val-215)/20,0,1)
keep=np.maximum(strong,highlight)
skin*=np.where(ring>0,keep,1)
erase=cv2.dilate(erase,np.ones((5,5),np.uint8))
background=cv2.inpaint(plate,erase,5,cv2.INPAINT_TELEA)
foreground=np.dstack([plate,np.rint(skin*255).astype(np.uint8)])
for p,image in zip(outputs,[background,foreground]):
 p.parent.mkdir(parents=True,exist_ok=True)
 assert cv2.imwrite(str(p),image),p
print('Prepared derived background and original-finger layers without modifying the manifest or source.')
