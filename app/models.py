from app import db
from datetime import datetime

class User(db.Model):
    id              = db.Column(db.Integer, primary_key=True)
    username        = db.Column(db.String(64), index=True, unique=True)
    email           = db.Column(db.String(120), index=True, unique=True)
    password_hash   = db.Column(db.String(128))
    projects        = db.relationship('Project', backref='user', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.username) 


class Project(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    number      = db.Column(db.String(140))
    name        = db.Column(db.String(140))
    timestamp   = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    value       = db.Column(db.Integer, nullable=False)
    completed   = db.Column(db.Boolean, default=False, nullable=False)
    user_id     = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return '<Project {}>'.format(self.name)