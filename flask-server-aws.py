from flask import Flask, jsonify, request
from pymongo import MongoClient
from send_email import send_mail
# por defecto para crear una instancia de aplicación
def create_app():
    app = Flask(__name__)
    return app
app = create_app()
client = MongoClient('localhost',27017) #coneccion a la base de datos
db = client['flask_db'] #seleccion de la base de datos
users = db['users'] #seleccion de la coleccion
#user = users.insert_one({'usuario':'jorge','pass':'qwert'})
user = users.find_one({'usuario':'jorge','pass':'qwert'})
query = {'usuario':'jorge','pass':'qwert'}
newvalues = {"$set": {'nombres':'Jorge Alessandri','matricula':'2055544422','correo':'d.labarin01@ufromail.cl'}}
users.update_one(query,newvalues)
print(users.find_one(sort=[('_id',-1)]))  #verificar el último registro de la coleccion
for user in users.find():
    print(user)

# metodo de respuesta GET para concoer el estado del servicio, devuelve un json
# para llamarlo poner SU_IP:8081/status
@app.route("/status")
def status():
    return {
        "estado": "1",
        "texto": "OK"
    }
# API REST que recibe un JSON lo imprime por consola y responde un json
@app.route("/events", methods=(['POST']))
def create_event():
    response = {'token': False}
    entrada = request.json
    print('json: ', entrada) #verficamos que el json se recibe correctamente
    user = entrada['username']
    password = entrada['password']
    print('usersdb: ', users.find_one({'usuario':user,'pass':password})) #verificamos si el usuario y contraseña esten en la base de datos

    if users.find_one({'usuario':user,'pass':password}): #preguntamos si la base de datos devuelve un diccionario
        userdb = users.find_one({'usuario':user,'pass':password})['usuario']
        passdb = users.find_one({'usuario':user,'pass':password})['pass']
        if user == userdb and password == passdb: #verificamos que el usuario y contraseña coincidan
            response = {'token': True} 

    return jsonify(response)

@app.route("/recover", methods=(['POST']))
def recover():
    entrada = request.json
    print('json: ', entrada)
    correo = entrada['email']
    print('usersdb: ', users.find_one({'correo':user}))
    if users.find_one({'correo':user}):
        correo_registrado = users.find_one({'correo':user})['correo']
        if correo == correo_registrado:
            send_mail(correo_registrado, 'dlc.ufro@gmail.com', 'Recuperar contraseña', 'Tu contraseña es: '+users.find_one({'correo':user})['pass'])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081, debug=True) #levanta el servicio REST API en puerto 8081