"""Archive unchanged vendor data and record unavailable downloads explicitly."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import urllib.request, json, hashlib, sys

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'Composants/dissipateur-relais'
TASKS=[
 ('sources-web/Sensata-HS251.html','https://www.sensata.com/products/relays/hs-series-heat-sinks-hs251'),
 ('notices/Sensata-HS251-datasheet.pdf','https://www.sensata.com/sites/default/files/a/sensata-hs251-heatsink-datasheet.pdf?cb=495b66ac'),
 ('notices/Sensata-HS251-plan.pdf','https://www.sensata.com/sites/default/files/a/sensata-hs251-heatsink-accessories-drawing.pdf?cb=e71f1c2f'),
 ('3D/sensata-hs251-officiel.step','https://www.sensata.com.cn/sites/default/files/a/sensata-hs251-heatsink-accessories-drawing.step'),
 ('photos/Sensata-HS251.jpg','https://www.sensata.com/sites/default/files/styles/p_img_active/public/media/images/2024-09-23/sensata-hs251-heatsink-accessories-product-image.jpg?cb=2c8a372b&itok=TLV5xU17'),
 ('notices/Sensata-HS-installation.pdf','https://www.sensata.com/sites/default/files/a/sensata-hs-series-installation-guide.pdf'),
 ('notices/Sensata-HSP-datasheet-actuelle.pdf','https://www.tti.com/content/dam/tti-commons/supplier/sensata/doc/sensata-hsp-series-thermal-pads-datasheet-and-specifications.pdf'),
 ('notices/Sensata-HSP-datasheet-historique-2018.pdf','https://www.sensata.com/sites/default/files/media/documents/2018-04-04/ourproducts_thermal_pads_hsp.pdf'),
 ('notices/Crydom-HS251-datasheet-miroir-2017.pdf','https://www.ic-relays.com/pdf-6a/hs251.pdf'),
 ('notices/Sensata-HS-installation-miroir-RS.pdf','https://docs.rs-online.com/766e/A700000009477596.pdf'),
 ('notices/Sensata-HSP-PCN-SSR-231214.pdf','https://www.ttiasia.com/content/dam/ttiinc/products/PCN/sensata/Sensata-PCN-SSR-231214.pdf'),
 ('notices/Sensata-HS-brochure-miroir-RS.pdf','https://docs.rs-online.com/cf62/A700000010035084.pdf'),
 ('notices/Sensata-HS251-datasheet-miroir-Farnell.pdf','https://www.farnell.com/datasheets/4619827.pdf'),
 ('photos/distributeur-HS251.jpg','https://www.newark.com/productimages/standard/en_US/41X7868-40.jpg'),
 ('notices/Sensata-HSP-datasheet-miroir-Farnell.pdf','https://www.farnell.com/datasheets/4600889.pdf'),
 ('notices/Sensata-HSP-PCN-miroir-Farnell.pdf','https://www.farnell.com/datasheets/4129384.pdf'),
 ('notices/Sensata-HSP-plan-miroir-Farnell.pdf','https://www.farnell.com/cad/4775092.pdf'),
]

def fetch(task):
    name,url=task;path=BASE/name;path.parent.mkdir(parents=True,exist_ok=True)
    record=dict(file=name,url=url,checked_on='2026-10-13',modified=False)
    try:
        if path.exists():
            data=path.read_bytes();final=url
            manifest=BASE/'assets.json'
            if manifest.exists():
                prior=next((a for a in json.loads(manifest.read_text(encoding='utf-8'))['assets'] if a['file']==name),None)
                if prior and prior.get('sha256')==hashlib.sha256(data).hexdigest():
                    return dict(prior,checked_on='2026-10-13')
        else:
            with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=25) as response:
                data=response.read();final=response.geturl()
            if name.endswith('.pdf'): assert data.startswith(b'%PDF'), 'not a PDF'
            if name.endswith('.step'): assert b'ISO-10303-21' in data[:150], 'not a STEP'
            if name.endswith('.jpg'): assert data[:2]==b'\xff\xd8', 'not a JPEG'
            path.write_bytes(data)
        record.update(final_url=final,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),status='downloaded')
    except Exception as exc: record.update(status='unavailable',error=str(exc))
    return record

def main():
    sys.stdout.reconfigure(encoding='utf-8');BASE.mkdir(parents=True,exist_ok=True)
    with ThreadPoolExecutor(max_workers=5) as pool: records=list(pool.map(fetch,TASKS))
    for record in records: print(record['file'],record.get('bytes',record.get('error')),flush=True)
    manifest=BASE/'assets.json'
    old=json.loads(manifest.read_text(encoding='utf-8'))['assets'] if manifest.exists() else []
    indexed={r['file']:r for r in old}
    indexed.update({r['file']:r for r in records})
    manifest.write_text(json.dumps(dict(checked_on='2026-10-13',assets=list(indexed.values())),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
