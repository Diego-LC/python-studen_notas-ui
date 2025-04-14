from flask import Flask, jsonify, request
from pymongo import MongoClient
from excel_email import send_mail
from excel_email import crear_exel
import random
import string
import os
from dotenv import load_dotenv

# Cargar variables de entorno del archivo .env
load_dotenv()

verificacion_val = "LPfFmn"
# por defecto para crear una instancia de aplicación
def create_app():
    app = Flask(__name__)
    return app
app = create_app()

# Usar variables de entorno para la conexión a MongoDB
client = MongoClient(os.getenv('MONGO_HOST', 'localhost'), int(os.getenv('MONGO_PORT', '27017')))
db = client[os.getenv('MONGO_DB', 'mydatabase')]
users = db[os.getenv('MONGO_COLLECTION', 'users')]

ids = users.find_one(sort=[('_id',-1)]) #verifica el primer registro de la coleccion
i=1
for user in users.find():
    print(f'user {i}: ', user)
    print('')
    i+=1

# metodo de respuesta GET para concoer el estado del servicio, devuelve un json
# para llamarlo poner SU_IP:8081/status
@app.route("/status")
def status():
    return {
        "estado": "1",
        "texto": "OK"
    }
# API REST que recibe un JSON lo imprime por consola y responde un json
@app.route("/login", methods=(['POST']))
def create_event():
    respuesta = {'token': False}
    entrada = request.json
    print('json: ', entrada) #verficamos que el json se recibe correctamente
    
    if entrada is None or 'username' not in entrada:
        return jsonify({'token': False, 'mensaje': 'Datos de entrada inválidos'})
    
    user = entrada['username']
    valor = 'usuario'
    if '@' in user and '.c' in user:
        valor = 'correo'
    password = entrada['password']
    userdb = users.find_one({valor: user,'pass':password})
    print('Está en bd(?): ', userdb) #verificamos si el usuario y contraseña esten en la base de datos

    if userdb: #preguntamos si la base de datos devuelve un diccionario
        udb = userdb[valor]
        passdb = userdb['pass']
        if user == udb and password == passdb: #verificamos que el usuario y contraseña coincidan
            respuesta = {'token': True, 'notas': userdb['notas'], 'userid': str(userdb['_id'])}
        else:
            print('no calsan usuario y pass')
    else:
        print('No se encontró usuario')
        respuesta = {'token': False, 'mensaje': 'Usuario o contraseña incorrectos'}
    return jsonify(respuesta)

@app.route("/recover", methods=(['POST']))
def recover():
    entrada = request.json
    print('json: ', entrada)
    
    if entrada is None or 'email' not in entrada:
        return jsonify({'status': False, 'mensaje': 'Datos de entrada inválidos'})
    
    correo = entrada['email']
    userdb = users.find_one({'correo':correo})
    print('usersdb: ', userdb)

    if userdb != None:
        correo_registrado = userdb['correo']
        if correo_registrado:
            # Usar la variable de entorno para el correo remitente
            envio = send_mail(correo_registrado, os.getenv('EMAIL_SENDER'), 'Recuperar contraseña', 'Tu contraseña es: '+ userdb['pass'])
            if envio:
                print('correo enviado')
                entrada = {'status': True, 'mensaje': 'Contraseña enviada al correo registrado'}
            else:
                print('correo no enviado')
                entrada = {'status': False, 'mensaje': 'Error al enviar el correo'}
    else:
        print('correo no registrado')
        entrada = {'status': False, 'mensaje': 'Correo no registrado'}

    return jsonify(entrada)

@app.route("/email_verification", methods=(['POST']))
def email_verification():
    respuesta = {'status': False}
    entrada = request.json
    print('json: ', entrada)
    
    if entrada is None or 'email' not in entrada:
        return jsonify({'status': False, 'mensaje': 'Datos de entrada inválidos'})
    
    correo = entrada['email']
    userdb = users.find_one({'correo':correo})
    print('usersdb: ', userdb)

    if not userdb and correo != '':
        code_str = string.ascii_letters + string.digits  # Genera rápidamente letras y números aleatorios
        global verificacion_val
        code_length = int(os.getenv('VERIFICATION_CODE_LENGTH', 6))
        verificacion_val = ''.join(random.sample(code_str, code_length))  # Genera código de verificación
        # Usar variables de entorno para el correo remitente
        envio = send_mail(correo, os.getenv('EMAIL_SENDER'), 'Código de verificación de email', 'Tu codigo de verificación es: '+ verificacion_val)

        if envio:
            respuesta = {'status': True, 'mensaje': 'Código enviado al correo'}
            print('correo enviado')
        else:
            respuesta = {'status': False, 'mensaje': 'Error al enviar el código  al correo'}
            print('correo no enviado')
    return jsonify(respuesta)

