

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

    path('solicitar-turno/', views.solicitar_turno, name='solicitar_turno'),

    path('lista-turnos-profesional/', views.lista_turnos_profesional, name='lista_turnos_profesional'),

    path('cambiar-estado-turno/<int:turno_id>/', views.cambiar_estado_turno, name='cambiar_estado_turno'),

    path('cerrar-sesion/', views.cerrar_sesion, name='cerrar_sesion'),

    path('editar-paciente/', views.editar_paciente, name='editar_paciente'),

    path('editar-profesional/', views.editar_profesional, name='editar_profesional'),

    path('baja-paciente/', views.baja_paciente, name='baja_paciente'),
    
    path('baja-profesional/', views.baja_profesional, name='baja_profesional'),
    
]