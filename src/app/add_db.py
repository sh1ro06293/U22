from os import environ
from dotenv import load_dotenv
load_dotenv()
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from ext import db
from models import StationTimetable, TrainTable, StationTable
import csv




DB_USER = environ.get('DB_USER')
DB_PASS = environ.get('DB_PASS')
DB_NAME = environ.get('DB_NAME')
print(DB_USER, DB_PASS, DB_NAME)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{DB_USER}:{DB_PASS}@localhost/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db) 

# csvの内容をmodelsを参考にdbに追加
def add_train_db():
    with open('../../station_data/yamanote_sotomawari_heijitu.csv', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            times = row[1:]
            for _ in times:
                train_data = TrainTable(
                    direction='外回り',
                    weekday='平日',
                    line='山手線'
                )
                db.session.add(train_data)
            db.session.commit()
            break

    with open('../../station_data/yamanote_sotomawari_kyuujitu.csv', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            times = row[1:]
            for _ in times:
                train_data = TrainTable(
                    direction='外回り',
                    weekday='休日',
                    line='山手線'
                )
                db.session.add(train_data)
            db.session.commit()
            break

    with open('../../station_data/yamanote_uchimawari_heijitu.csv', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            times = row[1:]
            for _ in times:
                train_data = TrainTable(
                    direction='内回り',
                    weekday='平日',
                    line='山手線'
                )
                db.session.add(train_data)
            db.session.commit()
            break

    with open('../../station_data/yamanote_uchimawari_kyuujitu.csv', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            times = row[1:]
            for _ in times:
                train_data = TrainTable(
                    direction='内回り',
                    weekday='休日',
                    line='山手線'
                )
                db.session.add(train_data)
            db.session.commit()
            break

def add_station_db():
    # 全ての駅をid割り振る
    yamanote_ID = {'東京':'JY01', '神田':'JY02', '秋葉原':'JY03', '御徒町':'JY04', '上野':'JY05', '鶯谷':'JY06', '日暮里':'JY07', '西日暮里':'JY08', '田端':'JY09', '駒込':'JY10', '巣鴨':'JY11', '大塚':'JY12', '池袋':'JY13', '目白':'JY14', '高田馬場':'JY15', '新大久保':'JY16', '新宿':'JY17', '代々木':'JY18', '原宿':'JY19', '渋谷':'JY20', '恵比寿':'JY21', '目黒':'JY22', '五反田':'JY23', '大崎':'JY24', '品川':'JY25', '高輪ゲートウェイ':'JY26', '田町':'JY27', '浜松町':'JY28', '新橋':'JY29', '有楽町':'JY30'}
    with open('../../station_data/yamanote_uchimawari_kyuujitu.csv', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            id = yamanote_ID[row[0]]

            # stationTableにデータがないなら
            if not StationTable.query.filter_by(Station_Id=id).first():
                station_data = StationTable(
                    Station_Id=id,
                    Name=f'{row[0]}-山手線',
                    Password=id.lower()
                )
                db.session.add(station_data)
            db.session.commit()



if __name__ == '__main__':
    with app.app_context():
        add_train_db()
        add_station_db()