from ext import db
from flask_login import UserMixin


class UserTable(db.Model, UserMixin):
    __tablename__ = 'UserTable'
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(100), nullable=False, unique=True)
    Number = db.Column(db.String(15), nullable=False)
    Password = db.Column(db.String(100), nullable=False)

class UserChatTable(db.Model):
    __tablename__ = 'UserChatTable'
    id = db.Column(db.Integer, primary_key=True)
    User_Id = db.Column(db.Integer, db.ForeignKey('UserTable.id'), nullable=False)
    Station_Id = db.Column(db.Integer, db.ForeignKey('StationTable.id'), nullable=False)
    Room_Name = db.Column(db.String(50), nullable=False)

class UserChatMessageTable(db.Model):
    __tablename__ = 'UserChatMessageTable'
    id = db.Column(db.Integer, primary_key=True)
    User_Chat_Id = db.Column(db.Integer, db.ForeignKey('UserChatTable.id'), nullable=False)
    From_User = db.Column(db.Boolean, nullable=False)
    Message = db.Column(db.Text, nullable=False)

class StationChatTable(db.Model):
    __tablename__ = 'StationChatTable'
    id = db.Column(db.Integer, primary_key=True)
    Station_Id1 = db.Column(db.Integer, db.ForeignKey('StationTable.id'), nullable=False)
    Station_Id2 = db.Column(db.Integer, db.ForeignKey('StationTable.id'), nullable=False)
    Room_Name = db.Column(db.String(50), nullable=False)

class StationChatMessageTable(db.Model):
    __tablename__ = 'StationChatMessageTable'
    id = db.Column(db.Integer, primary_key=True)
    Station_Chat_Id = db.Column(db.Integer, db.ForeignKey('StationChatTable.id'), nullable=False)
    To_Station = db.Column(db.Integer, db.ForeignKey('StationTable.id'), nullable=False)
    From_Station = db.Column(db.Integer, db.ForeignKey('StationTable.id'), nullable=False)
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
    Departure_Station_Id = db.Column(db.String(10), db.ForeignKey('StationTable.id'), nullable=False)
    Arrive_Station_Id = db.Column(db.String(10), db.ForeignKey('StationTable.id'), nullable=False)
    Departure_Datetime = db.Column(db.DateTime, nullable=False)
    Arrive_Datetime = db.Column(db.DateTime, nullable=False)
    Car_Number = db.Column(db.String(10))
    Departure_Complete = db.Column(db.Boolean, default=False)
    Arrive_Complete = db.Column(db.Boolean, default=False)
    Transfer_Id = db.Column(db.Integer)
    Note = db.Column(db.Text)

class StationTimetable(db.Model):
    __tablename__ = 'StationTimetable'
    id = db.Column(db.Integer, primary_key=True)
    Station_Id = db.Column(db.String(10), db.ForeignKey('StationTable.id'), nullable=False)
    Train_Id = db.Column(db.Integer, db.ForeignKey('TrainTable.id'), nullable=False)
    Departure_Datetime = db.Column(db.DateTime, nullable=False)
    final = db.Column(db.Boolean, default=False)

class TrainTable(db.Model):
    __tablename__ = 'TrainTable'
    id = db.Column(db.Integer, primary_key=True)
    direction = db.Column(db.String(20), nullable=False)
    weekday = db.Column(db.String(20), nullable=False)
    line = db.Column(db.String(20), nullable=False)
