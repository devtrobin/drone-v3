"""Small STEP layout views; all detailed surfaces remain in native CAD and GLB."""
from pathlib import Path
import os,sys,json,hashlib,shutil
import FreeCAD as App,FreeCADGui as Gui,Part,ImportGui
ROOT=Path(__file__).resolve().parents[1];BUILD=ROOT/'Assemblage/preparation'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    prep=json.loads((BUILD/'preparation.json').read_text(encoding='utf-8'))
    source=App.newDocument('ImplantationSource')
    ImportGui.insert(name=str(ROOT/'Composants/chassis/3D/chassis-a2-r1-implante.step'),docName=source.Name,merge=False,useLinkGroup=False)
    root=source.RootObjects[0]
    target=App.newDocument('ImplantationV3Legere');groups={z:target.addObject('App::DocumentObjectGroup',z) for z in ['structure','roulage','electronique','puissance']}
    power=('HS251_','D1D100_','D_plus_','D_moins_','UD80A_','ED80_')
    rolling=('Pneu','Jante','FT90M_','Servo_palonnier','Moteur2435_','Moteur_','Engrenage_','A7_','Axe_avant_','Arbre_sortie')
    electronic=('Pi5_','Pi_ports','Pi_GPIO','Pi_ActiveCooler','Pi_ventilateur','M1P_porteuse','ESC_','D42V55F5_','Pololu2813_','WAGO413_','WAGO415_','Camera_CAM_')
    def leaves(obj):
        if hasattr(obj,'Group'):
            for c in obj.Group:yield from leaves(c)
        elif hasattr(obj,'Shape') and not obj.Shape.isNull():yield obj
    for i,obj in enumerate(leaves(root)):
        name=obj.Label
        zone='puissance' if name.startswith(power) else 'roulage' if name.startswith(rolling) else 'electronique' if name.startswith(electronic) else 'structure'
        o=target.addObject('Part::Feature','Vue_'+str(i));groups[zone].addObject(o);o.Label=name
        s=obj.Shape.copy();s.Placement=obj.getGlobalPlacement();o.Shape=s
        o.ViewObject.ShapeColor=tuple(obj.ViewObject.ShapeColor)
        colors=list(obj.ViewObject.DiffuseColor)
        if len(colors)>1:o.ViewObject.DiffuseColor=colors
    target.recompute();total=0
    App.ParamGet('User parameter:BaseApp/Preferences/Mod/Part/STEP').SetString('Scheme','AP214IS')
    for row in prep['zones']:
        group=groups[row['zone']];p=BUILD/row['step_file'];ImportGui.export(group.Group,str(p))
        row['view_solids']=sum(len(o.Shape.Solids) for o in group.Group);total+=row['view_solids']
        row['step_bytes']=p.stat().st_size;row['step_sha256']=sha(p);row['view_representation']='Implantation A2-R1 simplifiée, détails dans FCStd et GLB'
        print('LIGHT STEP',p.name,p.stat().st_size,row['view_solids'],flush=True)
    p=BUILD/prep['view_step']['file']
    # Reuse the original verified light assembly directly, without another
    # nested assembly/style round trip. The four partitions retain its frame.
    shutil.copyfile(ROOT/'Composants/chassis/3D/chassis-a2-r1-implante.step',p)
    prep['view_step'].update(bytes=p.stat().st_size,sha256=sha(p),solids=total)
    prep['step_preview_simplifications']=['STEP : modèle d’implantation A2-R1 à formes simples et volumes réservés, 225 solides au total','Petits composants, pistes, pneus sculptés, dentures, interfaces et faisceaux détaillés sont dans les FCStd / GLB','Les STEP d’implantation ne qualifient pas les interfaces mécaniques ni les interférences locales']
    prep['view_step_source']='Composants/chassis/3D/chassis-a2-r1-implante.step'
    prep['view_step_source_sha256']=sha(ROOT/prep['view_step_source'])
    assert total==225,total
    (BUILD/'preparation.json').write_text(json.dumps(prep,ensure_ascii=False,indent=2),encoding='utf-8')
    print('LIGHT STEPS DONE',total,flush=True);sys.stdout.flush();os._exit(0)
if __name__=='__main__':main()
