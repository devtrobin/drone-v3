"""Coloured, individually validated STEP reconstructions for the V3 running gear.

Run with tools/temp/cad-env/Scripts/python.exe. Nominal supplier dimensions and
project design assumptions are recorded separately. These are NOT native vendor
CAD nor certified manufacturing drawings. Existing camera/motor/Pi/wheel files
are never rewritten. All dimensions in millimetres, all colours linear RGB.
"""
from pathlib import Path
import argparse, hashlib, json, math, sys, time
import cadquery as cq
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from OCP.STEPCAFControl import STEPCAFControl_Reader
from OCP.TDocStd import TDocStd_Document
from OCP.TCollection import TCollection_ExtendedString
from OCP.TDF import TDF_LabelSequence
from OCP.XCAFDoc import XCAFDoc_DocumentTool
from OCP.IFSelect import IFSelect_RetDone
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.BRepTools import BRepTools
from render_step_meshes import render_meshes

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'Composants'
COMMON = BASE / 'direction-et-transmission'
BLACK = (.022, .026, .032)
STEEL = (.38, .41, .45)
BRIGHT = (.62, .65, .69)
ALU = (.58, .61, .65)
BRASS = (.54, .34, .085)
WHITE = (.88, .87, .80)
RED = (.57, .014, .009)
ORANGE = (.92, .33, .012)
BROWN = (.085, .033, .012)
BLUE = (.018, .09, .39)
MODELS = []


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cyl(r, h, z=0, x=0, y=0, axis=(0, 0, 1)):
    return cq.Solid.makeCylinder(r, h, cq.Vector(x, y, z), cq.Vector(*axis))


def ring(ro, ri, h, z=0):
    return cyl(ro, h, z).cut(cyl(ri, h + .02, z - .01))


def box(x, y, z, pos=(0, 0, 0), fillet=0):
    w = cq.Workplane('XY').box(x, y, z, centered=(True, True, False))
    if fillet:
        w = w.edges('|Z').fillet(fillet)
    return w.val().translate(pos)


def hexagon(af, h, z=0):
    return cq.Workplane('XY').polygon(6, af / math.cos(math.pi / 6)).extrude(h).val().translate((0, 0, z))


def tube(points, radius):
    vectors = [cq.Vector(*p) for p in points]
    edge = cq.Edge.makeSpline(vectors)
    plane = cq.Plane(origin=vectors[0], normal=edge.tangentAt(0))
    return cq.Workplane(plane).circle(radius).sweep(cq.Workplane('XY').newObject([cq.Wire.assembleEdges([edge])]), isFrenet=True).val()


def servo_cable(y, radius):
    # Three cubic Bezier spans with equal tangent vectors at their joins.
    # More robust OCC tessellation than a high-degree interpolating sweep.
    spans=[ [(-11,3),(-20,3),(-18,12),(-20,23)],
            [(-20,23),(-22,34),(-34,35),(-35,24)],
            [(-35,24),(-36,13),(-35,2),(-40,2)] ]
    end_y=y*2.54/.95
    edges=[cq.Edge.makeBezier([cq.Vector(x,(end_y if i==2 and j>=2 else y),z)
           for j,(x,z) in enumerate(p)]) for i,p in enumerate(spans)]
    wire=cq.Wire.assembleEdges(edges)
    plane=cq.Plane(origin=(-11,y,3),normal=edges[0].tangentAt(0))
    # Parallel-transport frames avoid a Frenet flip at curvature changes.
    result=cq.Workplane(plane).circle(radius).sweep(cq.Workplane('XY').newObject([wire]),isFrenet=False).val()
    assert result.isValid() and len(result.Solids())==1
    for edge in edges:
        for u in np.linspace(0,1,21):
            assert result.isInside(edge.positionAt(float(u)),1e-6)
    for x,z,tx,tz in [(-20,23,-2,11),(-35,24,-1,-11)]:
        norm=math.hypot(tx,tz)
        for i in range(12):
            a=i*math.pi/6
            p=(x-.40*tz/norm*math.cos(a),y+.40*math.sin(a),z+.40*tx/norm*math.cos(a))
            assert result.isInside(cq.Vector(*p),1e-6)
    return result


def thread(d, length, pitch, z=0):
    """Nominal ISO-like external helix with truncated crests; tolerance omitted.

    Root/corner radii are approximations. This is visible helical geometry, not
    stacked rings, and not a gauge model. Trimmed ends keep nominal length.
    """
    depth = .54 * pitch
    core = cyl(d / 2 - depth + .015, length, z)
    helix = cq.Wire.makeHelix(pitch, length + 2 * pitch, d / 2 - depth / 2)
    r = d / 2 - depth / 2
    # Profile in the radial-axial plane at the beginning of the helix.
    ridge = (cq.Workplane('XZ').polyline([(r - depth / 2 - .03, -.38 * pitch),
             (r + depth / 2, -.065 * pitch), (r + depth / 2, .065 * pitch),
             (r - depth / 2 - .03, .38 * pitch)]).close()
             .sweep(cq.Workplane('XY').newObject([helix]), isFrenet=True).val()
             .translate((0, 0, z - pitch)))
    ridge = ridge.intersect(cyl(d / 2 + .01, length, z))
    result = core.fuse(ridge).clean()
    assert result.isValid() and len(result.Solids()) == 1
    return result


def screw(d, length, pitch, head_d=None, head_h=1.5, recess='cross', shoulder=0, shoulder_d=None):
    h = head_h
    s = thread(d, length - shoulder, pitch)
    if shoulder:
        s = s.fuse(cyl((shoulder_d or d) / 2, shoulder, length - shoulder))
    s = s.fuse(cyl((head_d or d * 1.8) / 2, h, length)).clean()
    if recess == 'hex':
        s = s.cut(hexagon(d * .5, h * .7, length + h * .35))
    else:
        for angle in (0, 90):
            cut = box(d * 1.15, d * .25, h * .7, (0, 0, length + h * .35))
            s = s.cut(cut.rotate((0, 0, 0), (0, 0, 1), angle))
    return s.clean()


def add(folder, filename, title, parts, published, estimated, params=None,
        view=(.7, -.9, 1.05), design=False, probes=None, source_pages=None):
    MODELS.append(dict(folder=folder, filename=filename, title=title, parts=parts,
        published=published, estimated=estimated, params=params or {}, view=view,
        design=design, probes=probes or [], source_pages=source_pages or []))


