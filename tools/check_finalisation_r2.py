"""Independent checks on delivered BREP/STEP and sampled steering positions."""
from pathlib import Path
import json,math,time,sys
import cadquery as cq
import numpy as np
from study_finalisation_r2 import calculate,end,drag_end
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib

def optimal(self,tolerance=None):
    b=Bnd_Box();BRepBndLib.AddOptimal_s(self.wrapped,b,False,False);return cq.BoundBox(b)
cq.Shape.BoundingBox=optimal
BOUNDS={}
def bounds(s):
    key=id(s)
    if key not in BOUNDS:BOUNDS[key]=(s,s.BoundingBox())
    return BOUNDS[key][1]

ROOT=Path(__file__).resolve().parents[1];B=ROOT/'Composants/finalisation-theorique-r2';V=B/'verification';CACHE=ROOT/'tools/temp/finalisation-r2'
def dump(p,o):p.write_text(json.dumps(o,indent=2,ensure_ascii=False),encoding='utf-8')
def overlap(a,b):
    aa=bounds(a);bb=bounds(b)
    if any(getattr(aa,d+'max')<=getattr(bb,d+'min')+1e-7 or getattr(bb,d+'max')<=getattr(aa,d+'min')+1e-7 for d in 'xyz'):return 0.
    return a.intersect(b).Volume()
