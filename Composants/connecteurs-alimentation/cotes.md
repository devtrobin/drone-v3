# Cotes, révisions et fidélité 3D

Unités : mm. Pas de mesure du lot physique. [Catalogue fabricant 2026](https://www.china-amass.com/public/upload/20260207/7fa24f5a6f35ec66c7a115c07a34ab06.pdf), page imprimée 15, index PDF 14 ; [fiche historique V1.2](https://www.shoptronica.com/ficheros/XT60H.pdf), F page 1 / M page 2 ; [plan de la page produit](photos/AMASS-plan-page-produit.png).

| Dimension | Catalogue 2026 | Page produit | Fiche V1.2 |
| --- | --- | --- | --- |
| Longueur F, capot compris hors fils | **24,95** | 25,00 | 23,50 |
| Longueur M, capot compris hors fils | **23,85** | 23,90 | 23,80 |
| Largeur maximale | **16,40** | 16,40 | 16,40 |
| Épaisseur maximale | **9,20** | 9,20 | 9,20 |
| Entraxe contacts | Non coté dans la vue courante | Non coté | **7,20**, conservé comme hypothèse courante |
| Longueur V1.2 entre arrière du contact et face avant | Pas transposée | Pas cotée | F20,20 / M20,50 |
| Segment avant indiqué V1.2 F | Pas transposé | Pas coté | **7,70** ; pas la hauteur générale |

Pour une réservation d'implantation, **25 × 16,4 × 9,2 mm pour F**, hors débattement de prise, longueur de fils, rayon de courbure et tolérances. Les 0,05 mm entre arrondi et catalogue ne sont pas une tolérance publiée. L'ancienne cote 20,2/20,5 ne désigne pas automatiquement le corps plastique complet.

## Construction des STEP

Les enveloppes F24,95 et M23,85 suivent **une même révision : catalogue 2026**. Profil extérieur détrompé, deux contacts métalliques séparés, logements femelles creux, broches mâles fendues, godets ouverts à souder, collerette, capot arrière creux, trous de sortie de fils, rainures de prise et fenêtres de clips. Marquages simplifiés gravés XT60H-F/M et +/-. Couleurs de lecture : PA jaune, capot gris sombre, contacts dorés ; pas de mesure colorimétrique.

Les diamètres internes, lèvres, fentes, épaisseurs, rayons, clips et gravures ne sont pas cotés intégralement dans les sources : **détails estimés**, pas CAO fabricant. Le Ø3,5 de contact, le godet Ø3,3, l'entraxe de la fiche V1.2 et la répartition des longueurs avant/capot sont des hypothèses d'implantation actuelle. Aucun résultat électrique déduit du volume de métal représenté.

Repère des pièces : X = entraxe des contacts, Y = épaisseur, Z = axe de connexion, face avant z=0, fils vers +Z. Capot isolé : face avant z=0. La paire accouplée est illustrée avec **7,5 mm d'engagement estimé**, sans collision volumique ; pas un ajustement qualifié. La vue éclatée décale les contacts et capots pour lecture, pas une instruction de démontage des contacts moulés.

Le modèle câblé représente du cuivre équivalent **3,31 mm²** avec une gaine Ø4,2 mm estimée, pas un fil acheté ni son nombre réel de brins. Soudure et fins dénudées illustratives. Dimensions du faisceau à arrêter après implantation. Les symboles + et - de la CAO ne remplacent pas la vérification des inscriptions, du point de vue avant/arrière et de la polarité réelle au multimètre.

## Données électriques séparées

| Source | Courant | Autres valeurs |
| --- | --- | --- |
| AMASS V1.2 | 30 A RC / 60 A MC, durée MC non publiée | 0,50 mΩ CR ; 1 000 usages ; 12 AWG ; PA UL94 V0 ; laiton doré ; -20 à +120 °C |
| AMASS catalogue 2026 p.15 | 35 A MAX (12 AWG / Δ < 85 °C) | 100 cycles ; IP40 ; tenue 500 V DC ; -20 à +120 °C ; UL94 V0 |
| Page fabricant courante | 35 A MAX (12 AWG / Δ < 85 K) | PA / laiton doré ; 100 cycles ; 48 h brouillard salin ; isolation ≥2 000 MΩ |

La page HTML imprime « ≤1.2MΩ » à la ligne résistance de contact : unité incohérente avec l'isolation et l'usage. **Ne pas recopier 1,2 MΩ comme résistance de contact.** Aucun plafond moderne en mΩ n'est adopté sans fiche de spécification du lot. Le lien LCSC 2023C0 redirige vers une visionneuse et n'a pas fourni de PDF original exploitable dans cette collecte ; il n'est pas utilisé pour combler cette erreur d'unité. Pour les calculs, 0,50 et 1,20 mΩ sont seulement deux valeurs d'analyse explicitement conditionnelles.

500 V est une valeur de tenue du document courant, pas un besoin du robot alimenté en 2S. IP40 n'est pas une étanchéité à l'eau. Ni PA120 °C ni Δ85 K ne fixent une température acceptable des soudures, câbles et interfaces du robot.
