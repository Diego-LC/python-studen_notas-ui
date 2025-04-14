# UfroGrades - Gestor de Calificaciones Académicas

UfroGrades es una aplicación de escritorio desarrollada en Python que permite a estudiantes y profesores gestionar calificaciones académicas. Esta herramienta facilita el seguimiento de las notas por asignatura, permitiendo calcular promedios ponderados y exportar la información en diferentes formatos.

## Características principales

- **Gestión de asignaturas**: Agregar, editar y eliminar asignaturas con sus respectivos códigos y módulos.
- **Control de calificaciones**: Administrar notas con diferentes tipos de evaluación y ponderaciones.
- **Cálculo automático de promedios**: La aplicación calcula automáticamente los promedios ponderados por tipo de evaluación.
- **Exportación de datos**: Posibilidad de guardar las calificaciones en formato Excel.
- **Envío por correo**: Funcionalidad para enviar las notas por correo electrónico.
- **Sistema de usuarios**: Registro e inicio de sesión para mantener los datos seguros y personalizados.
- **Recuperación de contraseña**: Mecanismo de recuperación de contraseña mediante correo electrónico.

## Requisitos

Para ejecutar esta aplicación, necesitarás:

```
blinker==1.9.0
certifi==2025.1.31
charset-normalizer==3.4.1
click==8.1.8
colorama==0.4.6
et_xmlfile==2.0.0
Flask==3.1.0
idna==3.10
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.2
openpyxl==3.1.5
python-dotenv==1.0.0
requests==2.32.3
urllib3==2.4.0
Werkzeug==3.1.3
pymongo
```

## Instalación

1. Clona este repositorio:
   ```
   git clone [URL-del-repositorio]
   ```

2. Instala las dependencias:
   ```
   pip install -r requeriments.txt
   ```

3. Configura una base de datos MongoDB local o remota.

4. Crea un archivo `.env` en el directorio raíz del proyecto con las siguientes variables:
   ```
   # Configuración del servidor
   API_HOST=0.0.0.0
   API_PORT=8081
   API_DEBUG=True

   # URLs
   API_URL=http://tu-ip-o-dominio:8081/

   # Configuración de la base de datos MongoDB
   MONGO_HOST=localhost
   MONGO_PORT=27017
   MONGO_DB=flask_db
   MONGO_COLLECTION=users

   # Configuración de correo
   EMAIL_SMTP_SERVER=smtp.gmail.com
   EMAIL_SMTP_PORT=587
   EMAIL_SENDER=tu-correo@gmail.com
   EMAIL_PASSWORD=tu-contraseña-o-clave-app

   # Verificación de correo
   VERIFICATION_CODE_LENGTH=6

   # Información de desarrollo
   DEBUG_ENABLED=True
   ```

## Uso

1. Inicia la aplicación ejecutando:
   ```
   python inicio_sesion.py
   ```

2. Inicia sesión con tu usuario o regístrate si es tu primera vez.

3. Para admin de prueba:
   - Usuario: admin
   - Contraseña: admin

## Estructura del proyecto

- `inicio_sesion.py`: Punto de entrada de la aplicación, maneja la autenticación.
- `UfroGrades.py`: Ventana principal y lógica de gestión de asignaturas.
- `ventana_asignatura.py`: Gestión de notas por asignatura.
- `registro.py`: Maneja el registro de nuevos usuarios.
- `Api-aws/`: Contiene la API REST para la comunicación con el servidor.
  - `flask-app.py`: Implementación de la API con Flask.
  - `excel_email.py`: Funciones para crear archivos Excel y enviar correos.

## API REST

La aplicación se comunica con una API REST que proporciona los siguientes endpoints:

- `/status`: Verificar el estado del servicio.
- `/login`: Autenticación de usuarios.
- `/recover`: Recuperación de contraseña.
- `/email_verification`: Verificación de correo electrónico.
- `/register`: Registro de nuevos usuarios.
- `/update`: Actualización de datos de notas.
- `/send`: Envío de correo con archivo Excel adjunto.

## Seguridad

- Las credenciales y configuraciones sensibles se almacenan en el archivo `.env` que debe mantenerse fuera del control de versiones.
- Para entornos de producción, asegúrate de configurar contraseñas seguras y utilizar conexiones HTTPS.

## Notas

- El servidor API se ejecuta por defecto en el puerto 8081.
- Para el envío de correos con Gmail, es posible que necesites habilitar el acceso de aplicaciones menos seguras o usar claves de aplicación.
- Los datos de ejemplo incluyen configuraciones para asignaturas como "Álgebra Lineal" y "Programación".

---

Desarrollado como parte del proyecto académico de gestión de calificaciones.
