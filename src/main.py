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
from models import db, User, People, Planets, Films, Favorites
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = os.environ.get('SALA_TRES')
jwt = JWTManager(app)
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/register/', methods=['POST'])
def handle_register():
    register_pack = request.json        
    newuser = User(username= register_pack["username"], firstname= register_pack["firstname"], lastname= register_pack["lastname"], email= register_pack["email"], password= register_pack["password"])
    print(newuser)
    db.session.add(newuser)
    db.session.commit()
    response_body = {
        "status": "Ok"
    }
    status_code = 200 
    
    return jsonify(response_body), status_code

@app.route("/login", methods=["POST"])
def login():
    user = request.json.get("username", None)
    pasw = request.json.get("password", None)
    finduser= User.query.filter_by(username=user, password=pasw).first()
    if finduser is None:
        return jsonify({"msg": "Invalid Information"}), 401

    access_token = create_access_token(identity=user)
    return jsonify(access_token=access_token)

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route('/people', methods=['GET'])
def handle_people():  
    
    return jsonify(People.getAllPeople()), 200

#Start App routes for Favorites

@app.route('/favorites/', methods=['POST'])
@jwt_required()
def handle_favorites():
    favorites_pack = request.json
    print("Request", favorites_pack)    
    user = favorites_pack["username"]
    fav = favorites_pack["value"]
    finduser = User.query.filter_by(username= user).first()
    findpeople = People.query.filter_by(name= fav).first()
    findplanets = Planets.query.filter_by(name= fav).first()
    findfilms = Films.query.filter_by(title= fav).first()    
    if findpeople is not None:
        peoplefavorites = Favorites(user_id= finduser.id, people_id= findpeople.id)
        db.session.add(peoplefavorites)
    elif findplanets is not None:
        planetsfavorites = Favorites(user_id= finduser.id, planets_id= findplanets.id)
        db.session.add(planetsfavorites)
    elif findfilms is not None:        
        filmsfavorites = Favorites(user_id= finduser.id, films_id= findfilms.id)        
        db.session.add(filmsfavorites)
    db.session.commit()
    response_body = {
        "status": "Ok"
    }
    status_code = 200 
    
    return jsonify(response_body), status_code

@app.route('/favorites/<int:id>', methods=['DELETE'])
@jwt_required()
def handle_deletefavorites(id):
    favdel= Favorites.query.get(id)
    if favdel is None:
        raise APIException('Favorite not found', status_code=404)
    db.session.delete(favdel)
    db.session.commit()
    response_body = {
        "status": "Ok"
    }
    status_code = 200
    
    return jsonify(response_body), status_code

@app.route('/favorites/', methods=['GET'])
@jwt_required()
def handle_favoritesget():

    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    response = Favorites.query.filter_by(user_id=user.id)
    all_favorites = list(map(lambda x: x.serialize(), response))
    print(all_favorites)
    return jsonify(all_favorites), 200

#End App routes for Favorites

@app.route('/planets', methods=['GET'])
def handle_planets():  
    
    return jsonify(Planets.getAllPlanets()), 200

@app.route('/films', methods=['GET'])
def handle_films():  
    
    return jsonify(Films.getAllFilms()), 200

@app.route('/people/<int:id>', methods=['GET'])
def handle_peopleid(id):  
    
    return jsonify(People.getPerson(id)), 200



# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)


