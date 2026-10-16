from collect_pi_cooler_refs import fetch,BASE
import json,re,sys
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin
TASKS=[
 ('sources-web/Amazon-COM-B0CLXZBR5P.html','https://www.amazon.com/dp/B0CLXZBR5P'),
 ('sources-web/Amazon-FR-B0CLXZBR5P.html','https://www.amazon.fr/dp/B0CLXZBR5P'),
 ('sources-web/Waveshare-produit.html','https://www.waveshare.com/product/accessories/power-heat-sinks/raspberry-pi-5-official-active-cooler.htm'),
 ('sources-web/PiHut-produit.html','https://thepihut.com/products/active-cooler-for-raspberry-pi-5'),
 ('sources-web/Desertcart-achat-reprise.html','https://www.desertcart.us/products/642583692-raspberry-pi-active-cooler-for-raspberry-pi-5-active-cooler')]
def main():
    sys.stdout.reconfigure(encoding='utf-8')
    with ThreadPoolExecutor(max_workers=3) as pool:r=list(pool.map(fetch,TASKS))
    for a in r:print(a['file'],a['status'],a.get('bytes',a.get('error')))
    wave=BASE/'sources-web/Waveshare-produit.html';extra=[]
    if wave.exists():
        s=wave.read_text(encoding='utf-8',errors='replace')
        urls=list(dict.fromkeys(re.findall(r'(?:src|href)=[\"\']([^\"\']+)',s)))
        for i,u in enumerate([u for u in urls if 'active-cooler' in u.lower() and '.jpg' in u.lower()][:8]):
            extra.append(('photos/Waveshare-produit-'+str(i+1)+'.jpg',urljoin('https://www.waveshare.com/',u)))
    if extra:
        with ThreadPoolExecutor(max_workers=4) as pool:r+=list(pool.map(fetch,extra))
    for a in r:
        if a['status']=='downloaded' and a['file'].endswith('.html'):
            text=(BASE/a['file']).read_text(encoding='utf-8',errors='replace')
            print('ASIN_CANDIDATES',a['file'],sorted(set(re.findall(r'\bB0[A-Z0-9]{8}\b',text))))
    p=BASE/'assets.json';d=json.loads(p.read_text(encoding='utf-8'));d['assets']=[a for a in d['assets'] if a['file'] not in {x['file'] for x in r}]+r
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