def servo():
    folder = 'servo-direction'
    # FEETECH historical sheet, PDF page 5: body 23.3 x 12.1, height to
    # shoulder 21.45, output envelope 25.25; tabs total 32.5 and holes diameter 2.
    case = box(23.3, 12.1, 12.0, (0, 0, 4.9), .55)
    bottom = box(23.3, 12.1, 4.75, fillet=.55)
    top = box(23.3, 12.1, 4.40, (0, 0, 17.05), .55)
    tabs = box(32.5, 12.1, 1.6, (0, 0, 16.8), .45)
    tabs = tabs.cut(box(23.32, 12.12, 2, (0, 0, 16.6)))
    for x in (-14.25, 14.25):
        tabs = tabs.cut(cyl(1, 2, 16.6, x))
    top = top.fuse(tabs).fuse(cyl(5.55, 2.0, 21.45, -5.7))
    top = top.fuse(cyl(2.9, 1.25, 21.45, .65)).clean()
    # Small opening: cable reaches the actual body rather than floating nearby.
    bottom = bottom.cut(box(1.6, 4.0, 1.7, (-11.4, 0, 2.2)))
    parts = [('Boitier_central_PC', case, BLACK), ('Capot_inferieur_PC', bottom, BLACK),
             ('Capot_reducteur_et_oreilles', top, BLACK)]
    output = ring(1.81, .80, 1.8, 23.45).translate((-5.7, 0, 0))
    # Twenty individual, fused spline ridges, OD nominal 3.95.
    for i in range(20):
        tooth = box(.34, .20, 1.8, (1.80, 0, 23.45)).rotate((0, 0, 0), (0, 0, 1), i * 18).translate((-5.7, 0, 0))
        output = output.fuse(tooth)
    parts.append(('Sortie_laiton_20T_OD3_95_estimee', output.clean(), BRASS))
    for i, (x, y) in enumerate([(-10.3, -4.8), (-10.3, 4.8), (10.3, -4.8), (10.3, 4.8)]):
        # Visible retaining screw heads; hidden internal screw routing unknown.
        head = cyl(.62, .35, .1, x, y).cut(box(.85, .20, .2, (x, y, .3)))
        parts.append((f'Tete_vis_boite_{i+1}_estimee', head, BRIGHT))
    label = box(17, .10, 7.0, (0, -6.10, 7.2))
    parts.append(('Etiquette_fond_blanc', label, WHITE))
    # Text is real shallow solid lettering, not external image texture.
    for content, size, z in [('FEETECH', 2.0, 12.0), ('FT90M', 2.1, 8.8)]:
        text = cq.Workplane('XY').text(content, size, .05, font='Arial', combine=False).val()
        text = text.rotate((0, 0, 0), (1, 0, 0), 90).translate((0, -6.16, z))
        parts.append(('Marquage_' + content, text, BLACK))
    # Compact laid-out 200-mm cable choice: current manufacturer length. The
    # 2020 drawing describes 250 mm instead; routing is illustrative.
    for i, color in enumerate([BROWN, RED, ORANGE]):
        yy = (i - 1) * .95
        parts.append((f'Cordon_{i+1}_trace_illustratif_longueur_non_imposee', servo_cable(yy, .43), color))
    plug = box(3.0, 7.65, 8.2, (-40, 0, -6.2), .25)
    for i,y in enumerate((-2.54, 0, 2.54)):
        plug = plug.cut(box(1.45, 1.45, 6.8, (-40, y, -6.3)))
        socket=box(1.10,1.10,5.6,(-40,y,-5.5)).cut(box(.68,.68,5.8,(-40,y,-5.6)))
        parts.append((f'Contact_femelle_{i+1}_estime',socket,BRASS))
    parts.append(('Connecteur_3_voies_geometrie_estimee', plug, BLACK))
    add(folder, 'servo-feetech-ft90m-detaille.step', 'FEETECH FT90M | servo sans palonnier', parts,
        ['PDF p.5: corps 23.3 x 12.1 mm; epaulement 21.45 mm; sortie 25.25 mm',
         'Oreilles: longueur 32.5 mm, deux trous diametre 2 mm; sortie 20T OD3.95',
         'Vue/photo PDF p.7: boitier noir, sortie laiton, cable brun/rouge/orange'],
        ['Rayons, epaisseurs, petites vis et etiquettes reconstruits',
         'Pas de moteur, electronique ou reducteur internes inventes',
         'Cable dessine compact: longueur du routage NON equivalente a 200/250 mm',
         'Connecteur non cote, pas de contacts propose 2.54 mm; variante recue a confirmer',
         'FT90M revision 2020, variante actuelle a confirmer'],
        params={'body_width':12.1,'body_length':23.3,'body_shoulder_height':21.45,
                'cables':3,'each_cable_closed_solids':1,'cable_axis_and_joint_material_probes_passed':True,
                'connector_pitch_assumed':2.54},
        source_pages=['FEETECH-FT90M-fiche-historique-miroir.pdf p.5 et p.7'])
    # Four accessory silhouettes are visible in the original product photo.
    horn_parts = []
    for kind, name, offset in [('single', 'palonnier-simple', 0), ('double', 'palonnier-double', 32),
                               ('cross', 'palonnier-croix', 70), ('disc', 'palonnier-disque', 105)]:
        hub = cyl(3.2, 3.2)
        if kind == 'disc':
            plate = ring(10, 1.99, 1.3)
        else:
            length = 12 if kind == 'single' else 26
            plate = box(length, 4.7, 1.3, ((5 if kind == 'single' else 0), 0, 0), 1.4)
            if kind == 'cross':
                plate = plate.fuse(plate.rotate((0, 0, 0), (0, 0, 1), 90))
            plate = plate.fuse(cyl(3.2, 1.3)).cut(cyl(1.99, 3.5))
        for angle in range(0, 360, 90 if kind in ('cross', 'disc') else 180):
            for r in (6, 8, 10):
                if kind == 'single' and angle:
                    continue
                x = r * math.cos(math.radians(angle)); y = r * math.sin(math.radians(angle))
                plate = plate.cut(cyl(.65, 1.5, -.1, x, y))
        horn = plate.fuse(hub).clean()
        # A screw head must bear on a roof, not fall through the spline socket.
        # Central M2 clearance through the roof; underside 20T study socket.
        horn=horn.cut(cyl(1.1,3.4,-.1)).cut(cyl(1.825,1.91,-.01))
        for tooth in range(20):
            slot=box(.38,.24,1.91,(1.82,0,-.01)).rotate((0,0,0),(0,0,1),tooth*18)
            horn=horn.cut(slot)
        horn=horn.clean()
        add(folder, name + '-ft90m.step', 'FT90M | ' + name, [('POM_blanc', horn, WHITE)],
            ['Accessoires blancs observes PDF p.7; famille de sortie 20T OD3.95'],
            ['Toutes cotes de palonnier, trous et profil estimees; spline interne 20T reconstruite NON certifiee',
             'Trou central Ø2.2, roof1.3 et socket1.9: choix geometriques non cotes',
             'Table PDF p.6: No Accessories, malgre photo p.7; contenu du sachet non garanti',
             'Dessins de pose uniquement: verifier accessoires du servo recu'],
            view=(.4, -.5, 1),probes=[dict(point=(0,0,2.5),occupied=False),dict(point=(1.2,0,2.5),occupied=True)])
        horn_parts.append((name, horn.translate((offset, 0, 0)), WHITE))
    add(folder, 'vis-palonnier-m2x4.step', 'FT90M | vis nominale M2 x 4',
        [('Vis_M2x4_estimee', screw(2, 4, .4, 3.6, 1.0), BRIGHT)],
        ['Vis M2 x 4 mentionnee dans la fiche'], ['Pas ISO 0.4 et forme de tete proposes; vis recue a comparer'])


