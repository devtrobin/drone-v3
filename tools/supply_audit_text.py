"""French text for the corrected electrical documentation."""
REGULATOR = '''# Régulateur actif : Pololu D42V55F5 / 5571

Remplace le D24V90F5 dans la sélection du 15 octobre 2026. **Sortie 5 V, pas 5,3 V.** [Source Pololu](https://www.pololu.com/product/5571). Prix fabricant affiché : 47,95 USD ; TVA, livraison France et offre Amazon.fr non confirmées. Non acheté et non testé.

La sortie annoncée est 5 V ±3 %, soit 4,85–5,15 V. L’entrée nominale est 5–60 V, sous réserve du dropout ; le courant continu typique est de 5–8 A selon les conditions. À 5 A, la courbe officielle donne un dropout d’environ 0,25 V. Le rendement de 80–95 % est typique. Ces courbes ne garantissent pas la tenue thermique dans le véhicule.

PCB nominal 25,4 × 25,4 mm. Le [plan original](notices/Pololu-D42V55Fx-plan-original.pdf) définit les interfaces. VIN, GND, VOUT, EN, PG : ne pas recopier le raccordement FB de l’ancien modèle. Prendre la puissance aux grands pads. La [CAO officielle](3D/README.md) est conservée sans modification.

La liaison Pi utilise deux positifs et quatre retours courts en 18 AWG, soudés aux pads du connecteur Pi. Le Molex reste réservé aux signaux. Critères de réception : VIN ≥5,8 V et 4,75–5,25 V mesurés aux pads Pi, à 0–5 A, y compris démarrage et échelons. Aucun montage effectué.

[Révision électrique](../../verification-alimentation/README.md) et [raccordements](../../verification-alimentation/integration.md).
'''

CHARGE = '''# Cordon de charge S65 vers pack IC5

Sélection du **15 octobre 2026 : Beez2B BEEC1067**, cordon XT60–EC5 de 12 cm, livré à l’unité. [Achat RC Team](https://www.rcteam.com/products/beez2b-cable-de-charge-xt60-vers-ec5-beec1067) : **6,90 EUR TTC**, SKU exact disponible dans le JSON public consulté. Aucun achat effectué ; aucune offre Amazon.fr exacte confirmée.

Le vendeur cite explicitement le S65, NANO B6 / Lite et T200. Spektrum documente la compatibilité IC5/EC5 pour la puissance. Le pack G1 utilise ici ses deux contacts de puissance, sans donnée Smart. Les désignations commerciales mâle/femelle varient entre logements et contacts : commander la référence compatible S65, puis contrôler les contacts et la polarité.

Ajouter **une rallonge INTERMODEL 3-RAL2S d’équilibrage 2S dédiée au chargeur**, distincte de celle de surveillance. Elle prolonge les trois voies XH du G1 vers le port d’équilibrage S65 selon son manuel. Les liaisons de puissance et d’équilibrage sont toutes deux nécessaires. Charger le pack retiré du véhicule.

Réglage initial : **LiPo BALANCE, 2S, 5 A (1C), 4,20 V par cellule**, soit 8,40 V et 42 W au maximum ; le S65 dispose de 65 W et 6 A. Cela concerne le **G1 avec prise d’équilibrage**. Un G2 sans câble classique n’est pas interchangeable. Les 5,2 A de l’ancienne Zeee ne sont plus le réglage actif.

[Notice PDF](notices/notice-cordon-charge-s65-ic5-v3.pdf) · [procédure](notice-montage.md) · [sélection et prix](selection.json) · [photo](references/Beez2B-photo-0.jpg) · [stock archivé](references/Beez2B-BEEC1067-stock.json).

Les 12 cm sont annoncés, pas mesurés. Section exacte, isolant et courant admissible du cordon ne sont pas publiés dans la fiche consultée. Critère de réception choisi : section au moins 16 AWG pour 5 A, contrôle de polarité et d’échauffement. Ce cordon sert à la charge de 5 A ; il ne remplace pas le cordon de propulsion. Aucun modèle 3D reconstruit ici : les dimensions non publiées restent inconnues.
'''

