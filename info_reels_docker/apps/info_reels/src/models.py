# coding: utf-8
import os

from dotenv import load_dotenv
from sqlalchemy import Column, Date, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()
db_host = os.getenv('DB_URL')
engine = create_engine(db_host, connect_args={'options': '-c timezone=utc'})
Base = declarative_base()


class InforDao(Base):
    __tablename__ = 'Info'
    info_id = Column(Integer, primary_key=True, autoincrement=True)
    notice = Column(Integer)
    title = Column(String)
    author = Column(String)
    date = Column(Date)
    view = Column(Integer)
    link = Column(String)


Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
