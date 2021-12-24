from datetime import datetime
from sqlalchemy import func, and_, or_, delete, create_engine, text, MetaData, Integer, String, Column, ForeignKey, Date, Time, DateTime, Boolean, extract
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, subqueryload, joinedload, relationship
from sqlalchemy.sql.expression import null
from werkzeug.security import generate_password_hash, check_password_hash
meta = MetaData()
Base = declarative_base()
engine = create_engine("postgresql://odya:o030101@127.0.0.1:5432/agrar_bot")

Session = sessionmaker(bind=engine)
session = Session()


class Kafedra(Base):
    __tablename__ = 'kafedra'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    teachers = relationship("Teacher", backref="kafedra", lazy=True)
    

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    token = Column(String, nullable=False)
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)


class Teacher(Base):
    __tablename__ = 'teacher'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    kafedra_id = Column(Integer, ForeignKey("kafedra.id"))
class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    complains = relationship("Complain", backref='category', lazy=True)
    def format(self):
        return {
            "id" : self.id,
            "name" : self.name
        }
class Complain(Base):
    __tablename__ = 'complain'
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('category.id'))
    type = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    username = Column(String, nullable=True)
    chat_id = Column(Integer,  nullable=True)
    created_time = Column(DateTime,default=datetime.now, nullable=False)
    complain_data = relationship("Complain_Data", backref="complain", lazy=True)
    def format(self):
        return {
            'id' : self.id,
            "category": self.category.name,
            "type": self.type,
            "first_name" : self.first_name,
            "username" : self.username,
            "chat_id" : self.chat_id,
            "created_time" : str(self.created_time),
            "complain_date" : [ x.format() for x in self.complain_data ]
        }

class Complain_Data(Base):
    __tablename__ = 'complain_data'
    id = Column(Integer, primary_key=True)
    complain_id = Column(Integer, ForeignKey('complain.id')) 
    key = Column(String, nullable=False) # kafedra_id, teacher_id,  data_type(img,text,video,voice,doc) 
    value = Column(String, nullable=False)
    def format(self):
        return {
            "id" : self.id,
            "key" : self.key,
            "value" : self.value
        }
    

class Session(Base):
    __tablename__ = 'session'
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, nullable=True)
    message = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    step = Column(String, nullable=True) # category, ( 2 - kafedra - teacher ), type, text, video, photo, voice 
    category = Column(String, nullable=True)
    type = Column(String, nullable=True)
    username = Column(String, nullable=True)


def Reset():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

#Reset()
categories = ['Ошхона', 'Ўқитувчи', 'TTJ (Ётоқхона)', 'Ҳожатхона']

session.close()

