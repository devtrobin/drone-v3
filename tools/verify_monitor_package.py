"""Final cross-file and artifact integrity checks. Never a hardware validation."""
from pathlib import Path
import ast,csv,hashlib,json,re,sys,zipfile,xml.etree.ElementTree as ET
import pymupdf
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'Composants/carte-surveillance-electrique'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    sys.stdout.reconfigure(encoding='utf-8');passed=[]
    def check(name,condition):assert condition,name;passed.append(name);print('PASS',name,flush=True)
    for p in B.rglob('*.json'):read(p)
    check('JSON syntax',True)
    expected=read(B/'KiCad/connectivite-attendue.json');actual={}
    for net in ET.parse(B/'KiCad/netlist.xml').findall('./nets/net'):
        for node in net.findall('node'):
            if not node.attrib['ref'].startswith('#'):actual.setdefault(node.attrib['ref'],{})[node.attrib['pin']]=net.attrib['name'].lstrip('/')
    check('Independent schematic connectivity',actual==expected)
    q=read(B/'verification/controle-kicad.json')
    check('Native KiCad ERC DRC connectivity and parity',q['erc_count']==q['drc_count']==q['unconnected_count']==q['parity_count']==0)
    check('KiCad checked sources unchanged',all(sha(B/'KiCad'/n)==h for n,h in q['source_sha256'].items()))
    check('Healthy LEDs shunted by OUTA, independent returns',all(expected[f'U{2*n-1}']['1']==expected[f'R{2*n-1}']['2']==f'HARD_A{n}' and expected[f'U{2*n-1}']['2']==expected[f'M{n+2}']['6']==('B0_R' if n==1 else 'B1_R') for n in [1,2]))
    check('Independent AUX LDO and no cell-to-Pi power return',expected['U6']['2']=='AUX' and expected['M3']['1']==expected['M4']['1']=='GND' and expected['J6']['1']=='3V3_PI')
    d=read(B/'KiCad/implantation.json');comps={c['ref']:c for c in d['components']};gpio=read(ROOT/'Composants/connecteur-gpio/brochage.json')
    check('WARN active high, pullups at Pi, 13 GPIO contacts',gpio['WARN_active_high'] and gpio['signal_contacts_used']==13 and comps['R7']['dnp'] and comps['R8']['dnp'])
    check('LDO capacitor margin and 5V fuse selection',comps['C7']['value'].startswith('2u2') and comps['C8']['value'].startswith('2u2') and all('0454.500MR' in comps[f'F{n}']['value'] for n in [1,2]))
    c=read(B/'calculs.json');hard,warn=c['thresholds']
    check('Worst-case threshold order',hard['with_sense_network_conservative_max_V']<warn['with_sense_network_conservative_min_V'])
    check('Three limited-current sense wires',c['sense_protection']['count']==3 and c['sense_protection']['power_at8_4V_with90ohm_W']<.79)
    selection=read(B/'selection.json')
    check('Five existing modules and honest prototype state',selection['existing_modules_count']==5 and not selection['additional_microcontroller'] and not selection['purchased'] and not selection['manufacturing_ready'] and len(selection['bounds_exclude'])>=4)
    release=read(B/'verification/liberation-prototype.json');manifest=read(B/'fabrication/manifest.json');coord=read(B/'verification/coordination-protections.json');dims=read(B/'modules/cotes-ti.json')
    check('Prototype-only release and no invented hardware results',selection['revision']=='M1P' and release['prototype_carrier_fabrication_ready'] and release['bench_procedure_ready'] and not release['hardware_tested'] and not release['vehicle_battery_release'] and not release['manufacturing_ready_for_vehicle'])
    check('TI specified pitch distinguished from inferred board dimensions',dims['exact_documented']['header_pitch_mm']==2.54 and not dims['exact_vendor_board_dimensions_verified'] and dims['inferred_NOT_certified']['drawing_tolerance_unknown'] and sha(B/dims['source'])==dims['sha256'])
    check('Manufacturing source hashes and geometry checks',manifest['source_sha256']==q['source_sha256'] and manifest['edge_dimensions_mm']==[140,75] and manifest['hole_centers_exact_match'] and manifest['native_npth_count']==4 and manifest['native_pth_count']==85 and manifest['vias']==52)
    check('Fabrication exports unchanged',all(sha(B/'fabrication'/r['path'])==r['sha256'] for r in manifest['files']))
    packet=B/release['package']['file']
    check('Prototype ZIP unchanged',sha(packet)==release['package']['sha256'])
    with zipfile.ZipFile(packet) as z:
        check('ZIP exactly contains checked exports and manufacturing specification',set(z.namelist())=={r['path'] for r in manifest['files']}|{'manifest.json'} and all(hashlib.sha256(z.read(r['path'])).hexdigest()==r['sha256'] for r in manifest['files']) and z.read('manifest.json')==(B/'fabrication/manifest.json').read_bytes())
    check('Power and signal routing sizes match copper study',d['routing']['width']==.4 and d['routing']['signal_width']==.2 and d['routing']['copper_nominal_um']==70 and d['routing']['via_diameter']==.8 and d['routing']['via_drill']==.4 and coord['copper']['minimum_finished_um']==55 and coord['copper']['minimum_hole_wall_um']==20)
    check('Bounded bench remains conditional, not LiPo coordination',not coord['fuses']['coordination_proven_for_LiPo'] and coord['fuses']['melting_is_not_max_total_clearing'] and coord['bench']['AUX_CC_setting_A']==.25 and coord['bench']['series_resistor_min_ohm']==4.4 and coord['bench']['source_characteristics_must_be_verified'] and not coord['bench']['hardware_results_exist'])
    results=list(csv.DictReader((B/'verification/resultats-banc.csv').open(encoding='utf-8-sig'),delimiter=';'))
    check('Fifteen bench records honestly unmeasured',len(results)==15 and all(r['Résultat']=='NON REALISE' and not r['Mesure réelle'] for r in results))
    bad=[]
    for p in [*B.rglob('*.md'),ROOT/'PLAN-CONCEPTION.md']:
        for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
            if re.match(r'\w+://',link) or link.startswith('#'):continue
            target=(p.parent/link.split('#')[0]).resolve()
            if not target.exists():bad.append([str(p.relative_to(ROOT)),link])
    check('Local document links',not bad)
    originals=read(B/'notices/inventaire-originaux.json')
    check('Original PDFs preserved',all(sha(B/r['file'])==r['sha256'] and not r['modified'] for r in originals))
    fc=read(B/'3D/validation-freecad.json');cad=read(B/'3D/provenance.json')
    check('Independent FreeCAD import of current STEP versions',fc['all_passed'] and len(fc['models'])==3 and all(sha(B/'3D'/r['file'])==r['sha256'] for r in fc['models']))
    check('STEP source/routing hashes and geometric round-trip',all(sha(B/'3D'/r['file'])==r['sha256'] and r['kicad_pcb_sha256']==sha(B/'KiCad/surveillance-2s-m1.kicad_pcb') and r['validation']['valid_after_reimport'] for r in cad['models']))
    check('Assembly STEP small enough for normal placement use',(B/'3D/ensemble-surveillance-2s-m1-gabarits.step').stat().st_size<6_000_000 and cad['models'][1]['parameters']['simplified_carrier_for_assembly'])
    pdf=B/'notices/notice-carte-surveillance-v3.pdf';pm=read(pdf.with_suffix('.json'));doc=pymupdf.open(pdf)
    check('Eight-page notice reviewed and current',len(doc)==8 and pm['visual_review_completed'] and pm['sha256']==sha(pdf))
    annex=B/'notices/annexe-preparation-fabrication-essais-m1p.pdf';am=read(annex.with_suffix('.json'));adoc=pymupdf.open(annex)
    check('Six-page prototype annex reviewed and current',len(adoc)==6 and am['visual_review_completed'] and am['sha256']==sha(annex))
    out_of_bounds=[]
    for i,page in enumerate([*doc,*adoc]):
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines',[]):
                for span in line['spans']:
                    x0,y0,x1,y1=span['bbox']
                    if x0<45 or x1>550 or y0<35 or y1>815:out_of_bounds.append([i+1,span['text']])
    check('PDF text inside page bounds',not out_of_bounds)
    for p in [ROOT/'tools'/n for n in ['build_monitor_package.py','build_monitor_kicad.py','kicad_symbols.py','check_monitor_kicad.py','build_monitor_step.py','check_monitor_freecad.py','build_monitor_pdf.py','finish_monitor_dossier.py','verify_monitor_package.py','prepare_monitor_prototype.py','export_monitor_prototype.py','build_monitor_qualification_pdf.py','monitor_typography.py']]:ast.parse(p.read_text(encoding='utf-8'))
    check('Package builder syntax',True)
    result=dict(checked_on='2026-10-15',revision='M1P',passed=passed,all_passed=True,hardware_tested=False,manufacturing_ready=False,prototype_carrier_fabrication_ready=True,bench_procedure_ready=True,vehicle_battery_release=False,
       remaining=['French procurement prices and stocks','Exact EVM native dimensions and final supports','Maximum total clearing envelope / qualified active current limiting for LiPo and R2 coordination','Execute bounded bench procedure, GPIO software, temperature and EMC'])
    (B/'verification/verification-dossier.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
if __name__=='__main__':main()
