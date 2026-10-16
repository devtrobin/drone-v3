> **R?vision active du15 octobre2026.** D1D100/HS251 conserv?s. R?gime moteur continu ?tudi?30 A ;40 A constitue le sc?nario court. V?rifier temp?rature dejonction ettransitoires selonl?audit. [?tat courant](../verification-alimentation/README.md). Les valeurs diff?rentes de l?alimentation dans les documents anciens restent historiques.

# Dissipateur du relais moteurs - Sensata/Crydom HS251

**Choix d'étude du 13 octobre 2026 : HS251 + une interface HSP-1. Non acheté, non testé.** Le dissipateur refroidit le D1D100 qui alimente les deux ESC arrière. Il ne refroidit ni les moteurs ni le Raspberry Pi.

Le HS251 est retenu pour sa résistance thermique documentée, son faible poids dans cette famille et ses fixations compatibles. La limite de travail proposée est **40 A au total en continu, avec un air local à 40 °C au maximum**, sous réserve d'essais et d'une convection suffisante. Le courant réel des moteurs n'est pas encore mesuré. Les 30 A de chaque ESC sont une capacité annoncée, pas la consommation du robot.

| Caractéristique | Donnée et origine |
| --- | --- |
| Référence | Sensata/Crydom **HS251**, dissipateur seul ; ne pas confondre avec HS251-D2450, ensemble avec relais AC |
| Résistance thermique | 2,5 °C/W, constructeur ; conditions de convection à respecter |
| Matière / finition | Aluminium naturel, sans traitement de surface annoncé |
| Masse | 100 g, fiche 2024 ; catalogue historique : 99 g |
| Fixation du relais | Deux taraudages **#8-32 UNC**, entraxe nominal 47,6 mm ; kit HK1 associé |
| Serrage | Dissipateur : 1,7-2,2 N·m ; D1D100 : 2-2,2 N·m ; guide HS : 2,2 N·m |
| Enveloppe complète de la CAO officielle | Environ **85,3 × 52,3 × 40,6 mm**, pattes incluses, dans le repère d'implantation V3 |
| Corps annoncé dans le catalogue | 58,7 × 50,3 × 38,4 mm ; cette valeur exclut les pattes et ne suffit pas à réserver l'espace |
| Ventilation | Passive ; pas de ventilateur fourni ou de fixation de ventilateur annoncée |
| Achat Amazon.fr | [Recherche HS251](https://www.amazon.fr/s?k=Crydom+HS251) : lien de recherche, **aucune offre exacte ni ASIN vérifié** |
| Prix français | Non confirmé ; hors budget chiffré tant qu'une offre livrable n'est pas vérifiée |

[Notice PDF du projet](notices/notice-dissipateur-relais-v3.pdf), [documents fabricant](notices/README.md), [recherche, alternatives et avis](recherche-technique.md), [montage et essais](integration.md), [modèles STEP et aperçus](3D/README.md), [source et cotes structurées](sources.json), [archives et SHA256](assets.json).

Le dossier contient le **STEP officiel inchangé**, une copie positionnée pour la V3, deux variantes d'étude du HSP-1 et un assemblage avec le relais. Les variantes de pad sont des alternatives de lot : **une seule interface est montée**, jamais les deux empilées.

Les PDF et la photo ont été récupérés via les miroirs publics Farnell/Newark/RS ; le STEP provient du site régional officiel Sensata. Les URL réellement utilisées et les échecs de téléchargement figurent dans `assets.json`. La disponibilité française et la conformité du lot reçu restent à vérifier.
