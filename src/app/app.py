from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
# envから取得
from os import environ
from dotenv import load_dotenv
load_dotenv()
from models import UserTable, StationTable
from ext import db
from flask_migrate import Migrate


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
def load_user(id):
    return UserTable.query.get(int(id))

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

@app.route('/mypage')
@login_required
def mypage():
    reservation_list = list()
    return render_template('mypage.html',
                           reservation_list=reservation_list)

@app.route('/route')
@login_required
def route():
    if request.method == 'POST':
        departure = request.form.get('departure')
        arrival = request.form.get('arrival')
        day = request.form.get('day')
        delattr_time = request.form.get('time')
        # db登録

        
    return render_template('route.html')



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
            # next_page = request.args.get('next')
            return redirect(url_for('staffPage'))
        else:
            flash('ログイン失敗しました', 'danger')
    return render_template('staffLogin.html')
@login_manager.user_loader
def load_user(user_id):
    user = UserTable.query.get(int(user_id))
    if user:
        return user
    return StationTable.query.get(int(user_id))

@login_manager.user_loader
def load_user(user_id):
    user = UserTable.query.get(int(user_id))
    if user:
        return user
    return StationTable.query.get(int(user_id))

@app.route('/staffPage')
@login_required
def staffPage():
    return render_template('staffPage.html')

if __name__ == '__main__':
    app.run(debug=True)


