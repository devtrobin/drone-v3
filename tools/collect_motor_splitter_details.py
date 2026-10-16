"""Archive official manuals and images discovered in the actual public product page."""
from collect_motor_splitter_refs import BASE,fetch
from concurrent.futures import ThreadPoolExecutor
import json,sys
TASKS=[
 ('notices/nVent-UD80A-instructions-IP7802.pdf','https://nvent.widen.net/content/vhxyvvgeqg/original/ip7802.pdf'),
 ('notices/nVent-UD-specifications.pdf','https://nvent.widen.net/content/ngmdxkxgcd/original/pi-ud_blocks_specs.pdf'),
 ('notices/nVent-UD-catalogue-P1215C.pdf','https://nvent.widen.net/content/yuoao2u6nw/original/p1215c-uken.pdf'),
 ('photos/nVent-UD80A-produit-original.webp','https://www.nvent.com/sites/default/files/styles/product_and_sku_image_582x334_no_crop/public/dam/0c9zfrqlic/ph22076.png.webp?itok=LSVDrJR-'),
 ('photos/nVent-UD80A-plan-face.webp','https://www.nvent.com/sites/default/files/styles/convert_only/public/dam/7rmakguwwo/il42001.png.webp?itok=W5CAQZ0z'),
 ('photos/nVent-UD80A-plan-profil.webp','https://www.nvent.com/sites/default/files/styles/convert_only/public/dam/mebscodrm7/il42002.png.webp?itok=n22vmi--'),
 ('photos/nVent-UD80A-plan-connexions.webp','https://www.nvent.com/sites/default/files/styles/convert_only/public/dam/q2lflunxr1/il42003.png.webp?itok=ZZmWOe6W'),
 ('sources-web/Forum-PLCtalk-SCCR.html','https://www.plctalk.net/forums/threads/sccr-in-the-feeder.125932/'),
]
def main():
    sys.stdout.reconfigure(encoding='utf-8')
    with ThreadPoolExecutor(max_workers=5) as pool:records=list(pool.map(fetch,TASKS))
    manifest=json.loads((BASE/'assets.json').read_text(encoding='utf-8'));old={a['file']:a for a in manifest['assets']};old.update({a['file']:a for a in records})
    for a in old.values():
        if a['file']=='sources-web/nVent-UD80A.html':
            a['status']='downloaded_with_product_content';a['note']='Full product attributes, download URLs and photos present; site also contains challenge script.'
    manifest['assets']=list(old.values());(BASE/'assets.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for a in records:print(a['file'],a['status'],a.get('bytes',a.get('error')),flush=True)
if __name__=='__main__':main()
