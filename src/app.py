import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, User, Character, Favorite, Planet, Vehicle



BASEDIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASEDIR,"swapi.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["ENV"] = "development"


db.init_app(app)
CORS(app)
Migrate(app, db)


@app.route("/")
def home():
    return "prueba exitosa"

@app.route("/people", methods=["GET"])
def people():
    character = Character.query.all()
    character_serialized = list(map( lambda character: character.serialize(), character))
    return jsonify(character_serialized)

@app.route("/character/<int:id>", methods=["GET"])
def character(id):
    character = Character.query.get(id)
    character_serialized = character.serialize()
    return jsonify(character_serialized)

@app.route("/add_character", methods=["POST"])
def add_character():
    character = Character()
    character.name = request.json.get("name")
    character.hair_color = request.json.get("hair_color")
    character.birth_year = request.json.get("birth_year")

    db.session.add(character)
    db.session.commit()

    return jsonify({
        "msg": "personaje añadido correctamente"
        }), 200

@app.route("/planets", methods=["GET"])
def planets():
    planet = Planet.query.all()
    planet_serialized = list(map( lambda planet: planet.serialize(), planet))
    return jsonify(planet_serialized)

@app.route("/planets/<int:id>", methods=["GET"])
def planet(id):
    planet = Planet.query.get(id)
    planet_serialized = planet.serialize()
    return jsonify(planet_serialized)

@app.route("/vehicles", methods=["GET"])
def vehicles():
    vehicle = Vehicle.query.all()
    vehicle_serialized = list(map( lambda vehicle: vehicle.serialize(), vehicle))
    return jsonify(vehicle_serialized)

@app.route("/vehicles/<int:id>", methods=["GET"])
def vehicle(id):
    vehicle = Vehicle.query.get(id)
    vehicle_serialized = vehicle.serialize()
    return jsonify(vehicle_serialized)


@app.route("/users", methods=["GET"])
def users():
    user = User.query.all()
    user_serialized = list(map( lambda user: user.serialize(), user))
    return jsonify(user_serialized)

@app.route("/users/favorites/<int:user_id>", methods=["GET"])
def user_favorites(user_id):
    user= User.query.get(user_id)
    favorite = Favorite.query.filter_by(user_id=user_id).all()
    favorite_serialized = list(map( lambda favorite: favorite.serialize(), favorite))
    return jsonify(favorite_serialized)

@app.route("/favorite/planet/<int:planet_id>", methods=["POST"])
def add_favorite_planet(planet_id):
    favorite = Favorite()
    user_id = request.json.get("user_id")

    found_user = Favorite.query.filter_by(user_id=user_id).all()

    if found_user is None:
        return jsonify({
            "msg": "no existe este usuario"
        }), 400

    favorite.planet_id = request.json.get("planet_id")
    favorite.user_id = user_id

    db.session.add(favorite)
    db.session.commit()

    return jsonify({
        "msg": "favorito añadido correctamente"
    }), 200

@app.route("/favorite/people/<int:character_id>", methods=["POST"])
def add_favorite_character(character_id):
    favorite = Favorite()
    user_id = request.json.get("user_id")

    found_user = Favorite.query.filter_by(user_id=user_id).all()

    if found_user is None:
        return jsonify({
            "msg": "no existe este usuario"
        }), 400

    favorite.character_id = request.json.get("character_id")
    favorite.user_id = user_id

    db.session.add(favorite)
    db.session.commit()


    return jsonify({
        "msg": "favorito añadido correctamente"
    }), 200

@app.route("/favorite/planet/<int:planet_id>/", methods=["DELETE"])
def delete_favorite_planet(planet_id):
    favorite = Favorite.query.get(planet_id)
    
    db.session.delete(favorite)
    db.session.commit()

    return "favorito eliminado correctamente"

@app.route("/favorite/people/<int:character_id>/", methods=["DELETE"])
def delete_favorite_character(character_id):
    favorite = Favorite.query.get(character_id)
    
    db.session.delete(favorite)
    db.session.commit()

    return "favorito eliminado correctamente"

@app.route("/add_user", methods=["POST"])
def add_user():
    user = User()
    email = request.json.get("email")
    password = request.json.get("password")

    found_email = User.query.filter_by(email=email).first()

    if found_email is not None:
        return jsonify({
            "msg": "Ya existe un usuario ingresado con este email"
        }), 400

    user.name = request.json.get("name")
    user.email = email
    user.password = password

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "msg": "usurario añadido correctamente"
        }), 200

if __name__ == "__main__":
    app.run(host="localhost", port=34025)