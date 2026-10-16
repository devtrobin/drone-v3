# STEP du refroidissement du relais

| Modèle | Type | Aperçu |
| --- | --- | --- |
| [HS251 officiel](sensata-hs251-officiel.step) | Original constructeur inchangé, couleur d'origine ; 1 solide | [PNG](sensata-hs251-officiel.png) |
| [HS251 positionné V3](sensata-hs251-implantation-v3.step) | Même forme officielle, rotation et translation seulement | [PNG](sensata-hs251-implantation-v3.png) |
| [HSP-1 gris 2018](sensata-hsp1-gris-2018.step) | Reconstruction 0,076 mm, encoches ouvertes | [PNG](sensata-hsp1-gris-2018.png) |
| [HSP-1 rose PCN 2023](sensata-hsp1-rose-pcn-2023.step) | Variante d'étude 0,127 mm, contour 2018 supposé | [PNG](sensata-hsp1-rose-pcn-2023.png) |
| [Relais + dissipateur + pad rose](assemblage-d1d100-hs251-hsp1-etude.step) | Assemblage d'implantation ; aucun essai physique | [PNG](assemblage-d1d100-hs251-hsp1-etude.png) |

Le fichier officiel vient du site régional Sensata. Les ailettes, rayons et pattes sont ceux de sa géométrie, sans détails inventés. Le taraudage est représenté par le perçage officiel ; les hélices, états de surface et tolérances physiques ne sont pas représentés. Le constructeur regroupe les éléments du HS251 dans un seul solide.

Le relais conserve la reconstruction extérieure précédente. Les vis de kit HK1, les fixations au châssis, les fils et films d'emballage ne sont pas ajoutés à l'assemblage. **Les deux pads sont des variantes alternatives**, pas deux pièces à empiler. L'épaisseur réelle après serrage et le contour du lot rose restent à vérifier.

Le repère V3 place la face de contact du dissipateur à Z = 40,640 mm, l'axe des trous selon X à ±23,8125 mm, Y = 0. Le relais est tourné de 90° et décalé en Z de 40,767 mm avec un pad rose de 0,127 mm. L'écart entre centres des trous du relais nominal et du STEP est 0,0125 mm par côté ; il est compatible avec l'étude nominale mais ne remplace pas un essai sur pièces.

[Catalogue et métriques](catalogue.json), [provenance](provenance.json), [validation FreeCAD](validation-freecad.json), [fiche](../README.md), [montage et hypothèses](../integration.md).