CHARGE_INSTALL = '''# Montage et première charge

1. Mettre hors tension le S65. Débrancher puissance et équilibrage du véhicule ; placer le pack hors du châssis.
2. Vérifier SPMX50002S30H5 G1, état et notice du lot. Contrôler le BEEC1067 : continuité rouge/noir, absence de court-circuit, polarité et contacts compatibles. Ne pas forcer un logement différent.
3. Respecter l’ordre du constructeur S65 : cordon côté chargeur avant le pack ; puissance et équilibrage selon sa notice. Vérifier le repère négatif et l’alignement des trois voies 2S dans le port 2–4S, sans centrer la prise au hasard.
4. Sélectionner LiPo BALANCE 2S / 5 A / 4,20 V par cellule. Vérifier les deux cellules détectées et les tensions avant START. Aucun mode LiHV ou G2 Smart nécessaire.
5. Surveiller la première charge et les températures selon les notices SkyRC et Spektrum. Arrêter en cas d’erreur ou d’échauffement anormal. Ne pas charger à travers les bornes D+ / D− du véhicule.
6. À la fin, respecter l’ordre de déconnexion constructeur : retirer le pack des liaisons avant le cordon du chargeur. Utiliser STORAGE selon la notice pour le stockage ; pack déconnecté du véhicule.

[Notice S65 originale V2.10](../chargeur-batterie/notices/SkyRC-S65-notice-constructeur-EN-V2-10.pdf). [FAQ G1/G2 originale](../cordon-principal-batterie/notices/README.md). L’EC5 ne transporte pas de donnée Smart ; l’équilibrage passe par XH. Les prises ne sont pas validées physiquement dans ce workspace.
'''

ROOT_README = '''# Drone terrestre V3

Robot à châssis fabriqué, avec deux moteurs arrière et deux roues avant directrices. Raspberry Pi 5 de 4 Go pour la commande, le Wi-Fi et la vidéo. Objectifs : 40 km/h, 10–20 min à 40 km/h, au moins 45 min à 20 km/h, retour vidéo 1080p60 vers le Mac. Budget initial de 200 EUR pour le matériel neuf ; dimensionner les performances puis rechercher les économies. Aucun achat ou essai matériel.

[Composants](Composants/README.md) · [Spécifications](SPECIFICATIONS.md) · [Faisabilité](faisabilite.md) · [Index précédent archivé](archives/README-avant-correction-alimentation-2026-10-15.md).

**Alimentation révisée le 15 octobre 2026 :** Spektrum G1 SPMX50002S30H5, 2S 5 Ah IC5 ; cordon SPMXCA510 10 AWG ; principal proposé JLLN50 classe T ; départs moteurs KLKD20 ; départ Pi KLKD10 et régulateur Pololu D42V55F5 ; fil principal LAPP 6 mm² ; faisceau GPIO de signaux séparé de l’alimentation. [Audit, calculs et confirmations restantes](Composants/verification-alimentation/README.md), [raccordements](Composants/verification-alimentation/integration.md).

**Charge complétée :** SkyRC S65 conservé, cordon Beez2B BEEC1067 XT60–EC5 et rallonge XH 2S dédiée. LiPo Balance 2S / 5 A, 42 W maximum. [Dossier de charge](Composants/cordon-charge-s65-ic5/README.md).

Caméra InnoMaker U20CAM-4M, deux Hobbywing 2435SL G3 4500 KV / WP16BL30 G2, quatre HobbyPark 63 × 26 mm, direction, réduction et autres composants documentés dans leurs dossiers. Les anciens PDF et assemblages électriques sont des références datées ; suivre la sélection révisée.

La qualification complète des protections reste ouverte : confirmations fabricant sur les supports et les brins fins, conditions de coupure DC, puis essais instrumentés. Le budget commun de 36 A est une enveloppe de dimensionnement ; 44–46 A est un scénario de pointe, pas une consommation mesurée de roulage. Les autonomies demandées nécessitent une puissance moyenne totale nettement plus basse.

Schéma et routage de surveillance, support caméra, visserie finale et châssis seront conçus ensemble à la fin, selon l’instruction utilisateur. Aucune carte de puissance ou pièce de châssis prête à fabriquer à ce stade.
'''