@app.route("/register", methods=(['POST']))
def register():
    respuesta = {'status': False, 'mensaje': 'no registrado'}
    entrada = request.json
    print('json: ', entrada)
    
    if entrada is None:
        return jsonify({'status': False, 'mensaje': 'Datos de entrada inválidos'})
    
    nombre = entrada.get('name', '')
    user = entrada['username']
    password = entrada['password']
    correo = entrada['email']
    codigo = entrada['code']
    matricula = entrada['matricula']
    print('verifi: ', verificacion_val, '\ncodigo: ', codigo)
    if not users.find_one({'correo':correo}): #verifica que el correo no este registrado
        if not users.find_one({'usuario':user}): #verifica que el usuario no este registrado
            if codigo == verificacion_val: #verifica que el codigo de verificacion sea correcto
                print('\nregistrado')
                users.insert_one({'usuario':user,'pass':password,'correo':correo,'matricula':matricula, 
                'nombres':nombre, 'notas':[{'ponderaciones':{'tipo_evaluacion':{'Eval. Teórica':1.0}, 
                                                'tipo_nota':{'Control':0.4, 'Prueba': 0.6}}},
                            {'notas':[["Control", "5.5", "Eval. Teórica"],["Prueba", "5.2", "Eval. Teórica"]]}]})
                respuesta = {'status': True, 'mensaje': 'registrado'}
            else:
                print('\ncodigo incorrecto')
                respuesta = {'status': False, 'mensaje': 'codigo incorrecto'}
        else:
            print('\nusuario ya registrado')
            respuesta = {'status': False, 'mensaje': ' El nombre de usuario ya se encuentra registrad\no'}
    else:
        print('\ncorreo ya registrado')
        respuesta = {'status': False, 'mensaje': 'El correo ya se encuentra registrado'}

    return jsonify(respuesta)

@app.route("/update", methods=(['POST']))
def update():
    respuesta = {'status': False, 'mensaje': 'no actualizado'}
    entrada = request.json
    
    if entrada is None or 'userid' not in entrada:
        return jsonify({'status': False, 'mensaje': 'Datos de entrada inválidos'})
    
    print('id: ', entrada['userid'], '\n')
    userbd = None  # Inicializar la variable antes del bucle
    
    for user in users.find():
        if str(user['_id']) == entrada['userid']:
            userbd = user
            break  # Terminamos el bucle una vez encontrado el usuario
    
    if userbd:
        print('userbd: ', userbd['correo'])
        print(userbd['_id'])
        busqueda = {'_id': userbd['_id']}
        new_val = {'$set': {'notas': entrada['notas']}}
        users.update_one(busqueda, new_val)
        respuesta = {'status': True, 'mensaje': 'Notas actualizadas'}
    else:
        respuesta = {'status': False, 'mensaje': 'Usuario no encontrado'}

    return jsonify(respuesta)

@app.route("/send", methods=(['POST']))
def send():
    respuesta = {'status': False, 'mensaje': 'Error al enviar por correo'}
    entrada = request.json
    
    if entrada is None or 'userid' not in entrada:
        return jsonify({'status': False, 'mensaje': 'Datos de entrada inválidos'})
        
    print(entrada)
    
    userbd = None  # Inicializar la variable antes del bucle
    
    for user in users.find():
        if str(user['_id']) == entrada['userid']:
            userbd = user
            break  # Terminamos el bucle una vez encontrado el usuario
    
    if userbd:
        print('userbd: ', userbd['correo'])
        correo = userbd['correo']
        ruta = crear_exel(entrada)
        envio = send_mail(correo, os.getenv('EMAIL_SENDER'), 'Archivo exel con notas', 'Adjunto se encuentra el arvivo excel:', ruta)
        if envio:
            respuesta = {'status': True, 'mensaje': 'Correo enviado'}
            print('correo enviado')

    return respuesta


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081, debug=True) #levanta el servicio REST API en puerto 8081
