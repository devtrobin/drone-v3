<!-- complements-r3 -->
> **Compléments du 17 octobre 2026 :** [dossier R3](Composants/complements-finalisation-r3/README.md), [assemblage FreeCAD R3](Assemblage/R3/drone-v3-r3-faisceau.FCStd). Partie fixe du faisceau définie et contrôlée ; [anomalie d’alimentation de direction](Composants/complements-finalisation-r3/alimentation-direction-a-revoir.md) et confirmations fournisseur encore ouvertes. Aucune pièce reçue, aucun essai physique réalisé.
<!-- /complements-r3 -->

<!-- finalisation-r2 -->
> **Revue du16octobre2026 :** [finalisation théoriqueR2](Composants/finalisation-theorique-r2/README.md), [visserie nominale](Composants/visserie-finale/README.md) et[assemblageR2](Assemblage/R2/README.md). Correction du dimensionnement de direction, arbres/paliers etimplantation repris. Des [conditions documentaires etde conception](Composants/finalisation-theorique-r2/conditions-restantes.md) restent ouvertes ; le véhicule complet n’est pas libéré pour fabrication/mise sous tension. Les modèles ultra détaillés précédents décriventA2-R1.
<!-- /finalisation-r2 -->

> **Surveillance M1P :** [porteuse pour fabrication de prototype et banc limit?](Composants/carte-surveillance-electrique/fabrication/README.md). Gerbers et proc?dure pr?par?s ; aucun essai r?alis?, cotes TI exactes et raccordement LiPo non lib?r?s.

# Drone terrestre V3

[Assemblage 3D complet et sous-ensembles](Assemblage/README.md) : vue FreeCAD détaillée à affichage rapide, CAO intégrale de 5 441 solides, GLB complet et cinq STEP d'implantation légers pour CAD Viewer.

Robot à châssis fabriqué, avec deux moteurs arrière et deux roues avant directrices. Raspberry Pi 5 de 4 Go pour la commande, le Wi-Fi et la vidéo. Objectifs : 40 km/h, 10–20 min à 40 km/h, au moins 45 min à 20 km/h, retour vidéo 1080p60 vers le Mac. Budget initial de 200 EUR pour le matériel neuf ; dimensionner les performances puis rechercher les économies. Aucun achat ou essai matériel.

[Composants](Composants/README.md) · [Spécifications](SPECIFICATIONS.md) · [Faisabilité](faisabilite.md) · [Index précédent archivé](archives/README-avant-correction-alimentation-2026-10-15.md).

**Alimentation révisée le 15 octobre 2026 :** Spektrum G1 SPMX50002S30H5, 2S 5 Ah IC5 ; cordon SPMXCA510 10 AWG ; principal proposé JLLN50 classe T ; départs moteurs KLKD20 ; départ Pi KLKD10 et régulateur Pololu D42V55F5 ; fil principal LAPP 6 mm² ; faisceau GPIO de signaux séparé de l’alimentation. [Audit, calculs et confirmations restantes](Composants/verification-alimentation/README.md), [raccordements](Composants/verification-alimentation/integration.md).

**Charge complétée :** Sky RC S65 conservé, cordon Beez 2B BEEC1067 XT60–EC5 et rallonge XH 2S dédiée. LiPo Balance 2S / 5 A, 42 W maximum. [Dossier de charge](Composants/cordon-charge-s65-ic5/README.md).

Caméra InnoMaker U20CAM-4M, deux Hobbywing 2435SL G3 4500 KV / WP16BL30 G2, quatre HobbyPark 63 × 26 mm, direction, réduction et autres composants documentés dans leurs dossiers. Les anciens PDF et assemblages électriques sont des références datées ; suivre la sélection révisée.

La qualification complète des protections reste ouverte : confirmations fabricant sur les supports et les brins fins, conditions de coupure DC, puis essais instrumentés. Le budget commun de 36 A est une enveloppe de dimensionnement ; 44–46 A est un scénario de pointe, pas une consommation mesurée de roulage. Les autonomies demandées nécessitent une puissance moyenne totale nettement plus basse.

**Ordre retenu :** [carte de surveillance, support caméra, supports capteurs, châssis, puis visserie finale](PLAN-CONCEPTION.md). La [surveillance M1 à modules existants](Composants/carte-surveillance-electrique/README.md) dispose de son schéma, routage, notice et STEP de porteuse avec gabarits. Contrôles KiCad réussis ; disponibilité, cotes EVM et qualification matérielle restent ouvertes.


[Mesure de vitesse des deux roues arrière](Composants/capteurs-vitesse/README.md) : deux capteurs Hall, deux aimants par roue, rappels et découplages ; extension GPIO à13 contacts. Implantation finale avec le châssis.
