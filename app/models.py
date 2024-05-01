### IF THIS FILE IS MODIFIED, RUN tables.py TO RECREATE TABLES
from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import login
from flask_login import UserMixin

class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(32), nullable=False)
    reg_role = db.Column(db.String(32), nullable=False)
    act_role = db.Column(db.String(32), nullable=False)
    approve = db.Column(db.Integer, nullable=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<user {self.id}: {self.username}>'

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    author = db.Column(db.String(200))
    reserve = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(32), nullable=False)
    
    def __repr__(self):
        return f'<Book {self.id}: {self.title}: {self.author}: {self.reserve}>'
class Tech(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    info = db.Column(db.String(200))
    time = db.Column(db.String(200))
    reserve = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(32), nullable=False)
    
    def __repr__(self):
        return f'<Book {self.id}: {self.name}: {self.info}: {self.time}: {self.reserve}>'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
