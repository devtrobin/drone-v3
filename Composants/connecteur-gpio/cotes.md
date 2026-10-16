# Cotes du connecteur GPIO

| Élément | Valeur | Statut |
| --- | --- | --- |
| Boîtier | 40 positions, 2 rangées de 20 | Référence 22-55-2401 |
| Pas de colonnes et rangées | 2,54 mm | Plan et CAO fabricant |
| A, entraxe extrêmes | 48,26 mm | Tableau pour 40 circuits |
| B, longueur | 50,77 mm de référence | Plan SD-70450-0001-0026, ancienne révision archivée |
| Largeur / hauteur | 5,05 / 15,24 mm de référence | Plan ; pas des tolérances du lot reçu |
| Enveloppe du solide natif | 50,7746 × 5,0546 × 15,24 mm | Mesure de la CAO, pas du matériel |
| Broche mâle admise | 0,64 mm carrée ou ronde | Plan du boîtier |
| Contact | 22 ou 24 AWG ; isolant Ø1,63 mm max | Fiche 16-02-0103 et page fabricant actuelle |
| Fil retenu | 22 AWG multibrin ; isolant Ø1,5 mm annoncé | Adafruit 3175 ; tolérance non publiée |
| Réserve nominale d’isolant | 0,13 mm | Différence arithmétique, pas une marge garantie |
| Dénudage | 2,54 à 3,17 mm | Notice ATS-638118700 révision E |
| Isolant pour le profil 22–24 AWG | 1,30 à 1,65 mm ; contact choisi limité à 1,63 | Révision E consultée sur Molex |
| Sertissage conducteur 22 AWG | Hauteur 0,75–0,85 ; largeur réf. 1,43 mm | Valeurs de procédure, avec l’outillage prescrit |
| Sertissage isolant | Hauteur réf. 1,70 ; largeur réf. 1,76 mm | Référence de procédure, pas dimensions détaillées du STEP reconstruit |

La CAO native décrit le boîtier et quelques annotations sans volume. Les variantes colorées conservent le solide exact, mais omettent les annotations non solides ; l’original reste archivé. Les tôleries et ressorts du contact ne proviennent pas d’une CAO native. Le modèle suit la photo d’un contact serti ; dimensions locales, détails du ressort et crimp sont estimés. Le dessin générique de la notice d’outillage n’est pas un plan de fabrication du contact.

Une petite réservation estimée de 0,014 mm³ est ajoutée au col du contact reconstruit pour dégager une nervure du boîtier natif. Le boîtier fournisseur n’est pas retouché. Ce détail de reconstruction permet un assemblage CAO sans chevauchement, mais ne certifie pas la forme du contact réel.

Les fils de pose ont une gaine de 1,5 mm et une âme équivalente de 0,326 mm². Le nombre de brins n’est pas publié, donc aucune subdivision arbitraire n’est présentée comme réelle. Les extrémités ouvertes sont volontaires. Les courbes ne constituent pas la liste de coupe finale.

La pose sur le Pi utilise le repère de sa CAO : centre du header (32,5 ; 52,5), emprise 50,8 × 5,08, face haute plastique Z=3,876. Le boîtier posé à cette cote donne un sommet Z=19,116. La profondeur réelle d’insertion reste à mesurer.

La pose indicative du refroidisseur reprend son premier clip à (3,5 ; 9,5). Le jeu en plan au boîtier GPIO serait environ **0,72 mm** dans ce repère. La lecture du plan Pi donne 37,5 mm entre les clips en Y, tandis que la reconstruction existante utilise 37 mm : cet écart de 0,5 mm et les cotes approximatives empêchent de déclarer l’ajustement acquis. Contrôler le lot et les deux orientations avant fabrication du support. Aucun STEP du Pi ou du refroidisseur modifié.

[Archives originales](notices/README.md), [provenance](3D/provenance.json), [calculs](calculs.json).
