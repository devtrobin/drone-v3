"""Fetch observed original public documents; retain failed downloads as such."""
from collect_harness_refs import fetch,BASE,ROOT
from concurrent.futures import ThreadPoolExecutor
import json,pymupdf,sys
TASKS=[
 ('photos/Klauke-photo-original','https://cdn.klauke.com/resources/images/58f368e6-8c3c-46db-9776-cd561880f2d7'),
 ('photos/Klauke-dessin-original','https://cdn.klauke.com/resources/images/6be6e875-a5d3-4ec9-b70a-b47478924bca'),
 ('notices/Klauke-catalogue-via-PowerCables.pdf','https://www.powerandcables.com/wp-content/uploads/2018/09/Klauke-Cable-Lug-Connectors-Tools-Crimping-Cutting-Section-1.pdf'),
 ('notices/TE-ATUM-fiche-via-Raytronics.pdf','https://raytronics.ch/phocadownloadpap/Datasheets/heat_shrink_tube_with_adhesive/Heat%20shrink%20tube%20with%20adhesive%20ATUM%203%20to%201%204%20to%201%20environmentally%20sealing%20Raytronics%20AG.pdf')]
def main():
    sys.stdout.reconfigure(encoding='utf-8')
    with ThreadPoolExecutor(max_workers=4) as pool:r=list(pool.map(fetch,TASKS))
    p=BASE/'assets.json';a=json.loads(p.read_text(encoding='utf-8'));a['assets']=[x for x in a['assets'] if x['file'] not in {v['file'] for v in r}]+r;p.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for x in r:print(x['file'],x['status'],x.get('bytes',x.get('error')),flush=True)
    tmp=ROOT/'tools/temp/harness-review/sources';tmp.mkdir(parents=True,exist_ok=True)
    for x in r:
        if x['status']=='downloaded' and x['file'].endswith('.pdf'):
            d=pymupdf.open(BASE/x['file'])
            for i,pg in enumerate(d):
                text=pg.get_text()
                if '95R4' in text or 'ATUM-8/2' in text:
                    print('SOURCE_PAGE',x['file'],i+1,text[:2000].replace('\n',' | '),flush=True)
                    pg.get_pixmap(matrix=pymupdf.Matrix(1.5,1.5)).save(tmp/f'{(BASE/x["file"]).stem}-p{i+1}.png')
if __name__=='__main__':main()