def ball_link():
    folder = 'biellettes-direction/rotules'
    s = cq.Solid.makeSphere(2.5, cq.Vector(0, 0, 8.2), angleDegrees1=-90)
    s = s.fuse(cyl(1.5, 1.8, 5)).fuse(hexagon(4.5, 1.8, 3.2)).fuse(thread(3, 3.2, .5)).clean()
    add(folder, 'rotule-tamiya-50592-5mm.step', 'Tamiya 50592 | rotule 5 mm', [('Rotule_metal', s, BRIGHT)],
        ['Boule nominale diametre 5 mm; principe visible notice TT01R p.10'],
        ['Hauteurs, hexagone AF4.5 et tige M3x0.5 reconstruits; pas un plan Tamiya cote',
         'Profil de col et longueur de filetage a mesurer'], source_pages=['Tamiya-TT01R-notice-constructeur.pdf p.10'])
    folder = 'biellettes-direction/chapes'
    # Axis of socket Z, rod axis X. Spherical socket with open faces so the
    # visible aperture is round and the ball has a real concave cavity.
    outer = cyl(4, 3.6, -1.8)
    outer = outer.fuse(box(8.8, 5.8, 3.6, (6, 0, -1.8), .6)).clean()
    outer = outer.cut(cq.Solid.makeSphere(2.55, angleDegrees1=-90))
    outer = outer.cut(cyl(2.05, 4, -2))
    outer = outer.cut(cq.Solid.makeCylinder(1.3, 9.0, cq.Vector(11, 0, 0), cq.Vector(-1, 0, 0)))
    for y in (-2.88, 2.88):
        for x in (4.5, 6, 7.5, 9):
            outer = outer.cut(box(.55, .22, 2.5, (x, y, -1.25)))
    add(folder, 'chape-tamiya-50596-5mm.step', 'Tamiya 50596 | chape pour rotule 5 mm', [('Chape_plastique', outer.clean(), BLACK)],
        ['Famille 5 mm; tige M3 selon notice TT01R p.10'],
        ['Longueur 14.4, anneau OD8, epaisseur3.6 et empreinte de prehension estimes',
         'Logement spherique R2.55 estime; precharge, clip et taraudage non certifies'],
        source_pages=['Tamiya-TT01R-notice-constructeur.pdf p.10'],
        probes=[dict(point=(0, 0, 0), occupied=False)])
    add('biellettes-direction/tiges', 'tige-m3-longueur-etude-35mm.step', 'Biellette | tige M3, exemple 35 mm',
        [('Tige_filetee_M3x0_5_L35_etude', thread(3, 35, .5), BRIGHT)],
        ['Famille retenue M3, pas nominal 0.5 mm'], ['Longueur 35 mm: exemple parametrique, pas cote de la direction V3'],
        params={'diameter':3, 'pitch':.5, 'example_length':35}, design=True, view=(1, -1, .25))


def bearing():
    # External nominal geometry only. Closed shields conceal the inside, so
    # no invented ball count or cage topology is included.
    outer = ring(5.5, 4.35, 4)
    inner = ring(3.1, 2.5, 4)
    for a in ('outer', 'inner'):
        s = outer if a == 'outer' else inner
        s = cq.Workplane('XY').newObject([s]).edges('%Circle').chamfer(.12).val()
        if a == 'outer':
            outer = s
        else:
            inner = s
    parts = [('Bague_exterieure', outer, STEEL), ('Bague_interieure', inner, BRIGHT),
        ('Flasque_Z_avant', ring(4.32, 3.13, .18, .18), BRIGHT),
        ('Flasque_Z_arriere', ring(4.32, 3.13, .18, 3.64), BRIGHT)]
    add('roulements', 'roulement-mr115zz-5x11x4.step', 'MR115ZZ | 5 x 11 x 4 mm', parts,
        ['Alésage 5 mm; exterieur 11 mm; largeur 4 mm; double flasque metal ZZ'],
        ['Diametres de partage bagues/flasques, chanfreins et epaisseurs estimes',
         'Billes, cage, chemins internes et jeu non documentes: non representes'],
        params={'bore':5, 'OD':11, 'width':4},
        probes=[dict(point=(2.49, 0, 2), occupied=False), dict(point=(2.60, 0, 2), occupied=True)],
        source_pages=['SMB-MR115ZZ-fiche-technique.pdf p.1'])


def axle_front():
    # Published 35-mm overall, nominal interface family inferred from bearing
    # and wheel hardware. Output is positive Z, inner dogbone cup at Z=0.
    cup = cyl(4.9, 9).cut(cyl(3.4, 8, -.01))
    for angle in (0, 180):
        slot = box(2.2, 5.4, 6.0, (0, 4.0, -.1)).rotate((0, 0, 0), (0, 0, 1), angle)
        cup = cup.cut(slot)
    s = cup.fuse(cyl(2.5, 20, 9)).fuse(thread(4, 6, .7, 29)).clean()
    s = s.cut(cq.Solid.makeCylinder(1, 7, cq.Vector(-3.5, 0, 26), cq.Vector(1, 0, 0)))
    add('axes-avant', 'axe-tamiya-50823-35mm.step', 'Tamiya 50823 | axe de roue 35 mm', [('Axe_acier', s, STEEL)],
        ['Longueur totale 35 mm (fiche Tamiya); famille roulement Ø5, ecrou M4, goupille Ø2'],
        ['Coupelle OD9.8/L9, fentes, epaulements et trou de goupille z26 estimes',
         'Longueur filetage M4x0.7 de 6 mm proposee; cote a mesurer',
         'Coupelle conservee mais sans dogbone dans architecture avant non motrice'],
        params={'overall_length':35, 'bearing_diameter':5, 'wheel_thread':'M4x0.7 assumed', 'pin_diameter':2},
        view=(1, -1, .5), probes=[dict(point=(0,0,26),occupied=False)],
        source_pages=['Tamiya-TT01R-notice-constructeur.pdf p.10 et p.15'])


