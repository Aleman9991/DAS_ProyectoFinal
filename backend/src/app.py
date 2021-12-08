from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS
import requests

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://localhost:27017/pythonUsers"
mongo = PyMongo(app)

CORS(app)

@app.route('/users', methods=["POST"])
def postUser():
    mongo.db.users.insert_one({
        'nombre':request.json['nombre'],
        'correo':request.json['correo'],
        'foto':request.json['foto'],
        'mascotas':request.json['mascotas'],
        
    })
    return 'received'

@app.route('/users', methods=["GET"])
def getUsers():

    users = []
    for doc in mongo.db.users.find():
        print(doc)
        users.append({
            '_id': str(ObjectId(doc['_id'])),
            'nombre': doc['nombre'],
            'correo': doc['correo'],
            'foto': doc['foto'],
            'mascotas': doc["mascotas"]
        })
    return jsonify(users)


@app.route('/user/<id>', methods=["GET"])
def getUser(id):
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    print(user)
    return jsonify({
        '_id': str(ObjectId(user['_id'])),
        'nombre': user['nombre'],
        'correo': user['correo'],
        'foto': user['foto'],
        "mascotas": user["mascotas"]
    })


@app.route('/users/<id>', methods=["DELETE"])
def deleteUser(id):
    mongo.db.users.delete_one({'_id': ObjectId(id)})
    return 'Eliminado'


@app.route('/users/<id>', methods=["PUT"])
def updateUser(id):
    mongo.db.users.update_one({'_id': ObjectId(id)}, {
        '$set': {
            "nombre": request.json['nombre'],
            "correo": request.json['correo'],
            "foto": request.json['foto'],
            "mascotas": request.json["mascotas"]
        }
    })
    return "Actualizado"


@app.route('/ducks', methods=["POST"])
def createDuck():
    mongo.db.ducks.insert_one({
        'nombre':request.json['nombre'],
        'año':request.json['año'],
        'dueño':request.json['dueño'],
        'foto':request.json['foto'],
        
    })
    return 'received'


@app.route('/ducks', methods=["GET"])
def getDucks():
    ducks = []
    for doc in mongo.db.ducks.find():
        print(doc)
        ducks.append({
            '_id': str(ObjectId(doc['_id'])),
            'nombre': doc['nombre'],
            'dueño': doc['dueño'],
            'año': doc['año'],
            'foto': doc["foto"]
        })
    return jsonify(ducks)


@app.route('/duck/<id>', methods=["GET"])
def getDuck(id):
    duck = mongo.db.ducks.find_one({'_id': ObjectId(id)})
    return jsonify({
        '_id': str(ObjectId(duck['_id'])),
        'nombre': duck['nombre'],
        'dueño': duck['dueño'],
        'año': duck['año'],
        "foto": duck["foto"]
    })


@app.route('/ducks/<id>', methods=["DELETE"])
def deleteDuck(id):
    mongo.db.ducks.delete_one({'_id': ObjectId(id)})
    return 'Eliminado'


@app.route('/ducks/<id>', methods=["PUT"])
def updateDuck(id):
    mongo.db.ducks.update_one({'_id': ObjectId(id)}, {
        '$set': {
            "nombre": request.json['nombre'],
            "dueño": request.json['dueño'],
            "foto": request.json['foto'],
            "año": request.json["año"]
        }
    })
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
