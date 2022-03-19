"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Person, Planet, Vehicles
# from models import Person

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

app.config["JWT_SECRET_KEY"] = "super-secret"
jwt = JWTManager(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/user', methods=['GET'])
def user():
    db.session.query(User).all()
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }
    return jsonify(response_body), 200

@app.route('/person', methods=['GET'])
def get_person():
    person = Person.query(Person)
    person = [person.serialize() for person in person]

    return jsonify(person), 200

@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicles.query.all()
    vehicles = [vehicles.serialize() for vehicles in vehicles]

    return jsonify(vehicles), 200

@app.route('/planet', methods=['GET'])
def get_planet():
    planet = Planet.query.all()
    planet = [planet.serialize() for planet in planet]

    return jsonify(planet), 200

@app.route('/create_user', methods=['POST'])
def create_user():
    email = request.json.get("email", None)
    password = request.json.get("pass", None)
    old_user = db.session.query(User).filter_by(email=email).one_or_none()
    if old_user is None and all([email, password]):
        new_user = User(email=email, password=password, is_active=True)
        db.session.add(new_user)
        db.session.commit()
        response_body = {
            "msg": "The user {} was created.".format(email)
        }
        return jsonify(response_body), 200
    return jsonify({"msg": "Invalid request."}), 400


@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("pass", None)
    user = db.session.query(User).filter_by(email=email).one_or_none()
    if user is not None:
        if user.check_password_hash(password):
            access_token = create_access_token(identity=email)
            return jsonify(access_token=access_token)
    return jsonify({"msg": "Invalid cedentials."}), 401


@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
