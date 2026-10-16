# Relevé des cotes TI - source et limite

**Les cotes exactes du contour, de l'épaisseur et de la hauteur assemblée ne sont pas publiées dans le guide accessible.** Les téléchargements publics SLVC413 renvoient HTTP 401. Le [registre](TI-SLVC413/tentatives-publiques.json) conserve les tentatives. Aucune connexion à un compte, commande ou demande au fabricant n'a été faite.

Le guide TI SLVU683A contient des vues vectorielles, utilisables pour contrôler le gabarit : treize entraxes de broches sont étalonnés au pas **2,54 mm**, donné explicitement dans la nomenclature TI p.8. Le contour dessiné donne **environ 51.05 x 48.26 mm**. Ce relevé est une **inférence**, sans tolérance de fabrication ; il ne devient pas une cote exacte parce que le calcul affiche plusieurs décimales. [Calcul reproductible](cotes-ti.json), [extrait constructeur](TI-vue-routage-originale-page5.png).

| Grandeur | Valeur utilisable | Origine / statut |
| --- | --- | --- |
| Pas J1-J11 | 2,54 mm | TI BOM p.8, spécifié |
| J1-J9 | 2 broches communes par connecteur | Schéma TI p.7 ; une broche par liaison suffit |
| J10/J11 | 3 broches au pas 2,54 | PEC03SAAN ; cavaliers 1-2 |
| Contour EVM | Environ 51,05 x 48,26 | Relevé du dessin ; non certifié |
| Épaisseur PCB / hauteur équipée | Inconnues exactement | Ne pas imposer 1,6 / 12 mm comme cotes fournisseur |
| Trous de fixation | Aucun entraxe validé | Les petits points de cuivre ne sont pas déclarés trous de montage |
| Enveloppe de conception | 60 x 60 x 12 par EVM | Réservation à confirmer à réception |

**Conséquence pour la fabrication :** J3/J4 de la porteuse sont des départs de câbles ; aucun trou, socle ni empreinte de porteuse ne dépend du contour TI. La porteuse peut être fabriquée seule pour le banc. Les EVM sont posés sur supports isolants séparés pendant les essais. Le support mécanique définitif attend le ZIP natif ou un relevé de la carte reçue ; ne pas percer les EVM.

Source primaire : [TI, guide SLVU683A](https://www.ti.com/lit/pdf/SLVU683), figures 3/4 et BOM. Pour fermer la cote exacte, archiver SLVC413 obtenu normalement depuis TI, extraire contour/perçages en unités natives et contrôler la révision PWR114 A ; à défaut relever largeur, longueur, épaisseur et hauteur maximale de l'exemplaire reçu, avec incertitude de mesure. La cote des connecteurs et de leurs fiches doit aussi être prise en compte.
