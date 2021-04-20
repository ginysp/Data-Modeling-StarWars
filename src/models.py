from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    firstname = db.Column(db.String(15), nullable=False)
    lastname = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(15), nullable=False)    

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email
            #"favorites": list(map(lambda x: x.serialize(), self.favorites))           
        }
        

class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(28), nullable=False)
    
    def __repr__(self):
        return '<People %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
            #"favorites": list(map(lambda x: x.serialize(), self.favorites))           
        }
    
    def getAllPeople():
        all_people = People.query.all()
        all_people = list(map(lambda x: x.serialize(), all_people))
        return all_people
    
    def getPerson(id):
        person = People.query.get(id)
        return person.serialize()

class Favorites(db.Model):
    __tablename__= 'favorites'
    id = db.Column(db.Integer, primary_key=True)    
    date = db.Column(db.String(10), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    planets_id = db.Column(db.Integer, db.ForeignKey("planets.id"))
    people_id = db.Column(db.Integer, db.ForeignKey("people.id"))
    films_id = db.Column(db.Integer, db.ForeignKey("films.id"))
    user= db.relationship('User', lazy=True)  
    planets= db.relationship('Planets', lazy=True)  
    people= db.relationship('People', lazy=True)  
    films= db.relationship('Films', lazy=True)  

    def serialize(self):
        if self.people_id is not None:
            value =  People.query.get(self.people_id).name
        elif self.planets_id is not None:
            value =  Planets.query.get(self.planets_id).name
        elif self.films_id is not None:
            value =  Films.query.get(self.films_id).title
        return {
            "id": self.id,
            "name": value         
            #"date": self.date,
        }
    def getAllFavorites(id):
        favorites = Favorites.query.get(id)        
        favorites = list(map(lambda x: x.serialize(), favorites))
        return favorites


class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(28), nullable=False)

    def __repr__(self):
        return '<Planets %r>' % self.name    

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
            #"favorites": list(map(lambda x: x.serialize(), self.favorites))           
        }
    def getAllPlanets():
        all_planets = Planets.query.all()
        all_planets = list(map(lambda x: x.serialize(), all_planets))
        return all_planets

class Films(db.Model):
    __tablename__ = 'films'
    id = db.Column(db.Integer, primary_key=True)    
    title = db.Column(db.String(100), nullable=False)  
    director = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Films %r>' % self.title    

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title
            #"favorites": list(map(lambda x: x.serialize(), self.favorites))           
        }
    def getAllFilms():
        all_films = Films.query.all()
        all_films = list(map(lambda x: x.serialize(), all_films))
        return all_films

