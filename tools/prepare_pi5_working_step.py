"""Produce a small, explicitly simplified layout STEP from official Pi 5 CAD.

Keep the full official sources separately; never pass this off as exhaustive CAD.
"""
from pathlib import Path
import hashlib, json, time, zipfile
import cadquery as cq
from prepare_pi5_step import read_xcaf, collect_leaves

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'Composants/raspberry-pi-5/3D'
SOURCE = OUT / 'raspberry-pi-5-4go-ultra-detaille.step'
ARCHIVE = OUT / 'raspberry-pi-5-officiel-sans-graphismes.zip'
EXPECTED_ZIP = '6841637b4cfa97637bf34b529bfe896f24d9634b2c40b57a156781f55d88f06f'
TARGET = OUT / 'raspberry-pi-5-implantation-legere.step'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    assert sha(ARCHIVE) == EXPECTED_ZIP
    with zipfile.ZipFile(ARCHIVE) as archive:
        assert archive.testzip() is None
        original = archive.read('rpi-5b_no_graphics.step')
        assert SOURCE.read_bytes() == original
    started = time.perf_counter()
    leaves, whole, _, roots, colors = collect_leaves(read_xcaf(SOURCE))
    source_import_seconds=time.perf_counter()-started
    print('Official import seconds',source_import_seconds,flush=True)
    source_valid = whole.isValid()
    assert source_valid
    assembly = cq.Assembly(name='Raspberry_Pi_5_layout_simplified')
    kept, omitted = [], []
    for index,(name,shape,color,raw) in enumerate(leaves):
        bb = shape.BoundingBox()
        # Exact retained shapes, no proxy boxes. This intentionally omits small
        # surface components; keep large parts and elongated connector contacts.
        keep = bool(shape.Solids()) and max(bb.xlen,bb.ylen,bb.zlen) >= 4 and bb.xlen*bb.ylen*bb.zlen >= 1
        entry = {'index':index,'name':name,'bounds_mm':[bb.xmin,bb.xmax,bb.ymin,bb.ymax,bb.zmin,bb.zmax]}
        if keep:
            assembly.add(shape,name=f'part_{index:04d}',color=cq.Color(*color))
            kept.append(entry)
        else:
            omitted.append(entry)
    # Save a separate bounding-box envelope model for fast opening. Its boxes
    # intentionally do not reproduce holes or the detailed connector cavities.
    envelope=cq.Assembly(name='Raspberry_Pi_5_envelope_approximate')
    for entry in kept:
        xmin,xmax,ymin,ymax,zmin,zmax=entry['bounds_mm']
        proxy=cq.Workplane('XY').box(xmax-xmin,ymax-ymin,zmax-zmin,centered=False).translate((xmin,ymin,zmin)).val()
        color=leaves[entry['index']][2]
        envelope.add(proxy,name=f'envelope_{entry["index"]:04d}',color=cq.Color(*color))
    envelope_path=OUT/'raspberry-pi-5-encombrement-simplifie.step'
    envelope.save(str(envelope_path))
    _,envelope_shape,_,_,_=collect_leaves(read_xcaf(envelope_path))
    assert envelope_shape.isValid() and len(envelope_shape.Solids())==len(kept)
    print('Envelope exported and validated',envelope_path.stat().st_size,'bytes',flush=True)
    candidate = OUT / 'raspberry-pi-5-implantation-legere.candidate.step'
    assembly.save(str(candidate))
    print('Compact exported',len(kept),'parts',candidate.stat().st_size,'bytes',flush=True)
    check_start=time.perf_counter()
    check_leaves,check,_,_,check_colors=collect_leaves(read_xcaf(candidate))
    assert check.isValid()
    kept_shape=cq.Compound.makeCompound([s for n,s,c,r in leaves if bool(s.Solids()) and max(s.BoundingBox().xlen,s.BoundingBox().ylen,s.BoundingBox().zlen)>=4 and s.BoundingBox().xlen*s.BoundingBox().ylen*s.BoundingBox().zlen>=1])
    expected_bb=kept_shape.BoundingBox();bb=check.BoundingBox();original_bb=whole.BoundingBox()
    error=max(abs(getattr(bb,k)-getattr(expected_bb,k)) for k in ['xmin','xmax','ymin','ymax','zmin','zmax'])
    assert error<1e-4 and len(check.Solids())==len(kept_shape.Solids())
    full_error=max(abs(getattr(bb,k)-getattr(original_bb,k)) for k in ['xmin','xmax','ymin','ymax','zmin','zmax'])
    candidate.replace(TARGET)
    data={'prepared_on':'2026-10-13','source':SOURCE.name,'source_sha256':sha(SOURCE),'source_archive_sha256':sha(ARCHIVE),
          'source_import_seconds':source_import_seconds,'preparation_before_check_seconds':check_start-started,'source_valid':source_valid,'source_leaves':len(leaves),'source_solids':len(whole.Solids()),'source_faces':len(whole.Faces()),
          'file':TARGET.name,'sha256':sha(TARGET),'bytes':TARGET.stat().st_size,'retained_parts':len(kept),'omitted_parts':len(omitted),
          'selection':'Solid-bearing parts with longest bounding-box side >= 4 mm and bounding-box volume >= 1 mm3; exact retained geometry, all other parts omitted',
          'validation':{'valid':True,'import_seconds':time.perf_counter()-check_start,'solids':len(check.Solids()),'faces':len(check.Faces()),'colors':check_colors,'retained_bbox_error_mm':error,'original_bbox_error_mm':full_error},
          'envelope_model':{'file':envelope_path.name,'sha256':sha(envelope_path),'bytes':envelope_path.stat().st_size,'solids':len(envelope_shape.Solids()),'valid':True,'geometry':'Bounding-box proxies of the same selected parts; no holes, curved outlines or connector cavities; not a fabrication model'},
          'limitations':['Simplified layout model, not an ultra detailed replacement','Small components and graphics omitted; consult original for local clearance','Actual 4GB memory variant and board revision not certified','FreeCAD GUI and VSCode CAD View not tested in this environment'],
          'kept':kept,'omitted':omitted}
    (OUT/'validation-versions-travail.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in data.items() if k not in ('kept','omitted')}),flush=True)

if __name__=='__main__':
    main()
