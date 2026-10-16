"""Package only current chassis deliverables; exclude heavy concept images/cache."""
from pathlib import Path
import hashlib,json,zipfile

B=Path(__file__).resolve().parents[1]/'Composants/chassis'
target=B/'kit-chassis-a2-r1.zip'
files=[B/n for n in ['README.md','liste-debit.csv','pieces.json','implantation.json','verification/conception.json','3D/README.md','3D/provenance.json','3D/validation-freecad.json']]
files += sorted((B/'plans').glob('*'))
files += sorted((B/'3D').glob('*.step'))
files += sorted((B/'3D').glob('*.png'))
assert all(p.is_file() for p in files)
reportpath=B/'verification/fichiers.json'
report=json.loads(reportpath.read_text(encoding='utf-8'));assert report['all_passed']
summary={k:v for k,v in report.items() if k!='files'}
summary['scope']='Verified workspace export summary; no recursive archive hash in this embedded copy.'
with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for path in files:z.write(path,path.relative_to(B).as_posix())
    z.writestr('verification/fichiers.json',json.dumps(summary,ensure_ascii=False,indent=2))
    z.writestr('LIRE-AVANT-FABRICATION.txt',
        'Chassis A2-R1 - prototype non teste.\n'
        'Ouvrir plans/plans-chassis-a2-r1.pdf et README.md.\n'
        'Decoupes DXF : millimetres, echelle1:1, elevationZ0. Pas de G-code.\n'
        'Gabarits de corniere : usiner seulement le calque PERCAGE.\n'
        'Interfaces fournisseur non mesurees : report sur cassettes apres montage a blanc.\n'
        'La visserie finale, les carters du train, le montage interne et les essais restent distincts.\n'
        'Les liens vers les dossiers de composants sont relatifs au projet DroneV3 complet, non inclus dans ce ZIP.\n')
with zipfile.ZipFile(target) as z:
    assert z.testzip() is None
    assert len(z.namelist())==len(files)+2
    for path in files:assert z.read(path.relative_to(B).as_posix())==path.read_bytes()
# Refresh only the archive entry in the workspace manifest, avoiding a cyclic
#digest between an archive and a manifest embedded inside itself.
entry=dict(file=target.name,sha256=hashlib.sha256(target.read_bytes()).hexdigest())
report['files']=[r for r in report['files'] if r['file']!=target.name]+[entry]
report['archive_integrity_checked']=True
reportpath.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(archive=target.name,files=len(files)+2,bytes=target.stat().st_size,integrity=True),indent=2))
