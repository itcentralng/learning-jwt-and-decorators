from flask import Flask, request, g
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash as gph
from werkzeug.security import check_password_hash as cph

import jwt

import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE')
app.config['SECRET_KEY'] = "somesecret"

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    password = db.Column(db.String)

with app.app_context():
    db.create_all()

from functools import wraps

def login_required(func):
    @wraps(func)
    def wrapper():
        try:
            token = request.headers['Authorization']
            token = token.split()[-1]
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            # {"id": user.id}
            user = User.query.filter_by(id=payload['id']).first()
            g.user = user
            return func()
        except:
            return "Invalid Token", 401
    return wrapper

@app.get('/')
@login_required
def index():
    return "Its working - your email is"+g.user.email

@app.post('/signin')
def signin():
    email = request.json.get('email')
    password = request.json.get('password')

    user = User.query.filter_by(email=email).first()
    if user and cph(user.password, password):
        token = jwt.encode({"id": user.id}, app.config['SECRET_KEY'], algorithm="HS256")
        return {"token":token.decode()}
    return "Invalid Credentials", 401

@app.post('/signup')
def signup():
    email = request.json.get('email')
    password = request.json.get('password')

    new_user = User(email=email, password=gph(password))
    db.session.add(new_user)
    db.session.commit()
    return "Signup Successful!"

if __name__ == "__main__":
    app.run()