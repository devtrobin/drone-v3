"""Calculations, reference provenance and extraction of unchanged vendor photo."""
from pathlib import Path
import json,hashlib,sys
import pymupdf
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'Composants/protection-surintensite'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    sys.stdout.reconfigure(encoding='utf-8')
    principal=40+25/(6.4*.90)+.05
    save(BASE/'calculs.json',dict(checked_on='2026-10-14',status='etude non qualifiee',motor_total_continuous_assumption_A=40,
        pi_camera_power_assumption_W=25,battery_min_calculation_V=6.4,regulator_efficiency_assumption=.9,
        auxiliary_current_assumption_A=.05,principal_current_A=principal,selected_fuse_A=60,
        cold_resistance_typical_ohm=.00087,prospective_fault_current_established=False,
        interrupt_rating_recent_A=2000,interrupt_rating_voltage_V=32,interrupt_rating_old_A=1000,
        loop_resistance_reference_ohm=8.4/2000,loop_model_is_simplified=True,
        copper_trunk_section_proposal_mm2=6,wire_ampacity_validated=False,relay_thermal_current_is_not_limited_by_fuse=True,
        time_current=[dict(percent=100,current_A=60,min_s=360000,max_s=None),dict(percent=110,current_A=66,min_s=14400,max_s=None),
            dict(percent=150,current_A=90,min_s=90,max_s=3600),dict(percent=200,current_A=120,min_s=3,max_s=100),
            dict(percent=300,current_A=180,min_s=.3,max_s=3),dict(percent=500,current_A=300,min_s=.1,max_s=1)],
        typical_derating_60A=[dict(ambient_C=t,recommended_current_A=i) for t,i in [(20,58),(65,48),(85,43),(110,36),(125,31)]],
        losses=[dict(current_A=i,cold_loss_W=i*i*.00087,cold_drop_V=i*.00087) for i in [10,20,30,40,principal,60]],
        source_revision='Littelfuse REV07272021, p1-2; actual lot applicability to verify',
        limitations=['Contacts, terminals, wiring and hot resistance excluded from loss calculation',
            'Interrupting capacity and wire protection must be coordinated; typical melting I2t is not total clearing guarantee',
            'Branch fuses, cable lugs and complete harness not yet selected']))
    save(BASE/'sources.json',dict(checked_on='2026-10-14',purchased=False,bench_tested=False,
        holder='Littelfuse 04980900ZXT',fuse='Littelfuse 0498060.M',fuse_current_A=60,current_selection_is_preliminary=True,
        amazon=dict(exact_asins=None,france_offer_confirmed=False,price_eur_ttc=None,status='Challenge bm-verify; aucune fiche produit verifiee'),
        sources=[dict(title='Holder TME public reference',url='https://www.tme.eu/en/details/04980900zxt/car-fuseholders/littelfuse/'),
            dict(title='Fuse exact Farnell reference',url='https://uk.farnell.com/littelfuse/0498060-m/automotive-fuse-time-delay-60a/dp/3516004'),
            dict(title='Manufacturer current fuse datasheet',url='https://www.littelfuse.com/assetdocs/midi-32v-bolt-down-series-data-sheet?assetguid=b55e8034-180d-40f6-a0a7-bebc2d4a94f5',local_downloaded=False),
            dict(title='Manufacturer CAD form',url='https://info.littelfuse.com/midi-498-series-3dmodel-landingpage',form_submitted=False)],
        vendor_cad_downloaded=False,originals='assets.json',cad='3D/catalogue.json'))
    manifest=BASE/'assets.json';data=json.loads(manifest.read_text(encoding='utf-8'))
    for a in data['assets']:
        if a['file'].startswith('sources-web/Amazon'):a['status']='challenge_html';a['product_page']=False
    # Extract the existing product photograph from the vendor PDF, unchanged.
    pdf=BASE/'porte-fusible/notices/Littelfuse-MIDI-498-fiche-miroir-TME.pdf';d=pymupdf.open(pdf)
    candidates=[]
    for image in d.get_page_images(0):
        rects=d[0].get_image_rects(image[0])
        if any(r.y0<300 and r.x0<320 for r in rects):candidates.append(image)
    if candidates:
        chosen=max(candidates,key=lambda r:r[2]*r[3]);im=d.extract_image(chosen[0]);p=BASE/'porte-fusible/photos'/('Littelfuse-photo-extraite-fiche-2008.'+im['ext'])
        p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(im['image'])
        rec=dict(file=str(p.relative_to(BASE)).replace('\\','/'),source_file=str(pdf.relative_to(BASE)).replace('\\','/'),
            source_sha256=sha(pdf),source_page=1,pdf_xref=chosen[0],status='extracted_embedded_image',
            bytes=p.stat().st_size,sha256=sha(p),image_pixels_modified=False,checked_on='2026-10-14')
        data['assets']=[a for a in data['assets'] if a['file']!=rec['file']]+[rec]
        print('VENDOR PHOTO',p.name,im['width'],im['height'],flush=True)
    save(manifest,data)
    for folder in ['porte-fusible','fusible-60a']:
        save(BASE/folder/'sources.json',dict(checked_on='2026-10-14',part='04980900ZXT' if folder=='porte-fusible' else '0498060.M',
            purchased=False,tested=False,source_manifest='../assets.json',notes='../recherche-technique.md',CAD='3D/provenance.json',
            native_vendor_cad=False,model_3d_created=True))
    print('DATA principal current',round(principal,4),'A',flush=True)
if __name__=='__main__':main()
