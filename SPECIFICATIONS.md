# Spécifications de cadrage — V3

Date : **12 octobre 2026**. Les valeurs ci-dessous sont des objectifs, pas des performances acquises.

| Fonction | Exigence ou point à préciser |
| --- | --- |
| Véhicule | Drone terrestre, dans la continuité de V1 et V2 |
| Budget | 200 € pour tout le matériel neuf, sans crédit de réutilisation ; inclure fabrication et livraison |
| Vitesse | Objectif de 40 km/h, avec autonomie à cette vitesse à valider |
| Autonomie à 40 km/h | Minimum visé 10 minutes ; objectif haut 20 minutes, vidéo active |
| Autonomie à 20 km/h | Au moins 45 minutes, vidéo active |
| Autonomie à vitesse inférieure | Rechercher une durée supérieure ; quantifier par essais, sans extrapolation inverse simple |
| Retour vidéo | 1920 × 1080, 60 images/s réellement acquises, transmises et affichées |
| Pilotage | Depuis le Mac existant, continuité de V1/V2 |
| Liaison | Wi-Fi ; exploiter sa portée utile avec vidéo active, sans portée chiffrée garantie |
| Terrain | Sol plat intérieur ; revêtement et espace disponible à relever |
| Fabrication | Châssis fabriqué, composants séparés ; pas de voiture RC complète |
| Latence | Mesurer le retard caméra–écran ; seuil d'acceptation à définir selon vitesse et distance de freinage |
| Arrêt | Freinage maîtrisé, arrêt sur perte de commande et absence de départ au démarrage ; à concevoir et tester |

Un flux enregistré localement en 1080p60 ne satisfait pas à lui seul l'exigence de retour vidéo. Un affichage à 60 Hz avec duplication d'images ne la satisfait pas non plus.

Les autonomies sont à obtenir sur une seule charge embarquée, sans échange de batterie pendant l'essai. Convention de dimensionnement à confirmer avant validation : vitesses réellement mesurées, vidéo active et énergie de tous les circuits incluse. Le réseau et le Mac déjà présents sont des infrastructures supposées ; tout équipement réseau supplémentaire requis doit être chiffré.

## Références antérieures

- V1 : cible d'autonomie minimale de 15 minutes et vidéo 720p30, sans résultat physique enregistré dans l'état du projet.
- V2 : cible minimale de 15 minutes ; estimation centrale de 4 h 53 à 5,8 W et environ 2,2 km/h. Ni autonomie ni vitesse mesurées.
- V2 : budget historique de 257,03 € hors livraison, déjà supérieur au plafond demandé pour V3.

Sources locales : [V1](../drone-v1/SPECIFICATIONS.md), [état V1](../drone-v1/project_state.md), [prévisions V2](../drone-v2/Mecanique/performance.md), [état V2](../drone-v2/project_state.md).
