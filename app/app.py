from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from models.models import Task, User
from models.database import db_session
from flask_login import LoginManager, current_user, login_user
from app.forms import LoginForm
import secrets
app = Flask(__name__)

# シークレットキーを設定
app.secret_key = secrets.token_hex(16) 

# LoginManagerの起動
login = LoginManager(app)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/index")
def index():
    to_do_lists = Task.query.all()
    return render_template("index.html",to_do_lists=to_do_lists)

@app.route("/home")
def home():
    to_do_lists = Task.query.all()
    return render_template("home.html",to_do_lists=to_do_lists)

@app.route("/add", methods=["post"])
def add():
    title = request.form["title"]
    name = request.form["name"]
    date = request.form["date"]
    place = request.form["place"]
    body = request.form["body"]
    user_id = 1
    
    content = Task(title, name, date, place, body)
    db_session.add(content)
    db_session.commit()
    return home()

@app.route("/delete/<int:id>", methods=["post"])
def task_delete(id):
    content = Task.query.get(id)
    db_session.delete(content)
    db_session.commit()
    return index()

@app.route("/user")
def user():
    name = request.args.get("name")
    return render_template("user.html", name=name)

# ログイン機構
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/login', methods=['get', 'post'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(user_name=form.user_name.data).one_or_none()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('home'))
    return render_template('login.html', form=form)
    
if __name__ == "__main__":
    app.run(debug=True)
