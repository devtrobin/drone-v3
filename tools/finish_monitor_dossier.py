"""Complete M1 indices and assembly BOM, preserving the historical dossiers."""
from pathlib import Path
import csv,hashlib,json,re,sys
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'Composants/carte-surveillance-electrique'
def write(path,text):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text.strip()+'\n',encoding='utf-8')
def banner(path,key,text):
    s=path.read_text(encoding='utf-8');s=re.sub(r'<!-- '+re.escape(key)+r' -->.*?<!-- /'+re.escape(key)+r' -->\s*','',s,flags=re.S)
    write(path,'<!-- '+key+' -->\n'+text+'\n<!-- /'+key+' -->\n\n'+s)
def main():
    sys.stdout.reconfigure(encoding='utf-8')
    if json.loads((B/'selection.json').read_text(encoding='utf-8')).get('revision')=='M1P':
        raise SystemExit('Historical M1 finishing script. M1P: use prepare_monitor_prototype.py; preserve the fabrication and bench release records.')
    s=json.loads((B/'selection.json').read_text(encoding='utf-8'));s['EVM_dimensions_status']='Enveloppes de réservation 60 x 60 x 12 mm, pas des cotes TI certifiées ; Gerbers refusés HTTP 401.'
    s['bounds_exclude']=['External FAUX fuse and holder/cover','100 ohm resistors at battery end','Wire harnesses, connector mates and bend radii','Mechanical attachment/supports not yet defined']
    if not any(x['part']=='0454.500MR' for x in s['items']):s['items'].append(dict(ref='F1,F2',part='0454.500MR',quantity=2,role='Fusibles lents 500 mA CMS, 125 V DC / 50 A, après M5 sur les entrées TMR ; qualification de coordination restante',url='https://www.littelfuse.com/assetdocs/fuse-452-and-454-datasheet?assetguid=8c87aa93-80a7-4ea8-8749-a19ba03901c2'))
    write(B/'selection.json',json.dumps(s,ensure_ascii=False,indent=2))
    p=B/'README.md';text=p.read_text(encoding='utf-8').replace('Réservation globale : **140 x 75 x 30 mm**, hors fiches et courbures de câble.','Réservation porteuse + modules : **140 x 75 x 30 mm**, hors FAUX/support, résistances au pack, fiches et courbures de câble.')
    write(p,text+'\n\n[Cotes et pièces extérieures](cotes.md) · [Nomenclature complète d’assemblage](nomenclature-assemblage.csv) · [Contrôles KiCad](verification/controle-kicad.json) · [Contrôle indépendant FreeCAD](3D/validation-freecad.json).')
    write(B/'cotes.md','''# Cotes et réservations M1

Unités millimètres. Aucun matériel reçu ou mesuré.

| Élément | Cote / statut |
| --- | --- |
| Porteuse V3 | 140 x 75 x 1,6 ; dimension de conception exacte dans le PCB |
| Fixations porteuse | 4 trous Ø3,2 ; origine coin PCB ; (4,4), (136,4), (4,71), (136,71) |
| Ensemble porteuse + modules | Réservation 140 x 75 x 30 ; pas une cote réelle fournisseur |
| TI TPS3700EVM-114 | Deux volumes réservés 60 x 60 x 12, au-dessus de la porteuse ; dimensions de la carte et supports non certifiés |
| Traco TMR 1-0511 | Corps nominal 17 x 7,62 x 11 ; tolérance corps ±0,5 ; hauteur au-dessus PCB environ 11,3 selon pose |
| Pololu 2831 | Fabricant : environ 18 x 13 x 3,5 hors connecteurs ; gabarit 18 x 13 x 5,5 dans le STEP |
| Vishay AC03 100 ohms | Corps nominal 13 x Ø4,8 ; fils Ø0,8, non coupés de 25 mm dans la CAO. Trois pièces hors porteuse au pack |
| FAUX KLKD001.T | Cartouche 10,31 x 38,1 nominal ; support L60030M1PQ et écran SPL001 hors porteuse, enveloppe à confirmer |

**Les 140 x 75 x 30 n'incluent ni FAUX et son support, ni les trois résistances au pack, ni les fiches de faisceaux, leurs courbures et leurs retenues.** Ces éléments doivent être réservés séparément dans le châssis. Les emplacements M3 restent nus : vis, entretoises et supports isolants définis dans les étapes mécaniques ultérieures.

Les cotes des EVM ne sont pas déduites arbitrairement de l'échelle d'un PDF. Leur ZIP Gerber SLVC413 est référencé mais inaccessible sans accès TI lors de cette recherche (HTTP 401). Contrôle au plan natif ou à la réception avant perçage définitif. Le dossier conserve un gabarit d'étude, pas une cote industrielle inventée.
''')
    write(B/'KiCad/README.md','''# KiCad - Surveillance 2S M1

Ouvrir [surveillance-2s-m1.kicad_pro](surveillance-2s-m1.kicad_pro). [Schéma](surveillance-2s-m1.kicad_sch), [PCB routé](surveillance-2s-m1.kicad_pcb), [schéma vectoriel](vues/surveillance-2s-m1.svg), [routage](vues/routage.svg), [montage](vues/montage.svg), [dessus](vues/cuivre-dessus.svg), [dessous](vues/cuivre-dessous.svg), [CSV porteuse](nomenclature.csv), [CSV assemblage complet](../nomenclature-assemblage.csv).

41 composants/connexions sur porteuse, dont R7/R8 DNP ; 26 nets ; PCB 140 x 75 x 1,6, deux couches. Pistes 0,20, isolement minimal 0,15, cuivre supposé 35 micromètres, vias 0,60/0,30. Ces règles ne sont pas une procédure d'usinage CNC. Les empreintes locales Nano454 et TMR1 et les symboles de blocs sont inclus ; les autres empreintes sont celles des bibliothèques standard KiCad 10. Les symboles de blocs représentent les fonctions et pins des interfaces, pas les composants internes des modules commerciaux.

**Contrôle KiCad 10.0.7 : ERC 0, DRC 0, aucun élément non connecté, aucune divergence de parité schéma/PCB.** Netlist XML comparée indépendamment aux connexions attendues. Rapports complets dans [verification](../verification/controle-kicad.json), sans exclusions ajoutées pour masquer les défauts. Les recommandations du fabricant et le montage réel restent à qualifier.

J3/J4 et J5 sont des départs de faisceaux vers les modules, pas des empreintes où enficher directement un EVM ou un Pololu. Les résistances de seuil restent sur les deux EVM, hors porteuse. RA0/RA1/RA2 au pack et FAUX près de sa dérivation ne sont pas placés sur ce PCB. R7/R8 sont achetées mais montées côté Pi ; leurs pads porteuse restent vides.

Génération reproductible depuis la racine V3 : `D:/KiCAD/bin/python.exe tools/build_monitor_kicad.py`. Contrôles : `tools/temp/cad-env/Scripts/python.exe tools/check_monitor_kicad.py`. Les paramètres et la connectivité sont dans le script et les JSON. Les vues de cuivre sont des documents de revue ; il faut une revue d'empreintes et les essais décrits avant de libérer une fabrication. Aucun Gerber n'est présenté comme validé pour production.
''')
    write(B/'3D/README.md','''# Modèles STEP M1

| Modèle | Usage |
| --- | --- |
| [Porteuse détaillée](porteuse-surveillance-2s-m1-detaillee.step) · [aperçu](porteuse-surveillance-2s-m1-detaillee.png) | PCB 140 x 75, perçages, vrais tracés KiCad, plages et fûts ; corps de composants reconstruits au nominal |
| [Ensemble avec gabarits](ensemble-surveillance-2s-m1-gabarits.step) · [aperçu](ensemble-surveillance-2s-m1-gabarits.png) | Porteuse allégée pour l'implantation ; cadres bleus réservés aux EVM et brun au Pololu ; **ce sont des volumes de réservation, pas les modèles réels de ces cartes** |
| [Trois AC03 100 ohms](resistances-mesure-3x-ac03-100ohm.step) · [aperçu](resistances-mesure-3x-ac03-100ohm.png) | Géométrie nominale des résistances de mesure au pack ; pattes droites non coupées |

Toutes les géométries sont des reconstructions V3, pas des CAO fabricant. La carte suit son routage vérifié ; cuivre 35 micromètres supposé, profil des raccords de pistes et détails de boîtiers approximés. Couleurs, inscriptions, petits congés et contacts non cotés sont estimés. Pas d'électronique interne inventée. Pas de câbles coupés ou de faisceau partiellement représenté : les faisceaux sont absents et leurs interfaces sont documentées.

Le modèle d'ensemble avec gabarits utilise une porteuse simplifiée sans les pistes, plages et fûts métallisés : les volumes extérieurs des composants et les fixations sont conservés. Utiliser cette version légère pour l'implantation du châssis ; la version détaillée garde le cuivre visible pour examiner la carte.

CadQuery/OCP : réimport STEP, validité, nombre de solides, volumes, enveloppes et présence des couleurs. [Provenance](provenance.json). FreeCAD : import indépendant en mode sans interface, validité, fermeture des solides et comparaison des enveloppes ; [résultats](validation-freecad.json). Aucun essai dans l'interface FreeCAD/CAD View ni mesure matérielle revendiqué.

**Réservation 140 x 75 x 30 pour porteuse + modules seulement**, hors FAUX/support, résistances au pack et faisceaux. Cotes TI et supports à confirmer avant châssis. Le fichier le plus utile pour examiner la géométrie réelle du projet est la porteuse détaillée ; l'ensemble avec cadres sert à réserver la place des modules.
''')
    # Complete procurement mapping, including all pads marked DNP but fitted at Pi.
    c=json.loads((B/'KiCad/implantation.json').read_text(encoding='utf-8'))['components'];rows=[]
    for it in s['items']:
        rows.append([it['ref'],it['part'],it['quantity'],it['role'],it.get('url',''),it.get('price',''),it.get('currency',''),'Non acheté / prix exact à revalider'])
    # Avoid counting semiconductor/module items twice: individual carrier BOM is separate.
    for family,part,count,role,url in [
        ('R1-R4','TNPW08052K20BEEA',4,'2,2 kohms, 0,1 %, LED ; calcul conservateur à 1 %','https://www.vishay.com/docs/28758/tnpw_e3.pdf'),
        ('R5-R8','TNPW080547K0BEEA',4,'47 kohms ; R5/R6 sur porteuse, R7/R8 côté Pi et DNP sur PCB','https://www.vishay.com/docs/28758/tnpw_e3.pdf'),
        ('R9-R10','TNPW0805100KBEEA',2,'100 kohms, rappels DONE/OFF','https://www.vishay.com/docs/28758/tnpw_e3.pdf'),
        ('C1,C2,C9','GRM21BR71E104KA01L',3,'100 nF, X7R, 25 V, 0805','https://www.murata.com/en-us/products/productdetail?partno=GRM21BR71E104KA01%23'),
        ('C3-C6','GRM21BR71E105KA99L',4,'1 microfarad, X7R, 25 V, 0805','https://www.murata.com/en-us/products/productdetail?partno=GRM21BR71E105KA99%23'),
        ('C7-C8','GRM21BR71E225KA73L',2,'2,2 microfarads, X7R, 25 V, 0805 ; conserver au moins 1 microfarad effectif pour le LDO','https://search.murata.co.jp/Ceramy/image/img/A01X/G101/ENG/GRM21BR71E225KA73-01.pdf'),
        ('C10-C11','GRM21BR61E106KA73L',2,'10 microfarads, X5R, 25 V, 0805 ; déclassement DC à vérifier','https://www.murata.com/en-us/products/productdetail?partno=GRM21BR61E106KA73%23'),
        ('J1,J7','B2B-XH-A(LF)(SN)',2,'Embases 2 positions, 2,50 mm, PCB','https://www.jst-mfg.com/product/pdf/eng/eXH.pdf'),
        ('J2,J5','B3B-XH-A(LF)(SN)',2,'Embases 3 positions ; réutiliser l’embase déjà prévue pour mesure si exacte','https://www.jst-mfg.com/product/pdf/eng/eXH.pdf'),
        ('J3,J4,J6','B5B-XH-A(LF)(SN)',3,'Embases 5 positions, connecteurs de faisceau','https://www.jst-mfg.com/product/pdf/eng/eXH.pdf'),
        ('Fiches J1/J7','XHP-2',2,'Fiches 2 positions','https://www.jst-mfg.com/product/pdf/eng/eXH.pdf'),
        ('Fiches J2/J5','XHP-3',2,'Fiches 3 positions ; éviter un achat en double avec la rallonge existante','https://www.jst-mfg.com/product/pdf/eng/eXH.pdf'),
        ('Fiches J3/J4/J6','XHP-5',3,'Fiches 5 positions','https://www.jst-mfg.com/product/pdf/eng/eXH.pdf'),
        ('Contacts XH','SXH-001T-P0.6',25,'Un contact par fil, 22 AWG ; quantité hors réserve ; vérifier référence et outillage','https://www.jst-mfg.com/product/pdf/eng/eXH.pdf'),
        ('Transition AUX','WAGO 221-413',2,'Une transition positive et une négative, 12/14 vers 22 AWG, hors porteuse','https://www.wago.com/221-413'),
        ('Câbles EVM','Fils 22 AWG, connexion sur connecteurs TI',10,'Cinq fils par EVM, broches doublées du même signal ; terminaisons et longueurs après réception des modules','modules/configuration.md'),
        ('PCB','Porteuse M1 140 x 75 x 1,6 mm',1,'Deux couches, à fabriquer après revue ; pas une carte de puissance','KiCad/surveillance-2s-m1.kicad_pcb'),
    ]:rows.append([family,part,count,role,url,'','','Référence de conception, panier France non établi'])
    with (B/'nomenclature-assemblage.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f,delimiter=';');w.writerow(['Repères','Référence','Quantité montée/affectée','Fonction/limites','Source/achat','Prix unitaire relevé','Monnaie','Statut']);w.writerows(rows)
    # Correct the two capacitor value strings without touching geometry/connectivity.
    for p in [B/'KiCad/nomenclature.csv']:
        text=p.read_text(encoding='utf-8-sig').replace('10uF X7R 25V','10uF X5R 25V');p.write_text(text,encoding='utf-8-sig')
    # Active order and links; preserve earlier content as explicitly dated history.
    write(ROOT/'PLAN-CONCEPTION.md','''# Ordre de conception retenu - 15 octobre 2026

1. [Carte de surveillance électrique, schéma et routage](Composants/carte-surveillance-electrique/README.md). Prototype M1 documenté ; contrôles de fichiers terminés, revue et essais matériels restants.
2. Support caméra arrière et en hauteur, pour observer le plateau et la route.
3. Supports des capteurs de vitesse.
4. Châssis plateau ouvert, à partir du concept A2 retenu.
5. Visserie finale de l'ensemble.

L'[image conservée à la racine Drone](../image.png) et le [concept A2 archivé](Composants/chassis/concepts-images-v1/a2-plateau-ouvert-camera-arriere.png) restent des références visuelles. Aucun modèle de châssis définitif n'est créé à cette étape. La couverture réelle caméra/plateau/route dépendra du support, de la hauteur, de l'inclinaison et du champ de vision.

Pour l'implantation, les réservations de la surveillance n'incluent pas le fusible auxiliaire et son support, le bloc de résistances près du pack, ni les fiches et faisceaux. Confirmer les cotes des EVM avant les perçages définitifs.
''')
    p=ROOT/'ReadMe.md';t=p.read_text(encoding='utf-8');t=t.replace('Schéma et routage de surveillance, support caméra, visserie finale et châssis seront conçus ensemble à la fin, selon l’instruction utilisateur. Aucune carte de puissance ou pièce de châssis prête à fabriquer à ce stade.',
      '**Ordre retenu :** [carte de surveillance, support caméra, supports capteurs, châssis, puis visserie finale](PLAN-CONCEPTION.md). La [surveillance M1 à modules existants](Composants/carte-surveillance-electrique/README.md) dispose de son schéma, routage, notice et STEP de porteuse avec gabarits. Contrôles KiCad réussis ; disponibilité, cotes EVM et qualification matérielle restent ouvertes.');write(p,t)
    p=ROOT/'Composants/README.md';t=p.read_text(encoding='utf-8');t=t.replace('| [Surveillance 2S](protection-batterie/surveillance-2s/README.md) | Carte analogique V3, TLV6700 et optocoupleurs | Fabrication à chiffrer | Concept à fabriquer ; seuils par cellule, pas de PCB prêt à produire |',
      '| [Surveillance électrique M1](carte-surveillance-electrique/README.md) | 2 TPS3700EVM-114, 2 TMR 1-0511, Pololu 2831 et porteuse | Devis partiel | Schéma/routage KiCad contrôlés, notice et STEP ; cotes TI et qualification matérielle restantes |');write(p,t)
    banner(p,'surveillance-m1','> **Surveillance active M1 :** [dossier, schéma, routage et CAO](carte-surveillance-electrique/README.md). Remplace le concept TLV6700 pour cette étude ; WARN maintenant actif haut. [Ordre de conception](../PLAN-CONCEPTION.md).')
    for rel,link in [('Composants/protection-batterie/README.md','../carte-surveillance-electrique/README.md'),('Composants/protection-batterie/integration.md','../carte-surveillance-electrique/README.md'),('Composants/protection-batterie/surveillance-2s/README.md','../../carte-surveillance-electrique/README.md')]:
        banner(ROOT/rel,'surveillance-m1','> **15 octobre 2026 - ce concept TLV6700 est historique.** La [surveillance M1 à modules existants]('+link+') définit désormais les seuils, les reprises EVM, les protections fines et le routage. WARN M1 est actif haut ; ne pas reprendre ici la polarité de l’ancien concept. Les Pololu 2813 et D1D100 restent dans la chaîne R2.')
    for rel in ['Composants/ENSEMBLES-AVANT-CHASSIS.md','Composants/verification-alimentation/README.md']:
        banner(ROOT/rel,'surveillance-m1','> **Suite active du 15 octobre 2026 :** [carte de surveillance M1](../carte-surveillance-electrique/README.md)' if 'verification-' in rel else '> **Suite active du 15 octobre 2026 :** [carte de surveillance M1](carte-surveillance-electrique/README.md). Ordre : surveillance, support caméra, supports capteurs, châssis, visserie finale. Les reports de phase ci-dessous sont historiques.')
    p=ROOT/'Composants/connecteur-gpio/brochage.json';j=json.loads(p.read_text(encoding='utf-8'))
    for pin in j['pins']:
        if pin['signal'] in ['WARN1','WARN2']:pin['destination']='Collecteur opto M1 ; actif HAUT en avertissement ; rappel 47 kohms à 3,3 V placé côté Pi'
        elif pin['signal']=='3V3_MON':pin['destination']='3,3 V des deux rappels WARN côté Pi ; pads de rappels sur porteuse M1 DNP'
    j['monitor_revision']='M1';j['monitor_source']='../carte-surveillance-electrique/integration.md';j['WARN_active_high']=True;write(p,json.dumps(j,ensure_ascii=False,indent=2))
    banner(ROOT/'Composants/connecteur-gpio/README.md','surveillance-m1','> **Surveillance M1 : WARN1/2 sont actifs hauts**, rappels 47 kohms au 3,3 V côté Pi. [Contrat courant](../carte-surveillance-electrique/integration.md). Les 13 contacts restent inchangés ; anciens PDF datés.')
    # Inventory every downloaded original without silently claiming failed downloads.
    records=[]
    for p in sorted((B/'notices').glob('*.pdf')):
        if p.name.startswith('notice-'):continue
        assert p.read_bytes().startswith(b'%PDF')
        records.append(dict(file=str(p.relative_to(B)).replace('\\','/'),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),modified=False))
    write(B/'notices/README.md','''# Notices originales et notice de projet

[Notice M1 du projet](notice-carte-surveillance-v3.pdf), distincte des PDF fabricants conservés sans modification. Origines et empreintes dans [assets](../assets.json), [compléments](../assets-modules.json), [réutilisations](../assets-reutilises.json) et [inventaire des PDF](inventaire-originaux.json).

Les notices d'origine comprennent TI EVM/TPS3700, TRACO TMR1, Pololu D24V10Fx, Vishay AC/TNPW/VOS618A, MCP1703A, SN74LVC2G17, BAT54 et le KLKD archivé lors de l'audit R2. Le guide TI fournit les schéma et vues de routage ; son ZIP Gerber n'a pas pu être archivé (401). Les documents non téléchargés ne sont pas recréés sous forme de faux originaux.
''');write(B/'notices/inventaire-originaux.json',json.dumps(records,ensure_ascii=False,indent=2))
    print('Completed M1 indices, complete assembly BOM and active GPIO documentation.')
if __name__=='__main__':main()
