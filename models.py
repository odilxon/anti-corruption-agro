from sqlalchemy import func, and_, delete, create_engine, text, MetaData, Integer, String, Column, ForeignKey, Date, Time, DateTime, Boolean, extract
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, subqueryload, joinedload, relationship

meta = MetaData()
Base = declarative_base()
engine = create_engine("postgresql://antiagro:antiagro@192.168.43.12:5432/antiagro")

Session = sessionmaker(bind=engine)
session = Session()

