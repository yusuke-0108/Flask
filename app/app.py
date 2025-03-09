from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
from models.models import Task, User
from models.database import db_session
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from app.forms import LoginForm, RegistrationForm
import secrets

app = Flask(__name__)

# シークレットキーを設定
app.secret_key = secrets.token_hex(16) 

# LoginManagerの起動
login = LoginManager(app)
login.login_view = 'login'

@app.route("/")
def top():
    return render_template("top.html")

@app.route("/lists")
@login_required
def lists():
    task_lists = Task.query.all()
    return render_template("lists.html",task_lists=task_lists)

@app.route("/user/<int:user_id>/home")
@login_required
def home(user_id):
    task_lists = Task.query.filter_by(user_id=user_id).all()
    return render_template("home.html",task_lists=task_lists)

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
    return redirect(url_for('home', user_id=user_id))

@app.route("/delete/<int:id>", methods=["post"])
@login_required
def task_delete(id):
    content = Task.query.get(id)
    
    if current_user.id == content.user_id:
        db_session.delete(content)
        db_session.commit()
    return redirect(url_for('home', user_id=content.user_id))

@app.route("/users")
@login_required
def users():
    users = User.query.all()
    return render_template("users.html", users=users)

# ログイン機構
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/login', methods=['get', 'post'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home', user_id=current_user.id))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(user_name=form.user_name.data).one_or_none()
        if user is None or not user.check_password(form.password.data):
            flash('ユーザー名またはパスワードが正しくありません。')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('home', user_id=current_user.id))
    return render_template('login.html', form=form)

# ユーザー登録
@app.route('/register', methods=['get', 'post'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home', user_id=current_user.id))
    
    form = RegistrationForm()
        
    # nameとemailが既に登録されているか確認
    existing_user = User.query.filter_by(user_name=form.user_name.data).one_or_none()
    existing_email = User.query.filter_by(email=form.email.data).one_or_none()
    
    if existing_user:
        flash('このユーザー名は既に使用されています。')
        return render_template('register.html', form=form)
    if existing_email:
        flash('このメールアドレスは既に使用されています。')
        return render_template('register.html', form=form)
    user = User(user_name=form.user_name.data, email=form.email.data)
    user.set_password(form.password.data)
    db_session.add(user)
    db_session.commit()
    login_user(user)
    return redirect(url_for('home', user_id=user.id))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
