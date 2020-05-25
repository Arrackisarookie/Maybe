#
# -*- coding: utf-8 -*-
#
# @Author: Arrack
# @Date:   2020-05-25 15:19:12
# @Last modified by:   Arrack
# @Last Modified time: 2020-05-25 18:10:25
#
from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import SmallInteger

from app.extensions import db


class Base(db.Model):
    __abstract__ = True

    createTime = Column(Integer)
    updateTime = Column(Integer)
    availiblity = Column(SmallInteger, default=1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.createTime = int(datetime.now().timestamp())

    # todo:
    # update time fuction

    def delete(self):
        self.availiblity = 0
