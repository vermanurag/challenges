from flask_login import UserMixin
from app import db, lm


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    source = db.Column(db.String(30), nullable=False, unique=False)

    def __repr__(self):
        return '<User {}>'.format(self.name)

class Access(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    app_id = db.Column(db.String(120), nullable=False, unique=False)
    email = db.Column(db.String(120), nullable=False, unique=False)

    def __repr__(self):
        return '<Access {}>'.format(self.name)

