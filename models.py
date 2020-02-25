from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

 
class User(db.Model):

    __tablename__ = "users"
    id = db.Column("id", db.Integer(), primary_key=True)
    name = db.Column("name", db.String(255))


class Translation(db.Model):

    __tablename__ = "translations"
    id = db.Column(db.Integer(), primary_key=True)
    src = db.Column(db.String(255))
    trg = db.Column(db.String(255))
    issue = db.Column(db.Boolean)
    translated = db.Column(db.Boolean)
    translatedOn = db.Column(db.Date)
    quality = db.Column(db.Integer)
