

### Sistema de Gestión de Turnos Médicos

Este es un proyecto desarrollado en **Django** y **Python** para la gestión integral de turnos médicos. Permite la administración de pacientes, profesionales de la salud y la asignación de citas médicas.

---

### Tecnologías Utilizadas:

***Python** 3.13+
***Django** 5.x
***SQLite** (Base de datos local por defecto)
***Git & GitHub** para el control de versiones

---

### Funcionalidades Principales

- Registro, login y cierre de sesión de pacientes y profesionales
- Alta, baja y modificación de datos de pacientes y profesionales
- Solicitud de turnos por parte del paciente
- Visualización de turnos propios (paciente ve los suyos, profesional los suyos)
- Cambio de estado del turno: Pendiente, Confirmado, Cancelado, Realizado
- Contraseñas encriptadas con hasheo seguro

---

### Instalación y Ejecución Local:

Si querés clonar este proyecto y correrlo en tu máquina, seguí estos pasos:

1. **Clonar el repositorio:**
   
   ### PowerShell

    git clone https://github.com/LoreMoli22/Sistema_Gestion_Turnos_Medicos.git

    cd Sistema_Gestion_Turnos_Medicos

2. **Crear y activar el entorno virtual:**

    ### PowerShell
   python -m venv env
     .\venv\Scripts\Activate.ps1
     

3. **Instalar dependencias:**

    ### PowerShell
    pip install -r requirements.tx


4. **Aplicar las migraciones:**

    ### PowerShell
    python manage.py migrate

5. **Iniciar el servidor de desarrollo:**

    ### PowerShell
    python manage.py runserver

### Luego, ingresá a http://127.0.0.1:8000/ en tu navegador. Para acceder al panel administrador, usá http://127.0.0.1:8000/admin.