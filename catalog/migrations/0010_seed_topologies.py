from django.db import migrations


# Default topology set per system code. Each tuple is:
# (code, name, shape, panel_layout, description, sort_order)
TOPOLOGIES_BY_SYSTEM_CODE = {
    'SY01': [  # Hinge Int Glz System (casement)
        ('1O', '1 Openable', 'rectangle', ['openable_l'],
         'Single openable shutter.', 0),
        ('2O', '2 Openable', 'rectangle', ['openable_l', 'openable_r'],
         'Two openable shutters meeting at a mullion.', 1),
        ('1F1O', '1 Fixed + 1 Openable', 'rectangle', ['fixed', 'openable_r'],
         'Fixed light beside a single openable shutter.', 2),
        ('3O', '3 Openable', 'rectangle', ['openable_l', 'openable_r', 'openable_l'],
         'Three openable shutters across a wide opening.', 3),
    ],
    'SY02': [  # Sliding 2-Track System
        ('2S', '2 Sliding', 'rectangle', ['sliding', 'sliding'],
         'Two sliding sashes on a 2-track frame.', 0),
        ('1F1S', '1 Fixed + 1 Sliding', 'rectangle', ['fixed', 'sliding'],
         'Fixed light on one track, sliding sash on the other.', 1),
        ('1S1F', '1 Sliding + 1 Fixed', 'rectangle', ['sliding', 'fixed'],
         'Sliding sash on one track, fixed light on the other.', 2),
        ('2S_ARCH', '2 Sliding – Semicircle Top', 'semi_circle_top', ['sliding', 'sliding'],
         'Two sliding sashes with a fixed semicircular light above.', 3),
    ],
    'SY03': [  # Sliding 3-Track System
        ('3S', '3 Sliding', 'rectangle', ['sliding', 'sliding', 'sliding'],
         'Three sliding sashes on a 3-track frame.', 0),
        ('2S1F', '2 Sliding + 1 Fixed', 'rectangle', ['sliding', 'sliding', 'fixed'],
         'Two sliding sashes and one fixed light.', 1),
        ('1F2S', '1 Fixed + 2 Sliding', 'rectangle', ['fixed', 'sliding', 'sliding'],
         'One fixed light and two sliding sashes.', 2),
        ('3S_ARCH', '3 Sliding – Semicircle Top', 'semi_circle_top',
         ['sliding', 'sliding', 'sliding'],
         'Three sliding sashes with a fixed semicircular light above.', 3),
    ],
    'SY04': [  # Fixed Frame System
        ('1F', 'Single Fixed Light', 'rectangle', ['fixed'],
         'One fixed pane, no opening sash.', 0),
        ('2F', '2 Fixed Lights', 'rectangle', ['fixed', 'fixed'],
         'Two fixed panes divided by a mullion.', 1),
        ('1F_ARCH', 'Fixed – Arched Top', 'arch_top', ['fixed'],
         'Single fixed light with an arched head.', 2),
    ],
    'SY05': [  # Tilt & Turn System
        ('1TT', '1 Tilt & Turn', 'rectangle', ['openable_l'],
         'Single tilt-and-turn sash.', 0),
        ('2TT', '2 Tilt & Turn', 'rectangle', ['openable_l', 'openable_r'],
         'Two tilt-and-turn sashes.', 1),
        ('1F1TT', '1 Fixed + 1 Tilt & Turn', 'rectangle', ['fixed', 'openable_r'],
         'Fixed light beside a tilt-and-turn sash.', 2),
    ],
    'SY06': [  # Super System Door (swing door)
        ('1D', 'Single Door', 'rectangle', ['openable_r'],
         'Single swing door leaf.', 0),
        ('2D', 'Double Door', 'rectangle', ['openable_l', 'openable_r'],
         'Two swing door leaves meeting at the centre.', 1),
        ('1D1F', '1 Door + 1 Fixed Side Light', 'rectangle', ['openable_r', 'fixed'],
         'Swing door with a fixed side light.', 2),
    ],
    'SY07': [  # Sliding Door System
        ('2SD', '2 Panel Sliding Door', 'rectangle', ['sliding', 'sliding'],
         'Two-panel sliding door.', 0),
        ('3SD', '3 Panel Sliding Door', 'rectangle', ['sliding', 'sliding', 'sliding'],
         'Three-panel sliding door.', 1),
        ('1F1SD', '1 Fixed + 1 Sliding Door', 'rectangle', ['fixed', 'sliding'],
         'Fixed panel beside a single sliding door panel.', 2),
    ],
    'SY08': [  # Louvre System
        ('STD', 'Standard Louvre', 'rectangle', ['louver'],
         'Single-bank adjustable louvre.', 0),
        ('2L', '2 Bank Louvre', 'rectangle', ['louver', 'louver'],
         'Two adjustable louvre banks side by side.', 1),
    ],
}


def seed_topologies(apps, schema_editor):
    System = apps.get_model('catalog', 'System')
    Topology = apps.get_model('catalog', 'Topology')

    for system_code, topologies in TOPOLOGIES_BY_SYSTEM_CODE.items():
        try:
            system = System.objects.get(code=system_code)
        except System.DoesNotExist:
            continue
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


def unseed_topologies(apps, schema_editor):
    System = apps.get_model('catalog', 'System')
    Topology = apps.get_model('catalog', 'Topology')
    codes = list(TOPOLOGIES_BY_SYSTEM_CODE.keys())
    Topology.objects.filter(system__code__in=codes).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_topology'),
    ]

    operations = [
        migrations.RunPython(seed_topologies, unseed_topologies),
    ]
