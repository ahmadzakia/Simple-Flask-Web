#!venv/bin/python
import os
from flask import Flask, escape, url_for, abort, redirect, make_response, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
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
    def serializable(self):
        return{
            'first_name':self.first_name,
            'last_name':self.last_name,
            'email':self.email,
            'is_active':self.active,
        }
def build_sample_db():
    import string
    db.drop_all()
    db.create_all()

    first_user = User(
        first_name = 'Ahmad Zaki',
        last_name = 'Anshori',
        email = 'admin@admin.com',
        active = True
    )
    db.session.add(first_user)
    for x in range(10):
        db.session.add(
            User(      
            first_name = 'User ',
            last_name = ''+str(x),
            email = 'user'+str(x)+'@gmail.com',
            active = False
            ))
    db.session.commit()
    
    return
@app.route('/api/v1.0/get_all_members/', methods=['POST'])
def getAllMembers():
    all_user = User.query.all()
    response = [row.serializable() for row in all_user]
    return jsonify({
            "data":response
        })

@app.route('/api/v1.0/get_member_by_id/<int:member_id>', methods=['POST'])
def getMemberById(member_id):
    member = User.query.get(member_id)
    if member==None:
        return jsonify({
            "error": {
                "code": 404,
                "message": "ID not found"
              }
            })
    return jsonify({
        "data":member.serializable()
        })

@app.route('/api/v1.0/get_member_by_email/<email>', methods=['POST'])
def getMemberByEmail(email):
    member = User.query.filter_by(email=email).first()
    if member==None:
        return jsonify({"error": {
                "code": 404,
                "message": "Email not found"
              }
            })
    return jsonify({
        "data":member.serializable()
        })


@app.route('/member', methods = ['GET'])
def member():
    if request.method == 'GET':
        all_user = User.query.all();
        data = {
            'all_user': all_user
        }

        return render_template('member.html', data=all_user)
    else:
        return render_template('404.html')

# Flask index route
@app.route('/index', methods = ['POST', 'GET'])
@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'GET':
        last_user = User.query.order_by(User.id.desc()).first()
        data = {
            'user' : last_user
        }
        return render_template('index.html',data=data)
    else:
        return render_template('404.html')

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')

if __name__ == '__main__':

    # Build a sample db on the fly, if one does not exist yet.
    app_dir = os.path.realpath(os.path.dirname(__file__))
    database_path = os.path.join(app_dir, app.config['DATABASE_FILE'])
    if not os.path.exists(database_path):
        build_sample_db()

    # Start app
    # app.run()
    app.run(debug=True)