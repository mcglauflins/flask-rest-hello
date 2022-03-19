from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorite_people = db.relationship("FavoritePeople")
    favorite_vehicles = db.relationship("FavoriteVehicles")
    favorite_planet = db.relationship("FavoritePlanet")

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favorite_people": self.favorite_people,
            "favorite_vehicles": self.favorite_vehicles,
            "favorite_planet": self.favorite_planet
            # do not serialize the password, its a security breach
        }

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def check_password_hash(self, password):
        return check_password_hash(self.password, password)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    birth_year = db.Column(db.String(120), unique=True, nullable=True)
    eye_color = db.Column(db.String(120), unique=True, nullable=True)
    gender = db.Column(db.String(120), unique=True, nullable=True)
    hair_color = db.Column(db.String(120), unique=True, nullable=True)
    height = db.Column(db.String(120), unique=True, nullable=True)
    mass = db.Column(db.String(120), unique=True, nullable=True)
    skin_color = db.Column(db.String(120), unique=True, nullable=True)
    homeworld = db.Column(db.String(120), unique=True, nullable=True)
    films = db.Column(db.String(120), unique=True, nullable=True)
    species = db.Column(db.String(120), unique=True, nullable=True)
    starships = db.Column(db.String(120), unique=True, nullable=True)
    vehicles = db.Column(db.String(120), unique=True, nullable=True)


class Vehicles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    model = db.Column(db.String(120), unique=True, nullable=True)
    vehicles = db.Column(db.String(120), unique=True, nullable=True)
    manufacturer = db.Column(db.String(120), unique=True, nullable=True)
    length = db.Column(db.String(120), unique=True, nullable=True)
    cost_in_credits = db.Column(db.String(120), unique=True, nullable=True)
    crew = db.Column(db.String(120), unique=True, nullable=True)
    passengers = db.Column(db.String(120), unique=True, nullable=True)
    max_atmosphering_speed = db.Column(
        db.String(120), unique=True, nullable=True)
    cargo_capacity = db.Column(db.String(120), unique=True, nullable=True)
    consumables = db.Column(db.String(120), unique=True, nullable=True)


class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    diameter = db.Column(db.String(120), unique=True, nullable=True)
    rotation_period = db.Column(db.String(120), unique=True, nullable=True)
    orbital_period = db.Column(db.String(120), unique=True, nullable=True)
    gravity = db.Column(db.String(120), unique=True, nullable=True)
    population = db.Column(db.String(120), unique=True, nullable=True)
    climate = db.Column(db.String(120), unique=True, nullable=True)
    terrain = db.Column(db.String(120), unique=True, nullable=True)
    surface_water = db.Column(db.String(120), unique=True, nullable=True)


class FavoritePeople(db.Model):
    user_id = db.Column(db.ForeignKey('user.id'), primary_key=True)
    person_id = db.Column(db.ForeignKey('person.id'), primary_key=True)
    person = db.relationship("Person")


class FavoriteVehicles(db.Model):
    user_id = db.Column(db.ForeignKey('user.id'), primary_key=True)
    vehicle_id = db.Column(db.ForeignKey('vehicles.id'), primary_key=True)
    vehicle = db.relationship("Vehicles")


class FavoritePlanet(db.Model):
    user_id = db.Column(db.ForeignKey('user.id'), primary_key=True)
    planet_id = db.Column(db.ForeignKey('planet.id'), primary_key=True)
    planet = db.relationship("Planet")
