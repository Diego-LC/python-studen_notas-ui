from flask import Flask, jsonify, request
from pymongo import MongoClient
# por defecto para crear una instancia de aplicación
def create_app():
    app = Flask(__name__)
    return app
app = create_app()
client = MongoClient('localhost',27017)
db = client.flask_db
users = db['users']
#user = users.insert_one({'usuario':'jorge','pass':'qwert'})
print(users.find_one())

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
    response = {'token': 'False'}
    entrada = request.json
    print('json: ', entrada)
    user = entrada['username']
    password = entrada['password']
    print('usersdb: ', users.find_one({'usuario':user,'pass':password}))

    if users.find_one({'usuario':user,'pass':password}): #preguntamos si la base de datos devuelve un diccionario
        userdb = users.find_one({'usuario':user,'pass':password})['usuario']
        passdb = users.find_one({'usuario':user,'pass':password})['pass']
        if user == userdb and password == passdb:
            response = {'token': 'True'}

    return jsonify(response)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081, debug=True) #levanta el servicio REST API en puerto 8081