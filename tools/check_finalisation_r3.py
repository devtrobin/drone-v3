"""Independent checks of exported nominal cable frame against the R2 scene."""
from pathlib import Path
import json,time,sys
import cadquery as cq
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'Composants/complements-finalisation-r3';T=ROOT/'tools/temp/finalisation-r3';V=B/'verification'
def optimal(self,tolerance=None):
    b=Bnd_Box();BRepBndLib.AddOptimal_s(self.wrapped,b,False,False);return cq.BoundBox(b)
cq.Shape.BoundingBox=optimal
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def dump(p,o):p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def main():
    t=time.time();rows=load(T/'scene.json');shapes={r['name']:cq.importers.importBrep(str(T/r['file'])).val() for r in rows};bounds={n:s.BoundingBox() for n,s in shapes.items()}
    new=[r['name'] for r in rows if r['group']!='base'];old=[r['name'] for r in rows if r['group']=='base'];coll=[];pairs=0;near=0
    def check(n,m):
        nonlocal pairs,near
        pairs+=1;a=bounds[n];b=bounds[m]
        if any(getattr(a,c+'max')<=getattr(b,c+'min')+1e-7 or getattr(b,c+'max')<=getattr(a,c+'min')+1e-7 for c in 'xyz'):return
        near+=1;v=shapes[n].intersect(shapes[m]).Volume()
        if v>.002:coll.append(dict(a=n,b=m,overlap_mm3=v))
    for i,n in enumerate(new):
        for m in old+new[i+1:]:check(n,m)
    valid=[]
    for p in sorted((B/'3D').glob('*.step')):
        s=cq.importers.importStep(str(p)).val();ok=s.isValid() and all(x.Closed() for x in s.Shells());valid.append(dict(file=p.name,valid=ok,solids=len(s.Solids())));assert ok,p
    # Recheck the new frame at the existing51 wheel-angle samples. The wheel
    # envelope is the documented R2 reconstruction, not measured vendor CAD.
    from build_wheel_step import tire_blank
    def xcyl(r,l,x):return cq.Solid.makeCylinder(r,l,cq.Vector(x,55,31.5),cq.Vector(1,0,0))
    rim=xcyl(23.5,24.8,187.6).cut(xcyl(21.9,25,187.5))
    tyre=tire_blank().rotate((0,0,0),(0,1,0),90).translate((200,55,31.5)).fuse(rim)
    moving_names=['R208_D','R210_D','R220_D','MR115_AV_D_178','MR115_AV_D_190','Entretoise_AV_8_D','Entretoise_AV_8_5_D','Moyeu53569_nominal_AV_D','Goupille2x10_AV_D','EcrouRoueM4_nominal_AV_D']
    sweeps=[]
    for angle in range(-25,26):
        for i,initial in enumerate([shapes[n] for n in moving_names]+[tyre]):
            moving=initial.rotate((170,55,0),(170,55,1),angle);bb=moving.BoundingBox()
            for n in new:
                b=bounds[n]
                if any(getattr(bb,c+'max')<=getattr(b,c+'min')+1e-7 or getattr(b,c+'max')<=getattr(bb,c+'min')+1e-7 for c in 'xyz'):continue
                v=moving.intersect(shapes[n]).Volume()
                if v>.002:sweeps.append(dict(angle_deg=angle,moving=moving_names[i] if i<len(moving_names) else 'tyre_R2',fixed=n,overlap_mm3=v))
    data=dict(pairs=pairs,exact_intersections=near,unexpected=coll,exported_STEP_files=valid,all_steps_valid=True,nominal_frame_and_cables_clear=not(coll or sweeps),old_vehicle_internal_overlaps_not_rechecked=True,nominal_endpoint_ports_not_actual_terminals=True,steering_samples=51,steering_unexpected=sweeps,steering_scope='New R3 objects versus right moving parts and reconstructed tyre; left nominal geometry is mirrored',hardware_tested=False,seconds=time.time()-t)
    dump(V/'geometrie.json',data);print(json.dumps({k:v for k,v in data.items() if k!='exported_STEP_files'},ensure_ascii=False),flush=True)
    if coll or sweeps:sys.exit(2)
if __name__=='__main__':sys.stdout.reconfigure(encoding='utf-8');main()
