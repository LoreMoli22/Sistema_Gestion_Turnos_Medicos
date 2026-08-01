import random
import string
import resend 

from django.shortcuts import render, redirect  
from django.contrib import messages             
from .models import Turno, Profesional, Paciente 
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings 
from django.core.exceptions import ValidationError

def lista_turnos(request):
    paciente_id = request.session.get('paciente_id')
    if paciente_id:
        todos_los_turnos = Turno.objects.filter(paciente_id=paciente_id)
        paciente = Paciente.objects.get(id=paciente_id)
    else:
        return redirect('ingreso_paciente')
    return render(request, 'turnos/lista_turnos.html', {'turnos': todos_los_turnos, 'paciente': paciente})

def inicio(request):
    return render(request, 'turnos/inicio.html')


def elegir_portal(request):
    return render(request, 'turnos/eleccion_portal.html')


def ingreso_paciente(request):
    if request.method == 'POST':
        dni = request.POST.get('dni')
        contrasena = request.POST.get('contrasena')
    
        try:
            paciente = Paciente.objects.get(dni=dni)
            if check_password(contrasena, paciente.contrasena):
                request.session['paciente_id'] = paciente.id
                return redirect('lista_turnos')
            else:
                messages.error(request, "Contraseña incorrecta.")
        except Paciente.DoesNotExist:
            messages.error(request, "No existe un paciente con ese DNI.")

    return render(request, 'turnos/ingreso_paciente.html')

def ingreso_profesional(request):
    if request.method == 'POST':
        matricula = request.POST.get('matricula')
        contrasena = request.POST.get('contrasena')

        try:
            profesional = Profesional.objects.get(matricula=matricula)
            if check_password(contrasena, profesional.contrasena):
                request.session['profesional_id'] = profesional.id
                return redirect('lista_turnos_profesional')
            else:
                messages.error(request, "Contraseña incorrecta.")
        except Profesional.DoesNotExist:
            messages.error(request, "No existe un profesional con esa matrícula.")

    return render(request, 'turnos/ingreso_profesional.html')


def registro_profesional(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        matricula = request.POST.get('matricula')
        especialidad = request.POST.get('especialidad')
        email = request.POST.get('email')  
        contrasena = request.POST.get('contrasena')
        conf_contrasena = request.POST.get('conf_contrasena')

        if contrasena != conf_contrasena:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, 'turnos/registro_profesional.html')

        if Profesional.objects.filter(matricula=matricula).exists():
            messages.error(request, "Esta matrícula ya se encuentra registrada.")
            return render(request, 'turnos/registro_profesional.html')

        nuevo_profesional = Profesional(
            nombre=nombre,
            apellido=apellido,
            matricula=matricula,
            especialidad=especialidad,
            email=email,
            contrasena=make_password(contrasena)
        )

        try:
            nuevo_profesional.save()
        except ValidationError as e:
            mensaje_error = e.message_dict.get('nombre') or e.message_dict.get('apellido') or e.message_dict.get('matricula') or "Error de validación."
            messages.error(request, mensaje_error[0] if isinstance(mensaje_error, list) else mensaje_error)
            return render(request, 'turnos/registro_profesional.html')
        
        messages.success(request, "¡Registro de profesional exitoso!")
        return redirect('ingreso_profesional')

    return render(request, 'turnos/registro_profesional.html')


def registro_paciente(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        dni = request.POST.get('dni')
        email = request.POST.get('email')
        contrasena = request.POST.get('contrasena')
        conf_contrasena = request.POST.get('conf_contrasena')

        if contrasena != conf_contrasena:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, 'turnos/registro_paciente.html')

        if Paciente.objects.filter(dni=dni).exists():
            messages.error(request, "Este DNI ya se encuentra registrado.")
            return render(request, 'turnos/registro_paciente.html')
            
        if Paciente.objects.filter(email=email).exists():
            messages.error(request, "Este correo electrónico ya está registrado.")
            return render(request, 'turnos/registro_paciente.html')

        nuevo_paciente = Paciente(
            nombre=nombre,
            apellido=apellido,
            dni=dni,
            email=email,
            contrasena=make_password(contrasena)
        )
        
        try:
            nuevo_paciente.save()
        except ValidationError as e:
            mensaje_error = e.message_dict.get('nombre') or e.message_dict.get('apellido') or e.message_dict.get('dni') or "Error de validación."
            messages.error(request, mensaje_error[0] if isinstance(mensaje_error, list) else mensaje_error)
            return render(request, 'turnos/registro_paciente.html')

        messages.success(request, "¡Registro de paciente exitoso!")
        return redirect('ingreso_paciente')

    return render(request, 'turnos/registro_paciente.html')


