# Révision de la batterie et du cordon IC5

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
