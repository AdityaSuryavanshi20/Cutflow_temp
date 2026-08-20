from django.db import migrations

# ---------------------------------------------------------------------------
# This migration collapses the Series (Brand) dropdown on the Add-Item
# wizard down to exactly 3 options:
#
#   1. "CutFlow Standard" -- ONLY the 2 Track (SY02) & 3 Track (SY03)
#      sliding systems, with their topologies.
#   2. "Generic"           -- every other existing System (SY01 casement,
#      SY04-SY08, AL01/UP01, or any other stray System) gets bucketed here.
#   3. "Jindal-Domal"       -- a brand-new 2 Track / 3 Track sliding series
#      (JD01 / JD02), fully wired with profiles, cut formulas, hardware
#      and topologies so bar optimization works out of the box. Panel
#      configurations are modelled on generic industry-standard 2T2P /
#      3T3P sliding assemblies (topology names/shapes only -- no
#      proprietary die numbers or dimensions are reproduced).
#
# Any other Brand row that happens to exist (e.g. leftover empty
# placeholder brands such as Rehau/VEKA/Schuco/Aluplast/Fenesta from an
# older seed command) is simply deactivated so it disappears from the
# Series dropdown -- nothing is deleted, so existing FKs stay intact.
# ---------------------------------------------------------------------------

CUTFLOW_BRAND_NAME = 'CutFlow Standard'
GENERIC_BRAND_NAME = 'Generic'
JINDAL_BRAND_NAME = 'Jindal-Domal'

# Systems that must stay on "CutFlow Standard"; everything else that
# already exists gets moved onto "Generic".
CUTFLOW_KEEP_CODES = ['SY02', 'SY03']

# New Jindal-Domal systems created by this migration.
JD_2T_CODE = 'JD01'
JD_3T_CODE = 'JD02'

JD_PROFILES_DATA = [
    # (stock_no, name, category, bar_len, wt, cost, offset_l, offset_r, offset_t, offset_b)
    ('JD-OF2T', 'Jindal-Domal 2 Track Outer Frame', 'slider_frame', 6000, 1.18, 318, 0, 0, 0, 0),
    ('JD-OF3T', 'Jindal-Domal 3 Track Outer Frame', 'slider_frame', 6000, 1.48, 372, 0, 0, 0, 0),
    ('JD-SS', 'Jindal-Domal Slider Sash', 'slider_sash', 6000, 0.98, 262, 3, 3, 3, 3),
    ('JD-INTL', 'Jindal-Domal Interlock Profile', 'mullion', 6000, 0.90, 232, 0, 0, 0, 0),
    ('JD-MULL', 'Jindal-Domal Mullion', 'mullion', 6000, 0.90, 232, 0, 0, 0, 0),
    ('JD-TRK', 'Jindal-Domal Sliding Track', 'slider_frame', 6000, 1.35, 340, 0, 0, 0, 0),
    ('JD-GB', 'Jindal-Domal Glass Bead 17mm', 'bead', 6000, 0.145, 39, 0, 0, 0, 0),
]

JD_HARDWARE_DATA = [
    # (stock_no, name, category, unit, cost, wt)
    ('JD-ROLLER', 'Jindal-Domal Slider Roller', 'roller', 'pcs', 160, 0.05),
    ('JD-HANDLE', 'Jindal-Domal Single Point Handle', 'handle', 'pcs', 115, 0.60),
    ('JD-LOCK', 'Jindal-Domal Multipoint Espag Lock', 'lock', 'pcs', 285, 0.55),
    ('JD-CORNER-F', 'Jindal-Domal Frame Corner Connector', 'accessory', 'pcs', 18, 0.04),
    ('JD-CORNER-S', 'Jindal-Domal Sash Corner Connector', 'accessory', 'pcs', 15, 0.03),
    ('JD-NIB', 'Jindal-Domal Nib / Lock Keeper', 'accessory', 'pcs', 8, 0.02),
    ('JD-COUNTERPLATE', 'Jindal-Domal Counterplate', 'accessory', 'pcs', 22, 0.03),
    ('JD-SCREW', 'Jindal-Domal Fixing Screw', 'screw', 'pcs', 1, 0.0),
    ('JD-GASKET-SL', 'Jindal-Domal Sliding Gasket', 'gasket', 'm', 26, 0.01),
]

