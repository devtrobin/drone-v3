"""Check the R2 documentary package; does not qualify physical hardware."""
from pathlib import Path
from urllib.parse import unquote
import ast
import hashlib
import json
import math
import re
import sys

import pymupdf

ROOT = Path(__file__).resolve().parents[1]
C = ROOT / 'Composants'
A = C / 'verification-alimentation'
RESULTS = []


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def check(name, passed, details):
    RESULTS.append(dict(check=name, passed=bool(passed), details=details))


def main():
    new_folders = [
        A, C / 'cordon-charge-s65-ic5', C / 'fusible-principal-classe-t',
        C / 'support-fusible-classe-t', C / 'fusibles-branches-rapides',
        C / 'supports-branches-rapides', C / 'cable-principal-silicone-6mm2',
        C / 'raccord-extension-cordon-ic5', C / 'raccords-entree-pi-wago',
        C / 'regulateur-alimentation/d42v55f5',
    ]
    json_errors = []
    json_count = 0
    for folder in new_folders:
        for path in folder.rglob('*.json'):
            if path.name == 'verification.json':
                continue
            json_count += 1
            try:
                read(path)
            except Exception as exc:
                json_errors.append(f'{path.relative_to(ROOT)}: {exc}')
    check('JSON syntax', not json_errors, dict(files=json_count, errors=json_errors))

    integrity_errors = []
    archived = 0
    for manifest in [A / 'assets.json', C / 'cordon-charge-s65-ic5/assets.json']:
        for asset in read(manifest)['assets']:
            if not asset.get('sha256'):
                continue
            archived += 1
            path = manifest.parent / asset.get('local', asset.get('file', ''))
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != asset['sha256']:
                integrity_errors.append(str(path.relative_to(ROOT)))
    check('Archived original integrity', not integrity_errors, dict(files=archived, errors=integrity_errors))

    step = C / 'regulateur-alimentation/d42v55f5/3D/pololu-d42v55fx-officiel.step'
    cad = read(step.parent / 'validation-freecad.json')
    step_hash = hashlib.sha256(step.read_bytes()).hexdigest()
    check('Native regulator STEP and existing FreeCAD import evidence',
          step_hash == cad['sha256'] == '849512fa686206951d282a92b8701418b7f5707e91d0abd70312e0af01caae5e'
          and cad['valid'] and cad['closed_solids'] and cad['solids'] == 1,
          dict(sha256=step_hash, importer=cad['importer'], bbox_mm=cad['bbox_mm'],
               scope='Checks unchanged file against earlier headless import; no GUI test'))

    broken = []
    link_count = 0
    md_files = [ROOT / 'ReadMe.md', C / 'README.md', C / 'ENSEMBLES-AVANT-CHASSIS.md']
    md_files += [p for folder in new_folders for p in folder.rglob('*.md')]
    for path in md_files:
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
            target = target.strip().strip('<>')
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target) or target.startswith('#'):
                continue
            target = unquote(target.split('#', 1)[0])
            if not target:
                continue
            link_count += 1
            if not (path.parent / target).exists():
                broken.append(dict(file=str(path.relative_to(ROOT)), target=target))
    check('Local Markdown links', not broken, dict(links=link_count, errors=broken))

    active = read(A / 'selection-active.json')
    calc = read(A / 'calculs.json')
    old = read(C / 'cordon-principal-batterie/selection-active.json')
    check('Active battery, fuse and charge references agree',
          old['active_battery']['ref'] in active['battery']
          and active['main_fuse'] in old['main_fuse']
          and 'BEEC1067' in old['charger'] and 'BEEC1067' in active['charger']
          and old['active_complete_cord_CAD'] is False,
          dict(revision=active['revision'], battery=active['battery'], main_fuse=active['main_fuse']))

    gpio = read(C / 'connecteur-gpio/brochage.json')
    bom = read(C / 'connecteur-gpio/nomenclature.json')
    pins = {item['physical_pin'] for item in gpio['pins']}
    power_pins = {2, 4, 6, 9, 14, 20}
    contacts = [p for p in bom['parts'] if '16-02-0103' in p['reference']][0]
    speed_extension = gpio.get('harness_revision') == 'vitesse-r1-after-alimentation-r2'
    expected_pins = {1, 11, 12, 13, 15, 32, 33, 34, 39} | ({16, 17, 18, 25} if speed_extension else set())
    expected_installed = len(expected_pins)
    check('Signal connector excludes Pi power contacts',
          pins == expected_pins
          and power_pins.issubset(gpio['unused_pins'])
          and gpio['power_through_Molex'] is False
          and contacts['installed'] == expected_installed and contacts['quantity'] == expected_installed+5 and contacts['spares'] == 5,
          dict(signal_pins=sorted(pins), separate_power_pads=sorted(power_pins), contacts=expected_installed+5,
               later_speed_sensor_extension=speed_extension))

    assumption = calc['Pi_assumptions']
    maximum_residual = 0
    supply_errors = []
    for row in calc['supply_rows']:
        # Independent quadratic solution for the physically high-voltage root.
        p = assumption['output_max_V'] * assumption['output_current_A'] / assumption['efficiency_min_study']
        r0 = assumption['common_loop_R_max_acceptance_ohm']
        rb = assumption['Pi_input_path_R_max_acceptance_ohm']
        b = row['Vpack_V'] - row['motors_A'] * r0 - 0.015 * (r0 + rb)
        v = (b + math.sqrt(b*b - 4 * (r0 + rb) * p)) / 2
        i = p / v + 0.015
        residual = max(abs(v-row['Pi_VIN_V']), abs(i-row['Pi_branch_A']),
                       abs(i+row['motors_A']-row['main_A']),
                       abs((i+row['motors_A'])**2*r0-row['main_loss_W']))
        maximum_residual = max(maximum_residual, residual)
        if residual > 1e-9 or v < assumption['minimum_VIN_acceptance_V']:
            supply_errors.append(row)
        if row['motors_A'] == 30 and row['main_A'] >= active['normal_main_budget_A']:
            supply_errors.append(row)
    check('Constant-power input and voltage budgets', not supply_errors,
          dict(rows=len(calc['supply_rows']), max_residual=maximum_residual,
               minimum_calculated_VIN_V=min(x['Pi_VIN_V'] for x in calc['supply_rows']),
               scope='Conditional calculation using resistance and efficiency acceptance assumptions'))

    fault = calc['fault_bound']
    rho0 = 0.01724 * (1 - 20 * 0.00393)
    rmin = rho0 * sum(x['length_min_m'] / x['section_max_acceptance_mm2'] for x in fault['credited_positive_segments'])
    isc = fault['voltage_max_V'] / rmin
    check('Conditional downstream fault bound uses positive wire only',
          abs(rmin-fault['positive_wire_R_min_ohm']) < 1e-12
          and abs(isc-fault['source_fault_upper_A']) < 1e-6
          and isc < fault['main_fuse_AIC_DC_A']
          and fault['return_wire_resistance_credited'] is False
          and fault['fuse_resistance_credited'] is False
          and fault['battery_internal_R_assumed_ohm'] == 0 and fault['conditional'],
          dict(calculated_upper_A=isc, scope='Downstream faults, stated lengths/sections/topology only; not pack measurement'))

    area = 150 * math.pi * 0.08**2 / 4
    strand_rows = [w for w in calc['short_wire_screening']['wires'] if abs(w['area_mm2']-area) < 1e-9]
    check('Supplier strand count used for actual 18 AWG screening',
          len(strand_rows) == 1 and abs(strand_rows[0]['allowable_I2t_A2s']-(100*area)**2) < 1e-6,
          dict(supplier_area_mm2=area, comparison_I2t_A2s=(100*area)**2,
               scope='Supplier dimensions, not measured conductor or completed fuse coordination'))

    charge = calc['charge']
    sku_data = read(C / 'cordon-charge-s65-ic5/references/Beez2B-BEEC1067-stock.json')
    sku_rows = [x for x in sku_data['variants'] if x['sku'] == 'BEEC1067']
    check('Charge SKU evidence and power budget',
          len(sku_rows) == 1 and sku_rows[0]['available'] and sku_rows[0]['price'] == 690
          and charge['current_A'] == 5 and charge['power_max_W'] == 8.4*5
          and charge['power_max_W'] < charge['S65_power_W']
          and charge['current_A'] < charge['S65_current_max_A'],
          dict(cable_price_EUR_TTC=6.9, archive_date='2026-10-15', charge_A=5, charge_max_W=42,
               scope='Archived seller declaration and charge settings, not physical connector/polarity check'))

    pdf_errors = []
    pdf_results = []
    for path, pages in [(A/'notices/verification-alimentation-v3.pdf', 7),
                        (C/'cordon-charge-s65-ic5/notices/notice-cordon-charge-s65-ic5-v3.pdf', 3)]:
        meta = read(path.with_suffix('.json'))
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        with pymupdf.open(path) as doc:
            if len(doc) != pages or meta['sha256'] != digest:
                pdf_errors.append(str(path))
            link_total = 0
            for page in doc:
                text = page.get_text()
                if '\ufffd' in text or '\x00' in text:
                    pdf_errors.append(f'{path.name} page {page.number+1}: replacement glyph')
                for block in page.get_text('dict')['blocks']:
                    for line in block.get('lines', []):
                        for span in line['spans']:
                            x0,y0,x1,y1 = span['bbox']
                            if x0 < 0 or y0 < 0 or x1 > page.rect.width+0.5 or y1 > page.rect.height+0.5:
                                pdf_errors.append(f'{path.name} page {page.number+1}: off-page span')
                link_total += len(page.get_links())
            if path.name == 'verification-alimentation-v3.pdf':
                p3 = doc[2].get_text()
                if '5 685' not in p3 or '6 773' in p3:
                    pdf_errors.append('Actual 18 AWG section not reflected in PDF')
        pdf_results.append(dict(file=str(path.relative_to(ROOT)), pages=pages, sha256=digest, links=link_total))
    check('Final authored PDFs', not pdf_errors, dict(files=pdf_results, errors=pdf_errors,
          visual_review='All final 7+3 rendered pages inspected in conversation on 2026-10-15'))

    syntax_errors = []
    for name in ['collect_supply_audit_refs.py', 'revise_supply_audit.py', 'supply_audit_text.py',
                 'supply_audit_pdf_text.py', 'build_supply_audit_pdf.py', 'verify_supply_audit.py']:
        try:
            ast.parse((ROOT/'tools'/name).read_text(encoding='utf-8'), filename=name)
        except SyntaxError as exc:
            syntax_errors.append(f'{name}: {exc}')
    check('Audit tools Python syntax', not syntax_errors, syntax_errors)

    check('Unresolved qualification remains explicit',
          active['hardware_tested'] is False and active['ready_for_power_on'] is False
          and active['full_fuse_coordination_validated'] is False
          and len(active['remaining_manufacturer_confirmations']) == 3,
          active['remaining_manufacturer_confirmations'])

    passed = all(item['passed'] for item in RESULTS)
    result = dict(date='2026-10-15', revision='alimentation-r2',
                  scope='Document consistency and conditional calculations; not electrical qualification',
                  document_checks_passed=passed, hardware_tested=False, ready_for_power_on=False,
                  full_fuse_coordination_validated=False, checks=RESULTS)
    (A/'verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    for item in RESULTS:
        print(('PASS' if item['passed'] else 'FAIL'), item['check'])
        if not item['passed']:
            print(json.dumps(item['details'], ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    raise SystemExit(main())
