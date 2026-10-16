"""Read heavy STEP zones as XCAF; avoid thousands of transient GUI objects."""
from pathlib import Path
import json,time,hashlib
import cadquery as cq
from prepare_pi5_step import read_xcaf,label_name,label_colour
from OCP.XCAFDoc import XCAFDoc_DocumentTool,XCAFDoc_ColorGen,XCAFDoc_ColorSurf
from OCP.TDF import TDF_LabelSequence,TDF_Label
from OCP.TopLoc import TopLoc_Location
from OCP.Quantity import Quantity_Color
ROOT=Path(__file__).resolve().parents[1];TMP=ROOT/'tools/temp/assemblage-viewers';OUT=TMP/'direct';OUT.mkdir(exist_ok=True)
def srgb(c):return tuple(12.92*x if x<=.0031308 else 1.055*x**(1/2.4)-.055 for x in c)
def main():
    rows=[]
    for zone in ['electronique','puissance']:
        print('XCAF',zone,flush=True);doc=read_xcaf(TMP/('drone-v3-'+zone+'.step'))
        st=XCAFDoc_DocumentTool.ShapeTool_s(doc.Main());ct=XCAFDoc_DocumentTool.ColorTool_s(doc.Main())
        roots=TDF_LabelSequence();st.GetFreeShapes(roots);assert roots.Length()==1
        root=roots.Value(1);children=TDF_LabelSequence();assert st.GetComponents_s(root,children)
        def walk(label,loc=TopLoc_Location(),col=(.65,.65,.65)):
            col=label_colour(label,ct,col)
            if st.IsReference_s(label):
                ref=TDF_Label();assert st.GetReferredShape_s(label,ref)
                yield from walk(ref,loc.Multiplied(st.GetLocation_s(label)),col);return
            sub=TDF_LabelSequence()
            if st.GetComponents_s(label,sub):
                for i in range(1,sub.Length()+1):yield from walk(sub.Value(i),loc,col)
            else:
                raw=st.GetShape_s(label)
                if raw.IsNull():return
                placed=cq.Shape.cast(raw.Moved(loc));fc=[]
                for face in cq.Shape.cast(raw).Faces():
                    c=Quantity_Color();color=col
                    for kind in [XCAFDoc_ColorSurf,XCAFDoc_ColorGen]:
                        if ct.GetColor(face.wrapped,kind,c):color=(c.Red(),c.Green(),c.Blue());break
                    fc.append(srgb(color))
                yield placed,fc
        for i in range(1,children.Length()+1):
            child=children.Value(i);name=label_name(child);print('COMPONENT',name,flush=True)
            exact=[];cols=[];simple=[];sc=[];omitted=0;proxies=0
            for shape,colors in walk(child):
                exact.append(shape);cols.extend(colors);b=shape.BoundingBox()
                if zone=='electronique' and (max(b.xlen,b.ylen,b.zlen)<2 or b.xlen*b.ylen*b.zlen<.2):omitted+=1;continue
                if zone=='electronique' and len(shape.Faces())>150:
                    shape=cq.Solid.makeBox(b.xlen,b.ylen,b.zlen,cq.Vector(b.xmin,b.ymin,b.zmin));colors=[colors[0]]*len(shape.Faces());proxies+=1
                simple.append(shape);sc.extend(colors)
            whole=cq.Compound.makeCompound(exact);view=cq.Compound.makeCompound(simple)
            filename=f'{zone}-{i:03d}.brep';vfilename=f'{zone}-{i:03d}-view.brep'
            whole.exportBrep(str(OUT/filename));view.exportBrep(str(OUT/vfilename))
            rows.append(dict(zone=zone,name=name,brep=filename,view_brep=vfilename,colors=cols,view_colors=sc,solids=len(whole.Solids()),faces=len(whole.Faces()),view_solids=len(view.Solids()),omitted=omitted,proxies=proxies))
        (OUT/'components.json').write_text(json.dumps(rows,separators=(',',':')),encoding='utf-8')
    print('DIRECT DONE',sum(r['solids'] for r in rows),len(rows),flush=True)
if __name__=='__main__':main()
