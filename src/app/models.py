from app import db
from flask_login import UserMixin

class UserTable(db.Model, UserMixin):
    __tablename__ = 'UserTable'
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(100), nullable=False, unique=True)
    Number = db.Column(db.String(15), nullable=False)
    Password = db.Column(db.String(100), nullable=False)

class StationTable(db.Model, UserMixin):
    __tablename__ = 'StationTable'
    id = db.Column(db.String(20), primary_key=True)
    Name = db.Column(db.String(50), nullable=False)
    Password = db.Column(db.String(100), nullable=False)