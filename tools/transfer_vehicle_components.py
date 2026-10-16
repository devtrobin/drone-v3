"""Direct original STEP to placed BREP, retaining XCAF face colours."""
from pathlib import Path
import json,time
import cadquery as cq
from prepare_pi5_step import read_xcaf,collect_leaves
from OCP.Quantity import Quantity_Color
from OCP.XCAFDoc import XCAFDoc_ColorSurf,XCAFDoc_ColorGen
from OCP.XCAFDoc import XCAFDoc_DocumentTool
from OCP.TDF import TDF_ChildIterator
from OCP.TopAbs import TopAbs_FACE
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'tools/temp/assemblage-viewers/direct';OUT.mkdir(exist_ok=True)
def srgb(c):return tuple(12.92*x if x<=.0031308 else 1.055*x**(1/2.4)-.055 for x in c[:3])
def main():
    source_rows=json.loads((ROOT/'Assemblage/provenance.json').read_text(encoding='utf-8'))['instances']
    source_rows=[r for r in source_rows if r['group'] in ('electronique','puissance')]
    cache={};rows=[];indices={}
    for record in source_rows:
        zone=record['group'];rel=record['source'];name=record['name']
        if rel not in cache:
            print('READ ORIGINAL',rel,flush=True)
            started=time.perf_counter();doc=read_xcaf(ROOT/rel)
            print('TRANSFERRED',round(time.perf_counter()-started,2),'s',flush=True)
            leaves,whole,ct,nroots,ncolors=collect_leaves(doc)
            # Read colour attributes directly from labelled faces. Asking the
            # colour tool to FIND every unlabelled face repeatedly is quadratic
            # on large boards; the label graph already contains all styles.
            st=XCAFDoc_DocumentTool.ShapeTool_s(doc.Main());palette={}
            it=TDF_ChildIterator(doc.Main(),True)
            while it.More():
                label=it.Value();c=Quantity_Color()
                for kind in [XCAFDoc_ColorSurf,XCAFDoc_ColorGen]:
                    if ct.GetColor_s(label,kind,c):
                        raw=st.GetShape_s(label)
                        if not raw.IsNull() and raw.ShapeType()==TopAbs_FACE:palette[cq.Shape.cast(raw)]=srgb((c.Red(),c.Green(),c.Blue()))
                        break
                it.Next()
            print('LEAVES',len(leaves),'FACE STYLES',len(palette),flush=True)
            data=[]
            for leaf_name,shape,base,raw in leaves:
                colors=[]
                for f in cq.Shape.cast(raw).Faces():
                    colors.append(palette.get(f,srgb(base)))
                data.append((leaf_name,shape,colors))
            cache[rel]=data
        print('PLACE',name,flush=True)
        pos,angles=record['location'];location=cq.Location(tuple(pos),tuple(angles))
        exact=[];cols=[];simple=[];sc=[];omitted=0;proxies=0
        for leaf_name,source,colors in cache[rel]:
            local=source.translate((0,0,3)) if name=='ED80' and 'tete_M5' in leaf_name else source
            shape=local.moved(location);exact.append(shape);cols.extend(colors);b=shape.BoundingBox()
            if zone=='electronique' and (max(b.xlen,b.ylen,b.zlen)<2 or b.xlen*b.ylen*b.zlen<.2):omitted+=1;continue
            if zone=='electronique' and len(shape.Faces())>150:
                shape=cq.Solid.makeBox(b.xlen,b.ylen,b.zlen,cq.Vector(b.xmin,b.ymin,b.zmin));colors=[colors[0]]*len(shape.Faces());proxies+=1
            simple.append(shape);sc.extend(colors)
        whole=cq.Compound.makeCompound(exact);view=cq.Compound.makeCompound(simple)
        indices[zone]=indices.get(zone,0)+1;i=indices[zone]
        filename=f'{zone}-{i:03d}.brep';vfilename=f'{zone}-{i:03d}-view.brep'
        whole.exportBrep(str(OUT/filename));view.exportBrep(str(OUT/vfilename))
        rows.append(dict(zone=zone,name=name,brep=filename,view_brep=vfilename,colors=cols,view_colors=sc,solids=len(whole.Solids()),faces=len(whole.Faces()),view_solids=len(view.Solids()),omitted=omitted,proxies=proxies))
        print('BREP READY',name,len(whole.Solids()),flush=True)
    assert len(rows)==17 and sum(r['solids'] for r in rows)==5015,(len(rows),sum(r['solids'] for r in rows))
    (OUT/'components.json').write_text(json.dumps(rows,separators=(',',':')),encoding='utf-8')
    print('TRANSFER DONE',len(rows),sum(r['solids'] for r in rows),flush=True)
if __name__=='__main__':main()
