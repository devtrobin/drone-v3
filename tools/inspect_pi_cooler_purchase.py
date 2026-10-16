from pathlib import Path
import re,html,json,sys,pymupdf
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/refroidissement-raspberry-pi-5'
def clean(s):return re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]+>',' ',s))).strip()
def main():
    sys.stdout.reconfigure(encoding='utf-8');s=(BASE/'sources-web/Amazon-FR-B0CLXZBR5P.html').read_text(encoding='utf-8',errors='replace')
    m=re.search(r'id="productTitle"[^>]*>(.*?)</span>',s,re.S);print('TITLE',clean(m[1]) if m else None)
    for token in ['corePrice_feature_div','apex_desktop','availability','sellerProfileTriggerId','merchant-info','deliveryBlockMessage','productDetails_techSpec_section_1','acrCustomerReviewText','averageCustomerReviews']:
        m=re.search(r'id="'+re.escape(token)+'"',s)
        if m:print(token,clean(s[m.start():m.start()+4000])[:950])
    visible=re.sub(r'<(?:script|style).*?</(?:script|style)>','',s,flags=re.S);text=clean(visible)
    for token in ['Expédié par','Vendu par','SC1148','TVA']:
        m=re.search(re.escape(token),text,re.I)
        if m:print('DETAIL',token,text[max(0,m.start()-40):m.start()+500])
    bodies=re.findall(r'data-hook="review-body"[^>]*>(.*?)</span>',visible,re.S)
    print('REVIEW_BODIES',[clean(t)[:650] for t in bodies[:6]])
    if '--purchase' in sys.argv:return
    p=pymupdf.open(BASE/'notices/RaspberryPi-ActiveCooler-plan-reference-original.pdf')[0]
    ds=p.get_drawings();print('DRAWING_SUMMARY',[(i,list(d['rect']),len(d['items']),d['type'],d['color'],d['fill']) for i,d in enumerate(ds)])
    paths=[]
    for d in ds:
        for item in d['items']:
            pts=[a for a in item[1:] if isinstance(a,pymupdf.Point)]
            if pts and all(195.5<q.x<222 and 226<q.y<253 for q in pts):paths.append([item[0],*[list(q) for q in pts]])
    print('LOGO_SEGMENTS',len(paths),paths[:3]);(BASE/'cotes-logo-vecteur.json').write_text(json.dumps(dict(source='notices/RaspberryPi-ActiveCooler-plan-reference-original.pdf',source_page=1,
        region_pdf_points=[195.5,226,222,253],segments=paths,reference_drawing_only=True),indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
