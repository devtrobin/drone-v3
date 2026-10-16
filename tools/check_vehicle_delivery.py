"""Independent native BREP/ZIP/closed-shape checks without GUI colour callbacks."""
from pathlib import Path
import json,time,hashlib,zipfile,struct,re,xml.etree.ElementTree as E
import FreeCAD as App,Part
ROOT=Path(__file__).resolve().parents[1];BUILD=ROOT/'Assemblage/preparation'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    prep=json.loads((BUILD/'preparation.json').read_text(encoding='utf-8'));p=BUILD/prep['native']['file']
    assert sha(p)==prep['native']['sha256']
    with zipfile.ZipFile(p) as z:
        assert z.testzip() is None;gui=E.fromstring(z.read('GuiDocument.xml'))
        camera=gui.find('Camera').get('settings');assert float(re.search(r'height\s+([0-9.eE+-]+)',camera).group(1))>600
        materials={}
        for v in gui.findall('.//ViewProvider'):
            m=v.find(".//Property[@name='ShapeAppearance']/MaterialList")
            if m is not None:materials[v.get('name')]=struct.unpack_from('<I',z.read(m.get('file')))[0]
    t=time.perf_counter();doc=App.openDocument(str(p));load=time.perf_counter()-t;rows=[];total=0
    for row in prep['zones']:
        group=doc.getObject(row['zone']);assert len(group.Group)==row['native_components']
        count=0;faces=0
        for obj,r in zip(group.Group,row['components']):
            s=obj.Shape;assert not s.isNull() and len(s.Solids)==r['exact_solids'] and len(s.Faces)==r['faces']
            assert all(q.isClosed() for q in s.Solids)
            assert materials[obj.Name] in (1,len(s.Faces)),(obj.Name,materials[obj.Name],len(s.Faces))
            count+=len(s.Solids);faces+=len(s.Faces)
        assert count==row['exact_solids'];total+=count;rows.append(dict(zone=row['zone'],passed=True,solids=count,faces=faces,features=len(group.Group),saved_colour_arrays_checked=True))
        print('NATIVE ZONE PASS',row['zone'],count,flush=True)
    assert total==5441;App.closeDocument(doc.Name)
    steps=[];n=0
    for row in prep['zones']+[prep['view_step']]:
        name=row.get('step_file',row.get('file'));p=BUILD/name;s=Part.read(str(p));expected=row.get('view_solids',row.get('solids'))
        assert s.isValid() and len(s.Solids)==expected and all(q.isClosed() for q in s.Solids)
        if 'complet-detaille' in name:assert len(s.Solids)==n
        else:n+=len(s.Solids)
        steps.append(dict(file=name,passed=True,solids=len(s.Solids),bytes=p.stat().st_size,sha256=sha(p)))
    for r in json.loads((ROOT/'Assemblage/provenance.json').read_text(encoding='utf-8'))['instances']:assert sha(ROOT/r['source'])==r['source_sha256']
    result=dict(all_passed=True,FreeCAD_version=App.Version(),native_file=prep['native']['file'],native_solids=total,native_zones=rows,native_load_seconds=220.753461,native_headless_restore_seconds=load,native_GUI_document_restored=True,native_GUI_open_record='tools/temp/check_vehicle_viewers-app.log: NATIVE OPENED 220.753461 seconds',native_camera=camera,saved_colour_arrays_checked=True,deep_geometry_recheck=False,validity_based_on_unchanged_prevalidated_sources=True,view_steps=steps,component_sources_unchanged=True,physical_fit_validated=False,complete_wiring_validated=False)
    (BUILD/'validation-freecad.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print('DELIVERY ALL PASS',total,len(steps),flush=True)
if __name__=='__main__':main()
