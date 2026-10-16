"""Cross-export checks: DXF area/units, STL topology, current STEP/PDF integrity."""
from pathlib import Path
import ast,collections,hashlib,json,math,re,sys
import cadquery as cq
import ezdxf,numpy as np,pymupdf

ROOT=Path(__file__).resolve().parents[1];B=ROOT/'Composants/support-camera'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    sys.stdout.reconfigure(encoding='utf-8');results=[]
    expected=[('C01-base-CP6',(80*70-2*(4.5*(14-4.5)+math.pi*2.25**2))*6),('C02-montant-CP6',(40*240-(4.5*(44.5-4.5)+math.pi*2.25**2)-2*math.pi*2**2)*6),('C03-gousset-CP6',40*40/2*6)]
    for name,vol in expected:
        p=B/'plans'/f'{name}.dxf';d=ezdxf.readfile(p);s=cq.importers.importDXF(str(p)).extrude(6).val();v=s.Volume()
        assert s.isValid() and abs(v-vol)<.001,(name,v,vol)
        assert d.units==4,(name,d.units)
        results.append(dict(file=str(p.relative_to(B)),valid=True,units='mm',volume_at6mm_mm3=v,expected_volume_mm3=vol))
    p=B/'3D/berceau-camera-provisoire-p1.stl';data=p.read_bytes();n=int.from_bytes(data[80:84],'little');assert len(data)==84+50*n
    arr=np.frombuffer(data,offset=84,count=n,dtype=np.dtype([('normal','<f4',(3,)),('v','<f4',(3,3)),('attr','<u2')]))['v'].astype(float)
    vertices,ids=np.unique(np.round(arr.reshape(-1,3),5),axis=0,return_inverse=True);ids=ids.reshape(-1,3)
    edges=collections.Counter(tuple(sorted((int(a),int(z)))) for tri in ids for a,z in [(tri[0],tri[1]),(tri[1],tri[2]),(tri[2],tri[0])])
    assert all(c==2 for c in edges.values()),collections.Counter(edges.values())
    assert arr[:,:,2].min()>-1e-5
    meshvol=abs(np.einsum('ij,ij->i',arr[:,0],np.cross(arr[:,1],arr[:,2])).sum()/6)
    meta=json.loads((B/'3D/berceau-camera-provisoire-p1.json').read_text(encoding='utf-8'));target=meta['validation']['volume_before_mm3'];assert abs(meshvol-target)/target<.01
    results.append(dict(file=str(p.relative_to(B)),triangles=n,watertight=True,on_print_bed=True,volume_relative_error=abs(meshvol-target)/target))
    missing=[]
    for p in B.rglob('*.md'):
        for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
            if not re.match(r'\w+://',link) and not (p.parent/link.split('#')[0]).exists():missing.append([str(p),link])
    assert not missing,missing
    fc=json.loads((B/'3D/validation-freecad.json').read_text(encoding='utf-8'));assert fc['all_passed']
    for m in fc['models']:assert sha(B/'3D'/m['file'])==m['sha256']
    source=json.loads((B/'3D/provenance.json').read_text(encoding='utf-8'));cam=ROOT/'Composants/camera/3D/camera-u20cam-4m-detaillee.step';assert sha(cam)==source['camera_source_sha256']
    pdf=B/'notices/notice-support-camera-provisoire-p1.pdf';pm=json.loads(pdf.with_suffix('.json').read_text(encoding='utf-8'));assert pm['visual_review_completed'] and pm['sha256']==sha(pdf)
    doc=pymupdf.open(pdf);assert len(doc)==3
    for page in doc:
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines',[]):
                for span in line['spans']:assert span['bbox'][0]>=40 and span['bbox'][2]<=555 and span['bbox'][3]<=815,span
    for name in ['build_camera_support.py','check_camera_support_freecad.py','verify_camera_support.py']:ast.parse((ROOT/'tools'/name).read_text(encoding='utf-8'))
    report=dict(all_passed=True,hardware_tested=False,FreeCAD_current_imports_valid=True,camera_original_unchanged=True,local_links_valid=True,PDF_pages_visually_reviewed=[1,2,3],CAD_DXF_STL=results,
        files=[dict(file=str(p.relative_to(B)).replace('\\','/'),sha256=sha(p)) for p in sorted(B.rglob('*')) if p.is_file() and p.name!='fichiers.json'])
    (B/'verification/fichiers.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(dict(all_passed=True,DXF_checked=3,STL_triangles=n,STL_watertight=True,mesh_volume_error=abs(meshvol-target)/target,STEP_checked_FreeCAD=3,PDF_pages_reviewed=3,camera_original_unchanged=True),indent=2),flush=True)

if __name__=='__main__':main()
