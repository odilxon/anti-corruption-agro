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
    teacher = relationship("Teacher", back_populates="kafedra")
    session = relationship("Session", back_populates="kafedra")


class Teacher(Base):
    __tablename__ = 'teacher'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    kafedra_id = Column(Integer, ForeignKey("kafedra.id"))
    complain = relationship("Complain", back_populates="teacher")
    session = relationship("Session", back_populates="teacher")


class Complain(Base):
    __tablename__ = 'complain'
    id = Column(Integer, primary_key=True)
    message = Column(String, nullable=False)
    teacher_id = Column(Integer, ForeignKey("teacher.id"))


class Session(Base):
    __tablename__ = 'session'
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, nullable=True)
    kafedra = Column(String, ForeignKey("kafedra.id"), nullable=True)
    teacher = Column(String, ForeignKey("teacher.id"), nullable=True)
    message = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    username = Column(String, nullable=True)


# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
session.close()