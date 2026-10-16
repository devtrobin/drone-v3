"""Export exact flat DXFs, purchase-interface notes and project navigation."""
from pathlib import Path
import json,csv,hashlib,re,math,zipfile,sys
import cadquery as cq
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'Composants/finalisation-theorique-r2';V=B/'verification'
def write(p,t):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t.strip()+'\n',encoding='utf-8')
def dump(p,o):write(p,json.dumps(o,indent=2,ensure_ascii=False))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def csvout(p,rows):
    with p.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=';');w.writeheader();w.writerows(rows)
def prepend(p,marker,text):
    old=p.read_text(encoding='utf-8');start='<!-- '+marker+' -->';end='<!-- /'+marker+' -->'
    block=start+'\n'+text.strip()+'\n'+end+'\n\n'
    if start in old:old=re.sub(re.escape(start)+r'.*?'+re.escape(end)+r'\s*','',old,flags=re.S)
    p.write_text(block+old,encoding='utf-8')

def flats():
    checks=[]
    for name,bottom,thick in [('C01_R2',8,3),('C03_R2',11,2.5),('C04_R2_droite',11,3),('C04_R2_gauche',11,3),('R212_support_servo',14,3),('R213_support_UBEC',42,3),('R214_cassette_FS',14,3)]:
        step=B/'3D'/(name+'.step');s=cq.importers.importStep(str(step)).val()
        face=cq.Workplane('XY').newObject([s]).faces('>Z').translate((0,0,-bottom-thick))
        path=B/'plans'/(name+'.dxf');cq.exporters.export(face,str(path),exportType='DXF')
        back=cq.importers.importDXF(str(path)).extrude(thick).val().translate((0,0,bottom))
        diff=back.cut(s).Volume()+s.cut(back).Volume()
        assert back.isValid() and diff<.001,(name,diff)
        checks.append(dict(part=name,step_sha256=sha(step),dxf_sha256=sha(path),symmetric_difference_mm3=diff,unit='mm',frame='assembly globalXY'))
    dump(V/'dxf.json',checks)
    write(B/'plans/README.md','''# Plans R2

LePDF est le dossier de revue et les empilages axiaux sont dans leCSV. Les7DXF C01/C03/C04G-D/R212/R213/R214 sont des contours réels avec leurs perçages, exportés depuis lesSTEP puis réimportés pour comparer leur volume et leur position.

**Repère global de l’assemblage pour lesDXF**, unitésmm, Z0 dans chaque fichier. Les anciensDXF R1 de pièces isolées utilisaient leurs origines locales : ne pas les superposer sans tenir compte de cette différence. La surcouche-percages-r2 est un gabarit de report ; son calqueREFERENCE_NE_PAS_DECOUPER n’est pas un contour d’usinage.

C01 : convertir Xglobal en Xlocal de perçage depuis le bord gauche parXlocal=Xglobal+150. Les trous deC03 au-delà de±150 et les trous extérieurs deC04 ne sont pas des trous du plateauC01. Les empreintes non cotées des équipements restent à releverD05.

Les arbres et pièces usinées sont définis par lesSTEP, les stationsCSV et les exigences du document mécanique. Les filetages ne sont pas hélicoïdaux dans cesSTEP ; lireM4x0.7 etM5x0.8 dans la nomenclature. AucunG-code ni capacité d’usinage de l’atelier n’est supposé.
''')

