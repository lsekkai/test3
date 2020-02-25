from datetime import datetime

from sqlalchemy_utils import database_exists
from flask import Flask, render_template, url_for, request, session
from models import db, Translation

app = Flask(__name__, template_folder="app/templates/",
                      static_folder="app/templates/")
DB_URI = 'sqlite:///test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
db.init_app(app)
if not database_exists(DB_URI):
    with app.app_context():
        db.create_all()
        for i in range(1, 21):
            db.session.add(Translation(src=f"text{i}"))
        db.session.commit()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/traduction', methods=['GET', 'POST'])
def traduction():
    id_traduction = request.args.get('id_traduction')
    if request.method == 'POST':
        traduction = Translation.query.filter(Translation.id == id_traduction).first()
        traduction.trg = request.args.get("traduction{id_traduction}")
        traduction.translated = True
        traduction.translatedOn = datetime.utcnow()
        traduction.translatedBy = session.get("user", default="Djamel")
        traduction.issue = request.args.get("exampleCheck{id_traduction}")

         # li ce commentaire stp
         # il ma dit meme si la phrase ne peut pas etre traduite il a coché sur issue
        # et l'utilisateur fait entrer du text on garde le text et le checkbox et a True

        db.session.commit()

    not_translated = Translation.query.filter(Translation.translated == False).all()
    return render_template('traductions.html', traductions=not_translated)


@app.route('/score', methods=['GET', 'POST'])
def score():
    id_traduction = request.args.get('id_traduction')
    if request.method == 'POST':
        username = session.get("user", default="Yahya")
        # Si c'est pas le meme user qui a traduit
        if username != traduction.translatedBy:
            traduction.verified = True
            traduction.verifiedOn = datetime.utcnow()
            traduction.verifiedBy = username
        # TODO: afficher un message d'erreur si c'est le meme...
        # else: ...
    not_scored = Translation.query.filter(Translation.translated == True and
                                          Translation.verified == False).all()
    return render_template('score.html', traductions=not_scored)


if __name__ == '__main__':
    app.run(debug=True,port=8080)