"""Verify the documented speed package and its integration; no physical tests."""
from pathlib import Path
from urllib.parse import unquote
import ast,hashlib,json,math,re,sys
import pymupdf

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'Composants/capteurs-vitesse'
CHECKS=[]


def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def check(name,passed,detail):
    CHECKS.append(dict(check=name,passed=bool(passed),details=detail))
    print('PASS' if passed else 'FAIL',name,flush=True)
    if not passed:print(json.dumps(detail,ensure_ascii=False),flush=True)


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    json_errors=[]
    for path in BASE.rglob('*.json'):
        try:read(path)
        except Exception as e:json_errors.append(f'{path.relative_to(ROOT)}: {e}')
    check('JSON syntax',not json_errors,json_errors)
    errors=[];count=0
    for asset in read(BASE/'assets.json')['assets']:
        if not asset.get('sha256'):continue
        count+=1;p=BASE/asset['local']
        if hashlib.sha256(p.read_bytes()).hexdigest()!=asset['sha256']:errors.append(asset['local'])
    check('Original archive hashes',not errors,dict(files=count,errors=errors))
    broken=[];links=0
    for path in BASE.rglob('*.md'):
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',path.read_text(encoding='utf-8')):
            target=target.strip().strip('<>')
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',target) or target.startswith('#'):continue
            target=unquote(target.split('#',1)[0]);links+=1
            if not (path.parent/target).exists():broken.append(dict(file=str(path.relative_to(ROOT)),target=target))
    check('Local document links',not broken,dict(links=links,errors=broken))
    c=read(BASE/'calculs.json');errors=[]
    for row in c['wheel_rows']:
        f=row['speed_kmh']/3.6/(math.pi*.063)*2
        if abs(f-row['pulses_per_s'])>1e-10 or abs(30*f-row['wheel_rpm'])>1e-9:errors.append(row)
    check('Wheel speed and two-pulse conversion',not errors,dict(rows=len(c['wheel_rows']),errors=errors))
    check('Pullup, line-rise and current calculations',
          abs(c['pullup']['loss_low_W']-0.001089)<1e-12
          and abs(c['pullup']['rise_10_90_s']-22e-6)<1e-12
          and c['sensor_supply']['total_with_two_pullups_max_study_A']<.008,
          dict(supply_budget_A=c['sensor_supply']['total_with_two_pullups_max_study_A'],scope='Conditional budget; no rail/cable measured'))
    omega=(40/3.6)/(.063/2)
    expected=.00011*.012*omega**2
    check('Illustrative magnet centrifugal force',abs(c['centrifugal']['force_per_magnet_at40_N']-expected)<1e-12,
          dict(force_N=expected,radius_m=.012,scope='Radius assumption; not validated retention'))
    gpio=read(ROOT/'Composants/connecteur-gpio/brochage.json')
    bom=read(ROOT/'Composants/connecteur-gpio/nomenclature.json')
    pins={p['physical_pin']:p for p in gpio['pins']};speed={16,17,18,25}
    contacts=next(p for p in bom['parts'] if '16-02-0103' in p['reference'])
    base=read(ROOT/'Composants/connecteur-gpio/brochage-alimentation-r2-9-contacts.json')
    baseline={p['physical_pin'] for p in base['pins']}
    check('GPIO extension and preserved R2 power separation',
          len(pins)==13 and set(pins)==baseline|speed and not baseline&speed
          and set(gpio['unused_pins'])==set(range(1,41))-set(pins)
          and {2,4,6,9,14,20}.issubset(gpio['unused_pins'])
          and contacts['installed']==13 and contacts['quantity']==18 and contacts['spares']==5
          and gpio['power_through_Molex'] is False,
          dict(installed=13,total_contacts_to_buy=18,new_physical_pins=sorted(speed),power_5V_separate=True))
    cat=read(BASE/'3D/catalogue.json');fc=read(BASE/'3D/validation-freecad.json');errors=[]
    for model in cat['models']:
        path=ROOT/model['relative_step_path']
        if hashlib.sha256(path.read_bytes()).hexdigest()!=model['sha256']:errors.append(path.name)
        result=next(x for x in fc['checks'] if x['file']==path.name)
        if not result['passed'] or result['sha256']!=model['sha256']:errors.append('FreeCAD '+path.name)
    native=BASE/'references/KEMET-C315C104K5R5TA-original.step'
    copy=BASE/'condensateurs-decouplage-100nf/3D/kemet-c315c104k5r5ta-officiel.step'
    if native.read_bytes()!=copy.read_bytes():errors.append('KEMET native copy changed')
    check('Five STEP files and independent FreeCAD evidence',not errors and cat['model_count']==5,
          dict(models=len(cat['models']),errors=errors,scope='Headless CAD import, not GUI or hardware test'))
    pdf=BASE/'notices/notice-capteurs-vitesse-v3.pdf';meta=read(pdf.with_suffix('.json'));errors=[]
    with pymupdf.open(pdf) as d:
        if len(d)!=7:errors.append('Wrong pagination')
        text='\n'.join(p.get_text() for p in d)
        if '\ufffd' in text or '\x00' in text:errors.append('Invalid glyph')
        for page in d:
            for block in page.get_text('dict')['blocks']:
                for line in block.get('lines',[]):
                    for span in line['spans']:
                        x0,y0,x1,y1=span['bbox']
                        if x0<0 or y0<0 or x1>page.rect.width+.5 or y1>page.rect.height+.5:errors.append('Off-page text')
        if len(d[6].get_links())!=9:errors.append('Missing source links')
    if meta['sha256']!=hashlib.sha256(pdf.read_bytes()).hexdigest():errors.append('PDF hash')
    check('Seven-page notice integrity and layout bounds',not errors,errors)
    errors=[]
    for path in ROOT.joinpath('tools').glob('*speed_sensor*.py'):
        try:ast.parse(path.read_text(encoding='utf-8'),filename=path.name)
        except SyntaxError as e:errors.append(str(e))
    check('Package Python syntax',not errors,errors)
    report=dict(checked_on='2026-10-15',document_and_CAD_checks_passed=all(x['passed'] for x in CHECKS),
                hardware_tested=False,mount_designed=False,Amazon_exact_offer_verified=False,checks=CHECKS)
    (BASE/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return 0 if report['document_and_CAD_checks_passed'] else 1


if __name__=='__main__':raise SystemExit(main())
