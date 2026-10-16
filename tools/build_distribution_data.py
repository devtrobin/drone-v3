"""Write traceable component data and indexes; do not rewrite original documents."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/distribution-alimentation'
def save(name,data):
    p=BASE/name;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    sys.stdout.reconfigure(encoding='utf-8')
    prev=json.loads((ROOT/'Composants/protection-surintensite/calculs.json').read_text(encoding='utf-8'))
    main_I=prev['principal_current_A']
    save('calculs.json',dict(checked_on='2026-10-14',status='hypotheses, pas de mesure',
        motor_total_continuous_assumption_A=40,pi_camera_power_assumption_W=25,regulator_efficiency_assumption=.9,
        minimum_battery_calculation_V=6.4,auxiliary_assumption_A=.05,principal_current_assumption_A=main_I,
        bus_continuous_rating_published_A=100,bus_loading_fraction_assumption=main_I/100,
        purchased_assemblies=2,weight_each_published_rounded_kg=.08,total_weight_rounded_kg=.16,
        power_loss_or_drop_guaranteed=False,branch_fuse_ratings_selected=True,branch_fuses_study_A={'Pi':7.5,'ESC1':30,'ESC2':30},branch_protection_qualified=False,wire_ampacity_validated=False,
        autonomy_validated=False,prospective_fault_current_established=False,
        base_envelope_mm=[106.68,22.86],mount_pitch_mm=90.49,
        twin_rail_centres_y_study_mm=[-23,23],twin_base_envelope_study_mm=[106.68,68.86],
        height_with_cover_published_minimum_mm=31.75,maximum_wired_height_established=False))
    save('nomenclature.json',dict(checked_on='2026-10-14',purchased=False,items=[dict(
        manufacturer='Blue Sea Systems',part_number='2315',quantity=2,
        description='MiniBus commun 100A, quatre goujons #10-32, capot2713 inclus',
        roles=['D+ positif apres MIDI principal','D- retours negatifs'],
        asin='B000OTJ8A0',asin_verified_at='Amazon.com via web tool',
        amazon_fr_url='https://www.amazon.fr/dp/B000OTJ8A0',amazon_fr_offer_confirmed=False,
        france_price_eur=None,france_stock_confirmed=False,
        indicative_alternative=dict(supplier='Hodges Marine',currency='USD',unit_price=26.40,
            quantity_price=52.80,shipping_and_france_taxes_included=False),
        included=dict(busbar_with_four_studs=1,serrated_flange_nuts=4,cover_2713=1),
        contents_need_lot_check=True,excluded=['cosses','fils','vis de chassis','fusibles de branches'])],
        additional_cover_purchase_quantity=0,additional_parts_not_yet_selected=['cosses serties','fils','fixations','qualification du repartiteur UD80A569010 apres SSR','qualification des protections de branches']))
    sources=[
        ('constructeur-2315','https://www.bluesea.com/products/2315','100A,48VDC,#10-32,capot,masse0.08kg; couple vis1.69Nm; page lue via web, archivage403'),
        ('constructeur-2305','https://www.bluesea.com/products/2305/Common_100A_Mini_BusBar_-_4_Gang','version sans capot, couple goujon2.03Nm; DXF propose mais inaccessible'),
        ('comparaison-officielle','https://www.bluesea.com/products/compare/2305/2314/2315','ecart des rubriques de couple conserve par le fabricant'),
        ('constructeur-capot','https://www.bluesea.com/products/2713/MiniBus_BusBar_Cover_for_PN_2304_and_2305','compatibilite et inclusion dans2315'),
        ('plan-2315','https://d2pyqm2yd3fw2i.cloudfront.net/files/resources/dimensioned_drawing/2315.jpg','cotes publiees du socle, entraxes et hauteur minimum'),
        ('catalogue-2024','https://primemarine.com.pl/pli/141_Katalog%20BlueSea.pdf','original fabricant via miroir; PDFp100: modeles, capots, goujons; p107: comparaison'),
        ('intensite-bus','https://www.bluesea.com/support/articles/506/How_a_BusBar_Should_be_Rated','principes de calibre fabricant; aucune resistance du2315 publiee'),
        ('pose-bus','https://www.bluesea.com/support/articles/497/Application_Steps_Which_Improve_Busbar_Performance','arrivee centrale et contacts; pas de hausse automatique du calibre'),
        ('ecrou-flasque','https://www.bluesea.com/support/articles/435/The_Benefit_of_Serrated_Flange_Nuts','ecrous a flasque dentee et empilage des cosses'),
        ('amazon-us','https://www.amazon.com/dp/B000OTJ8A0','reference exacte lue via web; offre et prix France non etablis; directchallenge'),
        ('amazon-fr','https://www.amazon.fr/dp/B000OTJ8A0','lien de recherche d achat, offre non confirmee'),
        ('marchand-prix','https://www.hodgesmarine.com/blu2315-blue-sea-2315-minibus-100-ampere-common-busbar-4-x.html','26.40USD affiche en ligne, pas un devis France'),
        ('avis-exact','https://www.walmart.ca/en/ip/Blue-Sea-Busbar-2315-BSS-Common-Mini-Busbar-4-Stud-Terminal-300-Volts-AC-48-DC-100-Amps-With-Insulation-Cover-Reinforced-Polycarbonate-Base-With-Tin-Plate/1MLBPWCKLUU7','avisRobert2020-10-20 qualitatif, aucune mesure'),
        ('forum-voisin','https://www.r3owners.net/threads/tidy-up-your-battery-terminals.44398/page-2','message13: proposition2305/couvert, pas essaiV3; note5024 exclue'),
        ('alternative-SD-MINI','https://www.littelfuse.com/assetdocs/littelfuse-fuse-block-sd-mini-datasheet?assetguid=e77927cb-1cc6-4ae4-a5e4-7a58b17682ff','100Atotal/30Aparcircuit, ne convient pas au depart40Acommun'),
        ('alternative-LX','https://www.littelfuse.com/products/dc-power-distribution-modules/fuse-only-pdms/lx.aspx','boitier mixte de plus grand encombrement'),
        ('alternative-Victron','https://www.victronenergy.com/dc-distribution-systems/busbars','serie150Aavec capot, alternative non retenue')]
    save('sources.json',dict(checked_on='2026-10-14',sources=[dict(id=i,url=u,support=s) for i,u,s in sources],
        youtube_exact_usable_test_found=False,manufacturer_contacted=False,native_step_obtained=False))
    cat=json.loads((BASE/'3D/catalogue.json').read_text(encoding='utf-8'));cat['model_count']=len(cat['models']);save('3D/catalogue.json',cat)
    lines=['# Modèles STEP - distribution électrique','',
        '**Cinq reconstructions extérieures, millimètres, solides nommés et teintes.** Pas de CAO native fournisseur ni de pièce mesurée.','',
        '| Modèle | STEP | Aperçu | Taille |','| --- | --- | --- | ---: |']
    for m in cat['models']:
        folder=ROOT/'Composants'/m['folder']/'3D'
        import os
        rel=Path(os.path.relpath(folder,BASE/'3D')).as_posix()
        label=m['title'].replace(' | ',' : ')
        lines.append(f"| {label} | [STEP]({rel}/{m['file']}) | [PNG]({rel}/{m['preview']['file']}) | {m['bytes']/1e6:.2f} Mo |")
    lines+=['','Les cotes et limites sont dans [cotes.md](../cotes.md) et les JSON voisins. Le capot transparent réel est affiché clair et opaque dans cet export. La vue éclatée est décalée de 19 mm, sans articulation simulée. Les deux rails du projet sont espacés de 46 mm ; les étiquettes de couleur sont ajoutées par la V3.','',
        'Contrôles : réimport STEP, validité, solides, enveloppe, volume, couleurs et absence de chevauchement matériel. [Rapport FreeCAD sans interface](validation-freecad.json). Pas d’essai dans le GUI FreeCAD ou CAD View de VSCode annoncé.','',
        'Les cosses et fils sont absents. La hauteur 31,75 mm est un minimum publié, pas un maximum avec faisceau. [Intégration](../integration.md), [fiche](../README.md).','']
    (BASE/'3D/README.md').write_text('\n'.join(lines),encoding='utf-8')
    for sub in ['bornier-2315','capot-2713']:
        (BASE/sub/'3D/README.md').write_text('# Modèles détaillés\n\nVoir le [catalogue commun et les contrôles](../../3D/README.md), les [cotes](../../cotes.md) et les JSON de provenance voisins.\n',encoding='utf-8')
    print('DATA and indexes written',flush=True)
if __name__=='__main__':main()