def main():
    sys.stdout.reconfigure(encoding='utf-8');t=time.time()
    data=json.loads((CACHE/'instances.json').read_text(encoding='utf-8'))
    shapes={x['name']:cq.importers.importBrep(str(CACHE/(x['name']+'.brep'))).val() for x in data}
    valid=[]
    for p in sorted((B/'3D').glob('*.step')):
        s=cq.importers.importStep(str(p)).val();ok=s.isValid() and all(sh.Closed() for sh in s.Shells())
        valid.append(dict(file=p.name,valid=ok,solids=len(s.Solids()),bytes=p.stat().st_size));assert ok,p
    print('STEP',len(valid),flush=True)
    # New mechanical parts must not interfere with one another. Normal joins
    # of ball/socket surrogate geometry and reserved electronics are excluded.
    rigid=[x['name'] for x in data if x['group'] in ['mecanique','carter','electricite'] and not x['name'].startswith(('Rotule','Biellette','Palonnier','Adaptateur'))]
    coll=[];pairs=0
    for i,n in enumerate(rigid):
        for m in rigid[i+1:]:
            vol=overlap(shapes[n],shapes[m]);pairs+=1
            if vol>.002:coll.append(dict(a=n,b=m,volume_mm3=vol))
    dump(V/'interferences-mecanique.json',dict(pairs=pairs,unexpected=coll,scope='Pièces mécaniques R2 seulement, assemblage nominal ; aucune qualification des références fournisseur'))
    print('STATIC',pairs,'collisions',len(coll),flush=True)
    for r in coll[:14]:print(r,flush=True)
    # Analytic reconstruction of the documented wheel envelope and its hub.
    # Retains the empty rim cavity and hex/socket depth assumptions of R1;
    # omits spokes/tread, so this is not a complete vendor-interface proof.
    def cyl(r,h,x):return cq.Solid.makeCylinder(r,h,cq.Vector(x,55,31.5),cq.Vector(1,0,0))
    rim=cyl(31.5,26,187).cut(cyl(21.9,26.2,186.9))
    hub=cyl(8.65,4.9,205).fuse(cyl(6.8,1.3,209.9)).cut(cyl(2,6.4,204.9))
    socket=cq.Workplane('YZ',origin=(205,55,31.5)).polygon(6,12/math.cos(math.pi/6)).extrude(3.5).val()
    wheel=rim.fuse(hub.cut(socket))
    rr=wheel.translate((0,390,0))
    wheel_checks=[]
    for n in rigid:
        if n.endswith('_G') or 'gauche' in n:continue
        for title,w in [('roue_AV_D',wheel),('roue_AR_D',rr)]:
            vol=overlap(shapes[n],w)
            if vol>.002:wheel_checks.append(dict(a=n,b=title,volume_mm3=vol))
    dump(V/'interfaces-roues.json',dict(unexpected=wheel_checks,source_wheel_offset_is_estimated=True,analytic_envelope_not_full_spokes_or_tread=True))
    print('WHEELS',len(wheel_checks),wheel_checks[:10],flush=True)
    from build_speed_mounts import station
    clip_swept=cq.Solid.makeCylinder(5.15,.6,cq.Vector(79.4,445,31.5),cq.Vector(1,0,0)).cut(cq.Solid.makeCylinder(2.4,.8,cq.Vector(79.3,445,31.5),cq.Vector(1,0,0)))
    hall_rows=[]
    for name,s,color in station():
        if name.startswith('Axe5'):continue
        if not name.startswith('P01'):s=s.translate((0,0,-3.5))
        s=s.translate((80,445,11));vol=overlap(clip_swept,s)
        hall_rows.append(dict(part=name,clip_full_revolution_overlap_mm3=vol));assert vol<.002,(name,'circlipHall',vol)
    dump(V/'retenue-hall.json',dict(full_circlip_envelope_diameter_mm=10.3,rotation360_checked_geometrically=True,rows=hall_rows,magnetic_detection_not_validated=True))
    battery=cq.Workplane('XY').box(46,139,25,centered=(True,True,False)).val().translate((0,270,13))
    cable_rows=[]
    for row in data:
        if row['group']!='cables' or row['name'] in ['P03','P04','P05','P06']:continue
        vol=overlap(shapes[row['name']],battery);cable_rows.append(dict(cable=row['name'],battery_overlap_mm3=vol))
        assert vol<.002,(row['name'],'cable through battery',vol)
    assert overlap(shapes['S01'],shapes['R213_support_UBEC'])<.002
    dump(V/'cables-batterie-support.json',dict(checks=cable_rows,S01_clear_of_support_R213=True,other_endpoints_and_high_corridors_unqualified=True))
    k=calculate();a=k['arm_inward_mm'];poses=[];dynamic=[]
    moving_names=['R208_D','R210_D','R220_D','MR115_AV_D_178','MR115_AV_D_190','Entretoise_AV_8_D','Entretoise_AV_8_5_D','Moyeu53569_nominal_AV_D','Goupille2x10_AV_D','EcrouRoueM4_nominal_AV_D']
    # A full cylinder is conservative for clearance to the fixed frame.
    from build_wheel_step import tire_blank
    rim_motion=cyl(23.5,24.8,187.6).cut(cyl(21.9,25,187.5))
    tyre=tire_blank().rotate((0,0,0),(0,1,0),90).translate((200,55,31.5)).fuse(rim_motion)
    moving=[shapes[n] for n in moving_names]+[tyre]
    fixed=[n for n in rigid if n not in moving_names and not n.endswith('_G') and not n.startswith(('R211','Bague6','C04','R201','R202','R203','R204','R205','R206','Entretoise_E','Collier5','MR115_AR'))]
    for deg in np.linspace(-25,25,51):
        if int(deg)%10==0:print('POSE',float(deg),flush=True)
        moved=[s.rotate((170,55,0),(170,55,1),float(deg)) for s in moving];total=0
        for n in fixed:
            for mi,s in enumerate(moved):
                vol=overlap(s,shapes[n]);total+=vol
                if vol>.002:dynamic.append(dict(angle_deg=float(deg),moving=moving_names[mi] if mi<len(moving_names) else 'pneu_sans_rainures',part=n,volume_mm3=vol))
        poses.append(dict(angle_deg=float(deg),overlap_mm3=total))
    dump(V/'balayage-direction.json',dict(samples=poses,unexpected=dynamic,continuous_sweep=False,angles_are_wheel_angles=True))
    print('SWEEP',len(dynamic),dynamic[:12],flush=True)
    # Close the four-bar equations at all tabulated poses, independently from
    # claimed maximum Ackermann error.
    residual=[]
    for row in k['rows']:
        l,r,p=map(math.radians,[row['left_deg'],row['right_deg'],row['servo_deg']])
        c=np.linalg.norm(end(1,r,a)-end(-1,l,a))-k['tierod_ball_centers_mm']
        d=np.linalg.norm(drag_end(l,a)-np.array([-20*math.sin(p),80+20*math.cos(p)]))-k['draglink_ball_centers_mm']
        residual.append(max(abs(c),abs(d)))
    assert max(residual)<1e-7
    result=dict(valid_step_files=valid,all_step_valid=True,kinematic_poses=len(residual),max_linkage_residual_mm=max(residual),static_unexpected=len(coll),wheel_interface_unexpected=len(wheel_checks),sweep_unexpected=len(dynamic),included_cables_clear_of_battery=True,all_selected_checks_passed=not(coll or wheel_checks or dynamic),seconds=time.time()-t,hardware_tested=False)
    dump(V/'synthese.json',result);print('DONE',result['all_selected_checks_passed'],flush=True)
if __name__=='__main__':main()
