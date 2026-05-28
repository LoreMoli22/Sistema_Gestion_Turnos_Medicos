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


class Turno(models.Model):
    ESTADOS_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADO', 'Confirmado'),
        ('CANCELADO', 'Cancelado'),
    ]

    # Conexiones con los otros modelos
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE) # models.ForeignKey, conecta el turno directamente con un registro de paciente y de profesional
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE) # on_delete=models.CASCADE, significa que si se borra un paciente del sistema, se van a borrar automáticamente todos sus turnos asociados.
    
    # Datos propios del turno
    fecha = models.DateField()
    hora = models.TimeField()
    motivo = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS_CHOICES, default='PENDIENTE')

    def __str__(self):
        return f"Turno: {self.fecha} {self.hora} - Paciente: {self.paciente.apellido} | Médico: {self.profesional.apellido}"