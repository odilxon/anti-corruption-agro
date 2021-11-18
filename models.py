from datetime import datetime
from sqlalchemy import func, and_, or_, delete, create_engine, text, MetaData, Integer, String, Column, ForeignKey, Date, Time, DateTime, Boolean, extract
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, subqueryload, joinedload, relationship
from sqlalchemy.sql.expression import null

meta = MetaData()
Base = declarative_base()
engine = create_engine("postgresql://odya:o030101@92.63.206.61:5432/agrar")

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

class Complain_Data(Base):
    __tablename__ = 'complain_data'
    id = Column(Integer, primary_key=True)
    complain_id = Column(Integer, ForeignKey('complain.id')) 
    key = Column(String, nullable=False) # kafedra_id, teacher_id,  data_type(img,text,video,voice,doc) 
    value = Column(String, nullable=False)

"го гс в тг? ок"
class Session(Base):
    __tablename__ = 'session'
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, nullable=True)
    message = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    step = Column(String, nullable=True)
    category = Column(String, nullable=True)
    type = Column(String, nullable=True)
    username = Column(String, nullable=True)


def Reset():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

#Reset()
# categories = ['Ошхона', 'Ўқитувчи', 'TTJ (Ётоқхона)', 'Ҳожатхона']

session.close()