def hub():
    s = hexagon(12, 6).cut(cyl(2.5, 6.2, -.1))
    s = cq.Workplane('XY').newObject([s]).edges('|Z').chamfer(.18).val()
    # Pin groove on rear face, clamp slit and transverse screw.
    s = s.cut(box(10.1, 2.1, 1.15, (0, 0, -.01)))
    s = s.cut(box(8, .35, 6.2, (6, 0, -.1)))
    screw_pos = (4.8, -3.25, 3.8)
    s = s.cut(cq.Solid.makeCylinder(.85, 6.5, cq.Vector(*screw_pos), cq.Vector(0, 1, 0)))
    clamp = screw(1.6, 5, .35, 2.6, 1.1, recess='hex')
    clamp = clamp.rotate((0,0,0),(1,0,0),90).translate((4.8, 1.75, 3.8))
    add('moyeux', 'moyeu-tamiya-53569-hex12-6mm.step', 'Tamiya 53569 | moyeu aluminium 6 mm',
        [('Moyeu_hexagonal_fendu', s.clean(), ALU), ('Vis_pince_estimee', clamp, STEEL)],
        ['Epaisseur constructeur 6 mm; famille hexagone AF12 et arbre Ø5'],
        ['Rainure de goupille, position fente, vis M1.6 et chanfreins estimes',
         'Verifier le diametre et le passage reels de la vis de pince'],
        params={'across_flats':12,'thickness':6,'bore':5},
        probes=[dict(point=(2.49,0,3),occupied=False),dict(point=(0,5.9,3),occupied=True)])


def uprights():
    # Reconstructed A7 from TT01R p.10. X axle; Z kingpin axis. Bearing seats
    # are exact nominal 11x4, but bearing separation and complete outline are
    # study dimensions, not measurements of the real Tamiya moulding.
    main = ring(7.2, 3.3, 14)
    main = main.cut(cyl(5.5, 4.1, -.01)).cut(cyl(5.5, 4.1, 9.91))
    main = main.rotate((0,0,0),(0,1,0),90).translate((-7,0,0))
    # Strengthening longitudinal ribs, matching the illustrated moulded barrel.
    for i in range(8):
        rib = box(14, 1.1, 1.05, (0, 0, 6.9), .2)
        main = main.fuse(rib.rotate((0,0,0),(1,0,0),i*45))
    for z in (-11, 7.0):
        boss = cyl(2.7, 4, z).cut(cyl(1.15, 4.2, z-.1))
        main = main.fuse(boss)
    arm = box(6, 12.7, 3.8, (0, -7, 3.7), 1.5).fuse(cyl(3,3.8,3.7,0,-13.0))
    arm = arm.cut(cyl(1.2,4,3.6,0,-13))
    main = main.fuse(arm).clean()
    common_est = ['Enveloppe, separation des roulements, bras et nervures reconstruits depuis notice',
                  'Logements nominaux Ø11 x4 sans ajustement; centre pivot et bras a relever sur A7 reel',
                  'Ne pas usiner les fourches a partir de ces estimations sans controle des pieces']
    for handed, shape in [('droite',main), ('gauche',main.mirror('XZ'))]:
        add('fusees-avant', f'fusee-a7-{handed}-tamiya-51002.step', 'Tamiya A7 | fusee ' + handed,
            [('Fusee_A7_plastique_reconstruction',shape,BLACK)],
            ['A7, deux roulements 1150 et vis pivots 3x10 identifies TT01R p.10'],common_est,
            params={'bearing_seats_nominal':11, 'bearing_width':4,'seat_start_x':[-7,2.9],
                    'pivot_extent_z_study':[-11,11]}, view=(1,-1,.7),
            probes=[dict(point=(0,0,0),occupied=False)],source_pages=['Tamiya-TT01R-notice-constructeur.pdf p.10'])
    collar = ring(2.8,1.55,1.0).fuse(ring(1.8,1.55,1.8,1.0))
    add('fusees-avant','bague-pivot-a6-tamiya-51002.step','Tamiya A6 | bague pivot',
        [('Bague_pivot_A6',collar.clean(),BLACK)],['Bague A6 identifiee dans la notice p.10'],
        ['Tous diametres et hauteurs reconstruits; Ø3.1 trou de vis et forme a confirmer'])
    for name, branch in [('a1',-1),('a8',1)]:
        s = box(18,7,3,(8,0,0),2.0).fuse(cyl(4,7)).fuse(cyl(3.5,3,0,16,branch*4))
        s = s.fuse(box(7,8,3,(16,branch*2,0),1)).cut(cyl(1.55,7.2,-.1))
        s = s.cut(cyl(1.2,3.2,-.1,16,branch*4))
        if name=='a8':
            s=s.fuse(box(7,13,3,(0,8,0),1.8)).cut(cyl(1.2,3.2,-.1,0,13))
        add('fusees-avant',f'renvoi-{name}-tamiya-51002.step','Tamiya '+name.upper()+' | renvoi de direction',
            [('Renvoi_'+name.upper(),s.clean(),BLACK)],['Renvoi '+name.upper()+' et vis decollétees identifies TT01R p.10'],
            ['Contours, epaisseurs, entraxes et alesages entierement reconstruits non mesures',
             'Etude d implantation, pas une copie garantie du moulage Tamiya'],source_pages=['Tamiya-TT01R-notice-constructeur.pdf p.10'])


