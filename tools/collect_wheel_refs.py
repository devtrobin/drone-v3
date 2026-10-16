"""Download the unmodified product photos for the selected wheel ASIN."""
from pathlib import Path
import urllib.request, hashlib, json

OUT=Path(__file__).resolve().parents[1]/'Composants/roues'
IDS=['71b3NqikBXL','71wcgoRimJL','7187ZYAZswL','81GE2a5k9IL','8101osXgWhL','81dIXHqIfNL','81EiKinNTOL','81xDa6V93dL']

def main():
    photos=OUT/'photos';photos.mkdir(parents=True,exist_ok=True)
    assets=[]
    for i,key in enumerate(IDS,1):
        url=f'https://m.media-amazon.com/images/I/{key}._AC_SL1500_.jpg'
        path=photos/f'{i:02d}-hobbypark-color-a.jpg'
        if not path.exists():
            with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=40) as r:path.write_bytes(r.read())
        assets.append({'file':'photos/'+path.name,'url':url,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size,'modified':False})
        print(path.name,path.stat().st_size,flush=True)
    (photos/'assets.json').write_text(json.dumps({'asin':'B0CTNVV7BJ','checked_on':'2026-10-13','source_page':'https://www.amazon.com/dp/B0CTNVV7BJ','assets':assets},indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':main()
