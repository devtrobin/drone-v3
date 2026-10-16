"""Render the delivered complete GLB itself for visual review."""
from pathlib import Path
import json,struct
import numpy as np
from render_step_meshes import render_meshes
ROOT=Path(__file__).resolve().parents[1];BUILD=ROOT/'Assemblage/preparation'
if not (BUILD/'preparation.json').exists():BUILD=ROOT/'Assemblage'
def main():
    data=(BUILD/'drone-v3-complet-ultra-detaille.glb').read_bytes()
    length=struct.unpack_from('<I',data,12)[0];d=json.loads(data[20:20+length]);binary=memoryview(data)[28+length:]
    meshes=[]
    for mesh in d['meshes']:
        for p in mesh['primitives']:
            a=d['accessors'][p['attributes']['POSITION']];v=d['bufferViews'][a['bufferView']]
            pts=np.frombuffer(binary,dtype='<f4',count=a['count']*3,offset=v.get('byteOffset',0)).reshape(-1,3).astype(float)
            # glTF metres/Y-up back to CAD millimetres/Z-up.
            pts=np.column_stack((pts[:,0],-pts[:,2],pts[:,1]))*1000
            a=d['accessors'][p['indices']];v=d['bufferViews'][a['bufferView']]
            tri=np.frombuffer(binary,dtype='<u4',count=a['count'],offset=v.get('byteOffset',0)).reshape(-1,3)
            c=np.array(d['materials'][p['material']]['pbrMetallicRoughness']['baseColorFactor'][:3])
            c=np.where(c<=.0031308,12.92*c,1.055*c**(1/2.4)-.055)
            meshes.append((pts,tri,c))
    for name,view in [('isometrique',(.65,-.9,.85)),('dessus',(0,0,1))]:
        render_meshes(BUILD/('apercu-assemblage-'+name+'.png'),meshes,view,'Drone V3 | Assemblage complet A2-R1','Apercu du GLB detaille - volumes reserves conserves - montage physique a qualifier')
        print('RENDER',name,flush=True)
if __name__=='__main__':main()
