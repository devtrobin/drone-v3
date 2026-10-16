"""Archive public original references for the principal MIDI fuse pair."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import urllib.request,json,hashlib,sys
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'Composants/protection-surintensite'
TASKS=[
 ('porte-fusible/notices/Littelfuse-MIDI-498-fiche-2015.pdf','https://static.chipdip.ru/lib/455/DOC012455921.pdf'),
 ('porte-fusible/notices/Littelfuse-MIDI-498-plan-catalogue-2012.pdf','https://www.datasheets.com/littelfuse/0498125.MXT/datasheet.pdf'),
 ('porte-fusible/notices/Littelfuse-MIDI-498-fiche-2025.pdf','https://www.littelfuse.com/assetdocs/littelfuse-fuse-holder-midi-498-datasheet-rd1?assetguid=b38a61f3-7d0b-4081-bfb5-86c4b4ea4f26'),
 ('fusible-60a/notices/Littelfuse-MIDI-32V-fiche-2024.pdf','https://www.littelfuse.com/assetdocs/midi-32v-bolt-down-series-data-sheet?assetguid=b55e8034-180d-40f6-a0a7-bebc2d4a94f5'),
 ('sources-web/CAD-Littelfuse-formulaire.html','https://info.littelfuse.com/midi-498-series-3dmodel-landingpage'),
 ('sources-web/TME-04980900ZXT.html','https://www.tme.eu/en/details/04980900zxt/car-fuseholders/littelfuse/'),
 ('sources-web/Amazon-recherche-support.html','https://www.amazon.fr/s?k=Littelfuse+04980900ZXT'),
 ('sources-web/Amazon-recherche-fusible.html','https://www.amazon.fr/s?k=Littelfuse+0498060.M'),
 ('porte-fusible/notices/Littelfuse-MIDI-498-fiche-miroir-TME.pdf','https://www.tme.eu/Document/751067cde59f8870ba92d17db0ce52da/04980900ZXT.pdf'),
 ('fusible-60a/notices/Littelfuse-MIDI-32V-fiche-miroir-TME.pdf','https://www.tme.eu/Document/c2a31dbed623c79f9b3491c387e36665/littelfuse_midi.pdf'),
 ('fusible-60a/notices/Littelfuse-MIDI-32V-revision-2021.pdf','https://4donline.ihs.com/images/VipMasterIC/IC/LFSI/LFSI-S-A0013274556/LFSI-S-A0013277374-1.pdf?hkey=6D3A4C79FDBF58556ACFDE234799DDF0'),
 ('fusible-60a/photos/distributeur-0498060M.jpg','https://uk.farnell.com/productimages/standard/en_GB/3516004-40.jpg'),
]
def fetch(task):
    filename,url=task;p=BASE/filename;p.parent.mkdir(parents=True,exist_ok=True)
    record=dict(file=filename,url=url,checked_on='2026-10-14',modified=False)
    try:
        if p.exists():
            data=p.read_bytes();final=url
            manifest=BASE/'assets.json'
            if manifest.exists():
                prior=next((a for a in json.loads(manifest.read_text(encoding='utf-8'))['assets'] if a['file']==filename),None)
                if prior and prior.get('sha256')==hashlib.sha256(data).hexdigest():return dict(prior,checked_on='2026-10-14')
        else:
            with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=25) as r:data=r.read();final=r.geturl()
            if filename.endswith('.pdf'):assert data.startswith(b'%PDF'),'not a PDF'
            p.write_bytes(data)
        status='challenge_html' if b'bm-verify' in data else 'downloaded'
        record.update(bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),final_url=final,status=status)
    except Exception as exc:record.update(status='unavailable',error=str(exc))
    return record
def main():
    sys.stdout.reconfigure(encoding='utf-8');BASE.mkdir(parents=True,exist_ok=True)
    with ThreadPoolExecutor(max_workers=5) as pool:records=list(pool.map(fetch,TASKS))
    p=BASE/'assets.json';old=json.loads(p.read_text(encoding='utf-8'))['assets'] if p.exists() else []
    indexed={r['file']:r for r in old};indexed.update({r['file']:r for r in records})
    p.write_text(json.dumps(dict(checked_on='2026-10-14',assets=list(indexed.values())),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for r in records:print(r['file'],r.get('bytes',r.get('error')),flush=True)
if __name__=='__main__':main()
