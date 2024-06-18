from flask import Flask, jsonify, render_template, redirect, url_for, flash, request
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
# envから取得
from os import environ
from dotenv import load_dotenv
load_dotenv()
from models import UserTable, StationTable, ReserveTable, UserChatTable, UserChatMessageTable,StationChatTable
from ext import db
from flask_migrate import Migrate
from datetime import datetime



DB_USER = environ.get('DB_USER')
DB_PASS = environ.get('DB_PASS')
DB_NAME = environ.get('DB_NAME')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{DB_USER}:{DB_PASS}@localhost/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db) 

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    user = UserTable.query.get(int(user_id))
    if user:
        return user
    return StationTable.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        number = request.form.get('number')
        password = request.form.get('password')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = UserTable(Name=name, Email=email, Number=number, Password=hashed_password)
        if UserTable.query.filter_by(Email=email).first():
            flash('This email is already taken. Please choose another', 'danger')
            return redirect(url_for('register'))
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in', 'success')
        login_user(user, remember=True)
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('mypage'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('mypage'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = UserTable.query.filter_by(Email=email).first()
        if user and bcrypt.check_password_hash(user.Password, password):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('mypage'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html')

@app.route('/mypage', methods=['GET', 'POST'])
@login_required
def mypage():

    current_time = datetime.now()
    reservation_list = ReserveTable.query.filter(
        ReserveTable.User_Id == current_user.id,
        ReserveTable.Departure_Datetime > current_time
    ).all()

    reservation_history_list = ReserveTable.query.filter(
        ReserveTable.User_Id == current_user.id,
        ReserveTable.Departure_Datetime < current_time
        ).all()
    return render_template('mypage.html', reservation_list=reservation_list, reservation_history_list=reservation_history_list)

@app.route('/reserveInfo/', methods=['GET'])
@login_required
def reserve_info_detail():
    id = request.args.get('id')
    print(id)
    # dbからidのデータを取得する
    # dbは rederveTableから取得
    reserve_db = ReserveTable.query.filter_by(id=id).first()
    if not reserve_db:
        flash('予約情報が存在しません', 'danger')
        return redirect(url_for('mypage'))

    else:
        reserve_data = {}
        reserve_data['id'] = reserve_db.id
        reserve_data['departureStationId'] = reserve_db.Departure_Station_Id
        reserve_data['arriveStationId'] = reserve_db.Arrive_Station_Id
        # 日にちだけにする
        reserve_data['departureDate'] = reserve_db.Departure_Datetime.strftime('%Y-%m-%d')
        # 時間だけにする
        reserve_data['departureTime'] = reserve_db.Departure_Datetime.strftime('%H:%M')
        reserve_data['arriveDatetime'] = reserve_db.Arrive_Datetime
        reserve_data['carNumber'] = reserve_db.Car_Number
        reserve_data['departureComplete'] = reserve_db.Departure_Complete
        reserve_data['arriveComplete'] = reserve_db.Arrive_Complete
        reserve_data['transferId'] = reserve_db.Transfer_Id
        reserve_data['note'] = reserve_db.Note
    
    return render_template('reserveInfo.html', reserveData=reserve_data)

@app.route('/route', methods=['GET', 'POST'])
@login_required
def route():
    return render_template('route.html')

@app.route('/submit_form1', methods=['POST'])
def submit_form1():
        if request.method == 'POST':
            departure = request.form.get('departure')
            if not StationTable.query.filter_by(Station_Id=departure).first():
                print('出発駅が存在しません')
                return redirect(url_for('route'))
            arrive = request.form.get('arrive')
            if not StationTable.query.filter_by(Station_Id=arrive).first():
                print('到着駅が存在しません')
                return redirect(url_for('route'))
            day = request.form.get('day')
            delattr_time = request.form.get('time')
            departure_Id = StationTable.query.filter_by(Station_Id=departure).first().id
            arrive_Id = StationTable.query.filter_by(Station_Id=arrive).first().id
            # db登録
            route = ReserveTable(
                # apiが来たら変更
                User_Id=current_user.id,
                Departure_Station_Id = departure,
                Arrive_Station_Id = arrive, 
                Departure_Datetime = day + ' ' + delattr_time,
                Arrive_Datetime = day + ' ' + delattr_time,
                Departure_Complete = False,
                Arrive_Complete = False,
                Note='test'
            )
            user_chat = UserChatTable(
                User_Id = current_user.id,
                Station_Id = departure_Id,
                Room_Name = 'test'
            )

            Station_chat = StationChatTable(
                Station_Id1 = departure_Id,
                Station_Id2 = arrive_Id,
                Room_Name = 'test'
            )
            db.session.add_all([route, user_chat, Station_chat])
            db.session.commit()
            flash('予約完了', 'success')
            return redirect(url_for('mypage'))
        
        return redirect(url_for('route'))


@app.route('/chatList', methods=['GET', 'POST'])
@login_required
def chatList():
    chatlist = UserChatTable.query.filter(
        UserChatTable.User_Id == current_user.id
    ).all()

    return render_template('Chatlist.html', chatlist=chatlist)

@app.route('/Userchat', methods=['GET', 'POST'])
@login_required
def Userchat():
    return render_template('Userchat.html')



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/staffRegister', methods=['GET', 'POST'])
def staffRegister():
    
    if request.method == 'POST':
        name = request.form.get('name')
        station_id = request.form.get('station_id')
        password = request.form.get('password')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        station = StationTable(Name=name, Station_Id=station_id ,Password=hashed_password)
        if station.query.filter_by(Station_Id=station_id).first():
            flash('すでに登録済み', 'danger')
            return redirect(url_for('staffRegister'))
        db.session.add(station)
        db.session.commit()
        flash('作成完了', 'success')

    return render_template('staffRegister.html')

@app.route('/staffLogin', methods=['GET', 'POST'])
def staffLogin():

    if current_user.is_authenticated:
        return redirect(url_for('staffPage'))
    if request.method == 'POST':
        stationid = request.form.get('stationid')
        password = request.form.get('password')
        station = StationTable.query.filter_by(Station_Id=stationid).first()

        if station and bcrypt.check_password_hash(station.Password, password):
            login_user(station, remember=True)

            return redirect(url_for('staffPage'))
        else:
            flash('ログイン失敗しました', 'danger')
    return render_template('staffLogin.html')

@app.route('/staffPage')
@login_required
def staffPage():
    return render_template('staffPage.html')

if __name__ == '__main__':
    app.run(debug=True)


