from datetime import datetime
from sqlalchemy import and_,or_
from sqlalchemy_utils import database_exists
from flask import Flask, render_template,request, session
from models import db, Translation, User

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
        db.session.add(User(name="Djamel"))
        db.session.add(User(name="Yahya"))
        db.session.commit()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/traduction', methods=['GET', 'POST'])
def traduction():
    id_traduction = request.args.get('id_traduction')
    if request.method == 'POST':
        traduction = Translation.query.filter(Translation.id == id_traduction).first()
        trg = request.form[f"translation{id_traduction}"]
        issue = request.form.get(f"issue{id_traduction}")
        if trg or issue:
            traduction.trg = trg
            traduction.translated = True
            traduction.translatedOn = datetime.utcnow()
            traduction.translatedBy = session.get("user", default="Djamel")
            traduction.issue = True if issue else False

         # li ce commentaire stp
         # il ma dit meme si la phrase ne peut pas etre traduite il a coché sur issue
        # et l'utilisateur fait entrer du text on garde le text et le checkbox et a True

        db.session.commit()

    not_translated = Translation.query.filter(Translation.translated == False).all()
    return render_template('traductions.html', traductions=not_translated)


@app.route('/score', methods=['GET', 'POST'])
def score():
    username = session.get("user", default="Yahya")
    if request.method == 'POST':

        id_traduction = request.args.get('id_traduction')
        traduction = Translation.query.filter(Translation.id == id_traduction).first()
        # Si c'est pas le meme user qui a traduit
        if username != traduction.translatedBy:
            traduction.verified = True
            traduction.quality = int(request.form['score'+id_traduction])
            traduction.verifiedOn = datetime.utcnow()
            traduction.verifiedBy = username
            traduction.com = request.form['com'+id_traduction]
            db.session.commit()


        # TODO: afficher un message d'erreur si c'est le meme...
        # else: ...
    not_scored = Translation.query.filter(and_(Translation.translated == True,
                                               Translation.verified == False,
                                               Translation.translatedBy != username,
                                               Translation.issue==False
                                               )).all()
    return render_template('score.html', traductions=not_scored)


@app.route('/reserch', methods=['GET', 'POST'])
def reserch():
    page = request.args.get('page')
    string = request.form['recherch']
    if request.method == 'POST' and string != '':
        if page == 'traduction':
            traduction = Translation.query.filter(and_(Translation.src.like('%' + string + '%'),
                                                       Translation.translated==False)).all()
            return render_template('traductions.html', traductions=traduction)
        elif page == 'score':
            traduction = Translation.query.filter(and_(or_(Translation.trg.like('%' + string + '%'),
                                                      Translation.src.like('%' + string + '%'))),
                                                  Translation.translated==True,
                                                  Translation.verified==False,
                                                  Translation.issue==False).all()
            return render_template('score.html', traductions=traduction)

if __name__ == '__main__':
    app.run(debug=True,port=8080)