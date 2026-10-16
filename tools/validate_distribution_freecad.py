"""Independent headless FreeCAD import of every delivered distribution STEP."""
from pathlib import Path
import FreeCAD,Part,json,hashlib,time,sys
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/distribution-alimentation';OUT=BASE/'3D'
def main():
    sys.stdout.reconfigure(encoding='utf-8');cat=json.loads((OUT/'catalogue.json').read_text(encoding='utf-8'));checks=[]
    old=json.loads((OUT/'validation-freecad.json').read_text(encoding='utf-8')) if (OUT/'validation-freecad.json').exists() else {}
    previous={c['file']:c for c in old.get('checks',[])} if old.get('version')==FreeCAD.Version() else {}
    for entry in cat['models']:
        p=ROOT/'Composants'/entry['folder']/'3D'/entry['file']
        m=json.loads(p.with_suffix('.json').read_text(encoding='utf-8'));m['folder']=entry['folder']
        assert hashlib.sha256(p.read_bytes()).hexdigest()==m['sha256']
        if m['file'] in previous and previous[m['file']].get('passed') and previous[m['file']]['sha256']==m['sha256']:
            checks.append(dict(previous[m['file']],reused_unchanged_file_check=True))
            print('FREECAD',p.name,'PASS (unchanged SHA256, earlier import)',flush=True);continue
        start=time.perf_counter();s=Part.read(str(p));seconds=time.perf_counter()-start;b=s.optimalBoundingBox()
        bb=dict(xmin=b.XMin,xmax=b.XMax,ymin=b.YMin,ymax=b.YMax,zmin=b.ZMin,zmax=b.ZMax)
        error=max(abs(v-m['bounds_mm'][k]) for k,v in bb.items());passed=s.isValid() and all(sol.isClosed() for sol in s.Solids) and len(s.Solids)==m['validation']['solids'] and error<.01
        checks.append(dict(file=m['file'],folder=m['folder'],passed=passed,valid=s.isValid(),solids=len(s.Solids),faces=len(s.Faces),bbox_error_mm=error,seconds=seconds,sha256=m['sha256']))
        print('FREECAD',p.name,'PASS' if passed else 'FAIL',round(seconds,2),'s',flush=True)
    result=dict(method='FreeCAD Part.read, headless',version=FreeCAD.Version(),checked_on='2026-10-14',
        GUI_tested=False,VSCode_CAD_View_tested=False,all_passed=all(c['passed'] for c in checks),checks=checks)
    (OUT/'validation-freecad.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');assert result['all_passed']
if __name__=='__main__':main()
