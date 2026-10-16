"""Native ERC/DRC, source/PCB/netlist comparison and vector views, isolated config."""
from pathlib import Path
import collections,hashlib,json,os,subprocess,sys,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'Composants/carte-surveillance-electrique';D=B/'KiCad';Q=B/'verification';NAME='surveillance-2s-m1';K=Path('D:/KiCAD')
def main():
    sys.stdout.reconfigure(encoding='utf-8');cfg=ROOT/'tools/temp/kicad-monitor-config';c=cfg/'10.0';c.mkdir(parents=True,exist_ok=True)
    libs=['Connector_JST','Resistor_SMD','Capacitor_SMD','Package_SO','Package_TO_SOT_SMD','MountingHole']
    (c/'fp-lib-table').write_text('(fp_lib_table (version 7) '+' '.join(f'(lib (name "{n}") (type "KiCad") (uri "D:/KiCAD/share/kicad/footprints/{n}.pretty") (options "") (descr "KiCad stock"))' for n in libs)+')',encoding='utf-8')
    (c/'sym-lib-table').write_text('(sym_lib_table (version 7))',encoding='utf-8')
    env=dict(os.environ,KICAD_CONFIG_HOME=str(cfg));results=[]
    def run(*args):
        r=subprocess.run([str(K/'bin/kicad-cli.exe'),*map(str,args)],env=env,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=90)
        results.append(dict(arguments=list(map(str,args)),returncode=r.returncode,stdout=r.stdout,stderr=r.stderr));print(r.stdout.strip(),flush=True)
        assert r.returncode==0,(r.stdout,r.stderr)
    sch=D/(NAME+'.kicad_sch');pcb=D/(NAME+'.kicad_pcb')
    run('sch','erc','--format','json','--severity-all','-o',Q/'erc.json',sch)
    run('pcb','drc','--format','json','--severity-all','--all-track-errors','--schematic-parity','-o',Q/'drc.json',pcb)
    run('sch','export','netlist','--format','kicadxml','-o',D/'netlist.xml',sch)
    run('sch','export','svg','-o',D/'vues',sch)
    for name,layers in [('routage','F.Cu,B.Cu,F.SilkS,Edge.Cuts'),('montage','F.Fab,Edge.Cuts'),('cuivre-dessus','F.Cu,Edge.Cuts'),('cuivre-dessous','B.Cu,Edge.Cuts')]:
        run('pcb','export','svg','--layers',layers,'--mode-single','--fit-page-to-board','--exclude-drawing-sheet','--sp','-o',D/'vues'/(name+'.svg'),pcb)
    expected=json.loads((D/'connectivite-attendue.json').read_text(encoding='utf-8'));actual={}
    for net in ET.parse(D/'netlist.xml').findall('./nets/net'):
        for node in net.findall('node'):
            if not node.attrib['ref'].startswith('#'):actual.setdefault(node.attrib['ref'],{})[node.attrib['pin']]=net.attrib['name'].lstrip('/')
    assert actual==expected,'Independent schematic pin/net mismatch'
    erc=json.loads((Q/'erc.json').read_text(encoding='utf-8'));drc=json.loads((Q/'drc.json').read_text(encoding='utf-8'))
    ev=[v for s in erc['sheets'] for v in s['violations']];dv=drc['violations']+drc['unconnected_items']+drc['schematic_parity']
    report=dict(checked_on='2026-10-15',kicad_version='10.0.7',hardware_tested=False,manufacturing_ready=False,
                source_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [sch,pcb]},
                pin_net_matches=True,erc_count=len(ev),drc_count=len(drc['violations']),unconnected_count=len(drc['unconnected_items']),parity_count=len(drc['schematic_parity']),
                erc_types=dict(collections.Counter(v['type'] for v in ev)),drc_types=dict(collections.Counter(v['type'] for v in dv)),commands=results,
                interpretation='Native file checks only. External EVM modifications, physical interfaces, protection coordination and bench tests are not validated by ERC/DRC.')
    (Q/'controle-kicad.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='commands'},ensure_ascii=False),flush=True)
    assert not ev and not dv,'Native issues remain'
if __name__=='__main__':main()