def involute_gear(teeth, module, bore, face, hub_d, hub_length, pressure=20):
    """Circular arcs and smooth interpolated involutes, no triangle teeth.

    Root transition is a smooth reconstructed curve, NOT a factory-generated
    trochoid. Standard unshifted full depth assumed. XY teeth, axial +Z hub.
    """
    rp=module*teeth/2; rb=rp*math.cos(math.radians(pressure))
    ra=rp+module; rf=rp-1.25*module
    inv=lambda t:t-math.atan(t)
    t_pitch=math.tan(math.radians(pressure))
    half_base=math.pi/(2*teeth)+inv(t_pitch)
    t_max=math.sqrt((ra/rb)**2-1)
    r_start=max(rb,rf+.08*module)
    t_start=math.sqrt(max(0,(r_start/rb)**2-1))
    root_half=min(half_base+.14*module/rf, math.pi/teeth*.87)
    def point(r,a):return cq.Vector(r*math.cos(a),r*math.sin(a),0)
    def arc(r,a,b):return cq.Edge.makeThreePointArc(point(r,a),point(r,(a+b)/2),point(r,b))
    edges=[]
    for i in range(teeth):
        center=2*math.pi*i/teeth
        left_root=center-root_half
        left_start=center-half_base+inv(t_start)
        left_tip=center-half_base+inv(t_max)
        if r_start>rf+.001:
            pts=[point(rf,left_root),point(rf+.20*(r_start-rf),left_root+.15*(left_start-left_root)),
                 point(rf+.60*(r_start-rf),left_root+.65*(left_start-left_root)),point(r_start,left_start)]
            edges.append(cq.Edge.makeSpline(pts))
        vals=np.linspace(t_start,t_max,12)
        edges.append(cq.Edge.makeSpline([point(rb*math.sqrt(1+t*t),center-half_base+inv(t)) for t in vals]))
        edges.append(arc(ra,left_tip,center+half_base-inv(t_max)))
        edges.append(cq.Edge.makeSpline([point(rb*math.sqrt(1+t*t),center+half_base-inv(t)) for t in vals[::-1]]))
        right_start=center+half_base-inv(t_start);right_root=center+root_half
        if r_start>rf+.001:
            pts=[point(r_start,right_start),point(rf+.60*(r_start-rf),right_root-.65*(right_root-right_start)),
                 point(rf+.20*(r_start-rf),right_root-.15*(right_root-right_start)),point(rf,right_root)]
            edges.append(cq.Edge.makeSpline(pts))
        edges.append(arc(rf,right_root,2*math.pi*(i+1)/teeth-root_half))
    outline=cq.Wire.assembleEdges(edges)
    assert outline.isValid(),(teeth,'outline')
    s=cq.Solid.extrudeLinear(outline,[],cq.Vector(0,0,face))
    assert s.isValid(),(teeth,'teeth extrusion')
    hub=cyl(hub_d/2,hub_length,face)
    if abs(hub_d-2*ra)<1e-8:
        # Exact OD13 hub and tooth tips share tangential vertices. Serialize
        # the two adjacent axial regions as separate, valid touching BReps,
        # keeping all nominal dimensions. They represent ONE physical gear.
        cutter=cyl(bore/2,face+hub_length+.2,-.1)
        return cq.Compound.makeCompound([s.cut(cutter).clean(),hub.cut(cutter).clean()])
    s=s.fuse(hub,tol=1e-6).clean().fix()
    assert s.isValid(),(teeth,'hub fusion')
    s=s.cut(cyl(bore/2,face+hub_length+.2,-.1))
    assert s.isValid() and len(s.Solids())==1,(teeth,'bore cut')
    return s


def gears():
    for folder,filename,title,z,bore,hd,hw,j,color,published,estimated in [
        ('transmission-arriere/pignon-moteur','pignon-losi-los212054-16t.step','Losi LOS212054 | 16 dents',16,2,7,4,2,BRIGHT,
         ['16 dents, module0.5, alesage2 mm publies par Losi'],
         ['Angle20 deg, denture5, moyeu OD7/L4 et vis M3 proposes: NON publies',
          'Compatibilite angle de pression avec KHK pas confirmee']),
        ('transmission-arriere/engrenages-54dents','couronne-khk-ss0-5-54a.step','KHK SS0.5-54A | 54 dents',54,5,25,7,3.5,BLACK,
         ['54 dents, module0.5, angle20 deg, bore5', 'Diametre primitif27, exterieur28, moyeu25, denture5, moyeu7, total12',
          'Vis M4; axe vis J=3.5 mm depuis face du moyeu; acier S45C noirci'],
         ['Raccord pied de dent, chanfreins et geometrie vis non cotes; pas de tolerance H8 appliquee']),
        ('transmission-arriere/pignon-intermediaire','pignon-khk-ss0-5-24b.step','KHK SS0.5-24B | 24 dents',24,5,13,11,3,BLACK,
         ['24 dents, module0.5, angle20 deg, bore5H8 nominal', 'Diametre primitif12, exterieur13, moyeu13, denture5, moyeu11, total16',
          'Vis M4; axe vis J=3 mm depuis face du moyeu; acier S45C noirci'],
         ['Raccord pied de dent, chanfreins et geometrie vis non cotes; tolerance H8 non appliquee'])]:
        s=involute_gear(z,.5,bore,5,hd,hw)
        sd=3 if z==16 else 4
        center_z=5+hw-j
        hole=cq.Solid.makeCylinder(sd/2,hd/2+.2,cq.Vector(0,0,center_z),cq.Vector(0,1,0))
        s=cq.Compound.makeCompound([solid.cut(hole,tol=1e-6).clean().fix() for solid in s.Solids()])
        assert s.isValid(),(z,'radial screw bore')
        screw_len=2.2 if z==16 else 3.8
        set_screw=thread(sd,screw_len,.5 if sd==3 else .7)
        set_screw=set_screw.cut(hexagon(sd*.5,1.5,screw_len-1.25))
        set_screw=set_screw.rotate((0,0,0),(1,0,0),-90).translate((0,hd/2-screw_len,center_z))
        # The screw already lies inside its nominal radial clearance bore.
        assert s.intersect(set_screw).Volume()<1e-5
        add(folder,filename,title,[('Engrenage_denture_involute',s,color),('Vis_pression_geometrie_estimee',set_screw,STEEL)],
            published,estimated+(['24B: deux volumes BRep axiaux adjacents pour un seul engrenage physique; aucune separation reelle'] if z==24 else [])+['Flancs par splines de developpante (12 points); raccord racine reconstruit non trochoidal',
                                'Pas un fichier natif KHK/Losi ni un profil de fabrication certifie'],
            params={'teeth':z,'module':.5,'pressure_angle':20,'pressure_angle_verified':z!=16,
                    'bore':bore,'pitch_diameter':z*.5,'tip_diameter':(z+2)*.5,'face_width':5,
                    'hub_diameter':hd,'hub_length':hw,'overall_length':5+hw,'set_screw_axis_from_hub_end':j},
            probes=[dict(point=(bore/2-.01,0,2.5),occupied=False),dict(point=(bore/2+.05,0,2.5),occupied=True)],
            source_pages=['KHK-engrenages-acier-SS.pdf p.1' if z!=16 else 'Losi LOS212054 product page'])


