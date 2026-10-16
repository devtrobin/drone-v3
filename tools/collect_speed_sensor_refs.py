"""Archive public evidence for the wheel-speed package; no purchase."""
from pathlib import Path
import concurrent.futures
import hashlib
import html
import json
import re
import sys
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'Composants/capteurs-vitesse'
SOURCES = [
 ('ti-datasheet','https://www.ti.com/lit/pdf/slis152','notices/TI-DRV5033-original.pdf'),
 ('ti-package','https://www.ti.com/lit/pdf/MPBC003B','notices/TI-LPG0003A-plan-original.pdf'),
 ('ti-part','https://www.ti.com/product/DRV5033/part-details/DRV5033AJQLPG','references/TI-DRV5033AJQLPG.html'),
 ('ti-forum-distance','https://e2e.ti.com/support/sensors-group/sensors/f/sensors-forum/816464/drv5033-hall-sensing-distance','references/TI-E2E-distance.html'),
 ('magnet','https://www.supermagnete.fr/aimants-disques-neodyme/disque-magnetique-3mm-2mm_S-03-02-N','references/supermagnete-S-03-02-N.html'),
 ('resistor','https://www.vishay.com/docs/28724/mrs16m25.pdf','notices/Vishay-MRS16-MRS25-original.pdf'),
 ('capacitor','https://search.kemet.com/component-documentation/download/specsheet/C315C104K5R5TA','notices/KEMET-C315C104K5R5TA-original.pdf'),
 ('rs-sensor','https://fr.rs-online.com/web/p/capteurs-a-effet-hall/9009807','references/RS-9009807.html'),
 ('rs-be-sensor','https://befr.rs-online.com/web/p/motion-sensor-ics/9009807','references/RS-BE-9009807.html'),
 ('amazon-sensor-search','https://www.amazon.fr/s?k=DRV5033AJQLPG','references/Amazon-capteur.html'),
 ('amazon-magnet-search','https://www.amazon.fr/s?k=supermagnete+S-03-02-N','references/Amazon-aimant.html'),
]


def fetch(item):
    ident,url,rel=item
    entry=dict(id=ident,url=url,checked_on='2026-10-15')
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=25) as r:
            data=r.read(); final=r.geturl(); mime=r.headers.get('Content-Type','')
        if not data or (rel.endswith('.pdf') and not data.startswith(b'%PDF')):
            raise ValueError('Expected original PDF not returned')
        p=BASE/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
        entry.update(local=rel,status='archived_original',bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),final_url=final,mime=mime)
    except Exception as exc:
        entry.update(status='not_archived',error=str(exc))
    return entry


def main():
    sys.stdout.reconfigure(encoding='utf-8');BASE.mkdir(parents=True,exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        assets=list(executor.map(fetch,SOURCES))
    page=BASE/'references/supermagnete-S-03-02-N.html'
    if page.exists():
        text=html.unescape(page.read_text(encoding='utf-8',errors='replace'))
        links=list(dict.fromkeys(re.findall(r'(?:href|src)=["\']([^"\']+)["\']',text)))
        for url in links:
            if 'S-03-02-N' in url or ('pdf' in url.lower() and 'product' in url.lower()):
                print('MAGNET_LINK',url,flush=True)
    for asset in assets:print(asset['id'],asset['status'],asset.get('bytes',asset.get('error')),flush=True)
    (BASE/'assets.json').write_text(json.dumps(dict(checked_on='2026-10-15',assets=assets),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':main()