def bought_notes():
    items=[
      ('servo-direction/ft5335m-r2','FT5335M - proposition de directionR2','FT5335M_RESERVE','Gabarit62.8x32.5x55.9 ; pas de cannelure17T/25T devinée. La page actuelle et lePDF historique diffèrent. Choix conditionné àla fiche du lot et au palonnierR20 assorti.'),
      ('alimentation-direction','Alimentation6V dédiée de directionR2','UBEC_30603003_RESERVE','Hobbywing30603003 UBEC10A-Car,2..6S,6V retenus,45x20x16.2. BrancheFS candidate5A depuisUD80 aprèsSSR. Confirmer protection et démarrage ; ne pas mettre lesBEC en parallèle.'),
      ('interface-pwm-isolee','Trois interfacesPWM isolées - étudeR2','Interface_3PWM_isoles_RESERVE','3ISO7710FDR et3MCP1703A3.3V locaux. AdaptateursSOIC8 séparés pour banc ; netlist etbrochage explicités. Aucun nouveauGerber ni moduleAmazon non vérifié annoncé prêt.')]
    cache=ROOT/'tools/temp/finalisation-r2'
    for rel,title,name,note in items:
        folder=ROOT/'Composants'/rel;folder.mkdir(parents=True,exist_ok=True)
        relbase='../'*len(rel.split('/'))+'finalisation-theorique-r2/'
        # relbase is relative to the component folder under Composants.
        relbase='../'*len(rel.split('/'))+'finalisation-theorique-r2/'
        write(folder/'README.md',f'''# {title}

{note}

Le choix est une correction de conception, aucun achat ni essai n’est réalisé. Le budget, le stock et le vendeur ne sont pas validés par ce dossier.

[DossierR2]({relbase}README.md) · [Raccordements]({relbase}electricite.md) · [Sources]({relbase}sources.json) · [Conditions]({relbase}conditions-restantes.md).

[GabaritSTEP](3D/gabarit-r2.step), réservation de montage uniquement, sans détails internes ni empreinte de fabrication.
''')
        out=folder/'3D/gabarit-r2.step';out.parent.mkdir(exist_ok=True)
        s=cq.importers.importBrep(str(cache/(name+'.brep'))).val();cq.exporters.export(s,str(out))

def totals():
    fast=list(csv.DictReader((ROOT/'Composants/visserie-finale/nomenclature.csv').open(encoding='utf-8-sig'),delimiter=';'))
    groups={};nuts={};washers={}
    for r in fast:
        d=re.search(r'M(\d+(?:\.\d+)?)',r['designation']).group(1);q=int(r['quantite']);length=float(r['longueur_retenue_mm'])
        if length:
            key=(d,length,'nylon' if 'nylon' in r['designation'] else 'métal','fraisée' if 'fraisée' in r['designation'] else 'basse' if 'basse' in r['designation'] else 'cylindrique')
            groups[key]=groups.get(key,0)+q
        if float(r['ecrou_mm']):nuts[d]=nuts.get(d,0)+q
        if float(r['rondelles_mm']):washers[d]=washers.get(d,0)+q*(2 if r['code'] in ['V03','V05','V14','V15','V16','V29'] else 3 if r['code']=='V30' else 1)
    rows=[]
    for (d,l,m,head),q in sorted(groups.items()):rows.append(dict(type='vis',reference=f'M{d}x{l:g} {m},tête{head}',besoin_nominal=q,reserve_conseillee=max(2,math.ceil(q*.1)),statut='Pièces propres au projet ; contenu des kits à déduire'))
    for d,q in sorted(nuts.items()):rows.append(dict(type='écrou',reference='M'+d,besoin_nominal=q,reserve_conseillee=max(2,math.ceil(q*.1)),statut='Nylon surcartes ; autofreiné métal saufspécification différente'))
    for d,q in sorted(washers.items()):rows.append(dict(type='rondelle',reference='M'+d,besoin_nominal=q,reserve_conseillee=max(2,math.ceil(q*.1)),statut='Épaisseurs/table de montage àrespecter ; isolements distincts'))
    csvout(ROOT/'Composants/visserie-finale/recapitulatif-approvisionnement.csv',rows)
    # Mass ranges are assumptions, not invented weighed component specifications.
    mass=[('StructureR1 hors équipements',2.55,2.8,'2.264kg deplats calculés +profilés/tubes ; estimation'),('PiècesR2 ajoutées nettes',.35,.65,'Ordre de grandeur issu des volumes, hors structureR1 réutilisée'),('Batterie',.25,.35,'Enveloppe de devis non pesée'),('PrincipalF0/support/capot',.15,.4,'Réservation, masse inconnue'),('5supports branches etfusibles',.35,.8,'Masse inconnue, marge de conception'),('ED80',.12,.3,'Masse non relevée surlot'),('SSR etHS251',.2,.4,'Masse de montage non pesée'),('Rails/UD80/connexions',.2,.4,'Masse totale non pesée'),('2moteurs et2ESC',.18,.28,'Inclutfils, ordre de grandeur'),('4roues',.16,.32,'Masse non pesée'),('EngrenagesKHK etpignons',.224,.24,'KHK214g publiés, pignons estimés'),('FT5335M etUBEC',.212,.24,'178g +34g publiés, marge accessoires'),('Pi/cooler/caméra/cartes',.1,.2,'Modules et câbles courts non pesés'),('Faisceaux/visserie/maintien',.35,.8,'Corridors principaux non arrêtés')]
    csvout(B/'budget-masse.csv',[dict(ensemble=n,min_kg=a,max_kg=b,origine=c) for n,a,b,c in mass])
    dump(V/'budget-masse.json',dict(min_assumed_kg=sum(r[1] for r in mass),max_assumed_kg=sum(r[2] for r in mass),design_mass_ceiling_kg=9,not_weighed=True,no_manufacturer_mass_inferred=True))

