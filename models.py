from sqlalchemy import func, and_, delete, create_engine, text, MetaData, Integer, String, Column, ForeignKey, Date, Time, DateTime, Boolean, extract
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, subqueryload, joinedload, relationship
from sqlalchemy.sql.expression import null

meta = MetaData()
Base = declarative_base()
engine = create_engine("postgresql://antiagro:antiagro@192.168.43.12:5432/antiagro")

Session = sessionmaker(bind=engine)
session = Session()


class Kafedra(Base):
    __tablename__ = 'kafedra'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    teachers = relationship("Teacher", backref="kafedra", lazy=True)
    sessions = relationship("Session", backref="kafedra", lazy=True)


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
    complain = relationship("Complain", backref="teacher", lazy=True)
    session = relationship("Session", backref="teacher", lazy=True)


class Complain(Base):
    __tablename__ = 'complain'
    id = Column(Integer, primary_key=True)
    message = Column(String, nullable=False)
    type = Column(String, nullable=True)
    teacher_id = Column(Integer, ForeignKey("teacher.id"))
    first_name = Column(String, nullable=True)
    username = Column(String, nullable=True)
    chat_id = Column(Integer, nullable=True)

class Session(Base):
    __tablename__ = 'session'
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, nullable=True)
    kafedra_id = Column(Integer, ForeignKey("kafedra.id"), nullable=True)
    teacher_id = Column(Integer, ForeignKey("teacher.id"), nullable=True)
    message = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    step = Column(String, nullable=True)
    type = Column(String, nullable=True)
    username = Column(String, nullable=True)


def Reset():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

#Reset()

session.close()

