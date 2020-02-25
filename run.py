from datetime import datetime

from sqlalchemy.orm import session
from sqlalchemy_utils import database_exists
from flask import Flask, render_template, url_for,request
from models import db, Translation

app = Flask(__name__, template_folder="app/templates/",
                      static_folder="app/templates/")
DB_URI = 'sqlite:///test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
if not database_exists(DB_URI):
    with app.app_context():
        db.create_all()


db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/traduction', methods=['GET', 'POST'])
def traduction():
    id_traduction = request.args.get('id_traduction')
    if request.method == 'POST':
        traduction = Translation.query.filter(id=id_traduction).first()
        traduction.trg= request.form['phrase-traduit']
        traduction.translated=True
        traduction.translatedOn = datetime.utcnow
        traduction.translatedBy = session['user']
        traduction.issue = request.form['issue']

         # li ce commentaire stp
         # il ma dit meme si la phrase ne peut pas etre traduite il a coché sur issue
        # et l'utilisateur fait entrer du text on garde le text et le checkbox et a True

        db.session.commit()
    return render_template('traductions.html',Translation.query.filter(translated=False).all())

@app.route('/score')
def score():
    return render_template('score.html')


if __name__ == '__main__':
    app.run(debug=True,port=8080)