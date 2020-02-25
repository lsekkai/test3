from flask import Flask, render_template, url_for
from models import db


app = Flask(
    __name__,
    template_folder="app/templates/",
    static_folder="app/templates/"
)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db.init_app(app)


with app.app_context():
    db.drop_all()
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/traductions')
def traductions():
    return render_template('traductions.html')


@app.route('/score')
def score():
    return render_template('score.html')


if __name__ == '__main__':
    app.run(debug=True,port=8080)