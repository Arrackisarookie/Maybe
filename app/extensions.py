#
# -*- coding: utf-8 -*-
#
# @Author: Arrack
# @Date:   2020-05-25 17:17:05
# @Last modified by:   Arrack
# @Last Modified time: 2020-05-25 18:25:18
#

from contextlib import contextmanager

from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def autoCommit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


db = SQLAlchemy()
loginmanager = LoginManager()
