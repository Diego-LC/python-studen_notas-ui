import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from openpyxl import Workbook
from openpyxl.styles import Alignment
import os
from dotenv import load_dotenv

# Cargar variables de entorno del archivo .env
load_dotenv()

def send_mail(to_mail, remitente, subject, text, filename=""):

# Iniciamos los parámetros del scrip
    destinatarios = [to_mail, remitente]
    cuerpo = text
    ruta_adjunto = filename
    nombre_adjunto = filename
    # Creamos el objeto mensaje
    mensaje = MIMEMultipart()
    # Establecemos los atributos del mensaje
    mensaje['From'] = remitente
    mensaje['To'] = ", ".join(destinatarios)
    mensaje['Subject'] = subject
    # Agregamos el cuerpo del mensaje como objeto MIME de tipo texto
    mensaje.attach(MIMEText(cuerpo, 'plain'))

    if (os.path.isfile(filename)):
        # Creamos un objeto MIME base
        adjunto_MIME = MIMEBase('application', 'octet-stream')
        # Abrimos el archivo que vamos a adjuntar
        archivo_adjunto = open(ruta_adjunto, 'rb')
        # Y le cargamos el archivo adjunto
        adjunto_MIME.set_payload((archivo_adjunto).read())
        # Codificamos el objeto en BASE64
        encoders.encode_base64(adjunto_MIME)
        # Agregamos una cabecera al objeto
        adjunto_MIME.add_header('Content-Disposition', "attachment; filename= %s" % nombre_adjunto)
        # Y finalmente lo agregamos al mensaje
        mensaje.attach(adjunto_MIME)
        # Creamos la conexión con el servidor
    try:
        smtp_server = os.getenv('EMAIL_SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('EMAIL_SMTP_PORT', 587))
        sesion_smtp = smtplib.SMTP(smtp_server, smtp_port)
        # Ciframos la conexión
        sesion_smtp.starttls()
        # Iniciamos sesión en el servidor
        email_password = os.getenv('EMAIL_PASSWORD')
        if email_password is None:
            print("Error: No se ha definido la variable de entorno EMAIL_PASSWORD")
            return False
        sesion_smtp.login(remitente, email_password)
        # Convertimos el objeto mensaje a texto
        texto = mensaje.as_string()
        # Enviamos el mensaje
        sesion_smtp.sendmail(remitente, destinatarios, texto)
        # Cerramos la conexión
        sesion_smtp.quit()
        print ("Envio email: "+to_mail)
        return True
    except Exception as e:
        print(f"NO Envio email (Error: {e}): {to_mail}")
        return False


def crear_exel(datos):
    # Agregar diagnóstico de la estructura de datos
    print("Estructura de datos recibida:")
    print(f"Tipo de datos: {type(datos)}")
    print(f"Claves en datos: {list(datos.keys()) if isinstance(datos, dict) else 'No es un diccionario'}")
    if isinstance(datos, dict) and 'notas' in datos:
        print(f"Tipo de datos['notas']: {type(datos['notas'])}")
        if isinstance(datos['notas'], dict):
            print(f"Ejemplo de clave en notas: {next(iter(datos['notas'].keys()), 'No hay claves')}")
            print(f"Ejemplo de valor en notas: {next(iter(datos['notas'].values()), 'No hay valores')}")
    
    libro_excel = Workbook()
    hoja = libro_excel.active

    # Validar estructura del diccionario datos
    if not isinstance(datos, dict):
        print("Error: datos debe ser un diccionario")
        return "error.xlsx"
        
    # Encabezados de las notas
    encabezados_notas = ['Tipo Nota', 'Nota', 'Ponderación Nota','Tipo Evaluación']
    hoja.append(encabezados_notas)

    # Escribir notas - verificando que exista la clave 'notas' y sea un diccionario
    if 'notas' in datos and isinstance(datos['notas'], dict):
        for key, fila_data in datos['notas'].items():
            try:
                fila = [fila_data['Tipo Nota'], fila_data['Nota'], fila_data['Ponderación Nota'], fila_data['Tipo Evaluación']]
                hoja.append(fila)
            except KeyError as e:
                print(f"Error: Falta la clave {e} en los datos de notas")
                continue
    else:
        hoja.append(["No hay datos de notas disponibles"])

    # Espacio en blanco entre las notas y las ponderaciones
    hoja.append([])

    # Encabezados de las ponderaciones
    encabezados_ponderaciones = ['Tipo Evaluación', 'Ponderación']
    hoja.append(encabezados_ponderaciones)

    # Escribir ponderaciones - verificando la estructura anidada
    if 'ponderaciones' in datos and 'tipo_evaluacion' in datos.get('ponderaciones', {}):
        for tipo_evaluacion, ponderacion in datos['ponderaciones']['tipo_evaluacion'].items():
            fila = [tipo_evaluacion, ponderacion]
            hoja.append(fila)
    else:
        hoja.append(["No hay datos de ponderaciones disponibles"])

    # Espacio en blanco entre las ponderaciones y los promedios
    hoja.append([])
    hoja.append(['Promedios'])

    # Encabezados y valores de los promedios por tipo de evaluación
    encabezados_promedios = ['Tipo Evaluación', 'Promedio']
    hoja.append(encabezados_promedios)

    # Verificar que exista la clave 'promedios'
    if 'promedios' in datos and isinstance(datos['promedios'], dict):
        for tipo_evaluacion, promedio in datos['promedios'].items():
            try:
                fila = [tipo_evaluacion, promedio]
                hoja.append(fila)
            except KeyError as e:
                print(f"Error: Falta la clave {e} en los datos de promedios")
                continue
    else:
        hoja.append(["No hay datos de promedios disponibles"])
    hoja.append([])

    # Encabezado y valor del promedio total
    if 'promedio_total' in datos:
        encabezado_promedio_total = ['Promedio Total', datos['promedio_total']]
        hoja.append(encabezado_promedio_total)
    else:
        hoja.append(["No hay datos de promedio total disponibles"])

    # Ajustar el ancho de las columnas
    for columna in hoja.columns:
        max_length = 0
        column = columna[0].column_letter  # Obtiene la letra de la columna (A, B, C, ...)
        for cell in columna:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2) * 1.2
        hoja.column_dimensions[column].width = adjusted_width

    # Centrar el contenido de las celdas
    for fila in hoja.iter_rows(min_row=2):
        for celda in fila:
            celda.alignment = Alignment(horizontal="center", vertical="center")
    
    ruta = "notas.xlsx"
    libro_excel.save(ruta)
    return ruta