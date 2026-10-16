from build_gpio_step import *
sys.stdout.reconfigure(encoding='utf-8');cq.Shape.BoundingBox=optimal
h=housing();g,t=terminal();x,y=pos(1)
for label,s in [('gold',g),('tin',t)]:
 common=h.intersect(s.translate((x,y,0)))
 if common.Volume()<1e-9:print(label,'V',0,flush=True);continue
 b=common.BoundingBox()
 print(label,'V',common.Volume(),'BBOX',b.xmin-x,b.xmax-x,b.ymin-y,b.ymax-y,b.zmin,b.zmax,flush=True)
