from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from models.models import Task, User
from models.database import db_session
from flask_login import LoginManager, current_user, login_user, login_required
from app.forms import LoginForm, RegistrationForm
import secrets

app = Flask(__name__)

# シークレットキーを設定
app.secret_key = secrets.token_hex(16) 

# LoginManagerの起動
login = LoginManager(app)
login.login_view = 'login'

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/index")
def index():
    to_do_lists = Task.query.all()
    return render_template("index.html",to_do_lists=to_do_lists)

@app.route("/home")
@login_required
def home():
    to_do_lists = Task.query.all()
    return render_template("home.html",to_do_lists=to_do_lists)

@app.route("/add", methods=["post"])
@login_required
def add():
    title = request.form["title"]
    name = request.form["name"]
    date = request.form["date"]
    place = request.form["place"]
    body = request.form["body"]
    user_id = current_user.id
    
    content = Task(title, name, date, place, body, user_id)
    db_session.add(content)
    db_session.commit()
    return redirect(url_for('home'))

@app.route("/delete/<int:id>", methods=["post"])
@login_required
def task_delete(id):
    content = Task.query.get(id)
    
    if current_user.id == content.user_id:
        db_session.delete(content)
        db_session.commit()
    return redirect(url_for('home'))

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

# ユーザー登録
@app.route('/register', methods=['get', 'post'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RegistrationForm()
    
    if form.validate_on_submit():
        user = User(user_name=form.user_name.data, email=form.email.data)
        user.set_password(form.password.data)
        db_session.add(user)
        db_session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)
