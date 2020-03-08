from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Translation(db.Model):

    __tablename__ = "translation"
    id = db.Column(db.Integer(), primary_key=True)
    src = db.Column(db.String(255), unique=True)
    trg = db.Column(db.String(255), default="---")
    issue = db.Column(db.Boolean, default=False)
    translated = db.Column(db.Boolean, default=False)
    translatedOn = db.Column(db.Date, default=datetime.utcnow)
    translatedBy = db.Column(db.String(255), default="---")
    quality = db.Column(db.Integer, default=0)
    verified = db.Column(db.Boolean, default=False)
    verifiedOn = db.Column(db.Date, nullable=True)
    verifiedBy = db.Column(db.String(255), default="---")
    com = db.Column(db.Text, default="---")


class User(db.Model):
    __tablename__ = "user"
    id = db.Column("id", db.Integer(), primary_key=True)
    name = db.Column("name", db.String(255), nullable=False, unique=True)
    avrg = db.Column(db.Integer, default=0)
    def __repr__(self):
        return self.name

    @property
    def average_score_user(self):
        translations = Translation.query.filter(Translation.translatedBy == self.name).all()
        if not translations:
            return 0
        scores = [trans.quality for trans in translations if trans.verified]
        self.avrg = round(sum(scores) / len(scores), 2)
        return self.avrg

    def Nmaxelements(self):
        users = sorted(User.query.all(),
                       key=lambda u: u.average_score_user, reverse=True)[:5]
        return [f"{u.name} : {u.avrg}" for u in users]
