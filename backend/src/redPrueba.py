"""[linea : Contenido]
    : Imports
    : servicio
    : POST (Usuario)
    : GET (Usuarios)
    : GET (Usuario Especifico)
    : DELETE (Usuario Espeficifo)
    : PUT (Usuario Especifico)
    
    : POST (Pato)
    : GET (Patos)
    : GET (Pato Especifico)
    : DELETE (Pato Espeficifo)
    : PUT (Pato Especifico)
    
    : GET (FotoCara)
    : GET (FotoPato)
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import redis
import requests

r = redis.StrictRedis(host="localhost", port=6379,
                      charset="utf-8", decode_responses=True)
app = Flask(__name__)

CORS(app)


@app.route('/users', methods=["POST"])
def createUser():
    user = {'_id': "user" + request.json['nombre'] + request.json['correo'], 'nombre': request.json['nombre'], 'correo': request.json['correo'],
            'mascotas': request.json['mascotas'], 'foto': request.json['foto']}

    name = "user" + request.json['nombre'] + request.json['correo']
    json_user = json.dumps(user)
    r.set(name, json_user)
    return json.loads(json_user)


@app.route('/users', methods=["GET"])
def getUsers():
    users = []
    for key in r.keys():
        if r.get(key).startswith("{\"_id\": \"user"):
            users.append(json.loads(r.get(key)))
    return jsonify(users)


@app.route('/user/<id>', methods=["GET"])
def getUser(id):
    user = json.loads(r.get(id))
    return user


@app.route('/users/<id>', methods=["DELETE"])
def deleteUser(id):
    r.delete(id)
    return 'ELIMINADO'


@app.route('/users/<id>', methods=["PUT"])
def updateUser(id):
    user = {'_id': id, 'nombre': request.json['nombre'], 'correo': request.json['correo'],
            'mascotas': request.json['mascotas'], 'foto': request.json['foto']}
    json_user = json.dumps(user)
    r.set(id, json_user)
    return "Actualizado"

#---------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------


@app.route('/ducks', methods=["POST"])
def createDuck():
    duck = {'_id': "duck" + request.json['nombre'] + request.json['dueño'], 'nombre': request.json['nombre'], 'dueño': request.json['dueño'],
            'año': request.json['año'], 'foto': request.json['foto']}
    name = "duck" + request.json['nombre'] + request.json['dueño']
    json_duck = json.dumps(duck)
    r.set(name, json_duck)
    return json.loads(json_duck)


@app.route('/ducks', methods=["GET"])
def getDucks():
    ducks = []
    for key in r.keys():
        if r.get(key).startswith("{\"_id\": \"duck"):
            ducks.append(json.loads(r.get(key)))
    return jsonify(ducks)


@app.route('/duck/<id>', methods=["GET"])
def getDuck(id):
    duck = json.loads(r.get(id))
    return duck


@app.route('/ducks/<id>', methods=["DELETE"])
def deleteDuck(id):
    r.delete(id)
    return 'ELIMINADO'


@app.route('/ducks/<id>', methods=["PUT"])
def updateDuck(id):
    duck = {'_id': id, 'nombre': request.json['nombre'], 'dueño': request.json['dueño'],
            'año': request.json['año'], 'foto': request.json['foto']}
    json_duck = json.dumps(duck)
    r.set(id, json_duck)
    return "Actualizado"


@app.route('/duckImg', methods=["GET"])
def getDuckImg():
    ROOT_LINK = 'https://random-d.uk/api/v2/random'
    res = requests.get(ROOT_LINK)
    duck = res.json()['url']
    return jsonify(duck)


@app.route('/face', methods=["GET"])
def getFace():
    LINK = 'https://fakeface.rest/face/json'
    res = requests.get(LINK)
    face = res.json()['image_url']
    return jsonify(face)


if __name__ == "__main__":
    app.run(debug=True)
