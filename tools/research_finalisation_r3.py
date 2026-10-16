"""Archive exact primary documents; missing downloads remain explicitly missing."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import urllib.request,json,hashlib,sys,zipfile,re,html
ROOT=Path(__file__).resolve().parents[1]
B=ROOT/'Composants/complements-finalisation-r3'
SOURCES=[
 ('TI-TPS3700EVM-gerbers.zip','https://www.ti.com/lit/zip/slvc413','TI original design files, source of nominal PCB geometry'),
 ('FEETECH-Pololu3429.html','https://www.pololu.com/product/3429','Identified seller variant; bursts over 9 A at 7.4 V reported by Pololu; not a maximum at 6 V'),
 ('FEETECH-horn3431.html','https://www.pololu.com/product/3431','Matching horn for Pololu 3429, not for an arbitrary 25T revision'),
 ('FEETECH-horn3431-drawing.pdf','https://www.pololu.com/file/0J1367/metal-servo-horn-for-feetech-giant-servo-ft5335m-dimensions.pdf','Original Pololu drawing; radius of supplied holes must be read, not assumed 20 mm'),
 ('KHK-SS.pdf','https://khkgears.net/pdf/ss.pdf','KHK SS specifications and torque tables; do not confuse surface durability with bending capacity'),
 ('KHK-spur-2025.pdf','https://khkgears.net/pdf/2025/spur-gears.pdf','2025 full spur catalogue, includes rating conditions and selection precautions'),
 ('Losi-LOS212054.html','https://www.horizonhobby.com/product/pinion-gear-16t-0.5m-2mm-shaft-mini-lmt/LOS212054.html','Original vendor confirms 16T m0.5 bore2; pressure angle not inferred'),
 ('Littelfuse-LFT.pdf','https://www.littelfuse.com/assetdocs/lft-datasheet?assetguid=56b8955c-9cf7-4814-a923-97a4406bfa77','Original drawing OL-LFT30060 and wire/torque table'),
 ('Littelfuse-CSA.pdf','https://www.littelfuse.com/assetdocs/csa-6225-01-007316?assetguid=203ad805-7e22-463f-997a-2431bbdfbbd1','CSA certificate lists LFT30060 20 kA dc; not a test report of the complete vehicle'),
 ('Littelfuse-JLLN.pdf','https://www.littelfuse.com/assetdocs/jlln-datasheet?assetguid=3a7bc9bf-d932-4401-bdc7-b39f302195cf','JLLN050 rating160VDC/20kA; low-voltage total clearing envelope not manufactured'),
 ('Littelfuse-LF-technical.pdf','https://m.littelfuse.com/~/media/electrical/brochures/littelfuse_lf_series_fuse_block_technical_brochure.pdf','Original LF-series block drawings and termination table'),
]
def fetch(row):
    name,url,note=row;p=B/'references'/name;p.parent.mkdir(parents=True,exist_ok=True)
    entry=dict(id=name,url=url,note=note,consulted_on='2026-10-16')
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
        with urllib.request.urlopen(req,timeout=18) as r:data=r.read()
        if name.endswith('.pdf'):assert data.startswith(b'%PDF')
        if name.endswith('.zip'):
            import io
            with zipfile.ZipFile(io.BytesIO(data)) as z:assert z.testzip() is None
        p.write_bytes(data);entry.update(archived=True,file='references/'+name,bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
    except Exception as e:entry.update(archived=False,error=str(e),verified_via_web=True)
    return entry
if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    if '--hitec' in sys.argv:
        existing=json.loads((B/'sources.json').read_text(encoding='utf-8'))
        extra=[
          ('Hitec-D950TW-US.html','https://hitecrcd.com/d950tw-wide-voltage-titanium-gear-25t-digital-coreless-servo/','Manufacturer expressly states4.8..8.4V, unlike nominal voltage columns'),
          ('Hitec-D950TW-CS.html','https://www.hiteccs.com/actuators/product-details/D950TW','Manufacturer data and CAD links'),
          ('Hitec-D950TW-EU.html','https://shop.hitec-europe.eu/collections/standard-servos/products/servo-d950tw','Official European site and original STEP link'),
          ('Hitec-D950TW-datasheet.pdf','https://www.hiteccs.com/public/uploads/data_sheet/HCS_D950TW_Specsheetv2.2_102-1729876661.pdf','Original Hitec V2.2 sheet; not D951TW')]
        with ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(fetch,extra))
        for entry in rows[:3]:
            if not entry.get('archived'):continue
            text=(B/entry['file']).read_text(encoding='utf-8',errors='replace')
            urls=re.findall(r'(?:href|data-url)=[\"\x27]([^\"\x27]+)[\"\x27]',text)
            for url in urls:
                url=html.unescape(url)
                if not any(ext in url.lower() for ext in ['.stp','.step','.zip']):continue
                if not any(key in url.lower() for key in ['950','cad']):continue
                if url.startswith('//'):url='https:'+url
                if url.startswith('/'):url=urllib.parse.urljoin(entry['url'],url)
                result=fetch(('Hitec-D950TW-original.stp',url,'Original manufacturer CAD linked by official product page'))
                rows.append(result);break
        ids={r['id'] for r in rows};existing=[r for r in existing if r['id'] not in ids]+rows
        (B/'sources.json').write_text(json.dumps(existing,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
        print(json.dumps([dict(id=r['id'],archived=r['archived'],error=r.get('error'),url=r['url']) for r in rows],ensure_ascii=False));sys.exit(0)
    with ThreadPoolExecutor(max_workers=6) as pool:rows=list(pool.map(fetch,SOURCES))
    (B/'sources.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps([dict(id=r['id'],archived=r['archived'],error=r.get('error')) for r in rows],ensure_ascii=False))
