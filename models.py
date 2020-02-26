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
    translatedBy = db.Column(db.String, default="---")
    quality = db.Column(db.Integer, default=0)
    verified = db.Column(db.Boolean, default=False)
    verifiedOn = db.Column(db.Date, nullable=True)
    verifiedBy = db.Column(db.String, default="---")
    com = db.Column(db.String, default="---")


class User(db.Model):
    __tablename__ = "user"
    id = db.Column("id", db.Integer(), primary_key=True)
    name = db.Column("name", db.String(255), nullable=False, unique=True)
    avrg = db.Column(db.Integer, default=0)

    @property
    def average_score_user(self):
        translations = Translation.query.filter(Translation.translatedBy == self.name).all()
        if not translations:
            return 0
        scores = [trans.quality for trans in translations]
        self.avrg =  int(round(sum(scores) / len(scores), 2))
        return  self.avrg

    def Nmaxelements(self):
        final_list = []
        list1 = (User.query.all())
        for user in list1:
            user.average_score_user
        length = len(User.query.all()) if len(User.query.all())<5 else 5
        for i in range(0, length):
            max1 = 0
            for j in range(len(list1)):
                if list1[j].avrg > max1:
                    max1 = list1[j].avrg
            string = list1[j].name+" : "+str(list1[j].avrg)
            list1.remove(list1[j])
            final_list.append(string)
        return (final_list)