# Topology sets for the two new Jindal-Domal systems.
# (code, name, shape, panel_layout, description, sort_order)
JD_TOPOLOGIES = {
    JD_2T_CODE: [
        ('2S', '2 Sliding', 'rectangle', ['sliding', 'sliding'],
         'Two sliding sashes on a 2-track frame.', 0),
        ('1F1S', '1 Fixed + 1 Sliding', 'rectangle', ['fixed', 'sliding'],
         'Fixed light on one track, sliding sash on the other.', 1),
        ('1S1F', '1 Sliding + 1 Fixed', 'rectangle', ['sliding', 'fixed'],
         'Sliding sash on one track, fixed light on the other.', 2),
        ('2S_ARCH', '2 Sliding – Semicircle Top', 'semi_circle_top', ['sliding', 'sliding'],
         'Two sliding sashes with a fixed semicircular light above.', 3),
    ],
    JD_3T_CODE: [
        ('3S', '3 Sliding', 'rectangle', ['sliding', 'sliding', 'sliding'],
         'Three sliding sashes on a 3-track frame.', 0),
        ('2S1F', '2 Sliding + 1 Fixed', 'rectangle', ['sliding', 'sliding', 'fixed'],
         'Two sliding sashes and one fixed light.', 1),
        ('1F2S', '1 Fixed + 2 Sliding', 'rectangle', ['fixed', 'sliding', 'sliding'],
         'One fixed light and two sliding sashes.', 2),
        ('2S1M', '2 Sliding + 1 Mosquito Mesh', 'rectangle', ['sliding', 'sliding', 'mesh'],
         'Two sliding sashes with an additional mosquito mesh track.', 3),
        ('1S1F1M', '1 Sliding + 1 Fixed + 1 Mosquito Mesh', 'rectangle',
         ['sliding', 'fixed', 'mesh'],
         'One sliding sash, one fixed light, plus a mosquito mesh track.', 4),
        ('3S_ARCH', '3 Sliding – Semicircle Top', 'semi_circle_top',
         ['sliding', 'sliding', 'sliding'],
         'Three sliding sashes with a fixed semicircular light above.', 5),
    ],
}

# New mosquito-mesh topology variants added to the existing CutFlow
# Standard 3-Track system (SY03), inspired by the mosquito shutter
# design options shown in the reference 26mm sliding window manual.
SY03_EXTRA_TOPOLOGIES = [
    ('2S1M', '2 Sliding + 1 Mosquito Mesh', 'rectangle', ['sliding', 'sliding', 'mesh'],
     'Two sliding sashes with an additional mosquito mesh track.', 4),
    ('1S1F1M', '1 Sliding + 1 Fixed + 1 Mosquito Mesh', 'rectangle',
     ['sliding', 'fixed', 'mesh'],
     'One sliding sash, one fixed light, plus a mosquito mesh track.', 5),
]


