from flask import Flask, jsonify, render_template, redirect, url_for, flash, request
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_socketio import SocketIO, emit
# envから取得
from os import environ
from dotenv import load_dotenv
load_dotenv()
from models import UserTable, StationTable, ReserveTable, UserChatTable, UserChatMessageTable,StationChatTable
from ext import db
from flask_migrate import Migrate
from datetime import datetime
import requests



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

socketio = SocketIO(app)


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

    return render_template('Userregister.html')

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
    return render_template('Userlogin.html')

@app.route('/mypage', methods=['GET', 'POST'])
@login_required
def mypage():
    need_info = ["id", "Departure_Datetime", "Departure_Station_Name", "Arrive_Station_Name"]
    need_db_info = ["id", "Departure_Datetime", "Departure_Station_Id", "Arrive_Station_Id"]
    reserve_info_list = []
    reserve_history_info_list = []
    current_time = datetime.now()
    # ReserveTable.Departure_Datetime < current_time
    reservation_list = ReserveTable.query.filter(
        ReserveTable.User_Id == current_user.id,
    ).all()

    for reserve in reservation_list:
        reserve_info = {}
        for i in range(len(need_info)):
            if need_info[i] == "Departure_Station_Name":
                reserve_info[need_info[i]] = StationTable.query.filter_by(id=reserve.Departure_Station_Id).first().Name
            elif need_info[i] == "Arrive_Station_Name":
                reserve_info[need_info[i]] = StationTable.query.filter_by(id=reserve.Arrive_Station_Id).first().Name
            elif need_info[i] == "Departure_Datetime":
                    reserve_info[need_info[i]] = reserve.Departure_Datetime.strftime('%Y年%m月%d日 %H時%M分')
            else:
                reserve_info[need_info[i]] = getattr(reserve, need_db_info[i])

        if reserve.Departure_Datetime > current_time:
            reserve_info_list.append(reserve_info)
        else:
            reserve_history_info_list.append(reserve_info)
            

    return render_template('Usermypage.html', reserve_list=reserve_info_list, reserve_history_list=reserve_history_info_list)

@app.route('/reserveInfo/', methods=['GET','POST'])
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
        departure_station_name = StationTable.query.filter_by(id=reserve_db.Departure_Station_Id).first().Name
        arrive_station_name = StationTable.query.filter_by(id=reserve_db.Arrive_Station_Id).first().Name
        reserve_data = {}
        reserve_data['id'] = reserve_db.id
        reserve_data['departureStationId'] = reserve_db.Departure_Station_Id
        reserve_data['arriveStationId'] = reserve_db.Arrive_Station_Id
        reserve_data['departureStationName'] = departure_station_name
        reserve_data['arriveStationName'] = arrive_station_name
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
    
    return render_template('UserreserveInfo.html', reserveData=reserve_data)

@app.route('/route', methods=['GET', 'POST'])
@login_required
def route():
    return render_template('Userroute.html')

