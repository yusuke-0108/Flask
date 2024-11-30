from sqlalchemy import Column, Integer, String, Text, DateTime
from models.database import Base
from datetime import datetime

class ToDo(Base):
    __tablename__ = 'todolists'
    id = Column(Integer, primary_key=True)
    title = Column(String(128), unique=False)
    name = Column(Text)
    date = Column(Text)
    place = Column(Text)
    body = Column(Text)
    
    
    def __init__(self, title, name, date, place, body):
        self.title = title
        self.name = name
        self.date = date
        self.place = place
        self.body = body
    
    def __repr__(self):
        return '<To Do %r>' % (self.title)