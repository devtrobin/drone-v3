<!-- alimentation-r2 -->
> **Sélection active révisée le 15 octobre 2026.** Appliquer le tableau de raccordements révisé : classe T, branches Midget, fil LAPP 6 mm², 18 AWG Pi et neuf signaux GPIO. Les nomenclatures, PDF et assemblages précédents restent des instantanés.
> [État électrique courant](../verification-alimentation/README.md) · [Raccordements](../verification-alimentation/integration.md). Les références différentes dans les documents ci-dessous sont historiques. Qualification matérielle non réalisée ; confirmations restantes explicites.
<!-- /alimentation-r2 -->

# Faisceau de puissance - Drone V3

**Huit références d’étude**, réparties par composant : trois cosses, un raccord droit, une gaine adhésive, un collier, une embase et une famille de fil principal. Aucun achat effectué ; les offres Amazon.fr, variantes et prix TTC restent à confirmer.

| Composant | Besoin d’étude | Dossier |
| --- | --- | --- |
| Ancor 312303 | 3 | [Documentation](../cosses-puissance/ancor-312303/README.md) |
| Klauke 95R4 | 2 | [Documentation](../cosses-puissance/klauke-95r4/README.md) |
| Klauke 95R5 | 5 | [Documentation](../cosses-puissance/klauke-95r5/README.md) |
| Ancor 309203 | 2 | [Documentation](../raccords-12awg/README.md) |
| TE / Raychem ATUM-8/2-0-STK (NB11802001) | 1 | [Documentation](../gaine-thermoretractable/README.md) |
| HellermannTyton T18R 111-01919 | 12 | [Documentation](../maintien-faisceau/colliers/README.md) |
| HellermannTyton MB2 151-28210 | 8 | [Documentation](../maintien-faisceau/embases/README.md) |
| AUPROTEC FLRY-B 6,00 mm² rouge / noir | 4 m | [Documentation](../cable-principal-6mm2/README.md) |

Le câble principal est retenu en section nominale **6 mm²**. Les manchons Ancor 12–10 AWG ont une plage publiée **3–5 mm²** et servent uniquement aux queues moteurs 12 AWG. Les cosses 95R4/95R5 concernent le 6 mm². Les écrous et vis restent ceux des appareils : M5 MIDI, #10-32 MiniBus et #8-32 relais.

[Notice PDF](notices/notice-faisceau-puissance-v3.pdf), [raccordements et préparation](integration.md), [recherche et avis](recherche-technique.md), [nomenclature](nomenclature.json), [calculs](calculs.json), [quatorze STEP colorés](3D/README.md), [validation du dossier](validation-dossier.json).

La prise commune XT60 de la batterie demeure à qualifier pour le scénario 44,39 A ; le remplacement des fils par du 6 mm² ne prouve pas sa tenue. Les deux XT60H-F des branches moteurs sont distinctes de cette prise. Aucun courant d’étude n’est une limite imposée par le matériel.

Les longueurs, quantités de maintien et accessoires de visserie seront arrêtés après implantation. Aucun des STEP ne sert de calibre de sertissage ni de plan d’usinage validé.
