"""Coloured STEP carrier from checked KiCad routing, plus honest module reserves.

Solder/pad outlines follow the PCB. Package bodies are nominal reconstructions;
unavailable EVM dimensions are open reservation frames, never fake vendor CAD.
"""
from pathlib import Path
import hashlib,json,math,sys
import cadquery as cq
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from build_running_gear_step import box,cyl,export_model

ROOT=Path(__file__).resolve().parents[1];B=ROOT/'Composants/carte-surveillance-electrique';OUT=B/'3D'
GREEN=(.012,.12,.045);TRACK=(.018,.16,.060);TIN=(.58,.61,.64);BLACK=(.013,.015,.018);WHITE=(.82,.83,.79)
def optimal(self,tolerance=None):
    b=Bnd_Box();BRepBndLib.AddOptimal_s(self.wrapped,b,False,False);return cq.BoundBox(b)
cq.Shape.BoundingBox=optimal
def point(x,y):return x,75-y
def mark(parts,text,x,y,z,size=1.3,color=WHITE):
    s=cq.Workplane('XY').text(text,size,.012,font='Arial',combine=False).val().translate((x,y,z))
    parts.append(('Marquage_'+str(len(parts)),s,color))
def save(name,title,parts,notes,params):
    m=export_model(dict(folder='carte-surveillance-electrique',filename=name,title=title,parts=parts,
        published=notes,estimated=['Study reconstruction, not native vendor CAD; no measured hardware.',
          'Package colours, component markings, solder fillets and micro-details estimated.',
          'EVM and Pololu reserves are open frames, not their true geometry. Harnesses and mounting hardware not defined.'],
        params=params,view=(.6,-1,1.15),design=True,probes=[],source_pages=['KiCad/implantation.json; notices/TI-TPS3700EVM-114-original.pdf; notices/Traco-TMR1-original.pdf']))
    m.update(generated_on='2026-10-15',coordinate_system='Carrier: X0..140,Y0..75; finished copper facesZ0..1.6; substrateZ0.07..1.53 at70um nominal copper. KiCad Y mirrored into CAD Y.',
        CAD_status='Prototype exact board outline and checked routing; nominal package reconstructions and explicit reserved modules.',
        kicad_pcb_sha256=hashlib.sha256((B/'KiCad/surveillance-2s-m1.kicad_pcb').read_bytes()).hexdigest())
    (OUT/Path(name).with_suffix('.json')).write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
    return m

