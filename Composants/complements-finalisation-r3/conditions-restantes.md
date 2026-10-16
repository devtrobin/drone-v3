# État après compléments R3

## D01 - Ouvert - fournisseur

Angle Losi, régime et endurance du couple Losi/KHK non publiés pour notre service. La table KHK est une référence à 600 tr/min, pas une qualification à 25 578 tr/min.

## D02 - Identification définie ; essais requis

Association retenue pour étude : Pololu 3429 FT5335M + palonnier 3431, trou à rayon 20 à reprendreØ3.2. Ne pas substituer la version 25T. Courants transitoires et alimentation 6 V restent à qualifier.

## D03 - Partiellement documenté

LFT30060 : tenue 20kA DC explicitement listée au certificat CSA. Restent les brins fins/terminaisons, le couple L60030M+KLKD enDC et les enveloppes maximales de coupure à 8.4 V.

## D04 - Mesure à réception

Relever fond hexagonal et face d’écrou des roues. Ajuster entretoises et extrémités d’axes avant le tournage final.

## D05 - Plans partiels ; mesure à réception

Plan LFT30060 trouvé. TI publie SLVC413 mais le téléchargement répond 401 ici ; aucune cote exacte TI n’en est déduite. Contrôler aussi UBEC, supports de fusibles, interfaces et accès.

## D06 - Partie fixe conçue ; terminaisons à présenter

Quatre parcours 3D et huit brides sur armature démontable définis. Les points extrêmes sont des approches. Les descentes terminales et le débit final se font aprèsD03/D05 ; elles ne sont pas déclarées entièrement raccordées.

## D07 - Câblage de banc défini ; essais requis

Netlist de trois canaux avec brochage exact ISO7710FDR et MCP1703 A-3302E/DB. Montage sur adaptateurs séparés ; aucun nouveauPCB/Gerber. Réactions électriques non mesurées.

## D08 - Association de puissance non validée

Le scénario 6.4 V/30 A moteurs/1 A servo donne 5.975 V à l’entréeUBEC. Un abaisseur ne peut alors tenir 6 V. Le coupleFT5335M+UBEC doit être revu ; l’alternativeHitec documentée n’est pas intégrée ni déclarée interchangeable.

## P01-P04 - Pratique

Pesée et charge avant, montage à blanc, échauffement/endurance, banc électrique limité, puis vitesse/autonomie/vidéo. Les objectifs ne deviennent pas des mesures par simulation.
