# Campagne M1P - procédure prête, résultats à relever

**Réservée au prototype de banc. LiPo, chargeur, moteurs et alimentation de puissance Pi absents.** Ne pas commencer par des courts-circuits du PCB. Toute valeur mesurée est à inscrire dans [resultats-banc.csv](resultats-banc.csv), initialement vide de résultats.

## Matériel et références

Source AUX de laboratoire 0-8,4 V, CC réglée 250 mA, maximum accepté 300 mA après 10 ms, capacité de sortie documentée au plus 470 microfarads ; résistance série 4,7 ohms / au moins 25 W / 5 % au plus. Deux voies de simulation de cellule **galvaniquement isolées, capables d'absorber un petit courant de retour**, réglables 0-4,2 V / 20 mA. Une source 3,3 V / 5 mA pour les rappels Pi. Multimètres, thermocouples et oscilloscope à sonde différentielle adaptée. Un oscilloscope relié à la terre ne doit pas court-circuiter les références de cellules par ses pinces de masse.

Les références des instruments, résistances et limites réellement utilisées sont consignées avant essais. Une alimentation à sorties communes ne devient pas isolée par changement de câbles. Aucune propriété de limite transitoire n'est présumée parce que la façade affiche « 250 mA ».

## Câblage hors tension

1. Pi et Pololu 2813 débranchés. OFF charge fictive 10 kohms vers D-. WARN1/2 rappelés chacun par 47 kohms à la source 3,3 V limitée. DONE au repos bas par R9 ; entrée non laissée reliée à un générateur éteint inconnu.
2. Source AUX + -> résistance série au départ -> J1.1 ; source AUX - -> J1.2 / D-. Départ FAUX du véhicule non branché au banc. F1/F2 500 mA restent montés. M5 reçoit VIN/GND/VOUT via son faisceau J5 repéré.
3. Simulateur C1 : - = B0 ; + = B1. Simulateur C2 : - = B1 ; + = B2. Relier B0 au D- **en amont** de RA0, pour représenter la masse batterie. B0/B1/B2 -> trois RA 100 ohms au départ -> J2.1/2/3. Ne jamais relier B0_R directement à D-.
4. M1/M2 restent sur supports isolants séparés, dans leur réservation. J3/J4 de porteuse : 1 ISO5, 2 REF, 3 SENSE, 4 OUTA, 5 OUTB. Chaque fil va à la broche TI correspondante, pas à cinq broches adjacentes. Vérifier les six remplacements 0603 et cavaliers.
5. Contrôle de continuité point à point hors tension, puis contrôle visuel à la loupe : pas de pont entre références isolées, pas de boîtier ou entretoise métallique reliant les masses. Les résistances de limitation sont présentes avant tout branchement des simulateurs.

## Paliers et critères

| ID | Action | Critère / relevé |
| --- | --- | --- |
| B00 | Instruments sur charge fictive, sans PCB | 8,4 V maximum, CC <=300 mA après10 ms ; résistance >=4,465 ohms à froid et minimum garanti4,4 avec température ; capacité source <=470 microfarads documentée. Sinon arrêt de la campagne. |
| B01 | Hors tension, EVM adaptés | R1 79,6k / R2 634 / R3 10k ; R6 absent ; J10/J11 1-2 ; pins et boîtiers comparés à la BOM. |
| B02 | Source AUX7,4 V avant résistance, EVM/TMR non montés au départ | Relever J1 réellement obtenu,3V3_AUX (objectif3,20-3,40 V),5V_MON (4,80-5,20 V). OFF doit demander coupure ; pas d'échauffement anormal. |
| B03 | Ajouter un TMR, puis l'autre et ses EVM | Entrée de chaque TMR 4,5-5,2 V après démarrage ; éviter le maintien sous 4 V. Si montée non établie dans 100 ms, couper et diagnostiquer. Courant AUX stabilisé <200 mA ; pas de hausse de limite pour masquer un défaut. |
| B04 | Deux cellules simulées à 4,0 V | WARN1/2 <0,4 V ; OFF <0,4 V en régime établi ; relever ISO5_1/2 et courant AUX. |
| B05 | C1 descente 4,0 ->3,1 puis remontée ; C2 à4,0 | WARN haut >2,8 V vers3,560 ; OFF >1,5 V vers3,347 ; seuil dur descente accepté3,258-3,420 ; warning3,466-3,636. Relever retours/hystérésis, délais et absence d'oscillation. |
| B06 | Même séquence sur C2, C1 à4,0 | Mêmes critères ; vérifier que la voie correcte change et que l'autre demeure cohérente. |
| B07 | Faible déséquilibre, rampes lentes et échelons | Établir bruit et temporisation utile ; comparer niveaux aux seuils calculés. Aucun délai d'arrêt Linux garanti. |
| B08 | Couper M5, puis chaque alimentation TMR séparément | WARN haut et OFF >1,5 V tant que 3V3_AUX reste alimenté ; relever délais. Pi absent. |
| B09 | DONE bas puis3,3 V via source limitée | OFF >1,5 V sur DONE haut, courant conforme à la source ; aucun retour depuis AUX vers3V3_PI. |
| B10 | Débrancher WARN1/2 à l'autre bout du câble | WARN haut côté rappel Pi ; tester DONE/câbles séparément. |
| B11 | Ouvrir B0/B1/B2 un à un, sources limitées | Relever tous les états. B1 ouvert peut rester trompeur ; une absence d'alarme n'est pas une réussite de détection de fil ouvert. |
| B12 | Perdre AUX ou D- | Relever l'état ; OFF n'est pas garanti. Aucune conclusion d'arrêt d'urgence. |
| B13 | Endurance fonctionnelle 30 min à4,0 V simulés | Ambiante <=40 °C ; élévation des pistes/connecteurs <=10 °C ; chaque boîtier >=20 °C sous son maximum recommandé ; pas de dérive de tension ou odeur. Consigner températures. |
| B14 | RA seule, hors PCB et pack, sous8,4 V CC150 mA | Réglage de défaut batterie seule, courant <=94 mA siR>=90 ; puissance<=0,784 W ; température de corps et isolants compatibles avec leur spécification et la pose. Pas de court-circuit de LiPo. |

Aux paliers B02/B03, les optos non alimentés doivent demander OFF : ce niveau au démarrage est attendu. Les objectifs3V3/5V de banc ne remplacent pas une analyse complète des tolérances sur toute température. Les bornes de seuils ci-dessus sont celles du calcul de conception ; hors fenêtre, arrêter et diagnostiquer, ne pas ajuster pour masquer une erreur de câblage.

## Après réussite de cette campagne

Enregistrer courbes et relevés, photographier le montage, revoir chaque écart. Brancher ensuite le Pololu 2813 sur une alimentation de banc à charge fictive légère et mesurer OFF réel, réarmement pendant défaut et démarrage : la charge 10 kohms ne remplace pas ce contrôle. Puis le Pi sans moteurs, avec alimentation principale de banc séparée et son 5 V qualifié ; vérifier gpio-poweroff et le service d'arrêt sur l'OS retenu. Les essais GPIO ne sont pas encore implémentés sur une machine réelle.

**La réussite B00-B14 ne libère pas la LiPo ou le roulage.** La coordination de la chaîne véhicule et les transitoires moteur restent une campagne distincte. Ne pas faire un essai destructif d'énergie de court-circuit dans l'atelier avec une LiPo.
