from sqlalchemy_utils import database_exists
from flask import Flask, render_template, url_for,request
from models import db


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

#
@app.route('/traductions')
def traductions():

    return render_template('traductions.html')


@app.route('/traduction', methods=['GET', 'POST'])
def traduction():
    request.method == 'POST'
    id_traduction = request.args.get('id_traduction')
    return render_template('traductions.html')

@app.route('/score')
def score():
    return render_template('score.html')


if __name__ == '__main__':
    app.run(debug=True,port=8080)