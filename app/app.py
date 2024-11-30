from flask import Flask, render_template, request, url_for
import os
from werkzeug.utils import secure_filename
from models.models import ToDo
from models.database import db_session

app = Flask(__name__)

# アップロードされたファイルを保存するディレクトリ
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 許可するファイルの拡張子
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    if '.' in filename:
        return filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    return False

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/index")
def index():
    to_do_lists = ToDo.query.all()
    return render_template("index.html",to_do_lists=to_do_lists)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/add", methods=["post"])
def add():
    title = request.form["title"]
    name = request.form["name"]
    date = request.form["date"]
    place = request.form["place"]
    body = request.form["body"]
    
    content = ToDo(title, name, date, place, body)
    db_session.add(content)
    db_session.commit()
    return index()

@app.route("/delete/<int:id>", methods=["post"])
def task_delete(id):
    content = ToDo.query.get(id)
    db_session.delete(content)
    db_session.commit()
    return index()

@app.route("/user")
def user():
    name = request.args.get("name")
    return render_template("user.html", name=name)


if __name__ == "__main__":
    app.run(debug=True)
