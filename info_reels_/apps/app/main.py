# from fastapi import FastAPI, Depends, Form
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import create_engine, Column, Integer, String, Date
# from sqlalchemy.orm import sessionmaker, Session
# from starlette.templating import Jinja2Templates
# from starlette.requests import Request
# from pydantic import BaseModel
# from typing import List
# from dotenv import load_dotenv
#
# import uvicorn
# import threading
# import requests
# import time
# import random
# from bs4 import BeautifulSoup
# import os
# from datetime import datetime
#
# load_dotenv()
#
# db_host = os.getenv('DB_URL')
#
# templates = Jinja2Templates(directory="info_reels/apps/app/templates")
# app = FastAPI()
#
# MINUTE = 60
# random_min = 10
# random_max = 20
#
# # 데이터베이스 연결 엔진 생성
# engine = create_engine(db_host, connect_args={"options": "-c timezone=utc"})
# Base = declarative_base()
#
#
# class InforDao(Base):
#     __tablename__ = "Info"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     notice = Column(String)
#     title = Column(String)
#     author = Column(String)
#     date = Column(Date)
#     view = Column(Integer)
#     link = Column(String)
#
#
# Base.metadata.create_all(engine)
#
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
#
# # 데이터베이스 세션 함수
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.commit()
#         db.close()
#
#
# class InforSchema(BaseModel):
#     id: int
#     notice: str
#     title: str
#     author: str
#     date: str
#     view: int
#     link: str
#
#     class Config:
#         from_attributes = True
#
#
# async def crawling(db: Session = Depends(get_db)):
#     global random_min, random_max
#     while True:
#
#
#         try:
#             for index in range(1, 6):
#                 url = f"https://www.syu.ac.kr/academic/academic-notice/page/{index}/"
#                 response = requests.get(url)
#                 html = response.content.decode('utf-8')
#                 soup = BeautifulSoup(html, 'html.parser')
#
#                 notices = soup.findAll('th', class_='step1')
#                 titles = soup.findAll('span', class_='tit')
#                 authors = soup.findAll('td', class_='step3')
#                 dates = soup.findAll('td', class_='step4')
#                 views = soup.findAll('td', class_='step6')
#                 links = soup.findAll('td', class_='step2')
#
#                 for elements in zip(notices, titles, authors, dates, views, links):
#                     notice, title, author, date, view, link = elements
#                     date_obj = datetime.strptime(date.text.strip(), "%Y.%m.%d").date()  # 날짜 문자열을 datetime.date 객체로 변환
#                     infor = InforDao(
#                         notice=notice.text.strip(),
#                         title=title.text.strip(),
#                         author=author.text.strip(),
#                         date=date_obj,  # 변환된 date 객체 사용
#                         view=int(view.text.strip().replace(',', '')),
#                         link=link.find('a', class_='itembx')['href']
#                     )
#
#                     db.add(infor)
#                 db.commit()
#         except Exception as e:
#             print(f"Error occurred: {e}")
#             db.rollback()
#         finally:
#             db.close()
#         time.sleep(MINUTE * random.randint(random_min, random_max))
#
#
# @app.get('/items', response_model=List[InforSchema])
# async def read_items(db: Session = Depends(get_db)):
#     items = db.query(InforDao).all()
#     return items
#
# @app.get("/")
# async def get_settings(request: Request):
#     return templates.TemplateResponse("settings.html", {"request": request, "random_min": random_min
#         , "random_max": random_max})
#
#
# @app.post("/settings")
# async def update_settings(random_min_val: int = Form(...), random_max_val: int = Form(...)):
#     global random_min, random_max
#     random_min = random_min_val
#     random_max = random_max_val
#     return {"message": "Settings updated", "random_min": random_min, "random_max": random_max}
#
#
# if __name__ == '__main__':
#     threading.Thread(target=crawling, daemon=True).start()
#
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
from fastapi import FastAPI, Depends, Form
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker, Session
from starlette.templating import Jinja2Templates
from starlette.requests import Request
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv

from datetime import date
import uvicorn
import multiprocessing
import requests
import time
import random
from bs4 import BeautifulSoup
import os
from datetime import datetime

load_dotenv()

db_host = os.getenv('DB_URL')

templates = Jinja2Templates(directory="info_reels/apps/app/templates")
app = FastAPI()

MINUTE = 60
random_min = 10
random_max = 20
pool = None
# 데이터베이스 연결 엔진 생성
engine = create_engine(db_host, connect_args={"options": "-c timezone=utc"})
Base = declarative_base()


class InforDao(Base):
    __tablename__ = "Info"
    id = Column(Integer, primary_key=True, autoincrement=True)
    notice = Column(String)
    title = Column(String)
    author = Column(String)
    date = Column(Date)
    view = Column(Integer)
    link = Column(String)


Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 데이터베이스 세션 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.commit()
        db.close()


class InforSchema(BaseModel):
    id: int
    notice: str
    title: str
    author: str
    date: date
    view: int
    link: str

    class Config:
        from_attributes = True


def crawling():
    global random_min, random_max
    db=SessionLocal()
    while True:
        try:
            for index in range(1, 6):
                url = f"https://www.syu.ac.kr/academic/academic-notice/page/{index}/"
                response = requests.get(url)
                html = response.content.decode('utf-8')
                soup = BeautifulSoup(html, 'html.parser')

                notices = soup.findAll('th', class_='step1')
                titles = soup.findAll('span', class_='tit')
                authors = soup.findAll('td', class_='step3')
                dates = soup.findAll('td', class_='step4')
                views = soup.findAll('td', class_='step6')
                links = soup.findAll('td', class_='step2')

                for elements in zip(notices, titles, authors, dates, views, links):
                    notice, title, author, date, view, link = elements
                    date_obj = datetime.strptime(date.text.strip(), "%Y.%m.%d").date()  # 날짜 문자열을 datetime.date 객체로 변환
                    infor = InforDao(
                        notice=notice.text.strip(),
                        title=title.text.strip(),
                        author=author.text.strip(),
                        date=date_obj,  # 변환된 date 객체 사용
                        view=int(view.text.strip().replace(',', '')),
                        link=link.find('a', class_='itembx')['href']
                    )

                    db.add(infor)
                db.commit()
        except Exception as e:
            print(f"Error occurred: {e}")
            db.rollback()
        finally:
            db.close()
        time.sleep(MINUTE * random.randint(random_min, random_max))


@app.get('/items', response_model=List[InforSchema])
async def read_items(request: Request,db: Session = Depends(get_db)):
    items = db.query(InforDao).all()
    return items

@app.get("/")
async def get_settings(request: Request):
    return templates.TemplateResponse("settings.html", {"request": request, "random_min": random_min
        , "random_max": random_max})

@app.get("/delete")
async def delete(request: Request,db: Session = Depends(get_db)):
    db.query(InforDao).delete()
    return templates.TemplateResponse("settings.html", {"request": request, "random_min": random_min
        , "random_max": random_max})

@app.post("/settings")
async def update_settings(random_min_val: int = Form(...), random_max_val: int = Form(...)):
    global random_min, random_max
    random_min = random_min_val
    random_max = random_max_val
    return {"message": "Settings updated", "random_min": random_min, "random_max": random_max}

@app.on_event("startup")
async def start_crawling():
    global pool
    pool = multiprocessing.Pool(processes=1)
    pool.apply_async(crawling)

@app.on_event("shutdown")
async def stop_crawling():
    global pool
    if pool:
        pool.terminate()
        pool.join()
        pool = None
        print("Stopped")

if __name__ == '__main__':

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
