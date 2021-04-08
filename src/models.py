from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    firstname = db.Column(db.String(15), nullable=False)
    lastname = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(15), unique=True, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email           
        }

class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(28), nullable=False)
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name           
        }
    
    def getAllPeople():
        all_people = People.query.all()
        all_people = list(map(lambda x: x.serialize(), all_people))
        return all_people
    
    def getPerson(id):
        person = People.query.get(id)
        return person.serialize()


class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(28), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name           
        }
    def getAllPlanets():
        all_planets = Planets.query.all()
        all_planets = list(map(lambda x: x.serialize(), all_planets))
        return all_planets

class Films(db.Model):
    __tablename__ = 'films'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(28), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title           
        }
    def getAllFilms():
        all_films = Films.query.all()
        all_films = list(map(lambda x: x.serialize(), all_films))
        return all_films
    