#!venv/bin/python
import os
from flask import Flask, escape, url_for, abort, redirect, make_response, request, render_template
from flask_sqlalchemy import SQLAlchemy

# Create Flask application
app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)


def build_sample_db():
    import string
    db.drop_all()
    db.create_all()
    return

# Flask index route
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':

    # Build a sample db on the fly, if one does not exist yet.
    app_dir = os.path.realpath(os.path.dirname(__file__))
    database_path = os.path.join(app_dir, app.config['DATABASE_FILE'])
    if not os.path.exists(database_path):
        build_sample_db()

    # Start app
    # app.run()
    app.run(debug=True)