def carrier(d):
    thickness=d['routing'].get('copper_nominal_um',35)/1000
    holes={(4,4,1.6),(136,4,1.6),(4,71,1.6),(136,71,1.6)}
    holes|={(p['x'],p['y'],p['hole']/2+.02) for p in d['pads'] if p['hole']>0}
    holes|={(x,y,d['routing']['via_drill']/2+.02) for _,x,y in d['routing']['vias']}
    board=box(140,75,1.6-2*thickness,(70,37.5,thickness))
    for x,y,r in holes:
        xx,yy=point(x,y);board=board.cut(cyl(r,1.8,-.1,xx,yy))
    parts=[('PCB_substrat_FR4_pour_epaisseur_finie1_6',board.clean(),GREEN)]
    # Rectangular segment projection, fused by net/layer. Top/bottom physical
    # copper thickness 35um is a design assumption, not a fabricated measurement.
    groups={}
    for n,a,b in d['routing']['segments']:
        x1,y1=point(a[0],a[1]);x2,y2=point(b[0],b[1]);length=math.hypot(x2-x1,y2-y1)
        if length<1e-6:continue
        z=1.6-thickness if a[2]==0 else 0
        width=d['routing'].get('width_by_net',{}).get(n,d['routing']['width'])
        s=box(length+.005,width,thickness).rotate((0,0,0),(0,0,1),math.degrees(math.atan2(y2-y1,x2-x1))).translate(((x1+x2)/2,(y1+y2)/2,z))
        groups.setdefault((n,a[2]),[]).append(s)
    for (n,l),ss in groups.items():
        # Fuse all intersections of one net so the STEP has real contiguous copper.
        s=ss[0].fuse(*ss[1:]).clean() if len(ss)>1 else ss[0]
        parts.append((f'Pistes_{n}_{l}',s,TRACK))
    for i,p in enumerate(d['pads']):
        for j,poly in enumerate(p['polygons']):
            x,y=point(p['x'],p['y']);shape=p.get('shape',6);sx,sy=p.get('size_local_mm',[p['sx'],p['sy']])
            if shape==0:s=cyl(sx/2,thickness,0,x,y)
            elif shape in [1,2,4]:
                wp=cq.Workplane('XY').box(sx,sy,thickness,centered=(True,True,False))
                r=p.get('corner_radius_mm',0) if shape==4 else (min(sx,sy)/2-.00001 if shape==2 else 0)
                if r>0:wp=wp.edges('|Z').fillet(r)
                s=wp.val().rotate((0,0,0),(0,0,1),-p.get('angle',0)).translate((x,y,0))
            else:
                pts=[point(x,y) for x,y in poly];s=cq.Workplane('XY').polyline(pts).close().extrude(thickness).val()
            if p['hole']:
                x,y=point(p['x'],p['y']);s=s.cut(cyl(p['hole']/2,thickness+.02,-.01,x,y))
            parts.append((f'Plage_{p["ref"]}_{p["num"]}_{j}',s.translate((0,0,1.6-thickness)),TIN))
            if p['tht']:parts.append((f'Pastille_dessous_{i}_{j}',s,TIN))
        if p['tht']:
            x,y=point(p['x'],p['y']);r=p['hole']/2
            barrel=cyl(r+.02,1.6,0,x,y).cut(cyl(r,1.62,-.01,x,y))
            parts.append((f'Fut_metallise_{i}',barrel,TIN))
    for i,(n,x,y) in enumerate(d['routing']['vias']):
        x,y=point(x,y);r=d['routing']['via_diameter']/2;h=d['routing']['via_drill']/2
        s=cyl(h+.02,1.6,0,x,y).cut(cyl(h,1.62,-.01,x,y))
        parts.append((f'Via_{i}_{n}_paroi20um',s,TIN))
        for side,z in [('dessus',1.6-thickness),('dessous',0)]:
            s=cyl(r,thickness,z,x,y).cut(cyl(h,thickness+.02,z-.01,x,y))
            parts.append((f'Via_{i}_{n}_{side}',s,TIN))
    for c in d['components']:
        if c['dnp']:continue
        ref=c['ref'];x,y=point(*c['xy']);kind=c['sym']
        if kind in ['R','C']:
            height=.55 if kind=='R' else (1.35 if ref in ['C7','C8','C10','C11'] else .8)
            parts.append((ref+'_corps',box(1.55,1.25,height,(x,y,1.68)),BLACK if kind=='R' else (.46,.32,.18)))
        elif kind=='Fuse':
            parts.append((ref+'_ceramique_454',box(6.1,2.69,2.69,(x,y,1.69)),(.70,.64,.40)))
            mark(parts,'T.5',x,y,4.39,1.1,BLACK)
        elif kind=='TMR':
            # Body pin datum: pin1 X=0; pin6 X=12.7, module depth datum 2.5.
            parts.append((ref+'_TMR1_corps_17x7_62x11',box(17,7.62,11,(x+6.35,y-1.31,1.9)),BLACK))
            mark(parts,'TRACO',x+6.35,y-1.3,12.91,1.3)
            for p in [p for p in d['pads'] if p['ref']==ref]:
                xx,yy=point(p['x'],p['y']);parts.append((ref+'_pin'+p['num'],box(.5,.25,3.2,(xx,yy,-1.3)),TIN))
        elif kind=='Opto':
            parts.append((ref+'_VOS618A_corps',box(4.4,2.6,2,(x,y,1.9)),BLACK))
            mark(parts,'618A8',x,y,3.91,.62)
            parts.append((ref+'_repere1',cyl(.16,.02,3.92,x-1.7,y+.72),(.40,.40,.40)))
            for p in [p for p in d['pads'] if p['ref']==ref]:
                px,py=point(p['x'],p['y']);parts.append((ref+'_patte'+p['num'],box(max(.3,abs(px-x)-2),.4,.18,((px+x+(-2 if px<x else 2))/2,py,1.7)),TIN))
        elif kind in ['Buf','LDO','Diode']:
            sx,sy,sz={'Buf':(1.25,2,1.0),'LDO':(2.5,4.5,1.6),'Diode':(1.3,2.9,1.0)}[kind]
            parts.append((ref+'_boitier_nominal',box(sx,sy,sz,(x,y,1.9)),BLACK))
            mark(parts,ref,x,y,1.91+sz,.65)
            for p in [p for p in d['pads'] if p['ref']==ref]:
                px,py=point(p['x'],p['y']);parts.append((ref+'_terminal'+p['num'],box(.5,.35,.23,(px,py,1.65)),TIN))
        elif ref.startswith('J'):
            count=len(c['nets']);cx=x+(count-1)*1.25
            # Nominal XH outline; exact latch/chamfer details not certified.
            outer=box(count*2.5+2.5,5.75,7,(cx,y,1.65))
            inner=box(count*2.5+.9,4.15,5.6,(cx,y,3.15))
            parts.append((ref+'_corps_XH_nominal',outer.cut(inner),WHITE))
            for p in [p for p in d['pads'] if p['ref']==ref]:
                px,py=point(p['x'],p['y']);parts.append((ref+'_broche'+p['num'],box(.64,.64,10,(px,py,-1.5)),TIN))
            mark(parts,ref,cx,y-3.5,1.655,1.0)
    mark(parts,'V3 - SURVEILLANCE 2S - M1P',70,5,1.70,2.2)
    mark(parts,'WARN HAUT = ALERTE',109,2.3,1.66,1.1)
    return parts