def solicitar_turno(request):
    paciente_id = request.session.get('paciente_id')
    if not paciente_id:
        return redirect('ingreso_paciente')

    profesionales = Profesional.objects.all()
    
    # Traemos los turnos existentes formateando la hora correctamente a 'HH:MM'
    turnos_existentes = list(Turno.objects.all().values('profesional_id', 'fecha', 'hora'))
    for t in turnos_existentes:
        if t['hora']:
            t['hora'] = str(t['hora'])[:5] # Recorta los segundos si los hubiera (ej: '10:00:00' -> '10:00')

    contexto = {
        'profesionales': profesionales,
        'turnos_existentes': turnos_existentes
    }

    if request.method == 'POST':
        profesional_id = request.POST.get('profesional')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        motivo = request.POST.get('motivo')

        from datetime import datetime, date, time
        
        fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
        hora_obj = datetime.strptime(hora, '%H:%M').time()

        # 1. Validar que no sea una fecha pasada
        if fecha_obj < date.today():
            messages.error(request, "No se pueden solicitar turnos para fechas que ya pasaron.")
            return render(request, 'turnos/solicitar_turno.html', contexto)

        # 2. Validar que no sea sábado (5) ni domingo (6)
        if fecha_obj.weekday() >= 5:
            messages.error(request, "Los fines de semana (sábados y domingos) no se atienden turnos.")
            return render(request, 'turnos/solicitar_turno.html', contexto)

        # 3. Validar la franja horaria (de 08:00 a 16:00)
        hora_inicio = time(8, 0)
        hora_fin = time(16, 0)
        
        if not (hora_inicio <= hora_obj <= hora_fin):
            messages.error(request, "Los turnos solo se pueden solicitar dentro de la franja horaria de 08:00 a 16:00 hs.")
            return render(request, 'turnos/solicitar_turno.html', contexto)

        # 4. Validar si ya existe un turno ocupado
        if Turno.objects.filter(profesional_id=profesional_id, fecha=fecha, hora=hora).exists():
            messages.error(request, "Lo siento, ese profesional ya tiene un turno reservado en ese día y horario.")
            return render(request, 'turnos/solicitar_turno.html', contexto)
       
        paciente = Paciente.objects.get(id=paciente_id)
        profesional = Profesional.objects.get(id=profesional_id)

        nuevo_turno = Turno(
            paciente=paciente,
            profesional=profesional,
            fecha=fecha,
            hora=hora,
            motivo=motivo,
            estado='PENDIENTE'
        )
        nuevo_turno.save()

        messages.success(request, "¡Turno solicitado con éxito!")
        return redirect('lista_turnos')

    return render(request, 'turnos/solicitar_turno.html', contexto)

def lista_turnos_profesional(request):
    profesional_id = request.session.get('profesional_id')
    if not profesional_id:
        return redirect('ingreso_profesional')

    profesional = Profesional.objects.get(id=profesional_id)
    turnos = Turno.objects.filter(profesional_id=profesional_id)

    return render(request, 'turnos/lista_turnos_profesional.html', {
        'turnos': turnos,
        'profesional': profesional
    })


def cambiar_estado_turno(request, turno_id):
    if not request.session.get('profesional_id'):
        return redirect('ingreso_profesional')

    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        try:
            turno = Turno.objects.get(id=turno_id)
            turno.estado = nuevo_estado
            turno.save()
            messages.success(request, f"El estado del turno se actualizó a {nuevo_estado}.")
        except Turno.DoesNotExist:
            messages.error(request, "El turno no existe.")

    return redirect('lista_turnos_profesional')


def cerrar_sesion(request):
    request.session.flush()
    return redirect('inicio')


