from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


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

    def __repr__(self):
        return '<Client {}>'.format(self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    creation_date = db.Column(db.DateTime, index=True, unique=True, default=datetime.utcnow)
    last_update = db.Column(db.DateTime, index=True, unique=True, default=datetime.utcnow)
    user_id = db.Column(db.String(24), db.ForeignKey("client.id"))
    tasks = db.relationship("Task", backref="parent", lazy="dynamic")

    def __repr__(self):
        return '<Project {}>'.format(self.title)


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


