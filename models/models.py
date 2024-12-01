from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from models.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship

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

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_name = Column(String(52), unique=True)
    hashed_pass = Column(String(128))
    
    task = relationship("Task", back_populates="user")
    
    def __init__(self, user_name, hashed_pass):
        self.user_name = user_name
        self.hashed_pass = hashed_pass
    
    def __repr__(self):
        return '<Name %r>' % (self.user_name)