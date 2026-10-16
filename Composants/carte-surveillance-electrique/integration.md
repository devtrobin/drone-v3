<!-- prototype-m1p -->
> [M1P : conditions de fabrication et de banc](fabrication/README.md). Pour AUX, appliquer au banc le câblage limité du [protocole](verification/banc-essais.md), pas une LiPo. Le câblage ci-dessous reste la cible véhicule non libérée.
<!-- /prototype-m1p -->

# Intégration électrique - surveillance M1

## Source indépendante

Positif **après F0 JLLN050.T, avant ED80** -> FAUX KLKD001.T / 1 A près de la dérivation -> AUX de J1. Retour J1 vers D-. Support FAUX proposé L60030M1PQ + écran SPL001, même famille que les protections R2 ; ses bornes n'acceptent pas directement le fil 22 AWG. Utiliser une courte liaison 12 ou 14 AWG admise au support, puis une WAGO 221-413 pour le départ 22 AWG. Un fil par borne. La qualification DC support/fusible et l'énergie de coupure à 8,4 V restent à obtenir ; aucun résultat antérieur n'est transformé en validation matérielle.

M5 fournit le 5V_MON des deux DC/DC isolés. Le MCP1703A fournit séparément le 3V3_AUX à la logique OFF, directement depuis AUX. Ainsi une panne de M5 ou d'un TMR éteint les optocoupleurs HEALTHY et demande OFF tant que le 3V3_AUX est présent. La perte commune d'AUX, du LDO ou du retour D- **n'est pas garantie de provoquer OFF**. Ce montage n'est pas une chaîne de sécurité certifiée ni un arrêt d'urgence.

## Équilibrage : mesure seulement

Au plus près de la sortie du pack, intercaler **100 ohms / 3 W dans chacun des trois fils B0, B1, B2**. Aucune portion longue de fil fin non protégée en amont ; les petits tronçons restant avant résistances doivent être séparés et enfermés mécaniquement. La fabrication du pack n'est pas modifiée. Cette terminaison est une pièce de faisceau à fabriquer, repérée SURVEILLANCE UNIQUEMENT. Ne pas étouffer thermiquement les corps de résistances sous une gaine groupée : prévoir leur fixation et ventilation hors contact de la LiPo. Leur thermique en défaut est à tester.

J2 : **1 B0_R, 2 B1_R, 3 B2_R**. REF1 = B0_R ; SENSE1 = B1_R. REF2 = B1_R ; SENSE2 = B2_R. Les résistances limitent un défaut situé en aval à moins de 94 mA dans le scénario conservateur 8,4 V / 90 ohms, avec moins de 0,79 W dans une résistance. Elles ne sont pas des fusibles et ne déconnectent pas le défaut. Aucun courant d'alimentation Pi, moteur, servo ou LED opto ne circule dans ces trois fils. La prise de charge 2S reste directe et distincte ; ne jamais utiliser cette dérivation résistive pour la charge ou l'équilibrage S65.

Une perte du point milieu B1 peut répartir artificiellement la tension entre les deux réseaux : **la détection certaine de fil ouvert n'est pas fournie**. Contrôle des trois tensions au branchement et maintien du connecteur requis. Une future détection active de fils ouverts demanderait une autre architecture.

## Interface du Pi et OFF

J6 : 1 = 3V3_PI (pin physique 1), 2 = WARN1 (GPIO17/pin11), 3 = WARN2 (GPIO27/pin13), 4 = DONE (GPIO22/pin15), 5 = GND (D-, point système existant). Le signal GND de surveillance utilise une dérivation du retour de référence existant ; ne pas prendre B0_R comme masse.

WARN1/2 sont **hauts en avertissement**, y compris en perte d'alimentation locale ; bas lorsque la cellule est au-dessus du seuil de retour. Rappels 47 kohms au 3,3 V du Pi seulement. Aucune remontée 5 V ou 3V3_AUX sur un GPIO. La perte d'un câble WARN reste un défaut lisible si le rappel est conservé côté Pi : placer les deux 47 kohms au plus près du connecteur GPIO côté Pi, et non uniquement à l'autre extrémité du câble. La porteuse comporte des emplacements marqués DNP pour les rappels WARN ; voir nomenclature de montage.

HEALTHY1/2 utilisent des optocoupleurs distincts et deux rappels 47 kohms au 3V3_AUX. Une LED HEALTHY éteinte remonte une entrée Schmitt ; sa sortie demande OFF par BAT54. DONE rejoint OFF par sa propre BAT54, avec rappel 100 kohms à GND. J7 : 1 OFF, 2 GND -> OFF/GND Pololu 2813. Aucune connexion à ON/CTRL. Le Pololu 2813 ne porte toujours pas le courant moteur ; VSW commande son régulateur Pi et l'entrée du D1D100 selon l'alimentation R2.

Le faisceau GPIO garde ses 13 contacts. Pas d'I2C, pas de SPI, pas d'ADC numérique : le Pi reçoit des **états de seuils**, pas une tension en volts, une intensité, une température ou un pourcentage de charge.

## Séquence et logiciel restant

1. Contrôle au voltmètre des deux cellules et de la polarité ; brancher la surveillance, puis mise sous tension manuelle.
2. Attendre des états cohérents et le neutre ESC ; ne pas armer au démarrage si WARN est haut ou flottant.
3. WARN haut maintenu selon un filtrage logiciel à définir après essais : arrêt des moteurs, arrêt de la vidéo/enregistrement, demande d'extinction Linux.
4. GPIO22 devient haut à la fin de poweroff et demande OFF. Si le seuil dur est atteint avant, la logique analogique demande OFF sans attendre Linux.
5. Le réarmement reste manuel et doit être inhibé tant qu'une cellule est trop basse ; tester le bouton Pololu pendant un défaut maintenu.

La documentation des overlays Raspberry Pi propose gpio-poweroff ; sa disponibilité et sa séquence Pi 5/OS doivent être vérifiées sur le système choisi. Aucun overlay n'est appliqué et aucun service d'arrêt n'est déployé. Le dossier logiciel décrit le contrat, pas un arrêt système testé.

**Débrancher la batterie principale ET l'équilibrage pour le stockage.** Les DC/DC consomment chacun typiquement 40 mA à vide sous 5 V, même après l'arrêt du Pi. L'étude réserve 0,7 W de puissance pack pour l'ensemble, soit environ 0,525 Wh en 45 minutes ; ce budget n'est pas une mesure. Ajouter environ 0,083 à 0,109 A pour 8,4 à 6,4 V aux scénarios de courant R2 qui ne comprenaient pas encore cette nouvelle réalisation. Le courant à vide maximum des TMR et les pertes réelles doivent être mesurés.

C7/C8 sont des 2,2 microfarads X7R / 25 V, afin de laisser de la marge au minimum de 1 microfarad effectif du MCP1703A ; vérifier tolérance, température et polarisation DC. La tenue I²t des pistes auxiliaires, des vias, des fils et des fusibles FAUX/F1/F2 ainsi que les courts-circuits amont/aval du Pololu restent à analyser avec les confirmations R2. La révision M1P porte les pistes à0,40 mm, le cuivre à70 micromètres nominaux (55 minimum) et les vias à0,80/0,40. La coordination est désormais analysée dans le document dédié : mode banc borné, pas de libération LiPo. Le DRC ne remplace pas cette analyse.
