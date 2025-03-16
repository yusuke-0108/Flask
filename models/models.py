from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from models.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import UserMixin
from flask import current_app
import os

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
    profile_img = Column(String(255), default="default-profile.png")
    
    task = relationship("Task", back_populates="user")
    
    def __init__(self, user_name, email):
        self.user_name = user_name
        self.email = email
    
    def __repr__(self):
        return '<Name %r>' % (self.user_name)
    
    def set_password(self, password):
        if password is not None:
            self.hashed_pass = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_pass, password)
    
    def save_profile_image(self, file):
        if file:
            filename = secure_filename(file.filename)
            user_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], f"user/{self.id}")
            os.makedirs(user_folder, exist_ok=True)  
            
            file_path = os.path.join(user_folder, filename)
            file.save(file_path)
            self.profile_img = f"uploads/user/{self.id}/{filename}"
