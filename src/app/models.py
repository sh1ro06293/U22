from app import app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import environ
from dotenv import load_dotenv
from flask_login import UserMixin
from flask_migrate import Migrate
load_dotenv()

DB_USER = environ.get('DB_USER')
DB_PASS = environ.get('DB_PASS')
DB_NAME = environ.get('DB_NAME')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{DB_USER}:{DB_PASS}@localhost/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class UserTable(db.Model, UserMixin):
    __tablename__ = 'UserTable'
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(100), nullable=False, unique=True)
    Number = db.Column(db.String(15), nullable=False)
    Password = db.Column(db.String(100), nullable=False)

class Chat(db.Model):
    __tablename__ = 'chatTable'
    id = db.Column(db.Integer, primary_key=True)
    User_Id1 = db.Column(db.Integer, db.ForeignKey('UserTable.id'), nullable=False)
    User_Id2 = db.Column(db.Integer, db.ForeignKey('UserTable.id'), nullable=False)
    Room_Name = db.Column(db.String(50), nullable=False)

class ChatMess(db.Model):
    __tablename__ = 'ChatMessageTable'
    id = db.Column(db.Integer, primary_key=True)
    Chat_Id = db.Column(db.Integer, db.ForeignKey('chatTable.id'), nullable=False)
    To_User = db.Column(db.Integer, db.ForeignKey('UserTable.id'), nullable=False)
    From_User = db.Column(db.Integer, db.ForeignKey('UserTable.id'), nullable=False)
    Message = db.Column(db.Text, nullable=False)

class Station(db.Model):
    __tablename__ = 'StationTable'
    id = db.Column(db.String(20), primary_key=True)
    Name = db.Column(db.String(50), nullable=False)
    Password = db.Column(db.String(100), nullable=False)

class Reserve(db.Model):
    __tablename__ = 'ReserveTable'
    id = db.Column(db.Integer, primary_key=True)
    User_Id = db.Column(db.Integer, db.ForeignKey('UserTable.id'), nullable=False)
    Departure_Station_Id = db.Column(db.Integer, db.ForeignKey('StationTable.id'), nullable=False)
    Arrive_Station_Id = db.Column(db.Integer, db.ForeignKey('StationTable.id'), nullable=False)
    Departure_Datetime = db.Column(db.DateTime, nullable=False)
    Arrive_Datetime = db.Column(db.DateTime, nullable=False)
    Car_Number = db.Column(db.String(10))
    Departure_Complete = db.Column(db.Boolean, default=False)
    Arrive_Complete = db.Column(db.Boolean, default=False)
    Transfer_Id = db.Column(db.Integer)
    Note = db.Column(db.Text)