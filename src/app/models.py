from ext import db
from flask_login import UserMixin


class UserTable(db.Model, UserMixin):
    __tablename__ = 'UserTable'
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(100), nullable=False, unique=True)
    Number = db.Column(db.String(15), nullable=False)
    Password = db.Column(db.String(100), nullable=False)

class ChatTable(db.Model):
    __tablename__ = 'chatTable'
    id = db.Column(db.Integer, primary_key=True)
    User_Id1 = db.Column(db.Integer, db.ForeignKey('UserTable.id'), nullable=False)
    User_Id2 = db.Column(db.Integer, db.ForeignKey('UserTable.id'), nullable=False)
    Room_Name = db.Column(db.String(50), nullable=False)

class ChatMessageTable(db.Model):
    __tablename__ = 'ChatMessageTable'
    id = db.Column(db.Integer, primary_key=True)
    Chat_Id = db.Column(db.Integer, db.ForeignKey('chatTable.id'), nullable=False)
    To_User = db.Column(db.Integer, db.ForeignKey('UserTable.id'), nullable=False)
    From_User = db.Column(db.Integer, db.ForeignKey('UserTable.id'), nullable=False)
    Message = db.Column(db.Text, nullable=False)

class StationTable(db.Model, UserMixin):
    __tablename__ = 'StationTable'
    id = db.Column(db.Integer, primary_key=True)
    Station_Id = db.Column(db.String(10), unique=True, nullable=False)
    Name = db.Column(db.String(50), nullable=False)
    Password = db.Column(db.String(100), nullable=False)

    def get_id(self):
        return self.id

class ReserveTable(db.Model):
    __tablename__ = 'ReserveTable'
    id = db.Column(db.Integer, primary_key=True)
    User_Id = db.Column(db.Integer, db.ForeignKey('UserTable.id'), nullable=False)
    Departure_Station_Id = db.Column(db.String(10), db.ForeignKey('StationTable.Station_Id'), nullable=False)
    Arrive_Station_Id = db.Column(db.String(10), db.ForeignKey('StationTable.Station_Id'), nullable=False)
    Departure_Datetime = db.Column(db.DateTime, nullable=False)
    Arrive_Datetime = db.Column(db.DateTime, nullable=False)
    Car_Number = db.Column(db.String(10))
    Departure_Complete = db.Column(db.Boolean, default=False)
    Arrive_Complete = db.Column(db.Boolean, default=False)
    Transfer_Id = db.Column(db.Integer)
    Note = db.Column(db.Text)