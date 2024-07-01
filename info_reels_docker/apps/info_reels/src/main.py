# coding: utf-8
import multiprocessing
from typing import List

import psutil
import uvicorn
from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from .jobs import crawling
from .models import InforDao
from .schemas import InforSchema
from .utils import get_db

templates = Jinja2Templates(directory='src/templates')
app = FastAPI()
app.mount('/static', StaticFiles(directory='src/static'), name='static')
pool = None


@app.get('/')
async def get_settings(request: Request):
    return templates.TemplateResponse(request=request, name='home.html')


@app.get('/info')
async def info():
    return RedirectResponse(url='/docs')


@app.get('/items', response_model=List[InforSchema])
async def read_items(request: Request, db: Session = Depends(get_db)):
    items = db.query(InforDao).all()
    items.sort(reverse=True, key=lambda x: (x.notice, x.date))
    return templates.TemplateResponse(request=request,
                                      name='board.html',
                                      context={'items': items})


@app.get('/dashboard')
def get_usage_data():
    cpu_usage = int(psutil.cpu_percent(interval=1))
    hdd_usage = int(psutil.disk_usage('/').percent)
    mem_usage = int(psutil.virtual_memory().percent)
    return {
        'cpu_usage': cpu_usage,
        'hdd_usage': hdd_usage,
        'mem_usage': mem_usage
    }


@app.get('/api/items', response_model=List[InforSchema])
async def api_read_items(db: Session = Depends(get_db)):
    items = db.query(InforDao).all()
    items.sort(reverse=True, key=lambda x: (x.notice, x.date))
    return items


@app.on_event('startup')
async def start_crawling():
    global pool
    pool = multiprocessing.Pool(processes=1)
    pool.apply_async(crawling)


@app.on_event('shutdown')
async def stop_crawling():
    global pool
    if pool:
        pool.terminate()
        pool.join()
        pool = None
        print('Stopped')


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
