<!-- alimentation-r2 -->
> **Sélection active révisée le 15 octobre 2026.** UD80 conservé : arrivée 6 mm² LAPP et départs selon le nouveau tableau. Ne pas substituer du 10 AWG nominal à son minimum IEC 6 mm².
> [État électrique courant](../verification-alimentation/README.md) · [Raccordements](../verification-alimentation/integration.md). Les références différentes dans les documents ci-dessous sont historiques. Qualification matérielle non réalisée ; confirmations restantes explicites.
<!-- /alimentation-r2 -->

# Implantation et raccordement V3

```mermaid
flowchart LR
 D[MiniBus positif P3] -->|Cuivre 6 mm2 proposé| S[D1D100 : +2 puis 1]
 S -->|Une seule cosse sur sortie SSR| J[UD80A 569010 : entrée IN]
 J --> O1[Sortie petite S1 : fil 12 AWG du 5065]
 J --> O2[Sortie petite S4 : fil 12 AWG du 5065]
 O1 --> F1[ATO30 puis ESC arrière 1]
 O2 --> F2[ATO30 puis ESC arrière 2]
```

Le bloc distribue **le positif commuté après le relais**, pas le positif permanent du MiniBus et pas le négatif. Ses sept connexions sont électriquement communes. Repères IN/S1–S4/L1–L2 définis pour le projet, **pas des inscriptions constructeur**. Aucun empilage de deux cosses sur la borne 1 du D1D100 nécessaire dans cette proposition.

| Repère V3 | Interface | Affectation |
| --- | --- | --- |
| IN | Grande entrée 6–16 mm² | Arrivée depuis borne 1 du D1D100, cuivre 6 mm² proposé |
| S1 | Première petite sortie 2,5–6 mm² | Fil d'arrivée 12 AWG du porte-fusible ESC1 |
| S4 | Quatrième petite sortie 2,5–6 mm² | Fil d'arrivée 12 AWG du porte-fusible ESC2 |
| S2, S3 | Deux petites sorties restantes | Réserves sans conducteur |
| L1, L2 | Grandes sorties 2,5–16 mm² | Réserves sans conducteur |

Le 12 AWG est environ 3,31 mm² nominal, dans la plage métrique des petites sorties. Les fils 16 AWG des ESC font environ 1,31 mm² : **ils ne vont pas directement dans ces sorties de minimum 2,5 mm²**. Les porte-fusibles et prolongements restent intercalés selon le dossier moteurs. Un fil par orifice utilisé ; pas de doublage improvisé dans un embout ou une borne.

Ne pas substituer un embout 4 mm² au 12 AWG sans vérifier son adaptation au conducteur et à la borne. Choisir un embout et un sertissage pour la section réelle et la classe des brins. La fiche d'entrée cite le multibrins compact ; l'acceptation de notre fil souple exact et de son embout doit être vérifiée avec la notice du lot. La possibilité générale « avec ou sans embout » ne dispense pas de cette vérification.

## Montage et serrage