@app.route('/submit_form1', methods=['POST'])
def submit_form1():
        if request.method == 'POST':
            departure = request.form.get('departure')
            arrive = request.form.get('arrive')
            departure_station_data = StationTable.query.filter_by(Name=departure).first()
            arrive_station_data = StationTable.query.filter_by(Name=arrive).first()

            if not departure_station_data:
                print('出発駅が存在しません')
                return redirect(url_for('route'))


            if not arrive_station_data:
                print('到着駅が存在しません')
                return redirect(url_for('route'))
            
            day = request.form.get('day')
            delattr_time = request.form.get('time')
            departure_Id = departure_station_data.id
            arrive_Id = arrive_station_data.id
            departure_statoin_name = departure_station_data.Name
            # db登録
            route = ReserveTable(
                User_Id=current_user.id,
                Departure_Station_Id = departure_Id,
                Arrive_Station_Id = arrive_Id, 
                Departure_Datetime = day + ' ' + delattr_time,
                Arrive_Datetime = day + ' ' + delattr_time,
                Departure_Complete = False,
                Arrive_Complete = False,
                Note='test'
            )
            user_chat = UserChatTable(
                User_Id = current_user.id,
                Station_Id = departure_Id,
                Room_Name = departure_statoin_name
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

    return render_template('UserChatlist.html', chatlist=chatlist)

@app.route('/Userchat', methods=['GET', 'POST'])
@login_required
def Userchat():
    id = request.args.get('id')
    print(id)
    # dbからidのデータを取得する
    # dbは rederveTableから取得
    User_Chat = UserChatTable.query.filter_by(id=id).first()
    return render_template('Userchat.html',Touser=current_user.id, User_Chat=User_Chat)

@app.route('/send_message', methods=['POST'])
def send_message():
    messages = [] 
    # jsからidをもらう
    data = request.get_json()
    id = data.get('id')
    FromUser = data.get('FromUser')
    print(FromUser)
    message = data.get('message')
    
    if message:
        userMassege = UserChatMessageTable(
            User_Chat_Id = id,
            From_User = FromUser,
            Message = message
        )
        # DB格納
        db.session.add(userMassege)
        db.session.commit()

        # jsにメッセージを送る
        usermessage_db = UserChatMessageTable.query.filter_by(User_Chat_Id=id)
        for i in usermessage_db:
            messages.append([i.Message, i.From_User])
        
        return jsonify({"message": "Message received", "messages": messages,})
        
    return jsonify({"error": "No message sent"}), 400

@app.route('/get_messages', methods=['GET','post'])
def get_messages():
    messages = []  # メッセージを保存するリスト
    # jsからidをもらう
    data = request.get_json()
    id = data.get('id')
    # jsにメッセージを送る
    usermessage_db = UserChatMessageTable.query.filter_by(User_Chat_Id=id)
    for i in usermessage_db:
        messages.append([i.Message, i.From_User])
    
    return jsonify({"message": "Message received", "messages": messages})
    




#     return jsonify({"messages": messages})




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
            return redirect(url_for('StaffRegister'))
        db.session.add(station)
        db.session.commit()
        flash('作成完了', 'success')

    return render_template('StaffRegister.html')

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
    return render_template('StaffLogin.html')

@app.route('/staffPage')
@login_required
def staffPage():
    return render_template('StaffPage.html')

@app.route('/staffChatList', methods=['GET', 'POST'])
@login_required
def staffChatList():
    chatlist = UserChatTable.query.filter(
        UserChatTable.Station_Id == current_user.id
    ).all()
    return render_template('StaffChatList.html', chatlist=chatlist)

@app.route('/staffChat', methods=['GET', 'POST'])
@login_required
def staffChat():
    id = request.args.get('id')
    print(id)
    # dbからidのデータを取得する
    # dbは rederveTableから取得
    User_Chat = UserChatTable.query.filter_by(id=id).first()
    return render_template('StaffChat.html',Touser=current_user.id, User_Chat=User_Chat)

@app.route('/apitest')
def apitest():
    data = {'key': 'values'}
    get_data = {}
    
    request_base = 'https://api.odpt.org'
    request_endpoint = f'/api/v4/odpt:Station?odpt:operator=odpt.Operator:JR-East&acl:consumerKey={environ.get("API_TOKEN")}'
    # request_endpoint = f'/api/v4/odpt:StationTimetable?acl:consumerKey={environ.get("API_TOKEN")}'
    # request_endpoint = f'/api/v4/odpt:StationTimetable?acl:consumerKey={environ.get("API_TOKEN")}'

    request_url = request_base + request_endpoint
    
    # リクエストを送る
    response = requests.get(request_url)
    
    # レスポンスのステータスコードを確認
    if response.status_code == 200:
        # レスポンスのjsonデータを取得
        station_data = []
        get_data = response.json() 
        for getdata in get_data:
            station_data.append(getdata['owl:sameAs'])
            print(getdata['owl:sameAs'])

        data = {
            'get_data': get_data,
            'station_data': station_data
        }

    else:
        get_data = 'error'
        print(response)
    
    return render_template('apitest.html', data=data)

@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    emit('message', msg, broadcast=True, include_self=False)


if __name__ == '__main__':
    socketio.run(app)