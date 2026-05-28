

### Sistema de Gestión de Turnos Médicos

Este es un proyecto desarrollado en **Django** y **Python** para la gestión integral de turnos médicos. Permite la administración de pacientes, profesionales de la salud y la asignación de citas médicas.

---

### Estado del Proyecto (Semana 2)

Actualmente, el proyecto cuenta con la estructura base configurada, la base de datos inicializada y los primeros modelos de datos registrados en el panel de administración.

### Componentes Desarrollados:

***Modelo Paciente:** Gestión de datos personales (Nombre, Apellido, DNI, Email, Contraseña).
***Modelo Profesional:** Gestión de especialistas (Nombre, Apellido, Matrícula, Especialidad, Contraseña).
***Panel de Administración:** Modelos registrados y listos para la gestión visual de datos.

---

### Tecnologías Utilizadas:

***Python** 3.13+
***Django** 5.x
***SQLite** (Base de datos local por defecto)
***Git & GitHub** para el control de versiones

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
     .\env\Scripts\Activate.ps1
     `

3. **Instalar Django:**

    ### PowerShell
    pip install django


4. **Aplicar las migraciones de la base de datos:**

    ### PowerShell
    python manage.py migrate

5. **Iniciar el servidor de desarrollo:**

    ### PowerShell
    python manage.py runserver

### Luego, ingresá a http://127.0.0.1:8000/ en tu navegador. Para acceder al panel administrador, usá http://127.0.0.1:8000/admin.