def frame(x,y,z,sx,sy,sz,name,color):
    # Open cage distinguishes a reserved volume from real hardware in any CAD viewer.
    ps=[];w=.45
    for zz in [z,z+sz-w]:
        ps.extend([(name+f'_railX_{zz}_{j}',box(sx,w,w,(x+sx/2,y+j*sy,zz)),color) for j in [0,1]])
        ps.extend([(name+f'_railY_{zz}_{j}',box(w,sy,w,(x+j*sx,y+sy/2,zz)),color) for j in [0,1]])
    ps.extend([(name+f'_montant_{i}_{j}',box(w,w,sz,(x+i*sx,y+j*sy,z)),color) for i in [0,1] for j in [0,1]])
    return ps

def main():
    sys.stdout.reconfigure(encoding='utf-8');OUT.mkdir(parents=True,exist_ok=True)
    q=json.loads((B/'verification/controle-kicad.json').read_text(encoding='utf-8'));assert q['erc_count']==q['drc_count']==q['parity_count']==q['unconnected_count']==0
    d=json.loads((B/'KiCad/implantation.json').read_text(encoding='utf-8'));ps=carrier(d)
    notes=['Carrier project dimensions140x75x1.6mm; four mounting holesdiam3.2, (4,4),(136,4),(4,71),(136,71).',
           'M1P checked KiCad: power tracks0.4mm, signals0.2mm, vias0.8/0.4mm; copper70um nominal,55um minimum specified.',
           'TRACO nominal body17x7.62x11mm, pins1/2/4/6; VOS618A body4.4x2.6mm nominal.']
    only='--assembly-only' in sys.argv
    previous=json.loads((OUT/'provenance.json').read_text(encoding='utf-8')) if only else None
    a=previous['models'][0] if only else save('porteuse-surveillance-2s-m1-detaillee.step','Surveillance 2S M1P | porteuse routee',ps,notes,dict(carrier_mm=[140,75,1.6],copper_um=70,hardware_measured=False))
    light=[part for part in ps if not part[0].startswith(('Pistes_','Plage_','Pastille_','Fut_','Via_','Marquage_'))]
    assembly=light+frame(6,8,15,60,60,12,'RESERVE_EVM_CELL1',(.10,.32,.55))+frame(74,8,15,60,60,12,'RESERVE_EVM_CELL2',(.10,.32,.55))
    assembly+=frame(10,20,7.8,18,13,5.5,'RESERVE_POLOLU2831',(.40,.20,.05))
    mark(assembly,'RESERVE EVM C1',36,38,27.1,2,(.1,.32,.55));mark(assembly,'RESERVE EVM C2',104,38,27.1,2,(.1,.32,.55))
    b=save('ensemble-surveillance-2s-m1-gabarits.step','Surveillance M1 | implantation allegee et modules reserves',assembly,
           ['Same external carrier/package envelopes; copper, plating and small markings omitted for faster assembly loading.',
            'EVM60x60x12mm are DESIGN RESERVATIONS ONLY, not manufacturer dimensions.'],dict(reserved_assembly_mm=[140,75,30],EVM_vendor_dimensions_known=False,simplified_carrier_for_assembly=True))
    rs=[]
    for i in range(3):
        rs.append((f'AC03_{i}_corps_13x4_8',cyl(2.4,13,0,-6.5,i*8,axis=(1,0,0)),(.18,.20,.17)))
        rs.append((f'AC03_{i}_fil_gauche',cyl(.4,25,0,-31.5,i*8,axis=(1,0,0)),TIN))
        rs.append((f'AC03_{i}_fil_droit',cyl(.4,25,0,6.5,i*8,axis=(1,0,0)),TIN))
    c=previous['models'][2] if only else save('resistances-mesure-3x-ac03-100ohm.step','Trois AC03 100 ohms | pattes droites non coupees',rs,['Vishay AC03 nominal body13xdiam4.8mm, leadsdiam0.8mm; straight25mm leads shown.'],dict(part='AC03000001000JAC00',lead_pose='Straight nominal, not the harness routing or its final length.'))
    (OUT/'provenance.json').write_text(json.dumps(dict(revision='M1P',models=[a,b,c],vendor_CAD=False,hardware_tested=False),ensure_ascii=False,indent=2),encoding='utf-8')
    print('Three STEP models saved and round-trip checked.',flush=True)
if __name__=='__main__':main()
