

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

### Estructura del proyecto

La lógica del sistema está centralizada en la aplicación `turnos`, organizada de la siguiente manera:

- `/sistema_gestion_turnos/`: Configuración principal del proyecto (settings, urls, wsgi).
- `/turnos/`: Aplicación principal que contiene:
    - `models.py`, `views.py`, `admin.py`: Lógica central, modelos y vistas para ambos portales.
    - `/templates/turnos/`: Todos los archivos HTML de las interfaces (paciente y profesional).
    - `/migrations/`: Historial de cambios en la base de datos.
- `/static/` y `/staticfiles/`: Archivos estáticos del proyecto.
- `manage.py`: Script de gestión de Django.
- `requirements.txt`: Dependencias necesarias para ejecutar el sistema.
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
    pip install -r requirements.txt


4. **Aplicar las migraciones:**

    ### PowerShell
    python manage.py migrate

5. **Iniciar el servidor de desarrollo:**

    ### PowerShell
    python manage.py runserver

### Luego, ingresá a http://127.0.0.1:8000/ en tu navegador. Para acceder al panel administrador, usá http://127.0.0.1:8000/admin.

---

### Sistema en línea (Deploy)

El sistema está disponible en:
https://sistemagestionturnosmedicos-production.up.railway.app


### Panel de Administración

Acceso al panel de administración (solo para administradores):
https://sistemagestionturnosmedicos-production.up.railway.app/admin/

---

### Entornos del sistema

El sistema cuenta con dos entornos independientes:

**Entorno local (desarrollo)**
- URL: http://127.0.0.1:8000/
- Base de datos: SQLite (archivo db.sqlite3 local)
- Solo accesible desde la computadora de desarrollo

**Entorno producción (Railway)**
- URL: https://sistemagestionturnosmedicos-production.up.railway.app/
- Base de datos: PostgreSQL en Railway
- Accesible desde cualquier navegador
- Los datos de ambos entornos son independientes y no se cruzan.