from pathlib import Path
import json,hashlib,sys
from build_final_components_data import TITLES
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants'
sys.stdout.reconfigure(encoding='utf-8')
p=BASE/'coupure-manuelle/sources.json';v=json.loads(p.read_text(encoding='utf-8'));ref=BASE/'faisceau-puissance/notices/Klauke-catalogue-via-PowerCables.pdf'
v['sources']=[e for e in v['sources'] if e.get('id')!='Klauke-catalogue-reutilise']
v['sources'].append(dict(id='Klauke-catalogue-reutilise',file='../faisceau-puissance/notices/Klauke-catalogue-via-PowerCables.pdf',
 url='https://www.klauke.com/gb/en/tubular-cable-lugs-cu-standard-type-4959',status='archived',
 sha256=hashlib.sha256(ref.read_bytes()).hexdigest(),original_unmodified=True,note='Original déjà archivé, catalogue viaPowerCables ; tableau95R6 page14PDF /12imprimée. URL ici : pagefabricant actuelle de la famille. Voir assets du faisceau pour URL de téléchargement originale.'))
p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for folder in TITLES:
 b=BASE/folder;a=json.loads((b/'sources.json').read_text(encoding='utf-8'))
 docs=[];photos=[]
 for e in a['sources']:
  if e.get('status')!='archived':continue
  rel=e['file'];path=b/rel
  if path.suffix=='.pdf':docs.append(f"- [{path.name}]({'../'+rel}) - original non modifié ; SHA256 dans le répertoire des sources.")
  elif path.suffix in ['.jpg','.png']:photos.append(f"- [{path.name}]({Path(rel).name}) - [source]({e['url']}).")
 (b/'notices/README.md').write_text(f'# Notices et documents originaux\n\n[Notice V3](notice-{folder}-v3.pdf) : document du projet en français, distinct des notices fabricant.\n\n'+('\n'.join(docs) if docs else 'Aucun PDF fabricant propre au kit trouvé. Plans cotés en images et instructions publiques conservés dans les sources.')+'\n\n[Répertoire des originaux et empreintes](../sources.json). Les versions, désaccords de cotes et erreurs d’accès sont explicités ; les documents originaux restent inchangés.\n',encoding='utf-8')
 (b/'photos/README.md').write_text('# Photographies et plans de référence\n\n'+'\n'.join(photos)+'\n\nImages originales publiques non modifiées. Les PNG des dossiers3D sont des rendus de reconstruction, pas des photographies du matériel.\n',encoding='utf-8')
print('SOURCES indexed, existing Klauke PDF reused')
