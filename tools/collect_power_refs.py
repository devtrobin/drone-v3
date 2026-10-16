"""Collect unmodified public primary references for the V3 power components.

No purchase, account access or original-document editing. All saved assets
have their source URL, byte count and SHA256. HTML is a dated snapshot, not a
claim of live Amazon France price or availability.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin
import urllib.request,re,json,hashlib,sys,html

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'Composants'
TEMP=ROOT/'tools/temp/power-review'
PAGES={
    'batterie':('zeee-produit','https://zeeebattery.com/products/zeee-2s-lipo-battery-5200mah-7-4v-80c-xt60-plug'),
    'regulateur-alimentation':('pololu-produit','https://www.pololu.com/product/2866'),
    'chargeur-batterie':('skyrc-produit','https://www1.skyrc.com/s65?from=nav'),
}


def sha(data):return hashlib.sha256(data).hexdigest()


def request(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=35) as response:
        data=response.read();final=response.geturl()
    assert data,'Empty public response: '+url
    return data,final


def asset(folder,file,url,kind):
    path=BASE/folder/file;path.parent.mkdir(parents=True,exist_ok=True)
    try:
        old_file=BASE/folder/'assets.json'
        old=json.loads(old_file.read_text(encoding='utf-8')) if old_file.exists() else {}
        recorded={a['file']:a for a in old.get('assets',[])}
        if path.exists() and recorded.get(file,{}).get('url')==url:data=path.read_bytes();final=url
        else:
            data,final=request(url)
            if file.endswith('.pdf'):assert data.startswith(b'%PDF'),url
            if file.endswith('.step'):assert b'ISO-10303-21' in data[:150],url
            path.write_bytes(data)
        return dict(file=file,url=url,final_url=final,kind=kind,bytes=len(data),sha256=sha(data),modified=False)
    except Exception as exc:return dict(file=file,url=url,kind=kind,error=str(exc))


def main():
    sys.stdout.reconfigure(encoding='utf-8');TEMP.mkdir(parents=True,exist_ok=True)
    work=[]
    for folder,(name,url) in PAGES.items():
        data,final=request(url)
        text=data.decode('utf-8','replace')
        (TEMP/(name+'.html')).write_bytes(data)
        work.append((folder,'sources-web/'+name+'.html',url,'manufacturer-page'))
        if folder=='batterie':
            # The product's first gallery consists of seven 1600-pixel photos.
            urls=list(dict.fromkeys(re.findall(r'[^\s\"\'<>]+(?:jpg|png)(?:\?[^\s\"\'<>]*)?',text)))
            urls=[u for u in urls if '/cdn/shop/files/' in u and '_1600x1600.' in u][:7]
            for i,u in enumerate(urls,1):work.append((folder,f'photos/{i:02d}-zeee-2s5200.jpg',urljoin(url,u),'manufacturer-photo'))
        elif folder=='regulateur-alimentation':
            work.append((folder,'notices/Raspberry-Pi-5-alimentation-USB-PD-livre-blanc-2026.pdf',
                'https://pip-assets.raspberrypi.com/categories/685-app-notes-guides-whitepapers/documents/RP-009856-WP-1-USB%2520Power%2520delivery%2520on%2520Raspberry%2520Pi%25205.pdf',
                'manufacturer-application-note'))
            resources,final=request(url+'/resources')
            (TEMP/'pololu-resources-9a.html').write_bytes(resources)
            links=re.findall(r'href=[\"\']([^\"\']+)',resources.decode('utf-8','replace'))
            for suffix,filename in [('.pdf','notices/Pololu-D24V60F5-D24V90F5-plan-cote.pdf'),
                                    ('.dxf','notices/Pololu-D24V60F5-D24V90F5-percages.dxf'),
                                    ('.step','3D/pololu-d24v90f5-officiel.step')]:
                chosen=[u for u in links if u.lower().endswith(suffix)]
                assert chosen,(folder,suffix)
                work.append((folder,filename,urljoin(url,chosen[0]),'manufacturer-cad' if suffix=='.step' else 'manufacturer-drawing'))
            # The gallery is JSON embedded in HTML; decode escaped quotes
            # before extracting the explicit full-resolution URL fields.
            photos_by_id={}
            for address,key,width,ext in re.findall(r'(https://a\.pololu-files\.com/picture/(0J\d+)\.(\d+)(?:x\d+)?\.(jpg|png))',text):
                if int(width)<600:continue
                if key not in photos_by_id or int(width)>photos_by_id[key][0]:
                    photos_by_id[key]=(int(width),address)
            photos=[u for w,u in photos_by_id.values()][:12]
            for i,u in enumerate(photos,1):work.append((folder,f'photos/{i:02d}-pololu-d24v90f5.'+('png' if '.png' in u else 'jpg'),html.unescape(u),'manufacturer-photo-or-graph'))
        else:
            work.append((folder,'notices/SkyRC-S65-notice-constructeur-EN-V2-10.pdf','https://www.skyrc.com/files/201/S65_Instruction_Manual_EN_V2.10.pdf','manufacturer-manual'))
            # Product hero graphics are CSS backgrounds; retain the original
            # CSS so its relative asset paths can be resolved accurately.
            css_url='https://www1.skyrc.com/catalog/view/theme/OPC080194_1/stylesheet/product/charger/s65/style.css?2019022101'
            css,final=request(css_url);(TEMP/'skyrc-s65.css').write_bytes(css)
            images=re.findall(r'url\(\s*[\"\']?([^\)\"\']+)',css.decode('utf-8','replace'))
            images=[u for u in images if any(e in u.lower() for e in ['.png','.jpg'])]
            images=[u for u in images if '/s65/' in u or not u.startswith('/')]
            for i,u in enumerate(list(dict.fromkeys(images))[:16],1):
                resolved=urljoin(css_url,u)
                ext='.png' if '.png' in u.lower() else '.jpg'
                work.append((folder,f'photos/{i:02d}-skyrc-s65'+ext,resolved,'manufacturer-photo-or-diagram'))
    collected={f:[] for f in PAGES}
    with ThreadPoolExecutor(max_workers=6) as pool:
        for task,result in zip(work,pool.map(lambda args:asset(*args),work)):
            folder=task[0];collected[folder].append(result)
            print(folder,result['file'],result.get('bytes',result.get('error')),flush=True)
    for folder,assets in collected.items():
        (BASE/folder/'assets.json').write_text(json.dumps(dict(checked_on='2026-10-13',assets=assets),indent=2)+'\n',encoding='utf-8')
    print('COLLECTED',sum('sha256' in x for a in collected.values() for x in a),'original assets',flush=True)


if __name__=='__main__':main()
