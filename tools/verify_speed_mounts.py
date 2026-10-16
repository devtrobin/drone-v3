"""Cross-export checks for P1 speed mounts, excluding physical qualification."""
from pathlib import Path
import ast,collections,hashlib,json,math,re,sys
import cadquery as cq
import ezdxf,numpy as np,pymupdf
from build_speed_mounts import bracket,head_parts,rotor

ROOT=Path(__file__).resolve().parents[1];B=ROOT/'Composants/supports-capteurs-vitesse'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    sys.stdout.reconfigure(encoding='utf-8');results=[]
    path=B/'plans/gabarit-fixation-40x30.dxf';d=ezdxf.readfile(path)
    solid=cq.importers.importDXF(str(path)).extrude(3).val()
    expected=(40*30-2*(3.5*(20-3.5)+math.pi*1.75**2))*3
    assert solid.isValid() and abs(solid.Volume()-expected)<.001
    assert d.units==4
    results.append(dict(file=str(path.relative_to(B)),units='mm',volume_at3mm_mm3=solid.Volume(),expected_volume_mm3=expected))
    head,cap=head_parts()
    for name,shape in [('P01-equerre',bracket()),('P02-porte-capteur',head),('P03-retenue',cap),('P04-rotor',rotor())]:
        path=B/'3D'/f'{name}.stl';data=path.read_bytes();n=int.from_bytes(data[80:84],'little');assert len(data)==84+50*n
        arr=np.frombuffer(data,offset=84,count=n,dtype=np.dtype([('normal','<f4',(3,)),('v','<f4',(3,3)),('attr','<u2')]))['v'].astype(float)
        vertices,ids=np.unique(np.round(arr.reshape(-1,3),5),axis=0,return_inverse=True);ids=ids.reshape(-1,3)
        edges=collections.Counter(tuple(sorted((int(a),int(z)))) for tri in ids for a,z in [(tri[0],tri[1]),(tri[1],tri[2]),(tri[2],tri[0])])
        assert all(c==2 for c in edges.values()),(name,collections.Counter(edges.values()))
        assert arr[:,:,2].min()>-1e-5
        meshvol=abs(np.einsum('ij,ij->i',arr[:,0],np.cross(arr[:,1],arr[:,2])).sum()/6)
        error=abs(meshvol-shape.Volume())/shape.Volume();assert error<.01
        results.append(dict(file=str(path.relative_to(B)),triangles=n,watertight=True,on_print_bed=True,volume_relative_error=error))
    missing=[]
    for path in B.rglob('*.md'):
        for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)',path.read_text(encoding='utf-8')):
            if not re.match(r'\w+://',link) and not (path.parent/link.split('#')[0]).exists():missing.append([str(path),link])
    assert not missing,missing
    fc=json.loads((B/'3D/validation-freecad.json').read_text(encoding='utf-8'));assert fc['all_passed']
    for m in fc['models']:assert sha(B/'3D'/m['file'])==m['sha256']
    source=json.loads((B/'3D/provenance.json').read_text(encoding='utf-8'))
    for path,digest in source['source_sha256'].items():assert sha(ROOT/path)==digest
    pdf=B/'notices/notice-supports-capteurs-vitesse-p1.pdf'
    meta=json.loads(pdf.with_suffix('.json').read_text(encoding='utf-8'));assert meta['visual_review_completed'] and meta['sha256']==sha(pdf)
    doc=pymupdf.open(pdf);assert len(doc)==3
    for page in doc:
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines',[]):
                for span in line['spans']:assert span['bbox'][0]>=40 and span['bbox'][2]<=555 and span['bbox'][3]<=815,span
    for name in ['build_speed_mounts.py','check_speed_mounts_freecad.py','verify_speed_mounts.py']:ast.parse((ROOT/'tools'/name).read_text(encoding='utf-8'))
    report=dict(all_passed=True,hardware_tested=False,FreeCAD_current_imports_valid=True,original_sources_unchanged=True,local_links_valid=True,PDF_pages_visually_reviewed=[1,2,3],CAD_DXF_STL=results,
        files=[dict(file=str(path.relative_to(B)).replace('\\','/'),sha256=sha(path)) for path in sorted(B.rglob('*')) if path.is_file() and path.name!='fichiers.json'])
    (B/'verification/fichiers.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(dict(all_passed=True,DXF_checked=1,STL_watertight_checked=4,STEP_checked_FreeCAD=3,PDF_pages_reviewed=3,original_sources_unchanged=True),indent=2),flush=True)

if __name__=='__main__':main()
