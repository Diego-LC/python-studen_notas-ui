from flask import Flask, jsonify, request
from pymongo import MongoClient
from send_email import send_mail
import random
import string

verificacion_val = ''
def create_app(): # por defecto para crear una instancia de aplicación
    app = Flask(__name__)
    return app
app = create_app()
client = MongoClient('localhost',27017) #coneccion a la base de datos
db = client['flask_db'] #seleccion de la base de datos
users = db['users'] #seleccion de la coleccion

ids = users.find_one(sort=[('_id',-1)]) #verifica el primer registro de la coleccion
#print(users.find_one()) #verifica el último registro
#print(ids)
i=1
for user in users.find():
    print(f'user {i}: ', user)
    i+=1

@app.route("/status")
def status():
    return {
        "estado": "1",
        "texto": "OK"
    }
# API REST que recibe un JSON lo imprime por consola y responde un json
@app.route("/login", methods=(['POST']))
def create_event():
    respuesta = {'token': False, 'tipo': ''}
    entrada = request.json
    print('json: ', entrada) #verficamos que el json se recibe correctamente
    user = entrada['username']
    valor = 'usuario'
    if '@' in user and '.c' in user:
        valor = 'correo'
    password = entrada['password']
    userdb = users.find_one({valor: user,'pass':password})
    print('usersdb: ', userdb) #verificamos si el usuario y contraseña esten en la base de datos

    if userdb: #preguntamos si la base de datos devuelve un diccionario
        udb = userdb[valor]
        passdb = userdb['pass']
        if user == udb and password == passdb: #verificamos que el usuario y contraseña coincidan
            respuesta = {'token': True, 'tipo': userdb['notas']}
    return jsonify(respuesta)

@app.route("/recover", methods=(['POST']))
def recover():
    entrada = request.json
    print('json: ', entrada)
    correo = entrada['email']
    print('usersdb: ', users.find_one({'correo':correo}))
    if users.find_one({'correo':correo}):
        userbd = users.find_one({'correo':correo})
        correo_registrado = users.find_one({'correo':correo})['correo']
        if correo == correo_registrado:
            envio = send_mail(correo_registrado, 'dlc.ufro@gmail.com', 'Recuperar contraseña', 'Tu contraseña es: '+ userbd['pass'])
            if envio:
                print('correo enviado')
            else:
                print('correo no enviado')

    return jsonify({'ok':''})

@app.route("/email_verification", methods=(['POST']))
def email_verification():
    respuesta = {'status': False}
    entrada = request.json
    print('json: ', entrada)
    correo = entrada['email']
    print('usersdb: ', users.find_one({'correo':correo}))
    if not users.find_one({'correo':correo}):
        respuesta = {'status': True}
        ## Genera rápidamente letras y números aleatorios
        code_str = string.ascii_letters + string.digits
        ## Imprime 4 letras o números aleatorios
        global verificacion_val
        verificacion_val = ''.join(random.sample(code_str,6))
        envio = send_mail(correo, 'dlc.ufro@gmail.com', 'Código de verificación de email', 'Tu codigo de verificación es: '+ verificacion_val)
        if envio:
            print('correo enviado')
        else:
            print('correo no enviado')
    return jsonify(respuesta)

@app.route("/register", methods=(['POST']))
def register():
    respuesta = {'status': False}
    entrada = request.json
    print('json: ', entrada)
    nombre = entrada['name']
    user = entrada['username']
    password = entrada['password']
    correo = entrada['email']
    codigo = entrada['code']
    matricula = entrada['matricula']
    tipo = entrada['tipo']
    if codigo == verificacion_val:
        respuesta = {'status': True}
        users.insert_one({'usuario':user,'pass':password,'correo':correo,'matricula':matricula, 'nombres':nombre, 'tipo':tipo})
    
    return jsonify(respuesta)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081, debug=True) #levanta el servicio REST API en puerto 8081