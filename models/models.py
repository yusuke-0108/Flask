from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from models.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# パスワードをハッシュ化
def set_password(self, password):
        self.password_hash = generate_password_hash(password)

# 入力されたパスワードが登録されているパスワードハッシュと一致するかを確認
def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String(128), unique=False)
    name = Column(Text)
    date = Column(Text)
    place = Column(Text)
    body = Column(Text)
    
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="task")
    
    def __init__(self, title, name, date, place, body, user_id):
        self.title = title
        self.name = name
        self.date = date
        self.place = place
        self.body = body
        self.user_id = user_id
    
    def __repr__(self):
        return '<To Do %r>' % (self.title)

class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_name = Column(String(52), unique=True)
    email = Column(String(52), unique=True)
    hashed_pass = Column(String(128))
    
    task = relationship("Task", back_populates="user")
    
    def __init__(self, user_name, email):
        self.user_name = user_name
        self.email = email
    
    def __repr__(self):
        return '<Name %r>' % (self.user_name)
    
    def set_password(self, password):
        self.hashed_pass = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_pass, password)
