from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id              = db.Column(db.Integer, primary_key=True)
    username        = db.Column(db.String(64), index=True, unique=True)
    email           = db.Column(db.String(120), index=True, unique=True)
    password_hash   = db.Column(db.String(128))
    projects        = db.relationship('Project', backref='user', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Project(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    number      = db.Column(db.String(140))
    name        = db.Column(db.String(140))
    timestamp   = db.Column(db.DateTime, index=True)
    value       = db.Column(db.Integer, nullable=False)
    completed   = db.Column(db.Boolean, default=False, nullable=False)
    client      = db.Column(db.String(140))
    user_id     = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    tasks       = db.relationship('Task', backref='task', lazy='dynamic')

    def __repr__(self):
        return '<Project {}>'.format(self.name)

class Task(db.Model):
    id           = db.Column(db.Integer, primary_key=True)
    title        = db.Column(db.String(140))
    description  = db.Column(db.Text)
    genre        = db.Column(db.String(50))
    completed    = db.Column(db.Boolean, default=False, nullable=False)
    project_id   = db.Column(db.Integer, db.ForeignKey('project.id'),nullable=False)

    def __repr__(self):
        return '<Task {}>'.format(self.title)

