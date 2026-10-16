"""Concatenate generated GLB buffers without remeshing or changing surfaces."""
from pathlib import Path
import json,struct,hashlib
ROOT=Path(__file__).resolve().parents[1];BUILD=ROOT/'Assemblage/preparation';OUT=ROOT/'tools/temp/assemblage-viewers'
def main():
    result=dict(asset=dict(version='2.0',generator='Drone V3 - concatenation of exact surface previews'),scene=0,scenes=[dict(nodes=[])],nodes=[],meshes=[],materials=[],buffers=[],bufferViews=[],accessors=[])
    binary=bytearray();zones=[]
    for zone in ['structure','roulage','electronique','puissance']:
        data=(BUILD/('drone-v3-'+zone+'.glb')).read_bytes();jl=struct.unpack_from('<I',data,12)[0];d=json.loads(data[20:20+jl]);raw=data[28+jl:]
        nv=len(result['bufferViews']);na=len(result['accessors']);nm=len(result['materials']);nmesh=len(result['meshes'])
        while len(binary)%4:binary.append(0)
        offset=len(binary);binary.extend(raw)
        for v in d['bufferViews']:v['byteOffset']=v.get('byteOffset',0)+offset;result['bufferViews'].append(v)
        for a in d['accessors']:a['bufferView']+=nv;result['accessors'].append(a)
        for m in d['meshes']:
            for p in m['primitives']:
                p['attributes']={k:v+na for k,v in p['attributes'].items()};p['indices']+=na;p['material']+=nm
            result['meshes'].append(m)
        result['materials'].extend(d['materials'])
        for n in d['nodes']:n['mesh']+=nmesh;result['nodes'].append(n)
        zones.append(dict(zone=zone,meshes=len(d['meshes'])))
    result['scenes'][0]['nodes']=list(range(len(result['nodes'])));result['buffers']=[dict(byteLength=len(binary))]
    j=json.dumps(result,separators=(',',':')).encode();j+=b' '*((-len(j))%4)
    path=OUT/'complete-display-cache.glb';path.write_bytes(struct.pack('<4sII',b'glTF',2,28+len(j)+len(binary))+struct.pack('<I4s',len(j),b'JSON')+j+struct.pack('<I4s',len(binary),b'BIN\0')+binary)
    (OUT/'display-cache-zones.json').write_text(json.dumps(zones),encoding='utf-8')
    print(path,len(binary))
if __name__=='__main__':main()
