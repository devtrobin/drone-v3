"""Delivery audit: links, matching parser/native reports, R1 preservation."""
from pathlib import Path
import json,hashlib,re,csv,math
from urllib.parse import unquote
from PIL import Image,ImageOps,ImageDraw
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'Composants/finalisation-theorique-r2';V=B/'verification'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def dump(p,o):p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
targets=[B,ROOT/'Composants/visserie-finale',ROOT/'Composants/retenues-axiales',ROOT/'Composants/alimentation-direction',ROOT/'Composants/interface-pwm-isolee',ROOT/'Composants/servo-direction/ft5335m-r2',ROOT/'Assemblage/R2']
links=[];missing=[]
for folder in targets:
    for p in folder.rglob('*.md'):
        for rel in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
            if rel.startswith(('https:','http:','#')):continue
            rel=unquote(rel.split('#')[0].strip('<>'));q=(p.parent/rel).resolve()
            links.append(dict(source=str(p.relative_to(ROOT)),target=str(q)))
            if not q.exists():missing.append(links[-1])
assert not missing,missing
step=ROOT/'Assemblage/R2/drone-v3-r2-etude.step';h=sha(step)
gui=load(V/'freecad.json');parser=load(V/'cad-viewer.json');geom=load(V/'synthese.json')
assert gui['source_sha256']==parser['sha256']==geom['assembly_step_sha256']==h
assert gui['native_reopen_tested'] and gui['all_imported_shapes_valid'] and parser['success'] and geom['all_selected_checks_passed']
for d in load(V/'dxf.json'):assert sha(B/'3D'/(d['part']+'.step'))==d['step_sha256'] and sha(B/'plans'/(d['part']+'.dxf'))==d['dxf_sha256']
r1=[]
for row in load(ROOT/'Assemblage/validation-cad-viewer.json')['models']:
    p=ROOT/'Assemblage'/row['file'];same=sha(p)==row['sha256'];assert same,p
    r1.append(dict(file=row['file'],unchanged=True))
pdf=load(V/'pdf.json');assert pdf['all_pages_rendered']
imgs=[ROOT/r['render'] for r in pdf['pages']]
for start in range(0,len(imgs),4):
    subset=imgs[start:start+4];sheet=Image.new('RGB',(1600,620*math.ceil(len(subset)/2)),'#d8e0e8');d=ImageDraw.Draw(sheet)
    for i,p in enumerate(subset):
        sheet.paste(ImageOps.contain(Image.open(p),(790,565)),((i%2)*800,(i//2)*620+30))
        d.text(((i%2)*800+10,(i//2)*620+8),p.stem,fill='black')
    sheet.save(ROOT/'tools/temp/finalisation-r2/pdf'/f'controle-{start//4+1}.png')
data=dict(local_markdown_links=len(links),all_local_links_exist=True,assembly_sha256=h,native_round_trip_passed=True,native_reopen_seconds=gui['gui_reopen_seconds'],cad_viewer_parser_passed=True,all_selected_geometry_checks_passed=True,R1_steps_unchanged=r1,flat_DXF_checks=len(load(V/'dxf.json')),PDF_pages=pdf['page_count'],visual_PDF_review_pending=pdf['visual_review_pending'],physical_vehicle_fit_validated=False,vehicle_fabrication_released=False)
dump(V/'livraison.json',data)
dump(V/'etat-liberation.json',dict(theoretical_review_documented=True,nominal_custom_mechanical_parts_defined=True,selected_geometry_checks_passed=True,normalised_axial_retention_defined=True,all_supplier_interfaces_exact=False,all_harness_routes_and_anchors_defined=False,full_electrical_protection_coordination_proven=False,vehicle_fabrication_released=False,vehicle_power_on_released=False,hardware_tested=False,remaining_conditions='../conditions-restantes.json'))
files=[]
for folder in targets:
    for p in folder.rglob('*'):
        if not p.is_file() or p.name.endswith(('.FCBak','.FCStd1','.zip','.candidate.step')) or p.name in ('manifest-livrables.json','archive.json'):continue
        files.append(dict(file=str(p.relative_to(ROOT)).replace('\\','/'),bytes=p.stat().st_size,sha256=sha(p)))
dump(V/'manifest-livrables.json',dict(files=files,includes_self=False,archive_record_excluded=True))
print(json.dumps(data,ensure_ascii=False))