def editar_paciente(request):
    paciente_id = request.session.get('paciente_id')
    if not paciente_id:
        return redirect('ingreso_paciente')

    paciente = Paciente.objects.get(id=paciente_id)

    if request.method == 'POST':
        paciente.nombre = request.POST.get('nombre')
        paciente.apellido = request.POST.get('apellido')
        paciente.email = request.POST.get('email')
        nueva_contrasena = request.POST.get('nueva_contrasena')
        if nueva_contrasena:
            paciente.contrasena = make_password(nueva_contrasena)
        paciente.save()
        messages.success(request, "Datos actualizados correctamente.")
        return redirect('lista_turnos')

    return render(request, 'turnos/editar_paciente.html', {'paciente': paciente})


def editar_profesional(request):
    profesional_id = request.session.get('profesional_id')
    if not profesional_id:
        return redirect('ingreso_profesional')

    profesional = Profesional.objects.get(id=profesional_id)

    if request.method == 'POST':
        profesional.nombre = request.POST.get('nombre')
        profesional.apellido = request.POST.get('apellido')
        profesional.especialidad = request.POST.get('especialidad')
        profesional.email = request.POST.get('email')  
        nueva_contrasena = request.POST.get('nueva_contrasena')
        if nueva_contrasena:
            profesional.contrasena = make_password(nueva_contrasena)
        profesional.save()
        messages.success(request, "Datos actualizados correctamente.")
        return redirect('lista_turnos_profesional')

    return render(request, 'turnos/editar_profesional.html', {'profesional': profesional})

def baja_paciente(request):
    paciente_id = request.session.get('paciente_id')
    if not paciente_id:
        return redirect('ingreso_paciente')

    paciente = Paciente.objects.get(id=paciente_id)
    paciente.delete()
    request.session.flush()
    messages.success(request, "Tu cuenta fue eliminada correctamente.")
    return redirect('inicio')


def baja_profesional(request):
    profesional_id = request.session.get('profesional_id')
    if not profesional_id:
        return redirect('ingreso_profesional')

    profesional = Profesional.objects.get(id=profesional_id)
    profesional.delete()
    request.session.flush()
    messages.success(request, "Tu cuenta fue eliminada correctamente.")
    return redirect('inicio')



# VISTAS DE RECUPERACION MODIFICADAS CON RESEND

def recuperar_contrasena_paciente(request):
    if request.method == 'POST':
        dni = request.POST.get('dni')
        try:
            paciente = Paciente.objects.get(dni=dni)
            nueva_contrasena = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            
            paciente.contrasena = make_password(nueva_contrasena)
            paciente.save()
            
            # Envio seguro con Resend API
            resend.api_key = settings.RESEND_API_KEY
            try:
                resend.Emails.send({
                    "from": "onboarding@resend.dev",
                    "to": "lore82laplata@gmail.com",
                    "subject": "Contrasena de Paciente - Turnos Medicos",
                    "html": f"<p>Paciente: {paciente.nombre}{paciente.apellido}. Nueva contraseña: <strong>{nueva_contrasena}</strong></p>"
                })
            except Exception as e:
                print(f"Error en Resend Paciente: {e}")
            
            messages.success(request, "Enviaremos una nueva contraseña.")
            return redirect('ingreso_paciente')
        except Paciente.DoesNotExist:
            messages.error(request, "No existe un paciente con ese DNI.")
    return render(request, 'turnos/recuperar_contrasena_paciente.html')


def recuperar_contrasena_profesional(request):
    if request.method == 'POST':
        matricula = request.POST.get('matricula')
        try:
            profesional = Profesional.objects.get(matricula=matricula)
            nueva_contrasena = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            
            profesional.contrasena = make_password(nueva_contrasena)
            profesional.save()
            
            # Envio seguro con Resend API
            resend.api_key = settings.RESEND_API_KEY
            try:
                resend.Emails.send({
                    "from": "onboarding@resend.dev",
                    "to": "lore82laplata@gmail.com",
                    "subject": "Contrasena de Profesional - Turnos Medicos",
                    "html": f"<p>Profesional: {profesional.nombre}{profesional.apellido}. Nueva contrasena: <strong>{nueva_contrasena}</strong></p>"
                })
            except Exception as e:
                print(f"Error en Resend Profesional: {e}")
                
            messages.success(request, "Enviaremos una nueva contraseña.")
            return redirect('ingreso_profesional')
        except Profesional.DoesNotExist:
            messages.error(request, "No existe un profesional con esa matricula.")
    return render(request, 'turnos/recuperar_contrasena_profesional.html')