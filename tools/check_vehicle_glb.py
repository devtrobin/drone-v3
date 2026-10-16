"""Validate generated glTF binary buffers and geometric bounds."""
from pathlib import Path
import json,struct,hashlib,math
ROOT=Path(__file__).resolve().parents[1];BUILD=ROOT/'Assemblage/preparation'
if not (BUILD/'preparation.json').exists():BUILD=ROOT/'Assemblage'
def check(path):
    blob=path.read_bytes();magic,version,size=struct.unpack_from('<4sII',blob)
    assert magic==b'glTF' and version==2 and size==len(blob)
    jl,jt=struct.unpack_from('<I4s',blob,12);assert jt==b'JSON'
    d=json.loads(blob[20:20+jl]);bl,bt=struct.unpack_from('<I4s',blob,20+jl)
    assert bt==b'BIN\0' and 28+jl+bl==len(blob)
    binary=memoryview(blob)[28+jl:];assert len(binary)>=d['buffers'][0]['byteLength']
    access=d['accessors'];views=d['bufferViews'];triangles=0;bounds=[[math.inf]*3,[-math.inf]*3]
    for view in views:assert view.get('byteOffset',0)+view['byteLength']<=len(binary)
    for node in d['nodes']:assert 0<=node['mesh']<len(d['meshes'])
    for mesh in d['meshes']:
        for p in mesh['primitives']:
            pos=access[p['attributes']['POSITION']];normal=access[p['attributes']['NORMAL']];idx=access[p['indices']]
            assert pos['componentType']==5126 and pos['type']=='VEC3'
            assert pos['count']==normal['count'] and idx['componentType']==5125
            pv=views[pos['bufferView']];iv=views[idx['bufferView']]
            assert pv['byteLength']==pos['count']*12 and iv['byteLength']==idx['count']*4
            values=list(struct.iter_unpack('<3f',binary[pv.get('byteOffset',0):pv.get('byteOffset',0)+pv['byteLength']]))
            for point in values:assert all(math.isfinite(x) for x in point)
            # Accessor extrema are stored as doubles; values are float32.
            for k in range(3):
                assert abs(min(v[k] for v in values)-pos['min'][k])<1e-7
                assert abs(max(v[k] for v in values)-pos['max'][k])<1e-7
                bounds[0][k]=min(bounds[0][k],pos['min'][k]);bounds[1][k]=max(bounds[1][k],pos['max'][k])
            assert max(x[0] for x in struct.iter_unpack('<I',binary[iv.get('byteOffset',0):iv.get('byteOffset',0)+iv['byteLength']]))<pos['count']
            assert idx['count']%3==0;triangles+=idx['count']//3
            assert 0<=p['material']<len(d['materials'])
    # Reverse the mm/Z-up -> metre/Y-up display transform.
    xyz=[bounds[0][0]*1000,bounds[1][0]*1000,-bounds[1][2]*1000,-bounds[0][2]*1000,bounds[0][1]*1000,bounds[1][1]*1000]
    return dict(file=path.name,passed=True,bytes=len(blob),sha256=hashlib.sha256(blob).hexdigest(),meshes=len(d['meshes']),triangles=triangles,bounds_mm=xyz)
def main():
    report=json.loads((BUILD/'preparation.json').read_text(encoding='utf-8'))
    rows=[]
    for zone in report['zones']:
        r=check(BUILD/('drone-v3-'+zone['zone']+'.glb'))
        r['native_bounds_error_mm']=max(abs(x-y) for x,y in zip(r['bounds_mm'],zone['bounds_mm']))
        # Native BREP bounding boxes are conservative on B-splines; tyre
        # control-polygon bounds may exceed tessellated surfaces by ~2.8 mm.
        assert r['native_bounds_error_mm']<5,(r['file'],r['native_bounds_error_mm'])
        assert r['triangles']==zone['glb']['triangles'];rows.append(r)
    full=check(BUILD/'drone-v3-complet-ultra-detaille.glb')
    assert full['triangles']==sum(r['triangles'] for r in rows)
    assert full['meshes']==sum(r['meshes'] for r in rows)
    rows.append(full)
    (BUILD/'validation-glb.json').write_text(json.dumps(dict(all_passed=True,models=rows),ensure_ascii=False,indent=2),encoding='utf-8')
    print('GLB ALL PASS',[(r['file'],r['triangles']) for r in rows])
if __name__=='__main__':main()
