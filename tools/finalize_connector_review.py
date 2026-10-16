"""Record completed manual preview/PDF review and synchronize new integration notes."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/connecteurs-alimentation'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    meta=BASE/'notices/notice-connecteurs-xt60h-v3.json';m=read(meta)
    assert m['pages']==4 and all((ROOT/p['render']).is_file() for p in m['renders'])
    m.update(visual_review_complete=True,review_note='All four rendered pages visually reviewed: no clipping, overlap or missing glyphs; all eight final CAD previews reviewed.')
    save(meta,m)
    assets=BASE/'assets.json';a=read(assets)
    for r in a['assets']:
        if r['file'].endswith('.html') and (BASE/r['file']).exists():
            blob=(BASE/r['file']).read_bytes()
            if any(t in blob for t in [b'validateCaptcha',b'bm-verify',b'challenge-platform']):r['status']='challenge_html'
    save(assets,a)
    calc=ROOT/'Composants/protection-branches-moteurs/calculs.json';c=read(calc)
    c.update(XT60H_tail_proposal_AWG=12,XT60H_tail_nominal_mm2=3.31,added_4mm2_is_loss_example_not_godet_fit=True,
        XT60H_reference='AMASS XT60H-F with cap, two proposed; contact current unqualified')
    save(calc,c)
    bom=ROOT/'Composants/protection-branches-moteurs/nomenclature.json';b=read(bom)
    b['connectors_proposed']=dict(reference='AMASS XT60H-F with caps',quantity=2,existing_ESC_males_retained=True)
    b['missing']=[t.replace('branch wiring, connectors, crimped joints and retention','branch wiring, qualification of selected XT60H-F, crimped joints and retention') for t in b['missing']]
    save(bom,b)
    print('Review and integration notes recorded')
if __name__=='__main__':main()