Valeurs de la [notice officielle IP7802_M](https://nvent.widen.net/content/vhxyvvgeqg/original/ip7802.pdf), tableau **IEC page 1**, retenues pour préparer l'étude européenne :

| Groupe | Sections IEC | Couple de borne | Dénudage publié |
| --- | --- | ---: | ---: |
| Entrée IN | 6–16 mm² | 3,5 N·m | 17,0 mm |
| Grandes sorties L1/L2 | 2,5–16 mm² | 3,5 N·m | 17,0 mm |
| Petites sorties S1–S4 | 2,5–6 mm² | **1,2 N·m** | **10,2 mm** |

La page **UL/CSA 2** indique 19,5 in-lb (environ **2,20 N·m**) et 0,36 pouce (**9,14 mm**) pour entrée/grandes sorties ; 10,6 in-lb (**1,20 N·m**) et 0,40 pouce (**10,16 mm**) pour les petites. Ce ne sont pas des conversions équivalentes du tableau IEC pour les grosses bornes. Garder les régimes séparés, vérifier le marquage/la notice reçue et résoudre l'écart avant câblage de l'entrée ; ne pas mélanger couple IEC et longueur UL.

La notice demande de **serrer aussi les vis des orifices inutilisés** au couple de leur groupe. Elle demande de maintenir le câble d'entrée à environ **15 cm du bloc**. Prévoir une retenue mécanique compatible avec notre implantation ; ni traction du faisceau ni charge sur la petite vis de borne. Aucune graisse ou traitement supplémentaire ajouté sans prescription applicable.

Fixation directe au panneau proposée pour éviter un rail DIN supplémentaire. La notice donne un repère de fixation **54 mm** et une cote **4,5 mm**, avec annotation **M5** ; la géométrie exacte et le passage de la vis doivent être contrôlés sur la pièce. Ne pas transformer automatiquement la cote 4,5 en un perçage de dégagement M5 garanti. Visserie, isolant de support et méthode de retenue restent à sélectionner. Ouverture du capot et accès à l'outil doivent rester possibles.

Batterie et prise d'équilibrage débranchées : dénuder selon le groupe et le régime applicable, ne pas blesser les brins, insérer entièrement et contrôler l'absence de cuivre exposé. Serrer avec un outil adapté et contrôlé ; refermer le capot. L'IP20 ne permet pas une exposition à l'eau ni au copeau conducteur.

## Courant, température et défauts

Scénario : **40 A total**, deux départs supposés 20 A. Capacité nominale IEC 80 A, soit charge nominale 50 %. Déclassement publié pour viser 85 °C de fonctionnement : 80 A jusqu'à 40 °C ambiants, **60 A à 60 °C**, **53,6 A à 65 °C**, **46,4 A à 70 °C**, **37,6 A à 75 °C**. Ces valeurs multiplient le coefficient fabricant par 80 A dans ses conditions ; elles ne prouvent pas 80 A avec notre câble 6 mm² ou n'importe quel montage.

Le scénario 40 A ne rentre plus à 75 °C selon cette seule courbe. Viser l'air local de l'étude V3, 40 °C, puis mesurer températures, courants et chutes des trois connexions utilisées. Résistance de contact et pertes exactes du bloc non publiées dans les documents consultés ; ne pas inventer un rendement ou une autonomie.

Le tronc et les fils d'arrivée avant les ATO30 restent **coordonnés avec le principal MIDI 60 A**, pas protégés par les ATO situés plus loin. Rapprocher les deux porte-fusibles de la dérivation et garder leurs arrivées très courtes, isolées et retenues. La section 12 AWG de ces arrivées ne devient pas automatiquement protégée par le principal : revoir sa tenue au défaut et le chemin réel.

Le fabricant publie **Icw 3 kA / 1 s**, **Ipk 22 kA** et **SCCR jusqu'à 100 kA** ; ces grandeurs sont distinctes. Le bloc est passif et ne coupe pas ce courant. La notice UL relie le SCCR 100 kA à une protection par fusible **200 A Class J ou T**, 600 V maximum ; cette association **n'est pas notre MIDI 60 A**. Ne pas transférer cette qualification au faisceau V3, aux ATO à 1 000 A ou au SSR. Aucune tenue globale LiPo ou sélectivité démontrée ici.

## Qualification à effectuer

Vérifier référence/lot, régime de serrage, dénudage, brins et embouts ; continuité des sept connexions, polarités et isolement hors tension. Première alimentation limitée après contrôle du schéma. Mesurer la somme des courants, les chutes aux trois bornes utilisées, l'échauffement et la tenue sous vibration sur l'usage prévu. Contrôler freinage/régénération et la perte d'un seul départ avec le système d'arrêt supervisé à concevoir. Aucun essai de court-circuit volontaire du pack.

[Relais et surveillance](../protection-batterie/integration.md), [deux protections ESC](../protection-branches-moteurs/integration.md), [distribution principale](../distribution-alimentation/integration.md), [fusible principal](../protection-surintensite/integration.md).

Après chaque ATO30, une [prise AMASS XT60H-F avec capot](../connecteurs-alimentation/integration.md) est proposée pour rejoindre le XT60 mâle existant de son ESC. Le retour négatif de cette prise rejoint séparément D- ; aucun négatif dans le UD80A. Queues 12 AWG proposées, pas de cuivre 6 mm² imposé dans les godets ; raccords et longueurs à sélectionner.

<!-- faisceau-puissance-v3 -->

Complément du14octobre2026 : [cosses, raccords, gaine, maintien et câble principal](../faisceau-puissance/README.md), avec [raccordements et notice de préparation](../faisceau-puissance/integration.md). Sélection d’étude, sans achat ni qualification matérielle.
