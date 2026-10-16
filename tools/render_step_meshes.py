"""Depth-buffer renderer for tessellated CAD, with optional Numba acceleration."""
import math
import numpy as np
from PIL import Image,ImageDraw,ImageFont
try:
    from numba import njit
except ImportError:
    def njit(**kwargs):return lambda function:function

@njit(cache=True)
def raster(world,screen,triangles,colour,light,rgb,depth):
    height,width=depth.shape
    for ti in range(len(triangles)):
        ia,ib,ic=triangles[ti]
        ax,ay,az=screen[ia];bx,by,bz=screen[ib];cx,cy,cz=screen[ic]
        denominator=(by-cy)*(ax-cx)+(cx-bx)*(ay-cy)
        if abs(denominator)<1e-8:continue
        x0=max(0,int(math.floor(min(ax,bx,cx))));x1=min(width-1,int(math.ceil(max(ax,bx,cx))))
        y0=max(70,int(math.floor(min(ay,by,cy))));y1=min(height-60,int(math.ceil(max(ay,by,cy))))
        if x1<x0 or y1<y0:continue
        u0=world[ib,0]-world[ia,0];u1=world[ib,1]-world[ia,1];u2=world[ib,2]-world[ia,2]
        v0=world[ic,0]-world[ia,0];v1=world[ic,1]-world[ia,1];v2=world[ic,2]-world[ia,2]
        nx=u1*v2-u2*v1;ny=u2*v0-u0*v2;nz=u0*v1-u1*v0
        norm=math.sqrt(nx*nx+ny*ny+nz*nz)
        shade=.68+.32*abs((nx*light[0]+ny*light[1]+nz*light[2])/norm) if norm else 1.
        red=min(255.,max(0.,colour[0]*shade*255));green=min(255.,max(0.,colour[1]*shade*255));blue=min(255.,max(0.,colour[2]*shade*255))
        for y in range(y0,y1+1):
            for x in range(x0,x1+1):
                xx=x+.5;yy=y+.5
                u=((by-cy)*(xx-cx)+(cx-bx)*(yy-cy))/denominator
                v=((cy-ay)*(xx-cx)+(ax-cx)*(yy-cy))/denominator
                w=1.-u-v
                if u < -1e-7 or v < -1e-7 or w < -1e-7:continue
                z=u*az+v*bz+w*cz
                if z>depth[y,x]:
                    depth[y,x]=z
                    rgb[y,x,0]=int(red);rgb[y,x,1]=int(green);rgb[y,x,2]=int(blue)

def render_meshes(path,meshes,view,title,footer='CAO officielle Raspberry Pi Ltd - geometrie et couleurs conservees'):
    width,height=1600,1300
    view=np.array(view,dtype=float);view/=np.linalg.norm(view)
    right=np.cross([0,1,0] if abs(view[2])>.99 else [0,0,1],view);right/=np.linalg.norm(right)
    up=np.cross(view,right);basis=np.array([right,-up,view]).T
    projected=[world@basis for world,triangles,colour in meshes]
    lo=np.vstack([p[:,:2].min(axis=0) for p in projected]).min(axis=0)
    hi=np.vstack([p[:,:2].max(axis=0) for p in projected]).max(axis=0)
    scale=min((width-140)/(hi[0]-lo[0]),(height-200)/(hi[1]-lo[1]));mid=(lo+hi)/2
    rgb=np.full((height,width,3),241,dtype=np.uint8);depth=np.full((height,width),-np.inf)
    light=view+np.array([-.35,.15,.35]);light/=np.linalg.norm(light)
    for (world,triangles,colour),p in zip(meshes,projected):
        screen=p.copy();screen[:,:2]=(screen[:,:2]-mid)*scale+[width/2,height/2+10]
        raster(np.ascontiguousarray(world),screen,np.asarray(triangles,dtype=np.int64),np.asarray(colour),light,rgb,depth)
    im=Image.fromarray(rgb);draw=ImageDraw.Draw(im)
    draw.text((width/2,20),title,font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',32),anchor='mt',fill='#182128')
    draw.text((width/2,height-30),footer,font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',21),anchor='mm',fill='#52616b')
    im.save(path)
