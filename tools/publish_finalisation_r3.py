"""Flat drill/cut templates, independent DXF comparison and mechanical screening."""
from pathlib import Path
import json,hashlib,csv,sys,time
import cadquery as cq
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'Composants/complements-finalisation-r3';P=B/'plans';V=B/'verification'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def dump(p,o):p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run():
    routes=load(B/'parcours.json')
    import math
    for r in routes:r['reserve_raccordement_mm']=300;r['brut_approvisionnement_mm']=math.ceil((r['longueur_axe_mm']+300)/10)*10
    dump(B/'parcours.json',routes)
    with (B/'longueurs-cables.csv').open('w',encoding='utf-8-sig',newline='') as f:
        flat=[{k:v for k,v in r.items() if k!='points_mm'} for r in routes];w=csv.DictWriter(f,fieldnames=list(flat[0]),delimiter=';');w.writeheader();w.writerows(flat)
    bolt_rows=list(csv.DictReader((B/'visserie-r3.csv').open(encoding='utf-8-sig'),delimiter=';'))
    grouped={}
    for r in bolt_rows:
        if r['reference'].startswith('M3') and float(r['ecrou_mm']):r['ecrou_mm']='4'
        grip=float(r['empilage_mm']);wash=float(r['rondelles_mm']);nut=float(r['ecrou_mm']);eng=float(r['engagement_mm'])
        r['longueur_min_mm']=round(grip+wash+(nut+1 if nut else eng),2)
        assert float(r['longueur_retenue_mm'])>=r['longueur_min_mm'],r
        key=(r['reference'],r['longueur_retenue_mm']);grouped[key]=grouped.get(key,0)+int(r['quantite'])
    with (B/'visserie-r3.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(bolt_rows[0]),delimiter=';');w.writeheader();w.writerows(bolt_rows)
    procurement=[dict(reference=ref+'x'+l,quantite=q) for (ref,l),q in sorted(grouped.items())]
    procurement.extend([dict(reference='Ecrou autofreiné M3 DIN985 hauteur4mm maximum',quantite=48),dict(reference='Ecrou autofreiné M4 DIN985 hauteur5mm maximum',quantite=8),dict(reference='RondelleM3 epaisseur0.5',quantite=96),dict(reference='RondelleM4 epaisseur0.8',quantite=20)])
    with (B/'approvisionnement-visserie-r3.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['reference','quantite'],delimiter=';');w.writeheader();w.writerows(procurement)
    rows=load(B/'pieces.json');checks=[]
    for r in rows:
        n=r['code']
        if not n.startswith(('R303_','R304_','R305_','R306_')):continue
        s=cq.importers.importStep(str(B/'3D'/(n+'.step'))).val()
        top=cq.Workplane('XY').newObject([s]).faces('>Z');face=top.val();bb=face.BoundingBox()
        flat=top.translate((-bb.xmin,-bb.ymin,-bb.zmax));out=P/(n+'.dxf');cq.exporters.export(flat,str(out),exportType='DXF')
        back=cq.importers.importDXF(str(out)).extrude(.5).val()
        f=flat.val();ref=cq.Solid.extrudeLinear(f.outerWire(),f.innerWires(),cq.Vector(0,0,.5))
        diff=ref.cut(back).Volume()+back.cut(ref).Volume();assert diff<.001,(n,diff)
        checks.append(dict(piece=n,local_origin_global_mm=[bb.xmin,bb.ymin,bb.zmax],unit='mm',top_face_template=True,profile_round_trip_difference_mm3=diff,STEP_sha256=sha(B/'3D'/(n+'.step')),DXF_sha256=sha(out),usage='Débit plat3' if n.startswith(('R305','R306')) else 'Perçages sur tube déjà débité; contour de référence uniquement'))
    dump(V/'dxf.json',checks)
    for old in P.glob('*.dxf'):
        if old.stem not in {r['piece'] for r in checks}:
            dest=ROOT/'tools/temp/finalisation-r3/iterations';dest.mkdir(exist_ok=True)
            assert old.resolve().is_relative_to(ROOT) and dest.resolve().is_relative_to(ROOT)
            old.rename(dest/(str(time.time_ns())+'-'+old.name))
    # Conservative screening for cable supports, not crash/hand-rest loads.
    E=69000;Ipost=(30*10**3-27*7**3)/12;Lpost=122;Fpost=10
    Ibeam=(30*10**3-28*8**3)/12;Lbeam=272;Fbeam=10
    custom=[r for r in rows if r['group'] not in ['cable','liner'] and not r['code'].startswith('L01_')]
    mass=sum(r['estimated_mass_g'] for r in custom)
    routes=load(B/'parcours.json');cablemass=sum(r['longueur_axe_mm']/1000*(6*8.96+(3.141592654*3.25**2-6)*1.1) for r in routes)
    data=dict(load_envelope_total_N=20,required_aluminium_yield_MPa=200,post_stress_MPa=Fpost*Lpost*5/Ipost,post_deflection_mm=Fpost*Lpost**3/(3*E*Ipost),crossbar_stress_MPa=Fbeam*Lbeam*5/(4*Ibeam),crossbar_deflection_mm=Fbeam*Lbeam**3/(48*E*Ibeam),offset_console_load_N=10,offset_console_stress_MPa=10*95*1.5/(20*3**3/12),offset_console_deflection_mm=10*95**3/(3*E*(20*3**3/12)),new_custom_parts_estimated_g=mass,four_cables_estimated_g=cablemass,fasteners_and_tails_mass_not_included=True,not_impact_or_hand_support_rated=True,full_frame_FEA=False,vehicle_mass_must_stay_under_9kg=True)
    dump(V/'dimensionnement-supports.json',data)
    print('DXF',len(checks),'fixed hardware mass g',round(mass,1),'cables',round(cablemass,1),flush=True)
if __name__=='__main__':sys.stdout.reconfigure(encoding='utf-8');run()