def custom_shafts_supports():
    # Explicit study dimensions. Two axial gear planes can be placed without
    # inventing a complete validated chassis. Lengths remain editable parameters.
    middle=thread(5,4,.8).fuse(cyl(2.5,42,4)).fuse(thread(5,4,.8,46)).clean()
    for z,length in [(10,12),(27,16)]:
        middle=middle.cut(box(2.2,2, length,(0,3.0,z)))
    add('arbres-transmission','arbre-a5-v3-intermediaire-etude.step','A5-V3 | arbre intermediaire, etude 50 mm',
        [('Arbre_intermediaire_acier',middle,STEEL)],['Ø5 interfaces roulements et engrenages choisis'],
        ['L50, M5x0.8 aux deux bouts, portees et meplats: choix de conception provisoires',
         'Ne pas fabriquer: ajustements, retenues et empilage doivent etre verifies'],
        params={'length_study':50,'diameter':5,'flat_start_z':[10,27],'flat_depth':.5},design=True,view=(1,-1,.3))
    rear=cyl(2.5,40).fuse(thread(4,10,.7,40)).clean()
    rear=rear.cut(box(2.2,2,12,(0,3,10)))
    rear=rear.cut(cq.Solid.makeCylinder(1,7,cq.Vector(-3.5,0,38.5),cq.Vector(1,0,0)))
    add('arbres-transmission','arbre-a5m4-v3-sortie-etude.step','A5M4-V3 | sortie de roue, etude 50 mm',
        [('Arbre_sortie_acier',rear,STEEL)],['Ø5 aux roulements; famille roue M4 et goupille2'],
        ['L50, reduction M4 a z40, filetage10 et goupillez38.5: choix provisoires',
         'Longueur et position du moyeu dependent du deport reel de la roue; usinage non valide'],
        params={'length_study':50,'bearing_diameter':5,'M4_length':10,'pin_center_z':38.5},design=True,
        view=(1,-1,.3),probes=[dict(point=(0,0,38.5),occupied=False)])
    # Single bearing block with shoulder: outer ring is inserted from z=0,
    # retained axially by a separate cap. Nominal seat without press-fit.
    block=box(23,25,6,(0,1.5,0),1.0)
    block=block.cut(cyl(5.5,4.1,-.1)).cut(cyl(3.1,6.2,-.1))
    for x in (-8.5,8.5):
        block=block.cut(cyl(1.65,6.2,-.1,x,9))
    for x in (-8,8):
        block=block.cut(cyl(1.3,6.2,-.1,x,0))
    cap=ring(7.8,3.1,1.5,-1.5)
    cap=cap.fuse(box(19,6,1.5,(0,0,-1.5),1)).cut(cyl(3.1,1.7,-1.6))
    for x in (-8,8):
        cap=cap.cut(cyl(1.65,1.7,-1.6,x,0))
    add('paliers-transmission','palier-p115-v3-un-appui-etude.step','P115-V3 | appui et capot de retenue',
        [('Corps_palier_aluminium',block.clean(),ALU),('Capot_retenue',cap.clean(),ALU)],
        ['Nominal roulement MR115ZZ OD11, largeur4; passage arbre5'],
        ['Enveloppe23x25x6, trou11 profondeur4, chapeau1.5, fixationM3 nominale: conception provisoire',
         'Un appui modelise: deux appuis par arbre; espacement a definir',
         'Ajustement, vis, rigidite et retenue a valider avant fabrication'],
        params={'body':[23,25,6],'bearing_seat_OD':11,'seat_depth':4,'shaft_clearance':6.2},design=True,
        probes=[dict(point=(0,0,2),occupied=False)])
    # Front two-sided bracket surrounds study A7's pivot z +/-11.
    # Mounting base is behind the barrel, away from X wheel axle.
    fork=box(8,29,5,(0,8,-18),1)
    fork=fork.fuse(box(8,6,32,(0,19,-16),1))
    for z in (-14,11):
        arm=box(8,22,3,(0,8,z),1.3).fuse(cyl(4,3,z))
        arm=arm.cut(cyl(1.55,3.2,z-.1))
        fork=fork.fuse(arm)
    for y in (1,15):
        fork=fork.cut(cyl(1.65,5.2,-18.1,0,y))
    add('paliers-transmission','fourche-f-av-v3-etude.step','F-AV-V3 | fourche de direction, etude',
        [('Fourche_deux_appuis_aluminium',fork.clean(),ALU)],
        ['Principe: A7 et bagues A6 guides par deux appuis'],
        ['Enveloppe, ouverture22, parois et trous: toutes cotes de conception provisoires',
         'A7 reconstruit: alignement, jeu, debattement et mecanique non valides'],
        params={'pivot_gap_study':22,'arm_thickness':3,'pivot_hole':3.1,'backbone_y':19},design=True)


