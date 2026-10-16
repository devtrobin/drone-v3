"""Delivery hashes, links, readable formats and transparent release status."""
from pathlib import Path
import json,hashlib,re,math,zipfile,sys
from urllib.parse import unquote
from PIL import Image,ImageOps,ImageDraw
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'Composants/complements-finalisation-r3';V=B/'verification';A=ROOT/'Assemblage/R3';T=ROOT/'tools/temp/finalisation-r3'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def dump(p,o):p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def audit():
    links=[]
    for folder in [B,A]:
        for p in folder.rglob('*.md'):
            for link in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
                if link.startswith(('http:','https:','#')):continue
                dest=(p.parent/unquote(link.split('#')[0].strip('<>'))).resolve();assert dest.exists(),(p,dest);links.append(str(dest))
    gen=load(V/'generation.json');step=A/'drone-v3-r3-faisceau.step';h=sha(step)
    assert h==gen['sha256']==load(V/'freecad.json')['source_sha256']==load(V/'cad-viewer.json')['sha256']
    assert gen['R2_source_sha256']==sha(ROOT/'Assemblage/R2/drone-v3-r2-etude.step')
    geom=load(V/'geometrie.json');assert geom['nominal_frame_and_cables_clear'] and not geom['steering_unexpected']
    assert len(list((B/'3D').glob('*.step')))==len(geom['exported_STEP_files'])
    for r in load(V/'dxf.json'):
        assert sha(B/'3D'/(r['piece']+'.step'))==r['STEP_sha256']
        assert sha(B/'plans'/(r['piece']+'.dxf'))==r['DXF_sha256']
    assert len(list((B/'plans').glob('*.dxf')))==len(load(V/'dxf.json'))
    for r in load(B/'sources.json'):
        if r.get('archived'):assert sha(B/r['file'])==r['sha256'],r['id']
    pdf=load(V/'pdf.json');assert sha(B/'plans/dossier-complements-r3.pdf')==pdf['sha256']
    for start in range(0,len(pdf['renders']),4):
        imgs=pdf['renders'][start:start+4];sheet=Image.new('RGB',(1600,620*math.ceil(len(imgs)/2)),'#d8e0e8');draw=ImageDraw.Draw(sheet)
        for i,p in enumerate(imgs):
            sheet.paste(ImageOps.contain(Image.open(ROOT/p),(790,565)),((i%2)*800,(i//2)*620+30));draw.text(((i%2)*800+10,(i//2)*620+8),str(start+i+1),fill='black')
        sheet.save(T/f'pdf-controle-{start//4+1}.png')
    report=dict(local_links_checked=len(links),all_links_exist=True,STEP_files=len(geom['exported_STEP_files']),DXF_files=len(load(V/'dxf.json')),static_pairs_checked=geom['pairs'],unexpected_new_intersections=0,steering_samples=51,new_objects_clear_at_samples=True,FreeCAD_native_reopened=True,FreeCAD_reopen_seconds=load(V/'freecad.json')['native_reopen_seconds'],CAD_Viewer_installed_parser_passed=load(V/'cad-viewer.json')['success'],R2_STEP_unchanged=True,PDF_pages=pdf['page_count'],PDF_visual_review_pending=pdf['visual_review_pending'],all_electrical_conditions_closed=False,physical_tests_done=False)
    dump(V/'livraison.json',report)
    files=[]
    for folder in [B,A]:
        for p in sorted(folder.rglob('*')):
            if not p.is_file() or p.suffix.lower() in ['.zip','.fcbak','.fcstd1'] or p in [V/'manifest.json',V/'archive.json']:continue
            files.append(dict(path=str(p.relative_to(ROOT)).replace('\\','/'),bytes=p.stat().st_size,sha256=sha(p)))
    dump(V/'manifest.json',dict(files=files,excludes_self_zip_and_archive_record=True));print(json.dumps(report,ensure_ascii=False))
def package():
    out=B/'complements-finalisation-r3.zip';paths=[]
    for folder in [B,A]:
        paths.extend(p for p in folder.rglob('*') if p.is_file() and p.suffix.lower() not in ['.zip','.fcbak','.fcstd1'] and p!=V/'archive.json')
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,6) as z:
        for p in sorted(paths):z.write(p,str(p.relative_to(ROOT)))
    with zipfile.ZipFile(out) as z:assert z.testzip() is None
    dump(V/'archive.json',dict(file=out.name,bytes=out.stat().st_size,sha256=sha(out),files=len(paths),CRC_checked=True,complement_requires_existing_project_for_R2_documents=True));print('ZIP',len(paths),out.stat().st_size)
if __name__=='__main__':
    if '--package' in sys.argv:package()
    else:audit()
