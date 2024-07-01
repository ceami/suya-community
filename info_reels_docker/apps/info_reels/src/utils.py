# coding: utf-8
from .models import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.commit()
        db.close()
