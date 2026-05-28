

from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.inicio, name='inicio'),

    path('elegir-portal/', views.elegir_portal, name='elegir_portal'),

    path('ingreso-paciente/', views.ingreso_paciente, name='ingreso_paciente'),

    path('ingreso-profesional/', views.ingreso_profesional, name='ingreso_profesional'),
    
    path('lista/', views.lista_turnos, name='lista_turnos'),

    path('registro-profesional/', views.registro_profesional, name='registro_profesional'),

    path('registro-paciente/', views.registro_paciente, name='registro_paciente'),
]