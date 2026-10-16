<!-- alimentation-r2 -->
> **Sélection active révisée le 15 octobre 2026.** Appliquer le tableau de raccordements révisé : classe T, branches Midget, fil LAPP 6 mm², 18 AWG Pi et neuf signaux GPIO. Les nomenclatures, PDF et assemblages précédents restent des instantanés.
> [État électrique courant](../verification-alimentation/README.md) · [Raccordements](../verification-alimentation/integration.md). Les références différentes dans les documents ci-dessous sont historiques. Qualification matérielle non réalisée ; confirmations restantes explicites.
<!-- /alimentation-r2 -->

# Raccordements et notice de montage du projet

| Repère | Chemin | Section / couleur | Terminaisons | Statut |
| --- | --- | --- | --- | --- |
| CP1+ | MIDI sortie → D+ P2 | 6 /rouge | 95R5 ; 95R5 | hors interface batterie |
| CP2+ | D+ P3 → relais +2 | 6 /rouge | 95R5 ; 95R4 | hors interface batterie |
| CP3+ | relais 1 → UD-80A IN | 6 /rouge | 95R4 ; borne UD / embout à qualifier | borne lot à qualifier |
| CP0+ | interface batterie → MIDI entrée | 6 /rouge | interface ouverte ; 95R5 conditionnelle | interface batterie non arrêtée |
| CP0- | interface batterie → D− N2 | 6 /noir | interface ouverte ; 95R5 | interface batterie non arrêtée |
| CM1- | XT60H-F1 → D− N1 | 12 AWG /noir | XT60 soudé ; Ancor 312303 | sertissage à qualifier |
| CM2- | XT60H-F2 → D− N3 | 12 AWG /noir | XT60 soudé ; Ancor 312303 | sertissage à qualifier |
| CM1+ | 5065 ATO30 ESC1 → XT60H-F1 | 12 AWG /rouge | Ancor 309203 ; XT60 soudé | sertissage à qualifier |
| CM2+ | 5065 ATO30 ESC2 → XT60H-F2 | 12 AWG /rouge | Ancor 309203 ; XT60 soudé | sertissage à qualifier |

Les sorties UD S1/S4 utilisent les fils 12 AWG déjà inclus dans les 5065 ; il ne faut pas rajouter un autre fil dans le même port. Le 5065 Pi peut recevoir la troisième 312303 sur son arrivée D+P4. Le retour électronique D−N4 et les petits fils de commande ont une section encore à définir. D+P1 reste libre.

## Quantités de terminaisons

Deux Ancor 312303 pour les retours moteurs, avec une troisième conditionnelle pour P4 ; deux 309203 plus un spare dans le pack 3 ; deux 95R4 ; quatre 95R5 hors extrémité positive de l’interface pack, plus une cinquième conditionnelle en entrée MIDI. Sept gaines de cosse prévues si cette cinquième est retenue. Un stock de huit morceaux 20 mm inclut une réserve, mais ne constitue pas la liste de coupe.

## Préparation et outillage

