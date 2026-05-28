from django.db import models

from django.db import models

class Paciente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=255) # Para guardar la clave encriptada

    def __str__(self):
        return f"{self.apellido}, {self.nombre} (DNI: {self.dni})"


class Profesional(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    matricula = models.CharField(max_length=50, unique=True)
    especialidad = models.CharField(max_length=100)
    contraseña = models.CharField(max_length=255) # Para guardar la clave encriptada

    def __str__(self):
        return f"Dr/a. {self.apellido}, {self.nombre} - M.P.: {self.matricula} ({self.especialidad})"