def fasteners():
    folder='fixations-train-roulant'
    pin=cyl(1,10)
    pin=cq.Workplane('XY').newObject([pin]).edges('%Circle').chamfer(.12).val()
    add(folder,'goupille-tamiya-50594-2x10.step','Tamiya 50594 | goupille 2 x 10', [('Goupille',pin,BRIGHT)],
        ['Ø2 x10 mm identifies dans notice TT01R p.15'],['Chanfreins0.12 estimes'],view=(1,-1,.4))
    nut=hexagon(7,4).fuse(cyl(4.5,1)).clean()
    nut=nut.cut(cyl(2,4.2,-.1)).cut(cyl(2.6,1.2,2.9))
    nylon=ring(2.57,2,1.1,2.95)
    add(folder,'ecrou-tamiya-9805557-m4-flasque.step','Tamiya 9805557 | ecrou M4 a flasque',
        [('Ecrou_metal',nut,BRIGHT),('Bague_nylon_estimee',nylon,BLUE)],
        ['Ecrou de roue nylstop a flasque M4, MC4 dans la notice'],
        ['AF7, flasqueOD9, hauteur4 et bague de couleur bleue estimes',
         'Taraudage interieur represente par alesage4, sans tolerances ni helix interne'])
    add(folder,'vis-tamiya-50577-3x10.step','Tamiya 50577 | vis autotaraudeuse 3 x 10',
        [('Vis_autotaraudeuse_estimee',screw(3,10,1.2,5.2,1.5),BRIGHT)],
        ['Diametre3 et longueur10 publies; vis autotaraudeuse et empreinte cruciforme illustrees'],
        ['Pas1.2, diametre tete5.2, filetage et pointe estimes; ne pas confondre avec M3x0.5'],view=(1,-1,.5))
    for ref,l,shoulder in [('9805945',18,10),('50582',14,7)]:
        s=screw(3,l,1.2,5.2,1.5,shoulder=shoulder,shoulder_d=3)
        add(folder,f'vis-tamiya-{ref}-3x{l}.step',f'Tamiya {ref} | vis decollétee 3 x {l}',
            [('Vis_pivot_tete_cruciforme',s,BRIGHT)],
            [f'Diametre3, longueur{l}; type step screw dans notice p.10'],
            [f'Portee lisse{shoulder}, pas partie filetée1.2 et forme tete estimes',
             'Pas, longueurs de portees et vis originale a relever'],view=(1,-1,.5))