1. Débrancher pack et équilibrage. Positionner les pièces et relever les chemins ; choisir les longueurs sans tension sur les connexions et prévoir maintien et dégagement.
2. Vérifier références, matières, section, diamètre de gaine, passage des œillets, largeur d’appui et état. Mesurer le lot ; aucun brin retiré pour faire entrer un fil.
3. Passer capots et gaines avant terminaison. Régler le dénudage sur le canon réel et la procédure de l’outil ; 10 mm du modèle du fil est illustratif. Aucun dénudage de 17 mm appliqué automatiquement à une cosse de 9 mm.
4. Ancor : outil à cliquet pour cosses thermorétractables, plage 12–10 AWG jaune. Le catalogue 2020 p.54 cite **703010** pour heat-shrink ; la double pince 703030 y est destinée aux nylon/vinyle. Un sertissage de cuivre et une rétraction de gaine sont deux opérations distinctes. Sur un manchon, terminer chaque côté séparément selon l’outil ; ne pas sertir seulement le centre.
5. Klauke : outil/matrice pour cosses tubulaires Cu standard 6 mm², selon la table fabricant PDF p.40. La K2 figure parmi les outils 0,75–16 mm² ; faire confirmer la combinaison 95R4/95R5, câble réel et procédure du lot. Ne pas prendre par défaut une matrice de cosse isolée Ancor.
6. Sertir sans ajouter de soudure non prévue. Contrôler insertion et absence de brins libres ; sur Klauke utiliser le trou de contrôle. Faire des éprouvettes avec le fil réel et contrôler tenue, section du sertissage et résistance avant les raccords définitifs. La force d’essai suit le système documenté, aucune force universelle inventée.
7. Ancor : rétraction 135 °C annoncée. ATUM : début 80 °C, rétraction complète 110 °C. Ces valeurs ne sont pas la consigne du pistolet. Chauffer localement selon le lot, préserver le PVC et les éléments voisins, puis inspecter l’adhésif et la gaine. Ne pas masquer les surfaces de contact et ne pas réchauffer un pack branché.
8. Monter une seule cosse prévue par borne du relais, sans empilement arbitraire. Garder les vis et écrous d’origine et suivre le couple indiqué pour le lot de chaque appareil. Ne pas remplacer une #8-32 par une M4 ou une #10-32 par une M5.
9. UD-80A : admission des fins brins et embout à confirmer. La fiche IEC décrit 17 mm/3,5 Nm ; l’alternativeUL décrit 9,14 mm/2,2 Nm. Suivre les instructions du lot et du système choisi. Ni une moyenne ni l’application aux cosses n’est justifiée. Un embout n’est pas encore une référence sélectionnée.
10. Fixer les MB2 avec vis M4 adaptées au châssis ; vis non incluses présumées. Poser les T18R sans écraser le câble, couper la queue proprement, protéger les arêtes et garder les fils hors roues, courroies, engrenages et ailettes chaudes. Ne pas serrer les colliers à 80 N : c’est une résistance de boucle annoncée.
11. Contrôler continuité, polarité, isolement, serrages et aucun contact de puissance exposé. Vérifier ensuite sous alimentation supervisée et limitée adaptée, courant et chutes de tension, température des câbles, cosses, prises et protections durant l’usage réel. Les ATO30 et le MIDI60 ne limitent pas le courant à 20/44 A.

## Dimensionnement restant à qualifier

Le scénario utilise 20 A par ESC,40 A total moteurs, et 44,39 A commun avec Pi et surveillance. Le 6 mm² est une section d’étude ; ni son ampacité dans l’implantation ni sa protection en défaut ne sont validées par le tableau de résistivité. L’interface commune XT60 du pack, les pointes, les fils 16 AWG d’usine et la coordination des fusibles restent à qualifier. Aucun godet XT60 n’est agrandi, aucun pack modifié.

Le servo reçoit un seul BEC6 V ; l’autre positifBEC est isolé. Les phases moteurs, fils de commande et liaison caméra ne sont pas concernés par ces raccords de puissance.

Les notices antérieures sont des états datés. Cette sélection complète leurs mentions « cosses/raccords à choisir » sans déclarer le matériel testé.

[Dossier commun](README.md), [nomenclature](nomenclature.json), [calculs](calculs.json), [notice PDF](notices/notice-faisceau-puissance-v3.pdf).

<!-- complements-avant-chassis-v3 -->

Mise à jour du 14 octobre 2026 : [coupure ED80 et deux cosses M6](../coupure-manuelle/integration.md) sur le positif commun **après MIDI, avant D+**. Le segment direct CP1+ est remplacé par CP1A+ MIDI→ED80 et CP1B+ ED80→D+. Les deux cosses 95R5 sont réutilisées ; deux 95R6 sont ajoutées. Les anciens PDF/STEP de faisceau ne comprennent pas ce changement et restent des références datées.

[Liaisons alimentation/mesure](../liaisons-alimentation-surveillance/integration.md) et [commandes servo/ESC](../connecteurs-commande/integration.md) détaillent les extrémités aval. L’interface batterie XT60 reste à qualifier ; schéma/routage de surveillance, support caméra, visserie restante et châssis réservés pour la phase finale.

<!-- /complements-avant-chassis-v3 -->


<!-- cordon-principal-batterie-v3 -->
15 octobre 2026 : version active IC5 après le choix utilisateur, pack G1 SPMX50002S30H5 et cordon SPMXCA510 pré-câblé en 10 AWG. CP0+ vers entrée MIDI M5 ; CP0- vers D- N2, avec deux TE 130191. Après MIDI, ED80 et D+ restent en 6 mm². Variante XT60 non retenue ; courant et coordination du MIDI 60 A à qualifier. Charge IC5/S65 distincte à sélectionner avant charge.
<!-- /cordon-principal-batterie-v3 -->
