"""Write sourced calculations, bill of materials and local CAD indexes."""
from pathlib import Path
import json,sys,math,hashlib,os
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/protection-branche-pi'
def save(name,d):
    p=BASE/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    sys.stdout.reconfigure(encoding='utf-8');current=25/(6.4*.9)+.015
    cases=[dict(input_voltage_V=v,efficiency_assumption=e,branch_current_A=25/(v*e)+.015) for v in [8.4,7.4,6.4,6.2] for e in [.9,.8]]
    tc=[dict(percent=p,current_A=7.5*p/100,min_s=mn,max_s=mx) for p,mn,mx in [(110,360000,None),(135,.75,600),(160,.25,50),(200,.15,5),(350,.08,.5),(600,None,.1)]]
    save('calculs.json',dict(checked_on='2026-10-14',status='etude non qualifiee, aucune mesure',
        output_power_assumption_W=25,pack_calculation_V=6.4,efficiency_assumption=.9,SSR_control_current_assumption_A=.015,
        branch_current_first_approximation_A=current,voltage_loss_not_in_first_sum=True,cases=cases,
        fuse_selected_study_A=7.5,cold_resistance_typical_ohm=.01091,
        fuse_drop_cold_first_approximation_V=current*.01091,fuse_loss_cold_first_approximation_W=current**2*.01091,
        melting_I2t_typical_A2s=60,interrupt_rating_A=1000,interrupt_rating_voltage_V=32,
        prospective_fault_current_validated=False,simplified_loop_resistance_reference_ohm=8.4/1000,
        loop_reference_excludes_branch_fuse_resistance=True,time_current=tc,
        derating_source='Littelfuse ATO aftermarket 11/15/2022 p3',
        typical_current_recommendation=[dict(nominal_A=f,at_20_C=a,at_65_C=b,at_85_C=c) for f,a,b,c in [(5,5,4,4),(7.5,7,6,5),(10,10,8,7)]],
        downstream_wire_proposed_mm2=1.5,wire_ampacity_validated=False,holder_wire_gauge_published='12AWG',
        holder_nominal_wire_area_conversion_mm2=3.31,series_combination_with_main_fuse_qualified=False,
        fast_semiconductor_protection_guaranteed=False,startup_measured=False,thermal_tested=False))
    save('nomenclature.json',dict(checked_on='2026-10-14',purchased=False,items=[
        dict(part_number='5065',manufacturer='Blue Sea Systems',quantity_installed=1,
             included=['support un circuit','capot et joint','deux fils12AWG'],excluded=['fusible','cosses','vis'],
             asin='B004ZIUA62',asin_verified_at='Amazon.com title/description via web',
             amazon_fr_url='https://www.amazon.fr/dp/B004ZIUA62',amazon_fr_offer_confirmed=False,price_eur=None,
             indicative_foreign_price=dict(supplier='Hodges Marine',unit_price=15.01,currency='USD',france_delivery_and_taxes_included=False)),
        dict(part_number='0ATO07.5V',manufacturer='Littelfuse',quantity_installed=1,nominal_A=7.5,
             retail_pack_alternative=dict(part_number='0ATO07.5VP',catalogue_name='ATO7.5BP',pack_count=5,
                installed_from_pack=1,spares_from_pack=4,conditioned_pack_to_verify_before_purchase=True),
             asin=None,amazon_fr_search='https://www.amazon.fr/s?k=Littelfuse+ATO7.5BP',amazon_fr_offer_confirmed=False,
             price_eur=None,indicative_foreign_price=dict(supplier='DigiKey',unit_price=1.35,currency='USD',france_delivery_and_taxes_included=False))],
        remaining_parts=['cosses et raccords de sections adaptees','fils de prolongement','fixation du support']))
    sources=[
        ('support-fabricant','https://www.bluesea.com/products/5065','12AWG,30Amax,ATO/ATC,fusiblesepare; aucunplan ni IPnumerique publie sur la fiche'),
        ('catalogue-2024','https://primemarine.com.pl/pli/141_Katalog%20BlueSea.pdf','copie dejaarchivee dans distribution-alimentation; pages60/72 pour5065'),
        ('fuse-exact-fiche','https://www.mouser.com/datasheet/2/240/media-3323444.pdf','ficheATOaftermarket2022 exacte: cotes, courbes, declassement et1000A; miroirRSP archive'),
        ('fuse-copie-RSP','https://rspsupply.com/images/downloads/Littelfuse/0/Littelfuse%200ATO020.VP/Specification%20Document.pdf','fiche2022 avec banniereRSP et pageMouser, conservee tellequefournie'),
        ('pololu-2813','https://www.pololu.com/product/2813','MOSFET55C a6A dansessai12Vamb22Caircalme; pas delimitation courant'),
        ('pololu-2866','https://www.pololu.com/product/2866','regulateur5V, courbes dependenttension/chargetemperature'),
        ('amazon-support','https://www.amazon.com/dp/B004ZIUA62','reference5065 identifiee; aucuneoffreFrance confirmee'),
        ('amazon-fr-support','https://www.amazon.fr/dp/B004ZIUA62','verificationautomatique, prix/stocknonconfirmes'),
        ('amazon-fuse','https://www.amazon.fr/s?k=Littelfuse+ATO7.5BP','rechercheparreference, pasde ASINexactconfirme'),
        ('mesures-support','https://shop.pkys.com/Blue-Sea-5065--Waterproof-In-Line-Fuse-Holder-for-ATOATC-Fuses_p_2716.html','mesuresapproximatives PeterKennedy2017: trou3/16, centrebord5/32; pasplanfabricant'),
        ('dimensions-secondaires','https://skysat.fr/en-gb/products/blue-sea-waterproof-inline-ato-atc-fuse-holder','38x25x15 marchand ambigu; IP66marchand nonconfirme, nonrepriscommefabricant'),
        ('prix-support','https://www.hodgesmarine.com/blu5065-blue-sea-5065-waterproof-inline-fuse-holder-atoa.html','15.01USDaffiche, pasdevisFrance'),
        ('prix-fuse','https://www.digikey.com/en/products/detail/littelfuse-inc/0ATO07-5V/2519125','referenceexacte 1.35USD/unite, dimensionsmarchandesne remplacentpas plan18.8total'),
        ('pack-et-avis','https://www.canadiantire.ca/en/pdp/littelfuse-ato-blade-fuse-5-pk-0201571p.0201576.html','ATO7.5BPpack5; avis151 agregesplusieurscalibres, pasessai7.5exact'),
        ('forum-exact','https://forums.sailboatowners.com/threads/what-are-you-using-as-a-bilge-pump-fuse-holder.162517/','MaineSail2014-05-23message2 utilise5065; pasessaiV3'),
        ('avis-exacts','https://www.ebay.com.au/urw/Blue%2BSea%2BSystems%2BWaterproof%2BIn-line%2BFuse%2BHolder%2B5065/product-reviews/721379242?_itm=391693814716','5avisqualitatifs5065 consultes; aucunprotocoleIPoumesuredecourant'),
        ('alternative-MINI','https://xonstorage.z8.web.core.windows.net/pdf/littelfuse_0fhm0002lxn_apr22_xonlink.pdf','LittelfuseFHM14AWG20A: alternativepluspetitfusible, pasoffreAmazonexacteverifiee')]
    save('sources.json',dict(checked_on='2026-10-14',sources=[dict(id=i,url=u,support=s) for i,u,s in sources],
        exact_youtube_test_found=False,manufacturer_contacted=False,all_hardware_measured=False,native_step_obtained=False))
    assets=json.loads((BASE/'assets.json').read_text(encoding='utf-8'))
    for a in assets['assets']:
        if a.get('bytes')==0:a['status']='empty_response'
        if 'via-RSP' in a['file']:a['supplier_annotations_present']=True
    src=ROOT/'Composants/distribution-alimentation/notices/BlueSea-catalogue-2024-miroir-PrimeMarine.pdf'
    rec=dict(file='../distribution-alimentation/notices/'+src.name,status='local_reference',modified=False,
        url='https://primemarine.com.pl/pli/141_Katalog%20BlueSea.pdf',bytes=src.stat().st_size,
        sha256=hashlib.sha256(src.read_bytes()).hexdigest(),checked_on='2026-10-14',relevant_pdf_pages=[60,72])
    assets['assets']=[a for a in assets['assets'] if a['file']!=rec['file']]+[rec];save('assets.json',assets)
    cat=json.loads((BASE/'3D/catalogue.json').read_text(encoding='utf-8'));assert cat['model_count']==6
    lines=['# Modèles 3D - protection du départ Pi','','**Six STEP en millimètres, solides nommés et teintes.** Reconstructions documentées, matériel non mesuré.','',
           '| Modèle | STEP | Aperçu | Taille |','| --- | --- | --- | ---: |']
    for m in cat['models']:
        folder=ROOT/'Composants'/m['folder']/'3D';rel=Path(os.path.relpath(folder,BASE/'3D')).as_posix();label=m['title'].replace(' | ',' : ')
        lines.append(f"| {label} | [STEP]({rel}/{m['file']}) | [PNG]({rel}/{m['preview']['file']}) | {m['bytes']/1e6:.2f} Mo |")
    lines+=['','Le fusible reprend ses cotes de référence. Le support, ses contacts, le joint et les fils sont estimés d’après la photo ; aucune CAO fournisseur obtenue. Le corps du fusible est affiché opaque, intérieur calibré absent.','',
        'Les deux fils rouges sont continus et sortent du même côté. Leur longueur extérieure de 100 mm, leur dénudage et leurs 19 brins sont illustratifs ; les bouts nus sont les terminaisons du modèle. La pose réelle du faisceau reste à définir.','',
        'Le capot de la vue éclatée est décalé de Y+36. Le modèle du socle sans capot ni fusible permet d’examiner les contacts. [Cotes et repères](../cotes.md), [intégration](../integration.md).','',
        'Réimport STEP : validité, nombre de solides, couleurs, volumes et enveloppes. Vérification de non-chevauchement des pièces représentées. [Contrôles FreeCAD sans interface](validation-freecad.json) ; aucun test GUI ou CAD View revendiqué. JSON de provenance voisins des STEP.','']
    (BASE/'3D/README.md').write_text('\n'.join(lines),encoding='utf-8')
    for sub in ['porte-fusible','fusible-7-5a']:
        (BASE/sub/'3D/README.md').write_text('# Modèles détaillés\n\n[Catalogue commun et contrôles](../../3D/README.md), [cotes et limites](../../cotes.md). Les JSON voisins donnent la provenance des fichiers.\n',encoding='utf-8')
    print('DATA and indexes written',flush=True)
if __name__=='__main__':main()