QUOTE = '''# Devis de correction — consultation du 15 octobre 2026

Aucune commande. Les frais, outils, TVA finale et disponibilités avant achat restent distincts.

| Référence | Quantité | Prix / état |
| --- | ---: | --- |
| Beez2B BEEC1067 | 1 | 6,90 EUR TTC, RC Team, SKU disponible dans le JSON public |
| INTERMODEL 3-RAL2S pour charge | 1 supplémentaire | 1,40 EUR TTC au relevé antérieur ; à revalider |
| JLLN050.T | 1 | Achat France non confirmé ; recherche par référence fournie |
| LFT300601C / capot LFT30060FBC | 1 / 1 | Stock américain affiché ; résultat Europe indexé à 21,96 EUR, TVA et stock France non confirmés ; capot non chiffré |
| KLKD020.T / KLKD010.T | 2 / 1 | Prix France non confirmés |
| L60030M1PQ | 3 | Résultat DigiKey France : 26,448 EUR TTC par pièce ; 79,344 EUR pour trois, à revalider. Association DC à confirmer avant achat. |
| SPL001, capots des supports de branche | 3 | Prix France non confirmé ; distincts des supports |
| LAPP 0054104 / 0054001 | Provision de 2 m par couleur | Prix France non confirmé ; remplace le FLRY-B |
| TE SOLISTRAND 32151 | 1 | Prix France non confirmé ; raccord du positif avant F0 |
| ATUM 8/2 au raccord | Provision de 35–40 mm | À prélever sur le lot prévu ; longueur finale selon recouvrement et retrait |
| WAGO 221-413 côté entrée Pi | 2 supplémentaires | Ancien prix de 0,75 EUR TTC par pièce, soit 1,50 EUR à revalider ; distinctes des bornes de sortie déjà prévues |
| Pololu 5571 D42V55F5 | 1 | 47,95 USD fabricant ; TVA, importation et livraison France non confirmées |
| Fil 18 AWG, WAGO et cosses restantes | Selon implantation | Utiliser les lots déjà prévus, sans doublon ; ils ne sont pas considérés comme déjà possédés |

Complément de charge : **8,30 EUR** avec l’ancien prix de rallonge, hors livraison et revalidation. Les protections à fort pouvoir de coupure coûtent plus cher que les ATO ; intégrer ce supplément au futur devis global. Aucun total complet en euros ne peut être calculé avec les prix inconnus.

Aucune offre Amazon.fr exacte vérifiée pour ces nouvelles références. Les recherches Mouser ne constituent pas une offre en stock. Les fiches distributeur et pages fabricant restent des pistes d’achat traçables.
'''

NOTICES = '''# Documents et sources de la révision

[Notice PDF du projet](verification-alimentation-v3.pdf). Les originaux téléchargés sont inchangés ; les refus 403 et réponses non PDF sont consignés dans [assets.json](../assets.json).

- [Plan original Pololu D42V55Fx](Pololu-D42V55Fx-plan-original.pdf), ressource fabricant 0J2180.
- [Fiche LAPP via Conrad](LAPP-SiF-via-Conrad-original.pdf), famille SiF, variante bleue. Les SKU rouge/noir viennent du catalogue fabricant.
- [Table thermique Blue Sea 2011 via distributeur](Blue-Sea-table-2011-originale-via-distributeur.pdf), page PDF 5, page imprimée 118. Comparaison de conducteurs libres / groupés, pas norme imposée au robot.
- [JLLN 2025](https://www.littelfuse.com/assetdocs/jlln-datasheet?assetguid=3a7bc9bf-d932-4401-bdc7-b39f302195cf), PDF fabricant consulté en ligne ; copie directe refusée 403.
- [KLKD 2025](https://www.littelfuse.com/assetdocs/klkd-fuse-datasheet?assetguid=7b52eebb-c7cc-43df-a8da-9682a338e0f6), consulté en ligne ; copie directe refusée 403. À 135 % du calibre : coupure ≤60 min ; à 200 % : ≤2 min. La cellule de pertes à 80 % du 20 A indique 15,930 W, incohérente : elle n’est pas utilisée.
- [LFT 2025](https://www.littelfuse.com/assetdocs/lft-datasheet?assetguid=56b8955c-9cf7-4814-a923-97a4406bfa77), plage de sections, couples et capot ; [certificat CSA](https://www.littelfuse.com/assetdocs/csa-6225-01-007316?assetguid=203ad805-7e22-463f-997a-2431bbdfbbd1), page PDF 7 pour le LFT30060. Copie directe refusée 403.

Les originaux S65, FAQ Horizon G1/G2, notice ESC et documentation GPIO restent dans leurs dossiers. Un miroir ancien n’est pas présenté comme une nouvelle révision constructeur. Sources, URL et empreintes des archives conservées dans assets.json.
'''

