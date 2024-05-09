from flask import Flask,render_template,request

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World"


@app.route("/index")
def index():
    name = request.args.get("name")

    num = [1,2,3,4,5,6,7,8,9,10]

    return render_template("index.html", aaa=name, num=num)

@app.route("/login")
def login():
    return render_template("login.html")