def export_model(item, render=True):
    started=time.perf_counter();out=BASE/item['folder']/'3D';out.mkdir(parents=True,exist_ok=True)
    parts=item['parts']
    print('EXPORT',item['folder'],item['filename'],flush=True)
    for name,shape,color in parts:
        assert shape.isValid(),(item['filename'],name,'invalid before export')
        assert shape.Solids(),(item['filename'],name,'not solid')
    original=cq.Compound.makeCompound([s for n,s,c in parts])
    for probe in item['probes']:
        inside=any(s.isInside(cq.Vector(*probe['point']),1e-6) for n,s,c in parts)
        assert inside==probe['occupied'],(item['filename'],probe,inside)
    assembly=cq.Assembly(name=Path(item['filename']).stem)
    for name,s,color in parts:
        assembly.add(s,name=name,color=cq.Color(*color))
    candidate=out/(item['filename']+'.candidate')
    assembly.export(str(candidate),exportType='STEP',mode='default',unit='MM',outputUnit='MM')
    imported=cq.importers.importStep(str(candidate)).val()
    assert imported.isValid() and len(imported.Solids())==len(original.Solids())
    # Adaptive integration is necessary for small helically trimmed surfaces.
    v_before=original.Volume(tol=1e-9);v_after=imported.Volume(tol=1e-9)
    error=abs(v_after-v_before)/v_before
    before=original.BoundingBox();bb=imported.BoundingBox()
    bb_error=max(abs(getattr(bb,k)-getattr(before,k)) for k in ['xmin','xmax','ymin','ymax','zmin','zmax'])
    # Helically trimmed surfaces can integrate differently after conversion
    # to STEP splines. Curved-surface bounding-box extrema also depend on the
    # representation. Require <0.01% volume drift AND <0.01 mm envelope drift.
    assert error<1e-4 and bb_error<.01,(item['filename'],error,bb_error)
    reader=STEPCAFControl_Reader();reader.SetNameMode(True);reader.SetColorMode(True)
    doc=TDocStd_Document(TCollection_ExtendedString('V3 validation'))
    assert reader.ReadFile(str(candidate))==IFSelect_RetDone and reader.Transfer(doc)
    colors=TDF_LabelSequence();XCAFDoc_DocumentTool.ColorTool_s(doc.Main()).GetColors(colors)
    assert colors.Length()>=len(set(c for n,s,c in parts))
    target=out/item['filename'];candidate.replace(target)
    datums={'servo-direction':'Z vertical; corps centre X/Y, fond z=0; sortie x=-5.7; etiquette vers -Y',
            'fusees-avant':'A7: axe roue X, pivot Z, centre de roulements (0,0,0); A6/renvois: pivot Z',
            'biellettes-direction/chapes':'Boule centre (0,0,0), ouverture Z, tige de biellette vers +X',
            'paliers-transmission':'Palier: axe arbre Z, face entree roulement z=0; fourche: axe pivot Z'}
    metadata=dict(file=target.name,title=item['title'],generated_on='2026-10-13',unit='mm',
        cadquery_version=cq.__version__,coordinate_system=datums.get(item['folder'],'Axe principal Z; face de reference z=0; dimensions selon parametres'),
        bytes=target.stat().st_size,sha256=sha(target),native_vendor_cad=False,hardware_measured=False,
        is_custom_project_design=item['design'],published_nominal=item['published'],
        estimates_and_limitations=item['estimated'],parameters=item['params'],source_pages=item['source_pages'],
        bounds_mm={k:getattr(bb,k) for k in ['xmin','xmax','ymin','ymax','zmin','zmax']},
        validation=dict(valid_after_reimport=True,solids=len(imported.Solids()),faces=len(imported.Faces()),
            colors=colors.Length(),volume_relative_error=error,volume_relative_error_limit=1e-4,
            volume_before_mm3=v_before,volume_after_mm3=v_after,
            adaptive_volume_tolerance=1e-9,bbox_error_mm=bb_error,bbox_error_limit_mm=.01,
            void_and_material_probes=item['probes'],elapsed_seconds=time.perf_counter()-started),
        parts=[dict(name=n,color_linear_rgb=c,solids=len(s.Solids())) for n,s,c in parts])
    if render:
        meshes=[]
        for n,s,color in parts:
            # CadQuery's default is relative deflection: long cable faces can
            # look clipped at joins even with a valid, continuous solid. Use
            # absolute 0.01-mm mesh tolerance for all previews.
            BRepTools.Clean_s(s.wrapped)
            BRepMesh_IncrementalMesh(s.wrapped,.01,False,.10,True)
            vertices,triangles=s.tessellate(.01,.10)
            c=np.array(color);c=np.where(c<=.0031308,12.92*c,1.055*np.power(c,1/2.4)-.055)
            meshes.append((np.array([v.toTuple() for v in vertices]),triangles,c))
        p=target.with_suffix('.png')
        render_meshes(p,meshes,item['view'],item['title'],
            'Etude V3 - cotes nominales + details estimes - mm - voir provenance')
        metadata['preview']=dict(file=p.name,sha256=sha(p))
    target.with_suffix('.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return metadata


def write_index(results):
    catalogs={}
    for item,meta in results:
        catalogs.setdefault(item['folder'],[]).append(meta)
    for folder,models in catalogs.items():
        out=BASE/folder/'3D'
        lines=['# Modèles 3D — '+folder,'',
            '**STEP en millimètres, solides nommés et couleurs.** Reconstructions ou conceptions V3 ; aucun fichier natif constructeur ni mesure de matériel.',
            '', '| Modèle | STEP | Aperçu | Taille |', '| --- | --- | --- | --- |']
        for m in models:
            preview=f'[PNG]({m["preview"]["file"]})' if 'preview' in m else '—'
            lines.append(f'| {m["title"]} | [{m["file"]}]({m["file"]}) | {preview} | {m["bytes"]/1e6:.2f} Mo |')
        lines+=['','## Fidélité et limites','',
            'Les fichiers `.json` voisins indiquent, pour chaque modèle, les cotes nominales documentées, les paramètres de conception, les estimations et les contrôles réalisés. Les dimensions inconnues ne deviennent pas des cotes constructeur parce qu’elles sont dessinées.',
            '', 'Les arbres, tiges et supports sont des **modèles paramétriques d’étude**. Les ajustements, longueurs, efforts, débattements et fixations doivent être validés avant fabrication. La denture Losi utilise un angle de 20° supposé ; son appairage KHK reste à confirmer.',
            '', 'Les fils du servo sont continus jusqu’au connecteur ; leur pose est illustrative et leur longueur développée ne reproduit pas le câble livré. Les éléments internes non documentés ne sont pas inventés.',
            '', 'Contrôles : réimport STEP, validité des solides, conservation du nombre de solides, volumes, enveloppes, couleurs et sondes de matière sur les interfaces indiquées. Les résultats FreeCAD sont dans le rapport commun après sa génération.',
            '', '[Provenance et contrôles](provenance.json), [fiche composant](../README.md).','']
        (out/'README.md').write_text('\n'.join(lines),encoding='utf-8')
        manifest=dict(generated_on='2026-10-13',generator='tools/build_running_gear_step.py',
            generator_sha256=sha(Path(__file__)),source_manifest_sha256=sha(COMMON/'notices/assets.json'),models=models)
        (out/'provenance.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        source=BASE/folder/'sources.json'
        if source.exists():
            data=json.loads(source.read_text(encoding='utf-8'));data['model_3d_created']=True
            data['model_3d_manifest']='3D/provenance.json'
            source.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# Modèles 3D de la direction et des transmissions','',
        f'**{len(results)} modèles STEP, dans {len(catalogs)} dossiers de composants.** Les caméra, moteurs, variateurs, Pi 5 et roues existants ne sont pas régénérés.',
        '', 'Les modèles reprennent les dimensions publiées disponibles et complètent les détails visibles par des estimations explicites. Les pièces à fabriquer sont des études paramétriques, pas des plans validés d’usinage.',
        '', '| Dossier | Modèles | Documentation 3D |', '| --- | --- | --- |']
    for folder,models in catalogs.items():
        import os
        link=Path(os.path.relpath(BASE/folder/'3D/README.md',COMMON/'3D')).as_posix()
        lines.append(f'| {folder} | {len(models)} | [STEP, aperçus et provenance]({link}) |')
    lines+=['','[Vue d’ensemble des 29 modèles](apercu-composants.png). Chaque tuile a sa propre échelle ; les tailles relatives ne représentent pas l’implantation.',
            '', '[Contrôle FreeCAD](validation-freecad.json), [catalogue structuré](catalogue.json), [sélection et notices](../README.md).',
            '', 'Génération : `tools/temp/cad-env/Scripts/python.exe tools/build_running_gear_step.py`. Sélection optionnelle `--group gears` ou `--group servo`, etc. Chaque STEP reste de taille modérée et peut être versionné directement dans Git ; aucune règle ne l’ignore.', '']
    out=COMMON/'3D';out.mkdir(parents=True,exist_ok=True)
    (out/'README.md').write_text('\n'.join(lines),encoding='utf-8')
    (out/'catalogue.json').write_text(json.dumps(dict(generated_on='2026-10-13',model_count=len(results),folder_count=len(catalogs),
        models=[dict(folder=i['folder'],**m) for i,m in results]),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if all('preview' in m for i,m in results):
        columns=4;tw,th=480,414;rows=math.ceil(len(results)/columns)
        gallery=Image.new('RGB',(columns*tw,rows*th+70),'white');draw=ImageDraw.Draw(gallery)
        font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
        heading=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',25)
        draw.text((20,18),'V3 | 29 composants et accessoires - reconstructions et etudes',font=heading,fill='#25313b')
        for index,(item,m) in enumerate(results):
            x=(index%columns)*tw;y=(index//columns)*th+70
            p=BASE/item['folder']/'3D'/m['preview']['file']
            im=Image.open(p).convert('RGB');im.thumbnail((tw-10,th-34))
            gallery.paste(im,(x+(tw-im.width)//2,y))
            draw.text((x+10,y+th-27),f'{index+1:02d}. '+Path(m['file']).stem[:43],font=font,fill='#25313b')
        gallery.save(out/'apercu-composants.png')


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    parser=argparse.ArgumentParser();parser.add_argument('--group',default='all');parser.add_argument('--no-render',action='store_true')
    parser.add_argument('--refresh-index',action='store_true',help='Rebuild indexes from existing per-model metadata without rebuilding CAD')
    args=parser.parse_args()
    if args.refresh_index:
        catalog=json.loads((COMMON/'3D/catalogue.json').read_text(encoding='utf-8'))
        results=[]
        for item in catalog['models']:
            out=BASE/item['folder']/'3D'
            meta=json.loads((out/Path(item['file']).with_suffix('.json')).read_text(encoding='utf-8'))
            assert sha(out/meta['file'])==meta['sha256']
            results.append((dict(folder=item['folder']),meta))
        write_index(results);print('INDEX',len(results),'models',flush=True);return
    groups=dict(servo=servo,links=ball_link,bearing=bearing,axle=axle_front,hub=hub,uprights=uprights,
                gears=gears,custom=custom_shafts_supports,fasteners=fasteners)
    for key,build in groups.items():
        if args.group in ('all',key):
            print('BUILD',key,flush=True);build()
    assert MODELS,'Unknown group'
    results=[]
    for item in MODELS:
        meta=export_model(item,not args.no_render);results.append((item,meta))
    if args.group=='all':
        write_index(results)
    print('DONE',len(results),'STEP files',flush=True)


if __name__=='__main__':
    main()