TESTS = '''# Qualification sur le montage reçu

Ces essais n’ont pas été exécutés : le matériel n’est pas présent. Ils constituent les critères de réception.

1. **Documents avant achat des supports.** Confirmer l’admission des brins fins / terminaison du 10 AWG, LAPP 6 mm² et 12 AWG. Confirmer la tenue DC de L60030M1PQ + KLKD au défaut borné et obtenir une enveloppe maximale de coupure pertinente à 8,4 V. Une recommandation de famille ne prouve pas la sélectivité ou la survie des semi-conducteurs.
2. **Réception à froid, pack isolé.** Contrôler G1, prises, polarités, jauges, isolants, sertissages et serrages. Le positif SPMXCA510 doit conserver ≥85 mm de conducteur après préparation, puis l’extension positive LAPP doit conserver ≥120 mm avant F0. Aucun segment négatif n’est crédité dans la borne de défaut. Vérifier l’absence de retour de puissance par B0 d’équilibrage. S65 et véhicule ne sont jamais branchés ensemble.
3. **Alimentation de laboratoire limitée en courant.** Régulateur seul avec charge électronique, puis Pi, caméra et cooler. Balayer VIN de 8,4 à 5,8 V, sortie 0–5 A, démarrage et échelons. Critère de projet : 4,75–5,25 V aux pads Pi, aucun redémarrage, sous-tension ou défaut vidéo. Vérifier EN et PG ; ne pas transposer FB de l’ancien régulateur.
4. **Résistances et pertes.** Mesure Kelvin ou chute V/I instrumentée : boucle commune ≤5 mΩ ; chemin d’entrée Pi ≤50 mΩ. Ce sont des budgets choisis. À 36 A, le budget commun produit 6,48 W ; à 46 A, 10,58 W. Recalculer avec les valeurs réelles et rechercher les pertes localisées aux contacts.
5. **Thermique.** Monter progressivement vers 15 A continus par ESC avec Pi active, jusqu’à stabilisation. Air local ≤40 °C ; fils, prises, cosses et supports ≤85 °C ou limite fabricant plus basse. Pour le pack, appliquer sa notice ; critère de projet conservateur de 45 °C. Contrôler IC5, XT60, supports de fusibles, ED80, MOSFET 2813, régulateur et radiateur SSR. Une lecture IR sur métal brillant seule est insuffisante.
6. **Pointes et incidents.** Étudier 20 A par départ pendant 2 s, puis mesurer les vraies accélérations et les freinages. Ces courants ne sont pas imposés par le Pi. Un profil dépassant l’enveloppe exige une nouvelle étude. Tester les pertes de commande et l’arrêt roues levées ; défauts de surveillance sur cellules simulées. Mesurer les transitoires à l’ouverture ED80 / SSR. Ne pas court-circuiter brutalement la LiPo pour connaître son courant.
7. **Coordination.** Avec fabricant ou banc à source limitée, comparer l’intégrale I²t de coupure complète aux fils et interfaces. Les courbes moyennes et valeurs à 600 V DC ne garantissent pas l’enveloppe à 8,4 V. Aucune sélectivité globale ou survie du D1D100 garantie ; arrêt manuel et remplacement peuvent être nécessaires après panne interne.
8. **Charge.** Contrôler BEEC1067 au multimètre avant le pack, puis G1 / équilibrage 2S. LiPo Balance, 5 A, 4,20 V par cellule. Batterie retirée, surveillance selon les notices. Enregistrer capacité et Wh ; l’EC5 n’utilise pas la donnée Smart.
9. **Roulage.** Mesurer à 20 et 40 km/h, vidéo 1080p60 et Wi-Fi actifs : vitesse, intensité, tension par cellule, Wh, durée et températures. Avec 29,6 Wh supposés utilisables, 45 min à 20 exige ≤39,47 W moyens ; 10–20 min à 40 exige ≤177,6–88,8 W. Ne pas employer 36 ou 44 A comme consommation permanente supposée.

Logiciel de commande et carte de surveillance restent à développer. Un fusible 20 A ne limite pas instantanément à 20 A ; une commande PWM ne mesure pas l’intensité. Schéma, protections des voies fines, ERC/DRC, essais et implantation précèdent la fabrication finale.
'''

