from django.urls import path
from . import views
urlpatterns = [
    path('systems/', views.system_list, name='system_list'),
    path('profiles/', views.profile_list, name='profile_list'),
    path('glass/', views.glass_list, name='glass_list'),
    path('hardware/', views.hardware_list, name='hardware_list'),
    path('api/systems/', views.api_systems_by_series, name='api_systems_by_series'),
    path('api/topologies/', views.api_topologies_by_system, name='api_topologies_by_system'),
]
