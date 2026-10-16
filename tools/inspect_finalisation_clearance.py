from pathlib import Path
import cadquery as cq
from build_wheel_step import tire_blank
from check_finalisation_r2 import bounds
ROOT=Path(__file__).resolve().parents[1];C=ROOT/'tools/temp/finalisation-r2'
f=cq.importers.importBrep(str(C/'R209_D.brep')).val()
rim=cq.Solid.makeCylinder(31.5,26,cq.Vector(187,55,31.5),cq.Vector(1,0,0)).cut(cq.Solid.makeCylinder(21.9,26.2,cq.Vector(186.9,55,31.5),cq.Vector(1,0,0)))
t=tire_blank().rotate((0,0,0),(0,1,0),90).translate((200,55,31.5))
for deg in [-25,25]:
    for n,sh in [('tire_blank',t),('rim_proxy',rim)]:
        inter=sh.rotate((170,55,0),(170,55,1),deg).intersect(f)
        if inter.Volume()>.001:
            bb=bounds(inter)
            print(deg,n,inter.Volume(),[(a,getattr(bb,a+'min'),getattr(bb,a+'max')) for a in 'xyz'],inter.Center().toTuple(),flush=True)
