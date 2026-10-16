# Recherche, alternatives, prix et témoignages

Recherche du **14 octobre 2026**. Le besoin est une jonction positive après SSR, pour deux départs protégés, avec capacité publiée supérieure ou égale à 60 A et une arrivée 6 mm². Une unité **nVent ERIFLEX UD-80A / 569010** est retenue pour l'étude.

| Solution examinée | Résultat |
| --- | --- |
| **UD-80A, 569010** | 80 A IEC, capot, arrivée 6–16 mm² et sorties adaptées au 12 AWG des supports ; fixation panneau, notice et CAO officielles disponibles |
| UKK80 générique | Annonces et tableaux marchands 80/85 A, variantes et dimensions différentes ; pas d'identification constructeur fiable pour une offre Amazon exacte, non assimilé au nVent |
| Blue Sea 2315 déjà retenu | 100 A documentés, mais 106,68 mm de long et environ 80 g ; un troisième bus n'est pas ajouté ici |
| Blue Sea 2303/2307 | 150 A, quatre goujons 1/4-20 ; cosses et encombrement supplémentaire, non retenu pour cette jonction |
| Mini PowerPost / empilage sur SSR | Connexions et capacité dépendant des cosses ; notre proposition évite un empilage non qualifié sur le relais |
| Répartiteur de charge à MOSFET ou diodes | Fonction différente et souvent 12/24 V ; ne remplace pas une jonction passive pour notre 2S et sa régénération |

## Achat et conditionnement

Requêtes Amazon : `Eriflex UD-80A 569010`, `répartiteur unipolaire 80 A`, `UKK80`, variantes Blue Sea. [Recherche Amazon.fr exacte](https://www.amazon.fr/s?k=Eriflex+UD-80A+569010) : réponse directe vide, **aucun ASIN exact, stock, vendeur ou prix vérifié**. L'icône Amazon affichée sur ejoker correspond au paiement, pas à une preuve de vente sur Amazon. Aucune commande effectuée.

Alternative française précise : [RS 277-6180](https://fr.rs-online.com/web/p/blocs-de-distribution/2776180), référence fabricant 569010, **17,61 € HT / 21,13 € TTC** affichés, stock annoncé. Frais de traitement/livraison non inclus dans ce prix validé ; ne pas prétendre une livraison gratuite pour une commande isolée. Repère étranger : Iconopower annonce 17,15 USD, hors conditions France. Le conditionnement fabricant est **une pièce**, avec capot. Aucun rail, embout ou conducteur supposé fourni.

## Documents qui lèvent les ambiguïtés

- [Fiche fabricante 2023 via RS](notices/nVent-UD80A-fiche-FR-2023-via-RS.pdf) : 80 A IEC / 85 A UL, plages distinctes entrée/sorties, nominal 69×30×46 mm, 70 g, IP20 et déclassement.
- [Notice IP7802_M](https://nvent.widen.net/content/vhxyvvgeqg/original/ip7802.pdf), deux pages : tableau IEC et tableau UL, dénudage, couples, serrage des orifices inutilisés, maintien de l'entrée vers 15 cm, fixation et condition de SCCR. Couples/dénudages des grosses bornes divergent entre régimes ; ne pas les mélanger et vérifier la notice reçue.
- [Spécification UD 2022](notices/nVent-UD-specifications.pdf) : composition générale, bornes et capot, ambiantes selon IEC/UL/CSA ; ce document de famille n'est pas une preuve de grade ou de performance de chaque lot.
- Catalogue P1215C et fiches 2020 sont conservés comme références historiques ; ni une température marchande « minimum 30 °C » ni une longueur Graybar de colis ne remplacent les documents fabricant.
- La page nVent contient un module CAD dynamique public. Le service proposé a fourni un **ZIP AP214**, dont le STEP est conservé intact. Pas d'authentification, de compte ou de contact fabricant utilisé.

Citation courte, fiche nVent française : **« Capot à charnière articulée et amovible »**. Le capot inclus est modélisé séparément ; il protège les doigts selon IP20, sans étanchéité annoncée.

## Retours utilisateurs et vidéos

[Forum PLCtalk, discussion « SCCR in the feeder »](https://www.plctalk.net/forums/threads/sccr-in-the-feeder.125932/), **rupej, 11 août 2020, message nº8**, dit utiliser souvent le UD-80A et interroge son SCCR. **jraef, message nº9**, renvoie à la notice et à la protection Class J/T. Témoignage d'usage industriel, pas test de notre robot ; l'information de coordination est corroborée par la notice officielle, pas acceptée sur le seul forum.

Iconopower affiche 5/5 avec **un avis intitulé « test3 » signé Iconopower Admin** en 2016. Ce n'est pas un retour utilisateur indépendant et il est exclu de l'appréciation de fiabilité. Aucun taux de panne, mesure de chute ou essai thermique V3 trouvé.

Recherches YouTube par `Eriflex UD80A`, `UD-80A installation` : aucun essai exact attribuable à cette référence apportant courant/thermique/défaut LiPo identifié. Aucune vidéo non visionnée utilisée comme preuve. Aucun forum, vendeur ou fabricant contacté.

## Points encore à qualifier

Serrage/dénudage du régime applicable au lot, compatibilité du fil d'entrée souple et de l'embout, passage des vis de panneau, retenue du faisceau et place d'ouverture. Mesurer chutes et échauffement avec notre courant et les câbles réels. Le SCCR 100 kA conditionnel ne qualifie ni notre MIDI, ni les ATO à 1 000 A, ni le SSR. La sélection n'établit aucune vitesse ou autonomie physique.