INTEGRATION = '''# Raccordements actifs — alimentation R2

Liaisons fonctionnelles avant schéma final. Pack déconnecté pendant préparation. Confirmer les terminaisons des nouveaux supports avant achat.

```mermaid
flowchart LR
 B[Pack G1 2S IC5] --> C[SPMXCA510 10 AWG]
 C --> F0[JLLN50 classe T]
 F0 --> ED[ED80]
 ED --> DP[D+ MiniBus 2315]
 DP --> FP[KLKD10 entrée Pi]
 FP --> HP[Pololu 2813 HP]
 HP --> R[D42V55F5 / 5571]
 R --> P[Pi 5 : deux positifs / quatre retours 18 AWG]
 DP --> SSR[D1D100 + HS251]
 SSR --> UD[UD80, arrivée 6 mm²]
 UD --> F1[KLKD20 ESC1]
 UD --> F2[KLKD20 ESC2]
 F1 --> E1[ESC1 / BEC 6 V servo]
 F2 --> E2[ESC2 / positif BEC isolé]
 F0 --> AUX[Protection auxiliaire, futur schéma]
 AUX --> LOG[Logique indépendante, retour D−]
 B -.->|B0 B1 B2, voies locales isolées| CELL[Comparateurs et optocoupleurs]
 CELL -.-> LOG
 LOG -.-> HP
```

| Liaison | Fil et terminaison active |
| --- | --- |
| IC5 → entrée F0 | Positif du510 avec ≥85 mm de conducteur, raccord TE32151, puis extension LAPP6 mm² avec ≥120 mm de conducteur avant F0. Retirer la zone étamée avant sertissage, sans raccourcir sous ces minimums. ATUM8/2 sur le raccord. Pas de cosse M5. Ces longueurs servent à la borne de défaut ; ne pas raccourcir l’ensemble pour l’implantation. |
| IC5 → D− N2 | CP0− 10 AWG ; une TE 130191, œil Ø5,26 mm, ATUM 8/2. Goujon #10-32 avec son écrou. |
| Sortie F0 → ED80 | LAPP 6 mm² ; préparation LFT à confirmer ; Klauke 95R6 à ED80. La 95R5 de sortie MIDI disparaît. |
| ED80 → D+ | LAPP 6 mm² ; 95R6 M6 côté ED80, 95R5 côté MiniBus. Écrou #10-32 conservé. |
| D+ → SSR +2 ; SSR 1 → UD80 | LAPP 6 mm² et cosses suivant les bornes du D1D100. Entrée UD80 IEC ≥6 mm². Polarité SSR respectée. |
| UD80 → F1/F2 → XT60H-F → ESC |12 AWG dans la pression sous vis duL60030M1PQ, plage10–14 AWG. Prises XT60 desESC conservées. Les languettes rapides20 A du support ne sont pas utilisées. |
| Retours ESC → D− | 12 AWG ; retours de propulsion séparés des signaux. Fils d’usine 16 AWG / 75 mm conservés. |
| D+ → FP → 2813 → VIN du régulateur |12 AWG côté FP10 A et dans son supportL60030M1PQ. AprèsFP, une WAGO221-413 positive relie12 AWG à18 AWG vers les grands pads2813 /régulateur. Le troisième port reste libre. Aucun18 AWG horsplage dans le support. |
| D− → GND du régulateur /Pi |12 AWG avec cosseAncor12 AWG au rail ; seconde WAGO221-413 pour12 AWG depuisD−,18 AWG versGND régulateur et18 AWG vers la221-415 de répartitionPi. Cette borne ne rejoint jamais le positif. |
| VOUT 5 V → Pi | Deux fils 18 AWG de même longueur ≤50 mm vers les pads des broches physiques 2 et 4 du connecteur déjà soudé sur Pi. Isolation individuelle et maintien hors pad. Aucun courant de puissance par les contacts Molex. |
| GND du régulateur → Pi | Quatre fils 18 AWG ≤50 mm vers les pads 6, 9, 14, 20. WAGO existants pour la répartition, un seul potentiel par boîtier. Liaisons communes régulateur → WAGO également courtes. |
| Molex 40 voies | Seulement 1, 11, 12, 13, 15, 32, 33, 34, 39 : neuf contacts, cinq de réserve. Positions 2/4/6/9/14/20 vides côté fiche de signaux. |
| Commande SSR | +3 sur VSW 2813 ; 4 sur D−. VSW batterie ne rejoint pas une GPIO. |
| Logique indépendante | Positif après F0 / avant ED80 à travers sa protection auxiliaire ; retour D−. MCP1703 et tampons selon futur schéma. Pas d’alimentation numérique depuis B2/B0 de la rallonge d’équilibrage. |

DeuxWAGO221-413 sont ajoutées côté entréePi ; les WAGO de sortie5 V/GND déjàprévues restent réutilisées. Aucun nouveaufil14 AWG nécessaire. Les entrées12 AWG et sorties18 AWG restent dans les plagesWAGO publiées. Pourles bornes de puissance, préparer selonle fabricant, sansétain souspression.

**Aucun retour électrique par le châssis ni par les fils d’équilibrage.** La borne de défaut devient invalide avec une alimentation ou un retour alternatif. La liaison de charge est débranchée pendant fonctionnement.

Pose du SiF : fixe, protégée contre abrasion, ventilée, avec fils de puissance espacés. Pas de faisceau serré sous mousse. Rayon fixe ≥30 mm. Sa tenue à 180 °C ne définit pas la température admissible du pack ou des composants voisins. Vérifier l’admission des brins ou embouts aux nouvelles bornes LFT / L60030M. Ne pas étamer sous vis et ne pas retirer de brins pour faire entrer un câble.

Couples publiés :LFT60 avec fils6–14 AWG,2,8 N·m ;L60030M1PQ,2,3 N·m. Ne pas les transposer aux bornesED80,SSR ou rails. LFT«solid/stranded» ne garantit pas à lui seul l’admission des brins trèsfins : confirmation de terminaison maintenue. RaccordTE32151 selonoutillageSOLISTRAND, pas de pinceuniverselle.

La soudure sur les pads du connecteur Pi exige accès dessous, isolation et maintien ; conserver ses broches existantes. Réserver le passage dans le futur châssis. Ce faisceau est à fabriquer : aucun montage n’a été réalisé.

## Surveillance et voies fines

Prévoir au futur schéma une protection près du pack pour B0/B1/B2, et une protection de l’alimentation auxiliaire après F0. Le principal 50 A ne protège pas ces fils. Cellules et optocoupleurs restent locales ; la logique numérique revient à D−. Dimensionner avec courant de repos, erreur de mesure, défauts et tolérances avant routage. Ces protections ne sont pas encore des composants validés.

## Configuration Pi

Après validation des 5 A et du budget USB/FAN, le livre blanc Raspberry Pi documente `PSU_MAX_CURRENT=5000` dans l’EEPROM, qui relève aussi le plafond USB partagé à 1,6 A. `usb_max_current_enable=1` est l’autre réglage du plafond USB. Ces paramètres ne créent ni source PD ni courant. Aucun réglage appliqué ; aucune alimentation USB-C simultanée.
'''

