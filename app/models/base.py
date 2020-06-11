#
# -*- coding: utf-8 -*-
#
# @Author: Arrack
# @Date:   2020-05-25 15:19:12
# @Last modified by:   Arrack
# @Last Modified time: 2020-06-10 14:50:06
#
from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import SmallInteger

from app.extensions import db


class Base(db.Model):
    __abstract__ = True

    createTime = Column(DateTime, default=datetime.utcnow)
    updateTime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    availiblity = Column(SmallInteger, default=1)

    # def __init__(self, **kwargs):
    #     if '_createTime' in kwargs.keys() and isinstance(kwargs['_createTime'], datetime):
    #         self.createTime = int(kwargs.pop('_createTime').timestamp())
    #     else:
    #         self.createTime = int(datetime.now().timestamp())
    #     super().__init__(**kwargs)

    # todo:
    # update time fuction

    # @property
    # def createDatetime(self):
    #     return datetime.utcfromtimestamp(self.createTime).strftime('%Y-%m-%d %H:%M:%S')

    def delete(self):
        self.availiblity = 0
