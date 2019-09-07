#!venv/bin/python
import os
from flask import Flask, escape, url_for, abort, redirect, make_response, request, render_template
from flask_sqlalchemy import SQLAlchemy

# Create Flask application
app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    active = db.Column(db.Boolean())

    def __str__(self):
        return self.email

def build_sample_db():
    import string
    db.drop_all()
    db.create_all()
    return

# Flask index route
@app.route('/')
def index():
    current_user = User(
                first_name = 'Ahmad Zaki',
                last_name = 'Anshori',
                email = 'email@gmail.com',
                active = True
            )
    data = {
        'user' : current_user
    }
    return render_template('index.html',data=data)


if __name__ == '__main__':

    # Build a sample db on the fly, if one does not exist yet.
    app_dir = os.path.realpath(os.path.dirname(__file__))
    database_path = os.path.join(app_dir, app.config['DATABASE_FILE'])
    if not os.path.exists(database_path):
        build_sample_db()

    # Start app
    # app.run()
    app.run(debug=True)