REPORT = '''# Vérification et correction de l’alimentation V3

Révision du **15 octobre 2026**. La liaison de charge du pack G1 est sélectionnée. La protection et l’alimentation Pi sont corrigées dans les dossiers. La qualification complète reste ouverte : confirmations fabricant des supports et de la coupure DC, puis essais matériels. Aucun achat, montage ou essai physique réalisé.

| Point trouvé | Correction de conception |
| --- | --- |
| S65 XT60 et pack IC5 sans cordon de charge | Beez2B BEEC1067 XT60–EC5 annoncé pour S65 ; IC5 accepte EC5 pour la puissance. Une rallonge XH 2S dédiée est ajoutée. |
| 44 A traités comme une consommation presque validée | Ancienne hypothèse de charge, sans mesure ni limite active. Étude continue : 15 A par ESC et budget commun de 36 A ; scénario court : deux fois 20 A pendant 2 s. |
| MIDI60 / 2 kA sans défaut du pack qualifié | Proposition JLLN050.T rapide 50 A / 20 kA DC, support LFT300601C et capot. Borne de défaut conditionnelle avec le positif avant F0. |
| ATO30 sur fils d’usine ESC16 AWG | Deux KLKD020.T rapides de 20 A ; régime continu étudié de 15 A par départ. Coupure plus exigeante, à qualifier au démarrage et aux conditions réelles. |
| Pi avec peu de marge en fin de batterie | KLKD010.T en entrée et Pololu D42V55F5 / 5571 : dropout typique ≈0,25 V à 5 A, tolérance de sortie ±3 %. |
| FLRY-B limité à70 °C | LAPP HEAT180 SiF6 mm², classe5, résistance et rayon documentés. Pose fixe protégée et ventilée. |
| 5 A supposés parfaitement répartis dans la prise Molex | Molex réservé à neuf signaux. Deux positifs et quatre retours courts en 18 AWG soudés aux pads du connecteur Pi. |
| Masse de logique pouvant doubler le retour par l’équilibrage | Logique indépendante après F0, avant ED80, retour D− ; comparateurs de cellule et optocoupleurs locaux. Protections des voies fines au futur schéma. |
| Plage du support Pi incompatible avec18 AWG direct | Supports L60030M1PQ à pression : 12 AWG dans les bornes10–14 AWG ; deux WAGO221-413 supplémentaires pour passer à18 AWG côté Pi. |

Les rails2315, ED80, D1D100 / HS251, UD80, moteurs, servo, caméra, Pi et le pack G1 IC5 restent sélectionnés. Les fils d’usine ESC et batterie ne sont pas dessoudés.

Le positif SPMXCA510 conserve ≥85 mm de conducteur, suivi d’un **raccord TE32151 et d’une extension LAPP6 mm² de ≥120 mm avant F0**, protégée mécaniquement et isolée par ATUM8/2 au raccord. Le négatif garde une TE130191 vers D−. La cosse M5 positive disparaît. Les minimums sont des exigences du calcul, pas une longueur arbitraire à raccourcir lors de l’implantation.

[Notice PDF](notices/verification-alimentation-v3.pdf) · [raccordements](integration.md) · [calculs](calculs.json) · [sélection active](selection-active.json) · [nomenclature](nomenclature.json) · [devis](devis.md) · [qualification](protocole-qualification.md) · [sources](notices/README.md).

## Charge

G1 avec prise d’équilibrage : compatible avec chargeur classique selon Horizon. S65 en LiPo Balance2S /5 A /4,20 V par cellule :42 W maximum contre65 W /6 A disponibles. BEEC1067 identifié à6,90 EUR TTC et en stock sur le SKU exact du JSON public. Contrôle des contacts, de la section et de la polarité sur le lot avant charge. Un pack G2 ne remplace pas ce G1 dans cette architecture.

## Protections, courant et échauffement

La borne calculée est d’environ **16,4 kA**, en supposant8,4 V, cuivre à0 °C, les deux segments positifs minimaux avant F0 et leurs sections maximales admises. Résistance interne de batterie, fil négatif, raccord et résistance du fusible sont tous exclus. Elle n’est valide que si ces segments restent inévitables pour les défauts en aval ; elle ne couvre pas un court-circuit avant F0 ni les voies fines d’équilibrage.

Le JLLN50 et son support disposent de20 kA DC publiés. Les KLKD disposent de50 kA DC dans le cadre UL248-14 ; leur valeur photovoltaïque UL248-19 de10 kA est distincte. Le support de branche est recommandé pour KLKD, mais sa tenue d’association en DC doit être confirmée ; un SCCR générique AC ne suffit pas.

Les énergies KLKD publiées à20 kA /600 V DC sont comparées aux fils comme examen préliminaire. Elles ne sont pas un maximum garanti à8,4 V. Les courbes moyennes ne permettent pas de garantir sélectivité totale ou survie du relais. Aucun fusible ne limite instantanément le courant à son calibre ; le logiciel PWM ne mesure pas l’intensité.

Repère thermique : table Blue Sea, conducteurs libres dans l’air, isolant105 °C, air30 °C :10 AWG60 A,6 mm²65 A,16 AWG25 A. Appliquer un facteur de comparaison prudent0,90 à40 °C donne54 /58,5 /22,5 A. C’est un repère de conception sous ces hypothèses, pas une certification du lot. La pose groupée réduit fortement ces valeurs : elle est exclue pour ces liaisons. Vérifier les isolants d’usine et les températures réelles.

**Confirmations documentaires restantes :** terminaison fine brins admise par LFT ; tenue DC de L60030M1PQ avec KLKD ; enveloppe maximale de coupure aux courants et tensions réels. Aucun de ces points n’est déclaré validé par un simple nouveau choix de référence. Les supports restent des propositions avant achat.

## Alimentation Pi

Le nouveau Pololu dispose d’un plan et d’un STEP officiels archivés. Sa sortie4,85–5,15 V et son dropout typique plus faible améliorent la marge. Critères de réception : boucle commune≤5 mΩ, chemin d’entrée Pi≤50 mΩ, VIN≥5,8 V et4,75–5,25 V aux pads Pi à0–5 A. Ce sont des budgets à mesurer ; les tolérances et courbes typiques seules ne prouvent pas tous les transitoires.

Molex : neuf signaux, positions de puissance vides. Deux WAGO supplémentaires reprennent les fils12 AWG admissibles au support Pi et les fils18 AWG côté cartes. La soudure aux pads Pi exige accès dessous, isolation et maintien, à réserver dans le châssis final. Aucun réglageEEPROM5 A appliqué avant qualification de la source.

## Performances et documents historiques

37 Wh nominaux,29,6 Wh avec80 % utilisables **supposés**. La puissance moyenne totale doit rester≤39,47 W pour45 min à20 km/h,≤88,8 W pour20 min à40 et≤177,6 W pour10 min à40. À44 A constants,5 Ah donneraient seulement6,82 min sans réserve ni pertes. Les courants de conception ne sont pas une consommation moyenne de roulage.

Les objectifs40 km/h /10–20 min et20 km/h /45 min sont conservés. Le courant ne se déduit pas du KV ou de la vitesse seule. Le régime15 A par ESC est une enveloppe thermique, sans limite active mise en œuvre ni résultat de roulage.

Les anciens PDF et STEP restent intacts. Assemblages avec MIDI, deux cossesCP0 ou six fils de puissance dans Molex : versions historiques. Les anciens contrôles303 PASS décrivent leur propre version et ne valident pas cette révision. Le STEP officiel du nouveau Pololu est la référence actuelle pour ce régulateur.

Schéma/routage de surveillance, support caméra, visserie finale et châssis restent pour la phase finale demandée. Les voies fines doivent recevoir leur protection au futur schéma ; aucune carte prête à fabriquer n’est produite ici.
'''
