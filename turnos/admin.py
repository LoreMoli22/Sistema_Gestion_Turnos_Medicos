from django.contrib import admin

from django.contrib import admin
from .models import Paciente, Profesional

###### Registramos los modelos para que aparezcan en el panel de administración
admin.site.register(Paciente)
admin.site.register(Profesional)
