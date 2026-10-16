from build_harness_step import *
def check(name,s):print(name,s.isValid(),len(s.Solids()),round(s.Volume(),3),flush=True);return s
def main():
    l=19;c1=6;c2=6;bs=l-9;t=2
    palm=check('palm',box(c1+c2,9.5,t,((c2-c1)/2,0,0),.55))
    wp=cq.Workplane(cq.Plane(origin=(c2,0,1),xDir=(0,1,0),normal=(1,0,0))).rect(9.5,2)
    transition=check('loft',wp.workplane(offset=bs-c2).center(0,2).circle(3).loft(combine=False).val())
    s=check('fusepalm',palm.fuse(transition));s=check('fusebarrel',s.fuse(cyl(3,9,3,bs,axis=(1,0,0))).clean())
    s=check('holepalm',s.cut(cyl(5.3/2,2.2,-.1)))
    s=check('bore',s.cut(cyl(2,l-bs+1.31,3,bs-1.3,axis=(1,0,0))))
    s=check('inspection',s.cut(cyl(.7,3,3,bs-.3)).clean())
    cone=cq.Solid.makeCone(2,2.2,.35,cq.Vector(l-.35,0,3),cq.Vector(1,0,0))
    check('chamfer',s.cut(cone).clean())
if __name__=='__main__':main()
