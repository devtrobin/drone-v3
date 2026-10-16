from pathlib import Path
import json,sys,zipfile
import cadquery as cq
from prepare_pi5_step import read_xcaf,collect_leaves
from build_running_gear_step import sha
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/connecteur-gpio';OUT=BASE/'3D'
sys.stdout.reconfigure(encoding='utf-8')
archive=OUT/'sources/Molex-22-55-2401-CAO-originale.zip'
with zipfile.ZipFile(archive) as z:b=z.read('022552401.stp')
source=OUT/'sources/022552401.stp';source.write_bytes(b)
doc=read_xcaf(source);leaves,whole,ct,roots,cols=collect_leaves(doc)
bb=whole.BoundingBox();print('NATIVE_BOUNDS',{k:getattr(bb,k) for k in ['xmin','xmax','ymin','ymax','zmin','zmax']})
print('NATIVE',len(leaves),len(whole.Solids()),len(whole.Faces()),whole.isValid())
for n,s,c,raw in leaves:print('LEAF',n,c, s.BoundingBox())
meta=dict(file='sources/022552401.stp',archive='sources/Molex-22-55-2401-CAO-originale.zip',
 source_zip_member='022552401.stp',sha256=sha(source),archive_sha256=sha(archive),native_vendor_cad=True,
 geometry_modified=False,unit='mm',solids=len(whole.Solids()),faces=len(whole.Faces()),valid=whole.isValid(),
 bounds_mm={k:getattr(bb,k) for k in ['xmin','xmax','ymin','ymax','zmin','zmax']})
(OUT/'source-native.json').write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8')
# Original embedded product image, unchanged.
import pymupdf
d=pymupdf.open(BASE/'notices/Molex-contact-fiche-originale-2013.pdf')
for page in d:
 for i,im in enumerate(page.get_images(full=True)):
  obj=d.extract_image(im[0])
  if obj['width']>60 and obj['height']>30:
   p=BASE/f'photos/Molex-contact-original-{i+1}.{obj["ext"]}';p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(obj['image'])
   print('IMAGE',p.name,obj['width'],obj['height'])
