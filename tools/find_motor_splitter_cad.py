"""Inspect public manufacturer CAD download code; no authentication or posting."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import re,html,urllib.request,sys
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/repartition-moteurs';TMP=ROOT/'tools/temp/motor-splitter-review/cad-discovery'
def main():
    sys.stdout.reconfigure(encoding='utf-8');TMP.mkdir(parents=True,exist_ok=True)
    source=(BASE/'sources-web/nVent-UD80A.html').read_text(encoding='utf-8')
    urls=[html.unescape(s) for s in re.findall(r'<script[^>]*src="([^"]+)"',source) if '/sites/default/files/js/' in s]
    def fetch(pair):
        i,url=pair
        try:
            with urllib.request.urlopen(urllib.request.Request('https://www.nvent.com'+url,headers={'User-Agent':'Mozilla/5.0'}),timeout=15) as r:b=r.read()
            p=TMP/f'manufacturer-{i}.js';p.write_bytes(b)
            t=b.decode('utf-8',errors='ignore');segments=[m.group() for m in re.finditer(r'.{0,90}(?:data-product-id|download-card__cad|CADFile|cadfile|cad-file|cadDownload|GetCAD|downloadCad|DownloadCAD|cad-files).{0,350}',t)]
            return '\n'.join(segments)
        except Exception as e:return str(e)
    with ThreadPoolExecutor(max_workers=4) as pool:
        for text in pool.map(fetch,enumerate(urls)):print(text[:7000],flush=True)
if __name__=='__main__':main()
