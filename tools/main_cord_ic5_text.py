"""Current French prose; data, prices and native evidence remain in their manifests."""
from pathlib import Path
MOUNT=[
"Utiliser un seul pack Spektrum G1 SPMX50002S30H5, équipé IC5 d’usine. Ne pas modifier ses fils. Pour cette version, la Zeee XT60 n’est plus retenue. Côté véhicule : SPMXCA510 « Device », distinct du SPMXCA505 « Battery » et des cordons série/parallèle.",
"CP0+ : fil rouge 10 AWG du 510 → TE 130191 → entrée MIDI M5. CP0- : fil noir 10 AWG du 510 → TE 130191 → MiniBus D- N2 #10-32. Après MIDI, le positif traverse ED80 puis D+ P2 par les deux segments 6 mm² existants ; l’UD80A conserve son arrivée 6 mm².",
"Les deux fils 10 AWG sont inclus dans le 510 : aucun nouveau lot de fil pour CP0. Longueur publiée : 4 pouces, soit 101,6 mm, arrondie à 100 mm chez les vendeurs ; origine de mesure et dénudage d’usine non cotés. Mesurer le lot. Placer le MIDI près du pack et adapter l’implantation à la longueur utile, en gardant court le segment positif non protégé.",
"La photo officielle du 510 montre deux fils de puissance et aucun fil Smart libre. Ne pas ajouter de liaison de télémétrie au Pi. Le pack G1 conserve sa prise d’équilibrage B0/B1/B2 ; schéma et protection des petites liaisons de surveillance restent pour la phase finale. B1 n’est jamais le retour de puissance.",
"Avant sertissage, vérifier conducteur et extrémités d’usine. Si elles sont pré-étamées à la soudure, retirer cette portion et redénuder un conducteur intact. L’étamage individuel de surface des brins, s’il existe, est distinct d’un paquet rigidifié à la soudure. La longueur utile dépend de cette préparation ; les fils du STEP installé mesurent environ 93 mm, à titre d’étude.",
"TE 130191 admet 12-10 AWG /2,62-6,64 mm². Le guide SOLISTRAND cite l’outil 49935 ; la notice 408-1542 Rev P décrit la chambre 12-10 AWG, un dénudage standard de 6,35-7,14 mm, le positionnement de la paume et le cycle complet du cliquet. Faire confirmer outil/matrice et fil réel ; réaliser des éprouvettes et contrôler insertion, brins, tenue et résistance. Ne pas ajouter de soudure au sertissage.",
"Enfiler deux morceaux ATUM 8/2 d’environ 20 mm avant sertissage. Couvrir le canon et recouvrir la gaine du fil ; laisser la paume électrique libre. Diamètre installé et retrait jusqu’à 15 % à vérifier sur le lot. Chauffer localement selon TE : début de rétraction 80 °C, complète 110 °C ; ces températures ne sont pas le réglage du pistolet. La prise IC5 arrive pré-câblée : aucune soudure au connecteur n’est nécessaire ici.",
"Batterie et équilibrage débranchés, monter les cosses avec écrous et rondelles d’origine. MIDI M5 : 4,5 N·m proposé dans la plage commune des documents existants, lot à confirmer. MiniBus #10-32 : écart 1,69/2,03 N·m à résoudre avec la notice du lot ; aucun écrou M5 ou couple de 4,5 N·m par défaut. Retenir les fils hors des bornes et vérifier les capots. Fixations du châssis réservées pour la fin.",
"Contrôler polarité réelle, continuité de chaque pôle, absence de liaison +/-, isolement, clips et tenue mécanique. Première vérification avec source adaptée et limitée ; puis qualification du courant RMS et des pointes, chutes de tension et températures sur la durée et à l’ambiante prévues. Aucun court-circuit volontaire du pack.",
"Spektrum emploie un IC5 unique sur le Firma 100 A SPMXSE1100. Cette application motive le choix pour le scénario 44,39 A, par inférence ; elle ne donne pas une ampacité indépendante garantie du 510. Aucun chiffre de 120 A continus n’est attribué au connecteur. Fils du pack, 10 AWG du cordon et coordination du MIDI 60 A restent à qualifier. Un fusible ne limite pas activement le courant.",
"Charge : la FAQ Horizon permet l’emploi d’une G1 avec équilibrage sur un chargeur classique. Le S65 couvre la LiPo standard 2S, 8,4 V max ; réglage initial 1C = 5 A, soit 42 W en fin de charge. Un cordon/adaptateur de charge vers IC5 et la liaison JST-XH 2S sont nécessaires avant utilisation. Ils sont distincts du cordon embarqué à cosses. La G2 sans équilibrage ne peut pas remplacer la G1 avec ce chargeur.",
"Le pack est annoncé à 139 × 46 × 25 mm /294 g sur l’ancienne page fabricant. La référence G1 est arrêtée chez le fabricant ; RC Team affiche encore le SKU exact disponible à 49,99 EUR. Vérifier date, état et notice du lot avant achat. Énergie nominale 37 Wh contre 38,48 Wh pour la Zeee (-3,85 %), masse annoncée +44 g. Vitesse et autonomie restent des objectifs à mesurer ; aucune baisse de performance n’est actée."
]
README="""# Cordon principal batterie vers distribution - IC5

**Choix du 15 octobre 2026 : batterie 2S avec une prise plus forte montée d’usine.** Proposition d’étude : **Spektrum Smart G1 SPMX50002S30H5**, 7,4 V /5 000 mAh /IC5, avec un **cordon SPMXCA510 pré-câblé en 10 AWG**. Aucun achat ni essai matériel.

| Élément actif | Dossier | Quantité | Achat |
| --- | --- | ---: | --- |
| IC5 véhicule + deux fils 10 AWG inclus | [SPMXCA510](cordon-ic5-spektrum/README.md) | 1 cordon | [Freakware](https://www.freakware.de/en/p/ic5-geraeteanschluss-kabel-4-100mm-10awg-spektrum-spmxca510-a167682.htm) |
| Cosses de puissance M5 | [TE 130191](cosses-te-130191/README.md) | 2 | [DigiKey](https://www.digikey.fr/fr/products/detail/te-connectivity-amp-connectors/130191/1864623) |
| Gaine adhésive | [ATUM 8/2](isolation-atum/README.md) | 2 coupes ≈20 mm | même barre déjà prévue |
| Batterie 2S révisée | [Spektrum G1 IC5](../batterie/spektrum-g1-ic5/README.md) | 1 pack | [RC Team](https://www.rcteam.com/products/spektrum-accu-lipo-smart-74v-5000mah-30c-ic5) |

[Notice PDF et originaux](notices/README.md) · [Montage](integration.md) · [Cotes IC5](cordon-ic5-spektrum/cotes.md) · [Devis, sources et avis](revision-batterie-ic5.md) · [Modèles STEP](3D/README.md) · [Sélection structurée](selection-active.json) · [Nomenclature](nomenclature.json) · [Contrôles](verification.json).

Le 510 arrive pré-câblé. Deux cosses et deux manchons le terminent vers l’entrée MIDI et D- N2. Les fils 6 mm² après MIDI, via ED80 et vers l’UD80A, restent distincts. Aucun adaptateur XT60 en propulsion et aucun lot de fil acheté en double.

Le choix IC5 repose sur son emploi documenté sur un Spektrum Firma 100 A : c’est une **inférence d’ingénierie**, sans ampacité garantie de notre cordon. Le scénario 44,39 A, les fils d’usine du pack, l’échauffement et la coordination du MIDI 60 A restent à qualifier.

Prix partiels : batterie 49,99 EUR, cordon 9,89 EUR avec taxe locale affichée, deux cosses 1,344 EUR TTC indicatifs. **Sous-total indicatif 61,224 EUR**, hors gaine, port et outils, avec TVA/livraison France à revalider. Les références G1/510 sont arrêtées chez le fabricant ; des offres distributeurs existent encore. Aucune offre Amazon exacte n’a été validée pour ces deux références.

Le S65 peut être conservé avec la G1 à équilibrage, charge initiale 5 A ; **cordon/adaptateur de charge IC5 distinct à sélectionner avant charge**. Ne pas substituer une G2. Énergie nominale 37 Wh contre 38,48 Wh pour la Zeee (-3,85 %), sans preuve d’autonomie.

Châssis, support caméra, surveillance et visserie finale restent pour la fin. [Variante XT60 non retenue](variante-xt60-non-retenue.md) : huit fichiers initiaux gardés pour comparaison ; pas un achat supplémentaire. Les cosses nues et la référence ATUM sont communes.
"""
RESEARCH="""# Révision de la batterie et du cordon IC5

15 octobre 2026, après le choix utilisateur de revoir la batterie 2S. Aucun achat, aucune modification de pack.

## Batterie et charge

Spektrum **G1 SPMX50002S30H5** : LiPo standard 2S, 7,4 V nominal /8,4 V pleine charge, 5 000 mAh /37 Wh, IC5 d’usine. Ancienne page fabricant : 139 × 46 × 25 mm /294 g. La page actuelle confirme G1 mais signale une référence arrêtée. Le SKU exact chez RC Team indique `available: true` et 49,99 EUR dans la consultation publique du 15 octobre 2026. La photo exacte montre la prise d’équilibrage trois voies ; les autres photos de gamme ne prouvent pas les cotes. Vérifier date, état et notice du lot. Un seul pack embarqué, aucune série ou mise en parallèle.

[RC Team](https://www.rcteam.com/products/spektrum-accu-lipo-smart-74v-5000mah-30c-ic5) · [Fabricant](https://my.spektrumrc.com/Products/Default.aspx?ProdID=SPMX50002S30H5) · [FAQ Horizon G1/G2](notices/Spektrum-G1-G2-FAQ-original.pdf).

La FAQ Horizon permet la charge d’une G1 avec équilibrage sur un chargeur classique. Le S65 reste proposé : LiPo Balance 2S, initialement 1C = 5 A, 8,4 V maximum et 42 W, équilibrage JST-XH. Il faut **sélectionner un cordon/adaptateur de charge IC5** séparé du cordon embarqué ; les cosses du véhicule ne sont pas un branchement de charge. La G2 sans port d’équilibrage est incompatible avec le S65 classique. La puce Smart G1 stocke des données et effectue l’auto-stockage ; elle ne remplace pas la coupure basse tension du robot.

## Pourquoi IC5

Le guide Spektrum du Firma **SPMXSE1100** indique 100 A continus pour cet ESC et une prise IC5 unique. Nous en **inférons** que cette famille authentique est une meilleure piste pour 44,39 A que le XT60 documenté à 35 A MAX sous conditions. Ce n’est pas une ampacité indépendante du SPMXCA510 ni un essai du montage V3. Aucune valeur de 120 A continus garantie n’est attribuée au connecteur. Les EC5 génériques ne sont pas retenus sur la seule ressemblance de leur logement : la fiche historique AMASS EC5 cite 40 A RC et ne justifie pas 44 A continus.

[Application Firma 100 A/IC5](notices/Spektrum-Firma100A-IC5-reference-original.pdf) · [Cordon fabricant](https://www.spektrumrc.com/product/connector-ic5-device-w-4-10awg-wires/SPMXCA510.html).

## Pièces et devis

**SPMXCA510**, version « Device » : prise IC5 et deux fils 10 AWG de 4 pouces, soit environ 100/101,6 mm. Photo officielle : deux fils rouge/noir, aucun fil Smart libre. Diamètres, brins, godets, datum de longueur et isolant exact non cotés ; aucune fausse cote fabricant ajoutée. Les extrémités paraissent étamées : contrôler le lot, retirer les parties rigidifiées à la soudure avant sertissage et relever la longueur restante. Ne pas rallonger automatiquement le positif avant MIDI.

| Ligne | Quantité | Prix / état |
| --- | ---: | --- |
| Batterie G1 RC Team | 1 | 49,99 EUR, SKU exact disponible à la consultation |
| Cordon SPMXCA510 Freakware | 1 | 9,89 EUR, taxe locale incluse et stock affichés ; France à vérifier |
| TE 130191 DigiKey | 2 | 0,672 EUR TTC indicatifs chacun, offre indexée ancienne |
| ATUM 8/2 | 2 coupes ≈20 mm | même barre prévue ; pas de second achat |

**Sous-total indicatif : 61,224 EUR**, hors gaine, frais et outils, avec taxe finale France à confirmer. Le lot BNTECHGO 12 AWG déjà proposé pour les ESC n’est pas racheté pour CP0. Les deux TE 130191 remplacent les terminaisons 95R5 de CP0 uniquement ; les autres 95R5 restent prévues.

[Freakware](https://www.freakware.de/en/p/ic5-geraeteanschluss-kabel-4-100mm-10awg-spektrum-spmxca510-a167682.htm) · [TE 130191](https://www.te.com/en/product-130191.html). Recherche Amazon.fr par SPMX50002S30H5/SPMXCA510 : aucune offre exacte vérifiée. Fournisseurs alternatifs identifiés ; les liens de recherche ne sont pas présentés comme des offres disponibles.

## Avis, citations et informations manquantes

Le forum ARRMA du 21 octobre 2020 décrit l’emploi du 510 pour relier une commande classique à un pack IC5. Les participants confondent parfois sexe des contacts et forme du logement : choisir **« Device » par référence** et contrôler polarité et contacts. Nous terminons les fils aux cosses, sans jonction fil à fil sur ce cordon.

[Retours utilisateurs ARRMA](https://www.arrmaforum.com/threads/castle-esc-to-spektrum-smart-battery-connection.29211/). Aucun essai instrumenté exact G1 +510 +130191 à 44 A retrouvé ; aucune vidéo présentée comme visionnée intégralement. Les notes des autres références ne sont pas transposées. Les avis courts sur le XT60 sont conservés dans la recherche initiale, sans servir à justifier l’IC5.

La FAQ Horizon dit : **« G1 Smart batteries with a balance lead do NOT require a Spektrum Smart charger for charging. »** (18 mots). Il faut néanmoins un chargeur adapté au type, au nombre de cellules et au courant, avec les deux raccordements adéquats.

Énergie -3,85 % et masse +44 g annoncées par rapport à la Zeee. Maintien provisoire de géométrie proche, à requalifier pour la masse. Empreinte du sertissage W, résistance de contacts, fil réel et température admissible dans l’implantation non établis. Le MIDI 60 A reste un calibre d’étude à coordonner. Vitesse et autonomie sont inchangées comme objectifs, sans preuve expérimentale.

[Sources et versions](sources.json) · [Archives SHA256](assets.json) · [Intégration](integration.md) · [Recherche initiale XT60](recherche-technique.md).
"""
CORDREADME="""# Spektrum SPMXCA510 - IC5 Device pré-câblé

Une prise IC5 côté véhicule avec **deux fils 10 AWG de 4 pouces inclus**, soit environ 100/101,6 mm. **Un cordon à acheter**, sans lot de fil ou connecteur supplémentaire. Référence « Device », complément du pack IC5 d’usine ; photo officielle conservée.

[Achat Freakware](https://www.freakware.de/en/p/ic5-geraeteanschluss-kabel-4-100mm-10awg-spektrum-spmxca510-a167682.htm), 9,89 EUR avec taxe locale affichée, livraison et TVA France à confirmer. Référence arrêtée chez le fabricant ; stock distributeur annoncé à la consultation. Aucune offre Amazon exacte vérifiée.

[Cotes](cotes.md) · [Notice PDF](../notices/notice-cordon-principal-batterie-v3.pdf) · [Montage](../integration.md) · [Devis et sources](../revision-batterie-ic5.md) · [STEP](3D/README.md) · [Photo originale](../references/Spektrum-SPMXCA510-original.jpg).

Contrôler le fil et le pré-étamage des extrémités avant sertissage. Aucune soudure dans la prise requise pour notre montage ; fils du pack inchangés. La qualification de courant et de protection ne découle pas du modèle 3D.
"""
COTES="""# Cotes et provenance du SPMXCA510

| Grandeur | Valeur | Statut |
| --- | --- | --- |
| Référence | IC5 Device SPMXCA510 | Spektrum |
| Conducteurs | Deux fils 10 AWG, 4 pouces ≈101,6 mm | Spektrum ; datum de longueur non publié |
| Section nominale AWG | ≈5,26 mm² | Conversion AWG, pas mesure du fil livré |
| Gaine dans le STEP | Ø5,5 mm | Estimée, aucune cote constructeur trouvée |
| Enveloppe métallique dans le STEP | Ø3,0 mm | Estimée ; pas un nombre de brins ou une masse de cuivre |
| Corps IC5 dans le STEP | Environ 24 × 21 × 11 mm | Reconstruction visuelle estimée |
| Entraxe et contacts dans le STEP | 9,6 mm /Ø5 mm | Estimés ; pas un gabarit d’accouplement |
| Extrémités d’usine | Pré-étamage apparent sur la photo | Contrôler le lot, recouper avant sertissage si nécessaire |
| Fils installés dans le STEP | Environ 93 mm développés | Pose provisoire ; pas une liste de coupe |

Les clips, capot, profondeurs, godets, rayons et teintes sont estimés. La petite cavité centrale est simplifiée ; aucun fil de télémétrie n’est ajouté. Le modèle pré-câblé conserve deux extrémités libres intentionnelles, comme une pièce avant terminaison. Le modèle installé est terminé par deux cosses isolées.
"""
BATTERY="""# Batterie 2S révisée - Spektrum G1 IC5

Proposition d’étude du **15 octobre 2026**, après le choix utilisateur de revoir le pack pour une prise plus forte d’usine : **SPMX50002S30H5 G1**. LiPo standard 2S, 7,4 V nominal /8,4 V max, 5 000 mAh /37 Wh, IC5 d’usine. Dimensions 139 × 46 × 25 mm /294 g annoncées sur l’ancienne page fabricant. Prise d’équilibrage trois voies visible sur la photo exacte, famille JST-XH à confirmer sur le lot.

[Achat RC Team](https://www.rcteam.com/products/spektrum-accu-lipo-smart-74v-5000mah-30c-ic5) : 49,99 EUR, SKU exact disponible à la consultation. Référence G1 arrêtée sur le site fabricant actuel ; vérifier état, date et notice du lot. Aucune offre Amazon exacte validée. Aucun achat ni essai matériel.

Le S65 reste proposé pour la G1, à 5 A initialement, **avec un cordon de charge IC5 adapté et l’équilibrage**. Ce cordon reste à sélectionner avant utilisation. Ne pas remplacer la G1 par une G2 dépourvue de prise d’équilibrage. Un seul pack embarqué ; aucune modification de ses fils.

Énergie nominale -3,85 % et masse annoncée +44 g par rapport à la Zeee : fixation et autonomie à vérifier. Objectifs de vitesse et d’autonomie conservés, non mesurés. Les STEP Zeee existants représentent l’ancien pack ; ils ne deviennent pas des modèles Spektrum.

[Notice commune](../../cordon-principal-batterie/notices/notice-cordon-principal-batterie-v3.pdf) · [Révision et sources](../../cordon-principal-batterie/revision-batterie-ic5.md) · [Photo exacte](../../cordon-principal-batterie/references/SPMX50002S30H5-photo-1.jpg) · [Sélection structurée](selection.json).
"""
def write_human_documents(root):
 b=root/'Composants/cordon-principal-batterie'
 contents={'README.md':README,'revision-batterie-ic5.md':RESEARCH,'integration.md':'# Montage du cordon IC5 actif\n\n'+'\n\n'.join(f'{i+1}. {s}' for i,s in enumerate(MOUNT))+'\n','cordon-ic5-spektrum/README.md':CORDREADME,'cordon-ic5-spektrum/cotes.md':COTES}
 for rel,text in contents.items():(b/rel).write_text(text,encoding='utf-8')
 (root/'Composants/batterie/spektrum-g1-ic5/README.md').write_text(BATTERY,encoding='utf-8')
 # Replace only the newly introduced prefix and scoped handoffs in older files.
 import re
 for p in [root/'README.md',root/'SPECIFICATIONS.md',root/'Composants/README.md',root/'Composants/batterie/README.md',root/'Composants/chargeur-batterie/README.md',root/'Composants/maintien-batterie/integration.md']:
  if not p.exists():continue
  s=p.read_text(encoding='utf-8');s=re.sub(r'^> \*\*Révisiondu15octobre2026.*?\n\n','',s,flags=re.S)
  if p.parent==root:link='Composants/cordon-principal-batterie/README.md'
  elif p.parent.name=='Composants':link='cordon-principal-batterie/README.md'
  else:link='../cordon-principal-batterie/README.md'
  prefix=f'> **Révision du 15 octobre 2026 : batterie 2S G1 IC5 et cordon 10 AWG proposés après le choix utilisateur.** [État courant]({link}). Les anciens plans/PDF Zeee restent datés. Charge S65 initiale à 5 A, avec un raccord IC5 distinct à sélectionner avant charge.\n\n'
  p.write_text(prefix+s,encoding='utf-8')
 for p in [root/'README.md',root/'SPECIFICATIONS.md',root/'Composants/README.md',root/'Composants/ENSEMBLES-AVANT-CHASSIS.md',root/'Composants/faisceau-puissance/integration.md',root/'Composants/protection-surintensite/integration.md',root/'Composants/distribution-alimentation/integration.md']:
  if p.exists():
   s=p.read_text(encoding='utf-8');s=re.sub(r'(?s)(<!-- cordon-principal-batterie-v3 -->).*?(<!-- /cordon-principal-batterie-v3 -->)',r'\1\n15 octobre 2026 : version active IC5 après le choix utilisateur, pack G1 SPMX50002S30H5 et cordon SPMXCA510 pré-câblé en 10 AWG. CP0+ vers entrée MIDI M5 ; CP0- vers D- N2, avec deux TE 130191. Après MIDI, ED80 et D+ restent en 6 mm². Variante XT60 non retenue ; courant et coordination du MIDI 60 A à qualifier. Charge IC5/S65 distincte à sélectionner avant charge.\n\2',s);p.write_text(s,encoding='utf-8')
if __name__=='__main__':write_human_documents(Path(__file__).resolve().parents[1])
