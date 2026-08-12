from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import System, Profile, Glass, Hardware, Topology

@login_required
def system_list(request):
    return render(request, 'catalog/system_list.html', {
        'systems': System.objects.filter(is_active=True).select_related('brand')
    })

@login_required
def profile_list(request):
    return render(request, 'catalog/profile_list.html', {
        'profiles': Profile.objects.filter(is_active=True).select_related('brand')
    })

@login_required
def glass_list(request):
    return render(request, 'catalog/glass_list.html', {
        'glasses': Glass.objects.filter(is_active=True)
    })

@login_required
def hardware_list(request):
    return render(request, 'catalog/hardware_list.html', {
        'hardware': Hardware.objects.filter(is_active=True).select_related('brand')
    })


@login_required
def api_systems_by_series(request):
    """
    Step-1 of the New Item wizard: return active Systems for the selected
    Series (Brand). If no brand is given, returns every active system so the
    wizard still works for systems that aren't tied to a specific brand.
    """
    brand_id = request.GET.get('brand')
    qs = System.objects.filter(is_active=True).select_related('brand')
    if brand_id and str(brand_id).isdigit():
        qs = qs.filter(brand_id=brand_id)
    data = [{
        'id': s.pk,
        'code': s.code,
        'name': s.name,
        'category': s.category,
        'category_label': s.get_category_display(),
        'material': s.material,
        'material_label': s.get_material_display(),
    } for s in qs]
    return JsonResponse({'systems': data})


@login_required
def api_topologies_by_system(request):
    """
    Step-2 of the New Item wizard: return the panel-configuration options
    (Topologies) available for the selected System, so the UI can render a
    clickable preview grid before the user fills in dimensions.
    """
    system_id = request.GET.get('system')
    if not system_id or not str(system_id).isdigit():
        return JsonResponse({'topologies': []})
    qs = Topology.objects.filter(system_id=system_id, is_active=True)
    data = [{
        'id': t.pk,
        'code': t.code,
        'name': t.name,
        'shape': t.shape,
        'panel_layout': t.panel_layout,
        'n_panels': t.n_panels,
        'description': t.description,
    } for t in qs]
    return JsonResponse({'topologies': data})
