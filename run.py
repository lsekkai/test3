from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__, template_folder="modules/templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/djamel/PycharmProjects/traduction/test.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

def create_app():
    app = Flask(__name__)
    db.init_app(app)
    return app

@app.before_first_request
def create_tables():
    db.create_all()

app = create_app()
app.app_context().push()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80),    nullable=False)
    email = db.Column(db.String(120),    nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/')
def index():

    return render_template('./templates/index.html')

if __name__ == '__main__':
    app.run(debug=True,port=8080)