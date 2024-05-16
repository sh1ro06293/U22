from app.app import app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:TeamTokuzawa2@localhost/barirakudb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class UserLogin(db.Model):
    __tablename__ = 'UserTable'
    User_Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(100), nullable=False, unique=True)
    Number = db.Column(db.String(15), nullable=False)
    Password = db.Column(db.String(100), nullable=False)

class Chat(db.Model):
    __tablename__ = 'chatTable'
    Chat_Id = db.Column(db.Integer, primary_key=True)
    User_Id1 = db.Column(db.Integer, db.ForeignKey('UserTable.User_Id'), nullable=False)
    User_Id2 = db.Column(db.Integer, db.ForeignKey('UserTable.User_Id'), nullable=False)
    Room_Name = db.Column(db.String(50), nullable=False)

class ChatMess(db.Model):
    __tablename__ = 'ChatMessageTable'
    Chat_Mess_Id = db.Column(db.Integer, primary_key=True)
    Chat_Id = db.Column(db.Integer, db.ForeignKey('chatTable.Chat_Id'), nullable=False)
    To_User = db.Column(db.Integer, db.ForeignKey('UserTable.User_Id'), nullable=False)
    From_User = db.Column(db.Integer, db.ForeignKey('UserTable.User_Id'), nullable=False)
    Message = db.Column(db.Text, nullable=False)

class Station(db.Model):
    __tablename__ = 'StationTable'
    Station_Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), nullable=False)

class Reserve(db.Model):
    __tablename__ = 'ReserveTable'
    Reserve_Id = db.Column(db.Integer, primary_key=True)
    User_Id = db.Column(db.Integer, db.ForeignKey('UserTable.User_Id'), nullable=False)
    Departure_Station_Id = db.Column(db.Integer, db.ForeignKey('StationTable.Station_Id'), nullable=False)
    Arrive_Station_Id = db.Column(db.Integer, db.ForeignKey('StationTable.Station_Id'), nullable=False)
    Departure_Datetime = db.Column(db.DateTime, nullable=False)
    Arrive_Datetime = db.Column(db.DateTime, nullable=False)
    Car_Number = db.Column(db.String(10))
    Departure_Complete = db.Column(db.Boolean, default=False)
    Arrive_Complete = db.Column(db.Boolean, default=False)
    Transfer_Id = db.Column(db.Integer)
    Note = db.Column(db.Text)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

