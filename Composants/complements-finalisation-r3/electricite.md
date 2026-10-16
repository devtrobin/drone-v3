# Revue électrique R3

## Protections et données nouvelles

La fiche officielle JLLN donne pour 50A160VDC et 20kA de pouvoir de coupure. Le certificat CSA Littelfuse mentionne explicitement les LFT30060 à 60 A avec tenue 20kADC ; ce point est documenté et n’est plus déduit d’un SCCR alternatif. Cela ne démontre ni la coordination de tout le véhicule ni l’énergie maximale de coupure à 8.4 V.

Les bornes «solid/stranded» n’acceptent pas automatiquement tous les câbles silicone à brins très fins. Ne pas ajouter arbitrairement un embout serti et le considérer homologué. Restent à confirmer : terminaison pour nos conducteurs, association L60030M+KLKD enDC et maximum d’énergie de coupure pour les défauts pertinents. Le principalJLLN050 et FS5 A ne sont pas augmentés en calibre pour masquer une pointe non qualifiée.

Le plan officiel OL-LFT30060 est identifié dans la ficheLFT, page 3. Les autres implantations non cotées restent des réservations sur cassettes démontables. Les fichiers TI SLVC413 sont publiés sur la page de l’EVM ; le téléchargement a répondu 401 dans cet environnement. Aucune dimension TI exacte ni nouveau trou n’a été inventé à partir d’une image sans échelle.

## Servo défini pour l’étude

Retenir ensemble Pololu 3429 (FT5335M) et 3431 (palonnier compatible). Le dessin du palonnier donne des trous au pas 5 mm, dont un àR20 ; reprendre ce trou deØ2.5 àØ3.2 pour la liaisonM3, sans toucher aux cannelures. Les données de cette variante ne sont pas fusionnées avec celles du FT5335M25T d’une autre page.

Pololu indique des pointes **supérieures à 9 A à 7.4 V**. Ce n’est ni une valeur maximale garantie, ni une mesure à 6 V. La fiche historique 4/6 A ne suffit donc plus à borner toutes les pointes. La brancheUBEC30603003 et le fusibleFS5 A restent à qualifier à 6 V. Le scénario 12 A de sortie utilisé dans les calculs est une épreuve choisie, pas une nouvelle spécification fabricant. Vérifier aussi le cordon et le connecteur d’usine du servo sous ce service. Le couple 35 kg.cm à 6 V publié est un couple de blocage, pas un couple permanent.

Le servo reste alimenté aprèsSSR, comme enR2, afin qu’une coupure analogique dure supprime aussi cette charge. Aucun BEC d’ESC n’est mis en parallèle avec l’UBEC ni avec le 5 V Pi.

## Résistance et tension

Les longueurs3D R3 remplacent les quatre anciens corridors hauts. [Calculs](calculs-electriques-r3.json) et [table de scénarios](scenarios-tension.csv) distinguent le chemin communIC5/F0/ED80/D+ et les deux cordons supplémentaires versSSR/UD80. Le courantPi ne traverse pasP05/P06. La résistivité est corrigée à80°C pour l’étude ; les résistances de contact et rendements sont des hypothèses d’acceptation, pas des mesures.

Le budget commun historique 5mΩ n’est plus traité comme prouvé. Mesurer la résistance de boucle à quatre fils et les chutes sous charge, puis vérifierPiVIN≥5.8 V selon le protocole du régulateur. Les pointes les plus défavorables en fin de pack ne sont pas garanties ; ne pas annoncer une tenue 6 V du servo sur la seule mention «2S» de l’UBEC. Les queues de raccordement sont à inclure dans la mesure finale.

## Prototype PWM à trois canaux

[Netlist complète](interface-pwm-netlist-r3.csv) et [nomenclature](interface-pwm-bom-r3.json). Trois ISO7710FDR SOIC8-D indépendants : 1et3=3V3_PI ;2=entrée via220ohms ;4=GND_PI ;5=GND local ;6=sortie via220ohms ;7=NC ;8=3V3 local. Rappel10kohms sur l’entrée après la résistance et sur le signal de sortie.100nF sur chaque alimentation de chaqueISO.

Trois **MCP1703 A-3302E/DB SOT223** : **1=VIN ;2etTAB=GND ;3=VOUT** selon la table 3-1 Microchip. Ce n’est pas le brochage d’un AMS1117. Chaque régulateur reçoit le BEC/UBEC de son actionneur et fournit 3.3 V au côté sortie correspondant. Deux 10µF25 V par LDO, polarité à respecter. Les adaptateurs doivent avoir des pastilles séparées ; tester leur continuité hors tension.

Le bornierJ_PI ne transporte que 3.3 V,GND et troisPWM. Les borniersJ_G/J_D/J_S sont explicitement ordonnés VINlocal/GNDlocal/signal ; cela ne présume pas l’orientation d’une priseFutaba. **La puissance du servo et des ESC contourne les adaptateurs**. Le circuit ne certifie pas une isolation globale : les retours d’alimentation rejoignentD− ailleurs ; la barrière évite de créer un retour parallèle par les petits fils de commande.

Le suffixeF donne un état par défaut bas ; un PWM valide resté figé doit encore être détecté par la stratégie de surveillance. Aucun nouveauPCB/Gerber n’est livré ; le prototype à fils sur adaptateurs doit être testé avant une éventuelle carte dédiée.

Sources : [Pololu3429](https://www.pololu.com/product/3429), [palonnier3431](https://www.pololu.com/product/3431), [LFT](https://www.littelfuse.com/assetdocs/lft-datasheet?assetguid=56b8955c-9cf7-4814-a923-97a4406bfa77), [certificatCSA](https://www.littelfuse.com/assetdocs/csa-6225-01-007316?assetguid=203ad805-7e22-463f-997a-2431bbdfbbd1), [ISO7710](https://www.ti.com/lit/ds/symlink/iso7710.pdf), [MCP1703A local](../carte-surveillance-electrique/notices/Microchip-MCP1703A-datasheet.pdf).
