"""Generate a bounded prototype manufacturing packet after native checks.

Run in KiCad Python. File integrity and export geometry are verified; the
release never authorizes a battery-powered vehicle or claims bench results.
"""
from pathlib import Path
import collections,csv,hashlib,json,os,re,subprocess,sys,zipfile
import pcbnew as pcb

ROOT=Path(__file__).resolve().parents[1];B=ROOT/'Composants/carte-surveillance-electrique';D=B/'KiCad';F=B/'fabrication';Q=B/'verification'
NAME='surveillance-2s-m1';K=Path('D:/KiCAD/bin/kicad-cli.exe')
POWER={'AUX','GND','5V_MON','TMR_IN1','TMR_IN2','ISO5_1','ISO5_2','3V3_AUX'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,o):p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    sys.stdout.reconfigure(encoding='utf-8');F.mkdir(exist_ok=True);G=F/'gerbers';G.mkdir(exist_ok=True)
    q=json.loads((Q/'controle-kicad.json').read_text(encoding='utf-8'))
    assert q['erc_count']==q['drc_count']==q['parity_count']==q['unconnected_count']==0
    path=D/(NAME+'.kicad_pcb')
    assert q['source_sha256'][path.name]==sha(path)
    b=pcb.LoadBoard(str(path));tracks=[];vias=[]
    for t in b.GetTracks():
        if isinstance(t,pcb.PCB_VIA):
            vias.append(dict(x=pcb.ToMM(t.GetPosition().x),y=pcb.ToMM(t.GetPosition().y),diameter=pcb.ToMM(t.GetWidth(pcb.F_Cu)),drill=pcb.ToMM(t.GetDrillValue())))
            assert abs(pcb.ToMM(t.GetWidth(pcb.F_Cu))-.8)<1e-6 and abs(pcb.ToMM(t.GetDrillValue())-.4)<1e-6
        else:
            net=t.GetNetname().lstrip('/');w=pcb.ToMM(t.GetWidth());expected=.4 if net in POWER else .2
            assert abs(w-expected)<1e-6,(net,w,expected)
            tracks.append(dict(net=net,width=w))
    # Independent native through-hole count to compare against Excellon output.
    pth=len(vias);npth=0;holes=[]
    for fp in b.GetFootprints():
        for p in fp.Pads():
            if p.GetDrillSize().x>0:
                is_np=p.GetAttribute()==pcb.PAD_ATTRIB_NPTH
                if is_np:npth+=1
                else:pth+=1
                holes.append(dict(ref=fp.GetReference(),number=p.GetNumber(),npth=is_np,x=pcb.ToMM(p.GetPosition().x),y=pcb.ToMM(p.GetPosition().y),drill=pcb.ToMM(p.GetDrillSize().x)))
    env=dict(os.environ,KICAD_CONFIG_HOME=str(ROOT/'tools/temp/kicad-monitor-config'))
    commands=[]
    def run(*args):
        r=subprocess.run([str(K),*map(str,args)],env=env,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=90)
        assert r.returncode==0,(args,r.stdout,r.stderr)
        commands.append(dict(args=list(map(str,args)),stdout=r.stdout,stderr=r.stderr));print(r.stdout.strip(),flush=True)
    run('pcb','export','gerbers','--layers','F.Cu,B.Cu,F.Mask,B.Mask,F.SilkS,Edge.Cuts','--subtract-soldermask','--no-protel-ext','-o',str(G)+os.sep,path)
    run('pcb','export','drill','--excellon-separate-th','--excellon-units','mm','--generate-map','--map-format','svg','-o',str(G)+os.sep,path)
    run('pcb','export','pos','--format','csv','--units','mm','--exclude-dnp','-o',F/'positions-montage.csv',path)
    run('pcb','export','ipcd356','-o',F/'netlist-controle-pcb.ipc',path)
    drill_counts={}
    for p in G.glob('*.drl'):
        text=p.read_text(encoding='utf-8');assert 'METRIC' in text
        drill_counts[p.name]=len(re.findall(r'^X[-\d.]+Y[-\d.]+$',text,re.M))
    assert sum(v for n,v in drill_counts.items() if 'NPTH' not in n)==pth,(drill_counts,pth)
    assert sum(v for n,v in drill_counts.items() if 'NPTH' in n)==npth==4,(drill_counts,npth)
    edge=next(G.glob('*Edge_Cuts.gbr'));text=edge.read_text(encoding='utf-8')
    assert '%MOMM*%' in text and '%FSLAX46Y46*%' in text
    coords=[(int(x)/1e6,int(y)/1e6) for x,y in re.findall(r'X(-?\d+)Y(-?\d+)D0[12]\*',text)]
    assert coords,'Edge coordinates not parsed'
    xs,ys=zip(*coords);assert abs(max(xs)-min(xs)-140)<1e-6 and abs(max(ys)-min(ys)-75)<1e-6,coords
    # Drill center coordinates exactly equal the native board data (including vias).
    native=collections.Counter((round(x,4),round(y,4)) for x,y in [(h['x'],h['y']) for h in holes]+[(v['x'],v['y']) for v in vias])
    actual=collections.Counter()
    for p in G.glob('*.drl'):
        for x,y in re.findall(r'^X([-\d.]+)Y([-\d.]+)$',p.read_text(encoding='utf-8'),re.M):actual[(round(float(x),4),round(-float(y),4))]+=1
    assert native==actual,'Exported hole positions differ from native board'
    readme='''# Fabrication M1P - porteuse pour prototype de banc

**Lot prototype seulement.** [Coordination](../verification/coordination-protections.md), [banc B00-B14](../verification/banc-essais.md) et [registre](../verification/liberation-prototype.json) définissent le périmètre. Aucune qualification LiPo, aucun matériel testé. Les Gerbers sont ceux de la porteuse, pas ceux des modules TI.

## Demande de fabrication à joindre au ZIP

- FR4,140 x75 mm, épaisseur1,6 mm ±0,16 ; deux couches ; vernis épargne deux faces, sérigraphie face composants. Contour rectangulaire,4 trous mécaniques non métallisésØ3,2. Finition soudable sans plomb (ENIG ou équivalent validé par l'assembleur).
- Cuivre fini **70 micromètres nominal,55 minimum** sur chacune des deux faces. Le nom «2oz» seul ne dispense pas de confirmer le cuivre fini minimal. Pistes alimentation0,40 (gravées>=0,35), signaux0,20 (>=0,175). Isolement cuivre minimal du projet0,15 ; le fabricant doit confirmer sa capacité avec cette épaisseur.
- ViasØ0,80, perçage **fini**Ø0,40, tolérance admise±0,05 ; métallisation paroi>=20 micromètres. Autres trous métallisés selon Excellon. Ne pas appliquer un diamètre de foret brut comme diamètre fini. Vérifier les jeux de broches sur les fiches reçues (TMR /XH) ; diamètres source dans le PCB et les fichiers de perçage.
- Dimensions hors tout ±0,20 mm ; centres de trous ±0,10. Pas de cuivre de puissance moteur/Pi. Ne pas diminuer les largeurs ou métallisations sans refaire l'étude. Demander au fabricant un contrôle électrique de continuité/isolement du PCB nu à partir de sa netlist de fabrication.
- **Ce routage n'est pas directement usinable sur la CNC** : trous métallisés, deux faces et pas CMS fin. Aucune trajectoire d'outil ou qualification de la CNC n'est fournie. La fabrication décrite est industrielle ou équivalente avec contrôle de métallisation.

## Montage et contrôle

Utiliser la [BOM complète](../nomenclature-assemblage.csv), la [BOM porteuse](../KiCad/nomenclature.csv), les positions et les vues de montage. R7/R8 sont DNP sur la porteuse et installées côté Pi ; ne pas les remplacer par des straps. Les EVM et le Pololu2831 restent hors porteuse, reliés par faisceaux. Les modifications de résistances TI sont réalisées sur les modules selon [configuration](../modules/configuration.md). Au banc, les EVM sont posés séparément sur supports isolants, sans attendre leurs supports définitifs.

Avant de souder : PCB nu propre, contrôle des largeurs/cotes, pas de court-circuit visible, contrôle électrique, comparaison des empreintes et brochages aux fiches/échantillons. Puis montage par sous-ensembles selon B01-B03, avec sources limitées. Les cotes exactes de contour TI ne conditionnent aucune empreinte de ce PCB : [preuve et limites](../modules/cotes-ti.md).

Les fichiers incluent cuivre, masque, sérigraphie, contour, perçages séparés PTH/NPTH et netlist de test **IPC-D-356** ; **pas de stencil de pâte validé** ou d'assemblage automatisé promis. Les positions CSV facilitent la revue et le montage ; les boîtiers traversants ne se montent pas par pick-and-place CMS.

## Intégrité

[Manifest SHA256](manifest.json) : PCB/schéma contrôlés, exports, comptage et coordonnées des perçages, dimensions contour. Les vues SVG de cuivre et montage servent à la revue visuelle. Le ZIP contient ces fichiers et cette spécification ; ne pas commander une variante du PCB sans régénérer et revérifier ce lot.
'''
    (F/'README.md').write_text(readme,encoding='utf-8')
    files=[p for p in G.iterdir() if p.is_file()]+[F/'README.md',F/'positions-montage.csv',F/'netlist-controle-pcb.ipc']
    report=dict(revision='M1P',scope='Prototype carrier fabrication only, bounded bench, no battery release',hardware_tested=False,
      source_sha256=q['source_sha256'],native_tracks=len(tracks),power_tracks=sum(t['width']==.4 for t in tracks),signal_tracks=sum(t['width']==.2 for t in tracks),vias=len(vias),
      native_pth_count=pth,native_npth_count=npth,excellon_counts=drill_counts,hole_centers_exact_match=True,edge_dimensions_mm=[max(xs)-min(xs),max(ys)-min(ys)],
      files=[dict(path=str(p.relative_to(F)).replace('\\','/'),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(files)],commands=commands)
    dump(F/'manifest.json',report)
    packet=F/'surveillance-m1p-prototype-banc.zip'
    with zipfile.ZipFile(packet,'w',zipfile.ZIP_DEFLATED) as z:
        for p in files+[F/'manifest.json']:z.write(p,str(p.relative_to(F)))
    release=dict(revision='M1P',date='2026-10-15',prototype_carrier_fabrication_ready=True,bench_procedure_ready=True,hardware_tested=False,manufacturing_ready_for_vehicle=False,vehicle_battery_release=False,
      native_file_checks_passed=True,manufacturing_exports_geometry_checked=True,package=dict(file=str(packet.relative_to(B)).replace('\\','/'),sha256=sha(packet)),
      release_conditions=['Manufacturer accepts all finished copper/etch/plating specifications','Bare PCB continuity/isolation and assembly incoming inspection','Bench sources verified against B00 before connection','External modules supported separately and interfaces inspected','B00-B14 results not yet recorded'],
      unresolved_exact_TI_dimensions=True,remaining_for_vehicle=['Native TI mechanical data or measured modules and final support validation','Maximum clearing envelope / current limiting and full R2 branch coordination','Bench thermal, electrical and fault tests','Pi software shutdown and 2813 interaction','EMC, motor transients and integration tests'])
    dump(Q/'liberation-prototype.json',release)
    print(json.dumps({k:v for k,v in report.items() if k not in ['files','commands']},ensure_ascii=False),flush=True)

if __name__=='__main__':main()
