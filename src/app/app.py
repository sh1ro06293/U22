from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
# envから取得
from os import environ
from dotenv import load_dotenv
load_dotenv()
from models import UserTable, StationTable

DB_USER = environ.get('DB_USER')
DB_PASS = environ.get('DB_PASS')
DB_NAME = environ.get('DB_NAME')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{DB_USER}:{DB_PASS}@localhost/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(id):
    return UserTable.query.get(int(id))

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
    return render_template('mypage.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/staffRegister', methods=['GET', 'POST'])
def staffRegister():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        name = request.form.get('name')
        id = request.form.get('id')
        password = request.form.get('password')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        station = StationTable(Name=name, id=id,  Password=hashed_password)
        if station.query.filter_by(id=id).first():
            flash('This email is already taken. Please choose another', 'danger')
            return redirect(url_for('staffRegister'))
        db.session.add(station)
        db.session.commit()
        flash('Your account has been created! You can now log in', 'success')
        login_user(station, remember=True)
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('staffPage'))

    return render_template('sraffRegister.html')

if __name__ == '__main__':
    app.run(debug=True)


