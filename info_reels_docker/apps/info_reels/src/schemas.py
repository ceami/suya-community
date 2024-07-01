# coding: utf-8
from datetime import date

from pydantic import BaseModel


class InforSchema(BaseModel):
    info_id: int
    notice: int
    title: str
    author: str
    date: date
    view: int
    link: str

    class Config:
        from_attributes = True
