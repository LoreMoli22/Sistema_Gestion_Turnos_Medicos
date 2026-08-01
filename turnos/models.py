from django.db import models
from django.contrib.auth.hashers import make_password, identify_hasher
from django.core.exceptions import ValidationError




class Paciente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=255) # Para guardar la clave encriptada

    def clean(self):
        super().clean()
        if any (char.isdigit() for char in self.nombre):
           raise ValidationError({'nombre': 'El nombre no puede contener números.'})
        if any(char.isdigit() for char in self.apellido):
            raise ValidationError({'apellido': 'El apellido no puede contener números.'}) 
        if not self.dni.isdigit():
            raise ValidationError({'dni': 'El DNI debe contener únicamente números.'})


    def save(self, *args, **kwargs):
        self.full_clean()
        # Si la contraseña NO está encriptada todavía, la encriptamos antes de guardar
        try:
            identify_hasher(self.contrasena)
        except ValueError:
            self.contrasena = make_password(self.contrasena)
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.apellido}, {self.nombre} (DNI: {self.dni})"


class Profesional(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    matricula = models.CharField(max_length=50, unique=True)
    especialidad = models.CharField(max_length=100)
    email = models.EmailField(unique=True, null=True, blank=True)
    contrasena = models.CharField(max_length=255) # Para guardar la clave encriptada

    def clean(self):
        super().clean()
        if any(char.isdigit() for char in self.nombre):
            raise ValidationError({'nombre': 'El nombre no puede contener números.'})
        if any(char.isdigit() for char in self.apellido):
            raise ValidationError({'apellido': 'El apellido no puede contener números.'})
        if not self.matricula.isdigit():
            raise ValidationError({'matricula': 'La matrícula debe contener únicamente números (sin puntos ni guiones).'})


    def __str__(self):
        return f"Dr/a. {self.apellido}, {self.nombre} - M.P.: {self.matricula} ({self.especialidad})"


    def save(self, *args, **kwargs):
        self.full_clean()
        # Si la contraseña NO está encriptada todavía, la encriptamos antes de guardar
        try:
            identify_hasher(self.contrasena)
        except ValueError:
            self.contrasena = make_password(self.contrasena)
            
        super().save(*args, **kwargs)

class Turno(models.Model):
    ESTADOS_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADO', 'Confirmado'),
        ('CANCELADO', 'Cancelado'),
        ('REALIZADO', 'Realizado'),
    ]

    # Conexiones con los otros modelos
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE) # models.ForeignKey, conecta el turno directamente con un registro de paciente y de profesional
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE) # on_delete=models.CASCADE, significa que si se borra un paciente del sistema, se van a borrar automáticamente todos sus turnos asociados.
    
    # Datos propios del turno
    fecha = models.DateField()
    hora = models.TimeField()
    motivo = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS_CHOICES, default='PENDIENTE')

    class Meta:
        unique_together = ('profesional', 'fecha', 'hora')

    def __str__(self):
        return f"Turno: {self.fecha} {self.hora} - Paciente: {self.paciente.apellido} | Médico: {self.profesional.apellido}"