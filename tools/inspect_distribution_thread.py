"""Check visible helical geometry by radial occupancy, not just STEP validity."""
from pathlib import Path
import cadquery as cq,sys,json
ROOT=Path(__file__).resolve().parents[1]
def main():
    sys.stdout.reconfigure(encoding='utf-8')
    shape=cq.importers.importStep(str(ROOT/'Composants/distribution-alimentation/bornier-2315/3D/bluesea-2305-borniers-sans-capot-detaille.step')).val()
    studs=[s for s in shape.Solids() if s.BoundingBox().zmax>28 and s.BoundingBox().xlen<5]
    print('STUDS',len(studs))
    s=studs[0];b=s.BoundingBox();x=(b.xmin+b.xmax)/2
    for r in [2.02,2.2,2.35]:
        values=[s.isInside(cq.Vector(x+r,0,22+i*.05),1e-6) for i in range(48)]
        print('r',r,'filled',sum(values),'faces',len(s.Faces()),'surface types',sorted(set(f.geomType() for f in s.Faces())))
if __name__=='__main__':main()
