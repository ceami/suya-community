# coding: utf-8
import random
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from .models import InforDao, SessionLocal


def crawling():
    MINUTE = 60
    random_min = 10
    random_max = 20
    start_index = 1
    end_index = 10
    db = SessionLocal()
    while True:
        try:
            db.query(InforDao).delete()
            for index in range(start_index, end_index):
                url = 'https://www.syu.ac.kr/academic/academic-notice/page/' \
                      f'{index}/'
                response = requests.get(url)
                html = response.content.decode('utf-8')
                soup = BeautifulSoup(html, 'html.parser')
                notices = soup.findAll('th', class_='step1')
                titles = soup.findAll('span', class_='tit')
                authors = soup.findAll('td', class_='step3')
                dates = soup.findAll('td', class_='step4')
                views = soup.findAll('td', class_='step6')
                links = soup.findAll('td', class_='step2')

                for elements in zip(notices, titles, authors, dates, views,
                                    links):
                    notice, title, author, date, view, link = elements
                    date_obj = datetime.strptime(
                        date.text.strip(),
                        '%Y.%m.%d').date()  # 날짜 문자열 을 datetime.date 객체로 변환
                    notice = notice.text.strip()
                    infor = InforDao(
                        notice=int(notice) if notice.isdigit() else 9999999,
                        title=title.text.strip(),
                        author=author.text.strip(),
                        date=date_obj,  # 변환된 date 객체 사용
                        view=int(view.text.strip().replace(',', '')),
                        link=link.find('a', class_='itembx')['href'])
                    db.add(infor)
        except Exception as e:
            print(f'Error occurred: {e}')
            db.rollback()
        finally:
            db.commit()
            db.close()
        time.sleep(MINUTE * random.randint(random_min, random_max))
