"""Chassis deliverables: compare actual DXF/STEP, thickness, hole data and PDF."""
from pathlib import Path
import ast,csv,hashlib,json,math,re,sys
import cadquery as cq
import ezdxf,pymupdf

ROOT=Path(__file__).resolve().parents[1];B=ROOT/'Composants/chassis'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    sys.stdout.reconfigure(encoding='utf-8');rows=[]
    data=json.loads((B/'pieces.json').read_text(encoding='utf-8'))
    csvrows=list(csv.DictReader((B/'plans/percages-et-decoupes.csv').open(encoding='utf-8-sig'),delimiter=';'))
    for d in data:
        path=B/'plans'/(d['code']+'.dxf');doc=ezdxf.readfile(path);assert doc.units==4
        s=cq.importers.importDXF(str(path)).extrude(d['t']).val();st=cq.importers.importStep(str(B/'3D'/(d['code']+'.step'))).val()
        err=abs(s.Volume()-st.Volume())/st.Volume()
        assert s.isValid() and st.isValid() and len(s.Solids())==1 and err<1e-7,(d['code'],err)
        # Symmetric difference checks position and contour, not merely equal area.
        diff=s.cut(st).Volume()+st.cut(s).Volume();assert diff<.001,(d['code'],diff)
        for f in d['features']:
            assert not s.isInside(cq.Vector(f['x'],f['y'],d['t']/2),1e-6),(d['code'],f)
        cr=[r for r in csvrows if r['piece']==d['code']];assert len(cr)==len(d['features'])
        for a,b in zip(cr,d['features']):
            assert float(a['x_mm'])==b['x'] and float(a['y_mm'])==b['y'] and a['type']==b['type']
            if b['type']=='hole':assert float(a['diametre_mm'])==b['d']
        rows.append(dict(piece=d['code'],DXF_units='mm',valid=True,solids=1,thickness_mm=d['t'],volume_mm3=s.Volume(),relative_volume_error=err,symmetric_difference_mm3=diff,features=len(d['features'])))
    templates=[]
    for code,w,h,count in [('L01-semelle',275,25,3),('L02-semelle',40,40,2),('L02-verticale',40,40,2),('L03-arriere',40,50,2),('L03-pivot',40,50,1)]:
        path=B/'plans'/(code+'.dxf');d=ezdxf.readfile(path);assert d.units==4
        cr=[r for r in csvrows if r['piece']==code];assert len(cr)==count
        # Import the drilling layer separately: reference rectangles belong to
        #another layer and are deliberately not machining contours.
        cuts=cq.importers.importDXF(str(path),include=['PERCAGE']).extrude(1).val()
        reference=cq.importers.importDXF(str(path),include=['REFERENCE_AILE_NE_PAS_DECOUPER']).extrude(1).val()
        assert abs(reference.Volume()-w*h)<.001
        solid=reference.cut(cuts);expected=w*h
        for r in cr:
            assert cuts.isInside(cq.Vector(float(r['x_mm']),float(r['y_mm']),.5),1e-6)
            if r['type']=='hole':expected-=math.pi*(float(r['diametre_mm'])/2)**2
            else:
                width=float(r['largeur_mm']);length=float(r['longueur_mm']);expected-=width*(length-width)+math.pi*(width/2)**2
        assert solid.isValid() and abs(solid.Volume()-expected)<.001,(code,solid.Volume(),expected)
        assert 'PERCAGE' in d.layers and 'REFERENCE_AILE_NE_PAS_DECOUPER' in d.layers
        templates.append(dict(template=code,features=count,reference_layer_not_for_cutting=True,valid=True,area_mm2=solid.Volume()))
    for code,expected in [('L01-section',141),('L02-section',231),('L03-section',231)]:
        path=B/'plans'/(code+'.dxf');d=ezdxf.readfile(path);assert d.units==4
        s=cq.importers.importDXF(str(path)).extrude(1).val();assert s.isValid() and abs(s.Volume()-expected)<.001
        templates.append(dict(section=code,area_mm2=s.Volume(),valid=True))
    fc=json.loads((B/'3D/validation-freecad.json').read_text(encoding='utf-8'));assert fc['all_passed']
    for m in fc['models']:assert sha(B/'3D'/m['file'])==m['sha256']
    sources=json.loads((B/'3D/provenance.json').read_text(encoding='utf-8'))
    for rel,digest in sources['sources_sha256'].items():assert sha(ROOT/rel)==digest,(rel,'changed since generation')
    missing=[]
    for path in [B/'README.md',B/'3D/README.md',B/'plans/README.md']:
        for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)',path.read_text(encoding='utf-8')):
            target=(path.parent/link.split('#')[0]).resolve()
            if target==(B/'verification/fichiers.json').resolve():continue  # report written after checks below
            if not re.match(r'\w+://',link) and not target.exists():missing.append([str(path),link])
    assert not missing,missing
    pdf=B/'plans/plans-chassis-a2-r1.pdf';meta=json.loads(pdf.with_suffix('.json').read_text(encoding='utf-8'))
    assert meta['visual_review_completed'] and meta['sha256']==sha(pdf)
    doc=pymupdf.open(pdf);assert len(doc)==meta['pages']
    for pg in doc:
        assert abs(pg.rect.width-1190.551)<.1 and abs(pg.rect.height-841.89)<.1
        for block in pg.get_text('dict')['blocks']:
            for line in block.get('lines',[]):
                for span in line['spans']:
                    assert span['bbox'][0]>=25 and span['bbox'][2]<=1170 and span['bbox'][1]>=22 and span['bbox'][3]<=828,span
    design=json.loads((B/'verification/conception.json').read_text(encoding='utf-8'));assert not design['custom_part_overlaps']
    assert len(design['machining_feature_checks'])==len(data)
    assert not design['selected_equipment_to_chassis']['overlaps']
    assert len(design['front_tire_clearance'])==62 and all(r['overlap_mm3']<1e-5 for r in design['front_tire_clearance'])
    for name in ['build_chassis_r1.py','check_chassis_freecad.py','verify_chassis_r1.py']:ast.parse((ROOT/'tools'/name).read_text(encoding='utf-8'))
    report=dict(all_passed=True,hardware_tested=False,custom_interferences=0,selected_equipment_to_chassis_clear=True,front_tire_sampled_poses=62,STEP_imports_FreeCAD=len(fc['models']),DXF_flat_parts_checked=len(rows),DXF_angle_templates_sections_checked=len(templates),PDF_pages_visually_reviewed=list(range(1,len(doc)+1)),sources_unchanged=True,details=rows,angle_templates=templates,
        files=[dict(file=str(path.relative_to(B)).replace('\\','/'),sha256=sha(path)) for path in sorted(B.rglob('*')) if path.is_file() and path.name!='fichiers.json' and 'concepts-images-v1' not in path.parts])
    (B/'verification/fichiers.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k not in ['details','files']},indent=2),flush=True)

if __name__=='__main__':main()
