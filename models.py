from app import db, app
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required,\
                                jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    projects = db.relationship("Project", backref="creator", lazy="dynamic")

    def __init__(self, name, username, email, password):
        self.name = name
        self.username = username
        self.email = email
        self.set_password(password)

    def __repr__(self):
        return '<Client {}>'.format(self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'email': self.email
        }

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        client = Client.query.get(data['id'])
        return client


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    creation_date = db.Column(db.DateTime, index=True, unique=True, default=datetime.utcnow)
    last_update = db.Column(db.DateTime, index=True, unique=True, default=datetime.utcnow)
    client_id = db.Column(db.String(24), db.ForeignKey("client.id"))
    tasks = db.relationship("Task", backref="parent", lazy="dynamic")

    def __init__(self, title, client_id):
        self.title = title
        self.client_id = client_id
        current_client = Client.query.filter_by(username=get_jwt_identity()).first()
        self.user_id = current_client.id

    def __repr__(self):
        return '<Project {}>'.format(self.title)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'created_at': self.creation_date,
            'updated_at': self.last_update
        }


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    order = db.Column(db.String(30), index=True, unique=True)
    creation_date = db.Column(db.DateTime, index=True, unique=True, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, index=True, unique=True, default=datetime.utcnow)
    completed = db.Column(db.Boolean, index=True)
    project_id = db.Column(db.String(24), db.ForeignKey("project.id"))

    def __repr__(self):
        return '<Task {}>'.format(self.title)


class TokenRevoked(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return '<RevokedToken {}>'.format(self.jti)


if not os.path.exists("database/app.db"):
    db.create_all()
