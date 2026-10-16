"""Preview the bounding-box layout model, explicitly labelling simplification."""
from pathlib import Path
import numpy as np
from prepare_pi5_step import read_xcaf,collect_leaves
from render_step_meshes import render_meshes

def main():
    out=Path(__file__).resolve().parents[1]/'Composants/raspberry-pi-5/3D'
    leaves,_,_,_,_=collect_leaves(read_xcaf(out/'raspberry-pi-5-encombrement-simplifie.step'))
    meshes=[]
    for _,shape,color,_ in leaves:
        vertices,triangles=shape.tessellate(.2,.3)
        color=np.array(color)
        color=np.where(color<=.0031308,12.92*color,1.055*np.power(color,1/2.4)-.055)
        meshes.append((np.array([v.toTuple() for v in vertices]),triangles,color))
    render_meshes(out/'vue-encombrement-simplifie.png',meshes,(.6,-.8,1.1),
                  'Pi 5 | Encombrement approximatif - formes simplifiees',
                  'Derive de la CAO officielle - boites approximatives, sans trous ni cavites')

if __name__=='__main__':main()
