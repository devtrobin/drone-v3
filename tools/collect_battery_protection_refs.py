"""Keep primary references intact for the proposed V3 battery supervision."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin
import urllib.request,json,hashlib,re,sys

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'Composants/protection-batterie'
TEMP=ROOT/'tools/temp/protection-review'
TASKS=[
 ('surveillance-2s','notices/TI-TLV6700-datasheet.pdf','https://www.ti.com/lit/ds/symlink/tlv6700.pdf'),
 ('surveillance-2s','notices/Vishay-VOS618A-datasheet.pdf','https://www.vishay.com/docs/83465/vos618a.pdf'),
 ('surveillance-2s','notices/Microchip-MCP1703A-datasheet.pdf','https://ww1.microchip.com/downloads/aemDocuments/documents/APID/ProductDocuments/DataSheets/MCP1703-Data-Sheet-DS20005122.pdf'),
 ('surveillance-2s','notices/Diodes-BAT54-datasheet.pdf','https://www.diodes.com/datasheet/download/BAT54.pdf'),
 ('surveillance-2s','notices/TI-SN74LVC2G17-datasheet.pdf','https://www.ti.com/lit/ds/symlink/sn74lvc2g17.pdf'),
 ('coupure-moteurs','notices/Sensata-Crydom-1-DC-D1D100-datasheet.pdf','https://www.farnell.com/datasheets/3917448.pdf'),
 ('interrupteur-pi','sources-web/Pololu-2813.html','https://www.pololu.com/product/2813'),
 ('interrupteur-pi','sources-web/Pololu-2813-resources.html','https://www.pololu.com/product/2813/resources'),
 ('surveillance-2s','sources-web/TI-TLV6700.html','https://www.ti.com/product/TLV6700'),
 ('interrupteur-pi','sources-web/retour-auto-demarrage.html','https://forum.pololu.com/t/problem-with-pushbutton-power-switch-item-2813-auto-on-with-power-fluctuation/13660'),
 ('interrupteur-pi','sources-web/retour-arret-pi.html','https://forum.pololu.com/t/raspberry-pi-can-it-turn-itself-off-with-the-mini-pushbutton-power-switch/21371'),
 ('surveillance-2s','sources-web/Pi-overlays-README.txt','https://raw.githubusercontent.com/raspberrypi/firmware/master/boot/overlays/README'),
]

def fetch(task):
    folder,file,url=task;p=BASE/folder/file;p.parent.mkdir(parents=True,exist_ok=True)
    try:
        if p.exists():data=p.read_bytes();final=url
        else:
            request=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
            with urllib.request.urlopen(request,timeout=30) as response:data=response.read();final=response.geturl()
            assert data
            if file.endswith('.pdf'):assert data.startswith(b'%PDF')
            if file.endswith('.step'):assert b'ISO-10303-21' in data[:150]
            p.write_bytes(data)
        return dict(file=file,url=url,final_url=final,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),modified=False)
    except Exception as exc:return dict(file=file,url=url,error=str(exc))

def main():
    sys.stdout.reconfigure(encoding='utf-8');TEMP.mkdir(parents=True,exist_ok=True)
    records={name:[] for name in ['surveillance-2s','interrupteur-pi','coupure-moteurs']}
    with ThreadPoolExecutor(max_workers=5) as pool:
        for task,record in zip(TASKS,pool.map(fetch,TASKS)):
            records[task[0]].append(record);print(task[0],task[1],record.get('bytes',record.get('error')),flush=True)
    page=(BASE/'interrupteur-pi/sources-web/Pololu-2813.html').read_text(encoding='utf-8')
    resources=(BASE/'interrupteur-pi/sources-web/Pololu-2813-resources.html').read_text(encoding='utf-8')
    links=re.findall(r'href=[\"\']([^\"\']+)',resources)
    extras=[]
    for extension,stem,folder in [('.pdf','notices/', 'interrupteur-pi'),('.step','3D/', 'interrupteur-pi'),('.dxf','notices/', 'interrupteur-pi')]:
        for link in links:
            if not link.lower().endswith(extension):continue
            filename='pololu-2813-officiel.step' if extension=='.step' else link.rsplit('/',1)[-1]
            extras.append((folder,stem+filename,urljoin('https://www.pololu.com',link)))
    photos={}
    for url,key,width,extension in re.findall(r'(https://a\.pololu-files\.com/picture/(0J\d+)\.(\d+)(?:x\d+)?\.(jpg|png))',page):
        if int(width)>=600 and (key not in photos or int(width)>photos[key][0]):photos[key]=(int(width),url,extension)
    for i,(_,url,extension) in enumerate(list(photos.values())[:11],1):extras.append(('interrupteur-pi',f'photos/{i:02d}-pololu-2813.{extension}',url))
    with ThreadPoolExecutor(max_workers=5) as pool:
        for task,record in zip(extras,pool.map(fetch,extras)):
            records[task[0]].append(record);print(task[0],task[1],record.get('bytes',record.get('error')),flush=True)
    for folder,assets in records.items():
        (BASE/folder/'assets.json').write_text(json.dumps(dict(checked_on='2026-10-13',assets=assets),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('References saved:',sum('sha256' in a for data in records.values() for a in data),flush=True)

if __name__=='__main__':main()
