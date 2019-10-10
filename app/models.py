from datetime import datetime
from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


class Developer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    dt = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Developer {}>'.format(self.body)

class HousingComplex(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    developer_id = db.Column(db.Integer, db.ForeignKey('developer.id'))
    name = db.Column(db.String(128))
    name_eng = db.Column(db.String(128))
    region = db.Column(db.String(128))
    region_city = db.Column(db.String(128))
    district_direction = db.Column(db.String(64))
    atd = db.Column(db.String(128))
    zone = db.Column(db.String(128))
    lat = db.Column(db.Float(8, 5))
    lng = db.Column(db.Float(8, 5))
    dt = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<HousingComplex {}>'.format(self.body)

class House(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    developer_id = db.Column(db.Integer, db.ForeignKey('developer.id'))
    housing_complex_id = db.Column(db.Integer, db.ForeignKey('housing_complex.id'))
    name = db.Column(db.String(128))
    name_corpus = db.Column(db.String(64))
    address = db.Column(db.String(256))
    house_type = db.Column(db.String(64))
    house_class = db.Column(db.String(128))
    decoration = db.Column(db.String(64))
    agreement = db.Column(db.String(8))
    date_complete = db.Column(db.String(16))
    stage = db.Column(db.String(16))
    dt = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<House {}>'.format(self.body)

class Object(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    developer_id = db.Column(db.Integer, db.ForeignKey('developer.id'))
    housing_complex_id = db.Column(db.Integer, db.ForeignKey('housing_complex.id'))
    house_id = db.Column(db.Integer, db.ForeignKey('house.id'))
    room = db.Column(db.Integer)
    square = db.Column(db.Float)
    price = db.Column(db.Float)
    price_meter = db.Column(db.Float)
    floor = db.Column(db.Integer)
    floor_number = db.Column(db.Integer)
    house_number = db.Column(db.Integer)
    section_number = db.Column(db.Integer)
    type_studio = db.Column(db.String(16))
    type = db.Column(db.String(32))
    decoration = db.Column(db.String(16))
    price_discont = db.Column(db.Float)
    source = db.Column(db.String(128))
    dt = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<House {}>'.format(self.body)