def reorganize_series(apps, schema_editor):
    Brand = apps.get_model('catalog', 'Brand')
    System = apps.get_model('catalog', 'System')
    Profile = apps.get_model('catalog', 'Profile')
    SystemProfile = apps.get_model('catalog', 'SystemProfile')
    ProfileFormula = apps.get_model('catalog', 'ProfileFormula')
    Hardware = apps.get_model('catalog', 'Hardware')
    SystemHardwareRule = apps.get_model('catalog', 'SystemHardwareRule')
    Topology = apps.get_model('catalog', 'Topology')

    # ------------------------------------------------------------------
    # 1. Ensure the 3 target brands exist & are active.
    # ------------------------------------------------------------------
    cutflow_brand, _ = Brand.objects.get_or_create(
        name=CUTFLOW_BRAND_NAME,
        defaults={'description': 'CutFlow in-house standard series (2 & 3 Track sliding only).',
                  'is_active': True})
    if not cutflow_brand.is_active:
        cutflow_brand.is_active = True
        cutflow_brand.save(update_fields=['is_active'])

    generic_brand, _ = Brand.objects.get_or_create(
        name=GENERIC_BRAND_NAME,
        defaults={'description': 'Catch-all for every other system not part of a named series.',
                  'is_active': True})
    if not generic_brand.is_active:
        generic_brand.is_active = True
        generic_brand.save(update_fields=['is_active'])

    jindal_brand, _ = Brand.objects.get_or_create(
        name=JINDAL_BRAND_NAME,
        defaults={'description': 'Jindal-Domal style 2 Track / 3 Track sliding series.',
                  'is_active': True})
    if not jindal_brand.is_active:
        jindal_brand.is_active = True
        jindal_brand.save(update_fields=['is_active'])

    # ------------------------------------------------------------------
    # 2. Reassign every existing System: SY02/SY03 stay on CutFlow
    #    Standard, everything else moves to Generic.
    # ------------------------------------------------------------------
    System.objects.filter(code__in=CUTFLOW_KEEP_CODES).update(brand=cutflow_brand)
    System.objects.exclude(code__in=CUTFLOW_KEEP_CODES + [JD_2T_CODE, JD_3T_CODE]).update(
        brand=generic_brand)

    # ------------------------------------------------------------------
    # 3. Deactivate any other stray Brand rows (old placeholder brands
    #    such as Rehau/VEKA/Schuco/Aluplast/Fenesta, or anything else
    #    created by hand in admin) so they no longer show up as Series
    #    options -- without deleting them / breaking FKs.
    # ------------------------------------------------------------------
    Brand.objects.exclude(
        name__in=[CUTFLOW_BRAND_NAME, GENERIC_BRAND_NAME, JINDAL_BRAND_NAME]
    ).update(is_active=False)

    # ------------------------------------------------------------------
    # 4. Create the Jindal-Domal systems.
    # ------------------------------------------------------------------
    jd_2t, _ = System.objects.get_or_create(
        code=JD_2T_CODE,
        defaults={'name': 'Jindal-Domal 2 Track Sliding System', 'category': 'sliding',
                  'material': 'aluminium', 'brand': jindal_brand, 'is_active': True}
    )
    if jd_2t.brand_id != jindal_brand.id:
        jd_2t.brand = jindal_brand
        jd_2t.save(update_fields=['brand'])

    jd_3t, _ = System.objects.get_or_create(
        code=JD_3T_CODE,
        defaults={'name': 'Jindal-Domal 3 Track Sliding System', 'category': 'sliding',
                  'material': 'aluminium', 'brand': jindal_brand, 'is_active': True}
    )
    if jd_3t.brand_id != jindal_brand.id:
        jd_3t.brand = jindal_brand
        jd_3t.save(update_fields=['brand'])

    jd_systems = {JD_2T_CODE: jd_2t, JD_3T_CODE: jd_3t}

    # ------------------------------------------------------------------
    # 5. Profiles used by the Jindal-Domal systems.
    # ------------------------------------------------------------------
    jd_profiles = {}
    for stock_no, name, category, bar_len, wt, cost, ol, orr, ot, ob in JD_PROFILES_DATA:
        profile, _ = Profile.objects.get_or_create(
            stock_no=stock_no,
            defaults={
                'name': name,
                'category': category,
                'brand': jindal_brand,
                'standard_bar_length': bar_len,
                'weight_per_meter': wt,
                'cost_per_meter': cost,
                'offset_left': ol,
                'offset_right': orr,
                'offset_top': ot,
                'offset_bottom': ob,
                'default_left_angle': 90,
                'default_right_angle': 90,
                'is_active': True,
            }
        )
        jd_profiles[stock_no] = profile

    # (system_code, profile_code, role, sort_order)
    jd_profile_link_data = [
        (JD_2T_CODE, 'JD-OF2T', 'outer_frame_top', 10),
        (JD_2T_CODE, 'JD-OF2T', 'outer_frame_bottom', 20),
        (JD_2T_CODE, 'JD-OF2T', 'outer_frame_left', 30),
        (JD_2T_CODE, 'JD-OF2T', 'outer_frame_right', 40),
        (JD_2T_CODE, 'JD-SS', 'shutter_vertical', 50),
        (JD_2T_CODE, 'JD-SS', 'shutter_horizontal', 60),
        (JD_2T_CODE, 'JD-INTL', 'interlock', 70),
        (JD_2T_CODE, 'JD-MULL', 'mullion', 80),
        (JD_2T_CODE, 'JD-GB', 'bead_horizontal', 90),
        (JD_2T_CODE, 'JD-GB', 'bead_vertical', 100),
        (JD_2T_CODE, 'JD-TRK', 'track', 110),
        (JD_3T_CODE, 'JD-OF3T', 'outer_frame_top', 10),
        (JD_3T_CODE, 'JD-OF3T', 'outer_frame_bottom', 20),
        (JD_3T_CODE, 'JD-OF3T', 'outer_frame_left', 30),
        (JD_3T_CODE, 'JD-OF3T', 'outer_frame_right', 40),
        (JD_3T_CODE, 'JD-SS', 'shutter_vertical', 50),
        (JD_3T_CODE, 'JD-SS', 'shutter_horizontal', 60),
        (JD_3T_CODE, 'JD-INTL', 'interlock', 70),
        (JD_3T_CODE, 'JD-MULL', 'mullion', 80),
        (JD_3T_CODE, 'JD-GB', 'bead_horizontal', 90),
        (JD_3T_CODE, 'JD-GB', 'bead_vertical', 100),
        (JD_3T_CODE, 'JD-TRK', 'track', 110),
    ]
    for system_code, profile_code, role, sort_order in jd_profile_link_data:
        system = jd_systems[system_code]
        profile = jd_profiles[profile_code]
        SystemProfile.objects.get_or_create(
            system=system,
            profile=profile,
            role=role,
            defaults={'sort_order': sort_order, 'is_required': True, 'is_active': True}
        )

    # (system_code, profile_code, position, formula, qty_formula, la, ra)
    jd_formulas_data = []
    for system_code, of_code in [(JD_2T_CODE, 'JD-OF2T'), (JD_3T_CODE, 'JD-OF3T')]:
        jd_formulas_data += [
            (system_code, of_code, 'outer_top', 'W', '1', 90, 90),
            (system_code, of_code, 'outer_bottom', 'W', '1', 90, 90),
            (system_code, of_code, 'outer_left', 'H', '1', 90, 90),
            (system_code, of_code, 'outer_right', 'H', '1', 90, 90),
            (system_code, 'JD-SS', 'sash_width', 'round((W / n_panels) - 35, 2)', 'n_panels', 90, 90),
            (system_code, 'JD-SS', 'sash_height', 'H - offset_t - offset_b', '2 * n_panels', 90, 90),
            (system_code, 'JD-INTL', 'interlock_length', 'H - offset_t - offset_b', 'n_panels - 1', 90, 90),
            (system_code, 'JD-MULL', 'mullion_length', 'H - offset_t - offset_b', 'n_panels - 1', 90, 90),
            (system_code, 'JD-GB', 'bead_horizontal', 'W - 20', '2 * n_panels', 90, 90),
            (system_code, 'JD-GB', 'bead_vertical', 'H - 20', '2 * n_panels', 90, 90),
            (system_code, 'JD-TRK', 'track_length', 'W', '1', 90, 90),
        ]

    for system_code, profile_code, position, formula, qty_formula, la, ra in jd_formulas_data:
        system = jd_systems[system_code]
        profile = jd_profiles[profile_code]
        system_profile = SystemProfile.objects.filter(system=system, profile=profile).first()
        ProfileFormula.objects.get_or_create(
            profile=profile,
            system=system,
            position=position,
            defaults={
                'system_profile': system_profile,
                'formula': formula,
                'quantity_formula': qty_formula,
                'cut_angle_left': la,
                'cut_angle_right': ra,
                'is_active': True,
            }
        )

    # ------------------------------------------------------------------
    # 6. Hardware used by the Jindal-Domal systems.
    # ------------------------------------------------------------------
    jd_hardware = {}
    for stock_no, name, category, unit, cost, wt in JD_HARDWARE_DATA:
        item, _ = Hardware.objects.get_or_create(
            stock_no=stock_no,
            defaults={
                'name': name,
                'category': category,
                'unit': unit,
                'unit_cost': cost,
                'weight_per_unit': wt,
                'brand': jindal_brand,
                'is_active': True,
            }
        )
        jd_hardware[stock_no] = item

    jd_hardware_rule_data = []
    for system_code in [JD_2T_CODE, JD_3T_CODE]:
        jd_hardware_rule_data += [
            (system_code, 'JD-ROLLER', 'n_panels * 2', 'Rollers for sliding sash'),
            (system_code, 'JD-HANDLE', 'n_panels', 'Slider handle'),
            (system_code, 'JD-LOCK', '1', 'Multipoint espag lock per unit'),
            (system_code, 'JD-CORNER-F', '4', 'Frame corner connectors'),
            (system_code, 'JD-CORNER-S', 'n_panels * 4', 'Sash corner connectors'),
            (system_code, 'JD-NIB', 'n_panels', 'Nib / lock keeper'),
            (system_code, 'JD-COUNTERPLATE', '1', 'Counterplate for lock'),
            (system_code, 'JD-SCREW', '10 * n_panels', 'Fixing screws'),
            (system_code, 'JD-GASKET-SL', 'n_panels * 4', 'Sliding gasket'),
        ]
    for system_code, hw_code, qty_formula, notes in jd_hardware_rule_data:
        system = jd_systems[system_code]
        item = jd_hardware[hw_code]
        SystemHardwareRule.objects.get_or_create(
            system=system,
            hardware=item,
            defaults={'quantity_formula': qty_formula, 'notes': notes, 'is_active': True}
        )

    # ------------------------------------------------------------------
    # 7. Topologies for the Jindal-Domal systems.
    # ------------------------------------------------------------------
    for system_code, topologies in JD_TOPOLOGIES.items():
        system = jd_systems[system_code]
        for code, name, shape, panel_layout, description, sort_order in topologies:
            Topology.objects.get_or_create(
                system=system,
                code=code,
                defaults={
                    'name': name,
                    'shape': shape,
                    'panel_layout': panel_layout,
                    'description': description,
                    'sort_order': sort_order,
                    'is_active': True,
                },
            )

    # ------------------------------------------------------------------
    # 8. Extra mosquito-mesh topology options for CutFlow Standard's
    #    3-Track system (SY03), inspired by the reference manual.
    # ------------------------------------------------------------------
    try:
        sy03 = System.objects.get(code='SY03')
    except System.DoesNotExist:
        sy03 = None
    if sy03 is not None:
        for code, name, shape, panel_layout, description, sort_order in SY03_EXTRA_TOPOLOGIES:
            Topology.objects.get_or_create(
                system=sy03,
                code=code,
                defaults={
                    'name': name,
                    'shape': shape,
                    'panel_layout': panel_layout,
                    'description': description,
                    'sort_order': sort_order,
                    'is_active': True,
                },
            )


def unreorganize_series(apps, schema_editor):
    """
    Best-effort reverse: reactivate any Brand we deactivated and remove the
    Jindal-Domal systems/topologies this migration created. System->brand
    reassignments for pre-existing systems are intentionally left as-is
    since there's no reliable way to know their prior brand.
    """
    Brand = apps.get_model('catalog', 'Brand')
    System = apps.get_model('catalog', 'System')

    Brand.objects.exclude(
        name__in=[CUTFLOW_BRAND_NAME, GENERIC_BRAND_NAME, JINDAL_BRAND_NAME]
    ).update(is_active=True)

    System.objects.filter(code__in=[JD_2T_CODE, JD_3T_CODE]).delete()
    Brand.objects.filter(name=JINDAL_BRAND_NAME).delete()

    try:
        sy03 = System.objects.get(code='SY03')
        sy03.topologies.filter(code__in=[c for c, *_ in SY03_EXTRA_TOPOLOGIES]).delete()
    except System.DoesNotExist:
        pass


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0010_seed_topologies'),
    ]

    operations = [
        migrations.RunPython(reorganize_series, unreorganize_series),
    ]
