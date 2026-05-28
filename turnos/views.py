
from django.shortcuts import render
from .models import Turno

def lista_turnos(request):
    todos_los_turnos = Turno.objects.all()  # Trae todos los turnos de la base de datos
    return render(request, 'turnos/lista_turnos.html', {'turnos': todos_los_turnos}) # Se los mandamos al HTML adentro de una bandeja llamada 'contexto'


def inicio(request):
    return render(request, 'turnos/inicio.html')


def elegir_portal(request):
    return render(request, 'turnos/eleccion_portal.html')


def ingreso_paciente(request):
    return render(request, 'turnos/ingreso_paciente.html')

def ingreso_profesional(request):
    return render(request, 'turnos/ingreso_profesional.html')

def registro_profesional(request):
    return render(request, 'turnos/registro_profesional.html')

def registro_paciente(request):
    return render(request, 'turnos/registro_paciente.html')