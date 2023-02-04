from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(250))
    password = db.Column(db.String(10))
    favorites = db.relationship("Favorite")
    
    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }

class Character(db.Model):
    __tablename__ = "characters"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    hair_color = db.Column(db.String(100))
    birth_year = db.Column(db.String(100))
    planet = db.relationship("Planet", back_populates="character", uselist=False)
    vehicle = db.relationship("Vehicle", back_populates="character", uselist=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "hair_color": self.hair_color,
            "birth_year": self.birth_year,
            "planet": self.planet,
            "vehicle": self.vehicle,
        }

class Planet(db.Model):
    __tablename__ = "planets"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    population = db.Column(db.Integer)
    character_id = db.Column (db.Integer, db.ForeignKey("characters.id"))
    character = db.relationship("Character", back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "character_id": self.character_id
        }


class Vehicle(db.Model):
    __tablename__ = "vehicles"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    crew = db.Column(db.Integer)
    character_id = db.Column(db.Integer, db.ForeignKey("characters.id"))
    character = db.relationship("Character", back_populates="vehicle")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "crew": self.population,
            "character_id": self.character_id
        }

class Favorite(db.Model):
    __tablename__ = "favorites"
    id = db.Column(db.Integer, primary_key = True)
    planet_id = db.Column(db.Integer, db.ForeignKey("planets.id")) 
    character_id = db.Column(db.Integer, db.ForeignKey("characters.id")) 
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False) 
    
    def serialize(self):
        return {
            "id": self.id,
            "planet_id": self.planet_id,
            "character_id": self.character_id,
            "user_id": self.user_id,
        }