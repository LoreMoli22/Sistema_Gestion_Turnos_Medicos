
from django.shortcuts import render, redirect  
from django.contrib import messages             
from .models import Turno, Profesional, Paciente 
from django.contrib.auth.hashers import make_password, check_password



def lista_turnos(request):
    paciente_id = request.session.get('paciente_id')
    if paciente_id:
        todos_los_turnos = Turno.objects.filter(paciente_id=paciente_id)
    else:
        return redirect('ingreso_paciente')
    return render(request, 'turnos/lista_turnos.html', {'turnos': todos_los_turnos})

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
        nuevo_profesional.save()

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
        nuevo_paciente.save()

        messages.success(request, "¡Registro de paciente exitoso!")
        return redirect('ingreso_paciente')

    return render(request, 'turnos/registro_paciente.html')


def solicitar_turno(request):
    paciente_id = request.session.get('paciente_id')
    if not paciente_id:
        return redirect('ingreso_paciente')

    profesionales = Profesional.objects.all()

    if request.method == 'POST':
        profesional_id = request.POST.get('profesional')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        motivo = request.POST.get('motivo')

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

    return render(request, 'turnos/solicitar_turno.html', {'profesionales': profesionales})


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
    # Verificamos que sea el profesional quien hace el cambio
    if not request.session.get('profesional_id'):
        return redirect('ingreso_profesional')

    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        try:
            # Buscamos el turno específico por su ID
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


