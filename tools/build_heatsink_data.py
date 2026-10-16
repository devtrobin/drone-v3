"""Store the researched choice and clearly labelled calculation assumptions."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/dissipateur-relais'
def write(name,data):(BASE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    write('sources.json',dict(checked_on='2026-10-13',selection='Sensata/Crydom HS251 + 1 HSP-1',
        purchased=False,physical_tested=False,amazon=dict(asin=None,exact_offer_confirmed=False,price_eur_ttc=None,
            search_url='https://www.amazon.fr/s?k=Crydom+HS251',status='Amazon.fr inaccessible; aucune offre exacte verifiee'),
        requirements=dict(thermal_study_current_total_A=40,thermal_study_ambient_max_C=40,qualified=False),
        dimensions=dict(vendor_cad_full_envelope_mm=[85.344,52.324,40.640],catalogue_body_mm=[58.7,50.3,38.4],
            vendor_plan_tolerance_mm=.5,ssr_hole_centres_cad_mm=47.625,ssr_threads='#8-32 UNC'),
        thermal=dict(heatsink_C_per_W=2.5,weight_g=100,material='aluminium naturel',fan_included=False),
        pad_variants=[dict(variant='gris-2018',thickness_mm=.076,outline_mm=[57.1,44.2],source='Fiche Sensata HSP 2018'),
            dict(variant='rose-PCN-2023',thickness_mm=.127,outline_mm=[57.1,44.2],outline_confirmed=False,
                source='PCN-SSR-231214 et annexe preliminaire TTI; contour 2018 suppose')],
        sources=[dict(title='Sensata HS251',url='https://www.sensata.com/products/relays/hs-series-heat-sinks-hs251',kind='manufacturer'),
            dict(title='STEP Sensata officiel',url='https://www.sensata.com.cn/sites/default/files/a/sensata-hs251-heatsink-accessories-drawing.step',kind='manufacturer'),
            dict(title='PCN avec annexe preliminaire',url='https://www.ttiasia.com/content/dam/ttiinc/products/PCN/sensata/Sensata-PCN-SSR-231214.pdf',kind='manufacturer_document_mirror',locally_downloaded=False),
            dict(title='Avis eBay HS251 du 2025-05-09',url='https://www.ebay.com/p/1210661465',kind='user_review',
                tested_relay='D06D100, autre reference',quote='Fits the D06D100 SSR',thermal_measurements=False)],
        original_assets_manifest='assets.json',cad_manifest='3D/provenance.json',model_3d_created=True))
    rows=[]
    for current in [10,20,30,40,60]:
        loss=current**2*.005
        rows.append(dict(current_A=current,loss_W=loss,voltage_drop_V=current*.005,
            estimated_junction_C=round(40+loss*(2.5+.2+.27),3),within_proposed_current_envelope=current<=40))
    write('calculs.json',dict(checked_on='2026-10-13',status='etude stationnaire non qualifiee',
        current_definition='Courant efficace traversant le relais: somme instantanee des branches ESC',
        resistance_ohm=.005,heatsink_C_per_W=2.5,junction_case_C_per_W=.27,
        interface_C_per_W=.2,interface_is_assumption=True,ambient_C=40,rows=rows,
        manufacturer_derating_crosscheck=dict(source='../protection-batterie/coupure-moteurs/notices/Sensata-Crydom-1-DC-D1D100-datasheet.pdf',
            page=4,curve_C_per_W=3,approx_current_A_at_40C=50,reading='graphique approximative',not_a_new_rating=True),
        losses_over_45min_Wh_at_30A=3.375,losses_over_45min_Wh_at_40A=6,
        does_not_predict_vehicle_autonomy=True,thermal_test_done=False,
        limitations=['Rds varie avec temperature; alimentation ESC impulsionnelle et transitoires non modelises',
            'Resistance d interface non garantie; convection, boitier et orientation a qualifier',
            '60 A continus et 100 A hors enveloppe proposee']))
if __name__=='__main__':main()