def navigation():
    write(ROOT/'PLAN-CONCEPTION.md','''# Plan de conception - état du16octobre2026

1. [SurveillanceM1P](Composants/carte-surveillance-electrique/README.md) : fichiers deprototype/banc préparés ; qualificationLiPo non libérée.
2. [Support caméraP1](Composants/support-camera/README.md) : conçu, repris par leportique ; cadrage réel àtester.
3. [SupportsHallP1](Composants/supports-capteurs-vitesse/README.md) : conçus ; **implantationR2 àX±80**, pieds±51.
4. [ChâssisA2-R1](Composants/chassis/README.md) conservé ; [variantesR2 deC01/C03/C04 etsupports](Composants/finalisation-theorique-r2/README.md).
5. [Visserie nominaleR2](Composants/visserie-finale/README.md) : longueurs etquantités propres au projet calculées ; fixations fournisseur non cotées encore conditionnelles.

## Passe de finalisation demandée

[DossierR2](Composants/finalisation-theorique-r2/README.md) : arbres/paliers/retentions/direction, intégration, électricité etvisserie. [Conditions encore ouvertes](Composants/finalisation-theorique-r2/conditions-restantes.md). **La conception complète n’est pas déclarée prête àfabriquer/alimenter.**

Restent en particulier l’appairage etle régime des engrenagesD01, la version servoD02, les confirmations de protectionD03 etles parcours/ancrages principauxD06. Ces points documentaires/de conception précèdent les essais ; ils ne sont pas présentés comme de simples mesures futures.

Les modèlesFreeCAD ultra détaillésA2-R1 restent inchangés. L’assemblageR2 léger est distinct dans[Assemblage/R2](Assemblage/R2/README.md). Aucun achat niessai matériel réalisé.
''')
    prepend(ROOT/'ReadMe.md','finalisation-r2','''> **Revue du16octobre2026 :** [finalisation théoriqueR2](Composants/finalisation-theorique-r2/README.md), [visserie nominale](Composants/visserie-finale/README.md) et[assemblageR2](Assemblage/R2/README.md). Correction du dimensionnement de direction, arbres/paliers etimplantation repris. Des [conditions documentaires etde conception](Composants/finalisation-theorique-r2/conditions-restantes.md) restent ouvertes ; le véhicule complet n’est pas libéré pour fabrication/mise sous tension. Les modèles ultra détaillés précédents décriventA2-R1.''')
    prepend(ROOT/'SPECIFICATIONS.md','finalisation-r2','''> **ÉtudeR2 du16octobre2026 :** objectifs de vitesse/autonomie/vidéo conservés. Masse limite de calcul9kg etcharge avant45% ; valeurs non mesurées. FT90M insuffisant dans cette enveloppe ; propositionFT5335M avecalimentation dédiée etcommandes isolées. [Choix etconditions](Composants/finalisation-theorique-r2/README.md).''')
    prepend(ROOT/'Composants/README.md','finalisation-r2','''> **Finalisation du16octobre2026 :** [mécanique/intégration/électricitéR2](finalisation-theorique-r2/README.md), [visserie](visserie-finale/README.md), [servo proposéFT5335M](servo-direction/ft5335m-r2/README.md), [alimentation de direction](alimentation-direction/README.md), [interfacePWM isolée](interface-pwm-isolee/README.md). Révision d’étude sous conditions, pas de panier intégral validé.''')
    for rel in ['chassis','arbres-transmission','axes-avant','fusees-avant','paliers-transmission','biellettes-direction','servo-direction','supports-capteurs-vitesse','direction-et-transmission']:
        prepend(ROOT/'Composants'/rel/'README.md','finalisation-r2','''> **ÉtudeR2 du16octobre2026 :** [définition mécanique etimplantation révisées](../finalisation-theorique-r2/README.md). Les anciens arbres50mm etFT90M ne sont plus la définition nominaleR2 ; les réservations/interfaces non mesurées restent conditionnelles. Conserver les modèles/documents ci-dessous comme référencesA2-R1.''')
    prepend(ROOT/'Composants/verification-alimentation/README.md','integration-r2','''> **Complément d’intégration du16octobre2026 :** [étudeR2](../finalisation-theorique-r2/electricite.md) avecdirection6V dédiée, enveloppe40A etinterfacePWM isolée proposée. Les conditions de qualification ci-dessous restent applicables. Les parcours hauts etleurs descentes ne sont pas encore libérés.''')
    prepend(ROOT/'Assemblage/README.md','finalisation-r2','''> **Une étudeR2 distincte existe :** [assemblageR2](R2/README.md), [dossier de conception](../Composants/finalisation-theorique-r2/README.md). Les fichiers de cette page restentA2-R1 ; ils ne contiennent pas les corrections de direction/paliers/visserieR2.''')
    write(B/'3D/README.md','''# ModèlesR2

LesSTEP de pièces sont des solides nominaux, avecfiletages indiqués dans lesplans etnon représentés en hélice. C01/C03/C04 etles supports sont dans le **repère global de l’assemblage**. Pour lespièces gauches, symétrie suivantYZ ; utiliser le fichierG lorsqu’il existe.

[AssemblageR2](../../../Assemblage/R2/README.md) · [Dimensions etquantités](../pieces.json) · [Empilages](../plans/empilages-arbres.csv) · [Ajustements](../mecanique.md).

Le complémentmécanique-integration-r2 contient les pièces R2 etles parcours inclus ; ce n’est pas un véhicule autonome. Ne pas l’ajouter àl’assemblageR2 complet, cela doublerait cespièces. Les équipements bleus/nommésRESERVE ne sont pas des modèles exacts fournisseur.
''')

def package():
    out=B/'dossier-finalisation-r2.zip';files=[]
    folders=[B,ROOT/'Composants/visserie-finale',ROOT/'Composants/retenues-axiales',ROOT/'Composants/alimentation-direction',ROOT/'Composants/interface-pwm-isolee',ROOT/'Composants/servo-direction/ft5335m-r2',ROOT/'Assemblage/R2']
    for folder in folders:
        files.extend(p for p in folder.rglob('*') if p.is_file() and p!=out and p.name!='archive.json' and not p.name.endswith(('.FCStd1','.FCBak','.candidate.step')))
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,6) as z:
        for p in sorted(files):z.write(p,str(p.relative_to(ROOT)))
    with zipfile.ZipFile(out) as z:assert z.testzip() is None
    dump(V/'archive.json',dict(file=out.name,bytes=out.stat().st_size,sha256=sha(out),files=len(files),zip_crc_valid=True))

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    if '--package' in sys.argv:package();print('ARCHIVE OK');return
    flats();bought_notes();totals();navigation();print('PUBLICATION ET DXF OK')
if __name__=='__main__':main()
