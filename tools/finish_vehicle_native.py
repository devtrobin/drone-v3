"""Finish the native document from direct XCAF/BREP component transfers."""
import os,sys,json,hashlib
from pathlib import Path
os.environ.setdefault('QT_QPA_PLATFORM','offscreen')
import FreeCAD as App,FreeCADGui as Gui,Part
if not App.GuiUp:Gui.showMainWindow()
import ImportGui
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bounds(s):
    b=s.BoundBox
    return [b.XMin,b.XMax,b.YMin,b.YMax,b.ZMin,b.ZMax]
sys.stdout=sys.__stdout__
ROOT=Path(__file__).resolve().parents[1];TMP=ROOT/'tools/temp/assemblage-viewers';BUILD=ROOT/'Assemblage/preparation'
def main():
    report=json.loads((BUILD/'progress.json').read_text(encoding='utf-8'))
    assert [r['zone'] for r in report['zones']]==['structure','roulage']
    records=json.loads((TMP/'direct/components.json').read_text(encoding='utf-8'))
    assert len(records)==17 and sum(r['solids'] for r in records)==5015
    native=App.openDocument(str(BUILD/'seed-assemblage.FCStd'))
    visual=App.newDocument('VisuelsDirects')
    groups={}
    for zone in ['electronique','puissance']:
        ng=native.addObject('App::DocumentObjectGroup',zone);ng.Label=zone.capitalize()
        vg=visual.addObject('App::DocumentObjectGroup',zone);vg.Label=zone.capitalize();groups[zone]=vg
        exact=[];simplified=[];entries=[]
        for i,r in enumerate(x for x in records if x['zone']==zone):
            print('BREP',r['name'],flush=True)
            s=Part.read(str(TMP/'direct'/r['brep']));v=Part.read(str(TMP/'direct'/r['view_brep']))
            assert len(s.Solids)==r['solids'] and len(s.Faces)==r['faces']
            assert len(s.Faces)==len(r['colors']) and len(v.Faces)==len(r['view_colors'])
            n=native.addObject('Part::Feature','Detail_'+zone+'_'+str(i));ng.addObject(n)
            n.Label=r['name'];n.Shape=s;n.ViewObject.DiffuseColor=[tuple(c) for c in r['colors']]
            n.ViewObject.DisplayMode='Shaded';n.ViewObject.Deviation=.25;n.ViewObject.AngularDeflection=20
            n.addProperty('App::PropertyString','Representation','Provenance');n.Representation='BREP intégral transféré directement du XCAF source, avec couleurs par face'
            o=visual.addObject('Part::Feature','Visu_'+zone+'_'+str(i));vg.addObject(o);o.Label=r['name'];o.Shape=v
            o.ViewObject.DiffuseColor=[tuple(c) for c in r['view_colors']]
            exact.append(s);simplified.append(v)
            entries.append(dict(component=r['name'],exact_solids=r['solids'],faces=r['faces'],view_solids=r['view_solids'],electronic_leaves_omitted=r['omitted'],envelope_proxies=r['proxies']))
        whole=Part.makeCompound(exact);vs=Part.makeCompound(simplified)
        assert len(whole.Solids)==({'electronique':4882,'puissance':133}[zone])
        report['zones'].append(dict(zone=zone,exact_solids=len(whole.Solids),exact_faces=len(whole.Faces),native_components=len(ng.Group),view_solids=len(vs.Solids),bounds_mm=bounds(whole),volume_mm3=None,centre_mm=None,original_source_bounds_match=None,original_volume_and_centre_match=None,step_file='drone-v3-'+zone+'.step',components=entries,glb=None))
    native.recompute();App.setActiveDocument(native.Name)
    p=BUILD/'drone-v3-complet-ultra-detaille.FCStd';native.saveAs(str(p))
    report['native']=dict(file=p.name,bytes=p.stat().st_size,sha256=sha(p),solids=sum(r['exact_solids'] for r in report['zones']),features=sum(r['native_components'] for r in report['zones']))
    assert report['native']['solids']==5441 and report['native']['features']==194
    print('NATIVE SAVED',report['native'],flush=True)
    visual.recompute()
    for row in report['zones'][2:]:
        p=BUILD/row['step_file'];ImportGui.export(groups[row['zone']].Group,str(p))
        row['step_bytes']=p.stat().st_size;row['step_sha256']=sha(p)
        print('STEP',p.name,p.stat().st_size,flush=True)
    report['view_step']=dict(file='drone-v3-complet-detaille.step',bytes=None,sha256=None,solids=sum(r['view_solids'] for r in report['zones']))
    report['full_glb']=None;report['all_original_BREP_solids_preserved']=True
    (BUILD/'preparation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print('NATIVE AND VIEW ZONES READY',flush=True);sys.stdout.flush();os._exit(0)
if __name__=='__main__':main()
