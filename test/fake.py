#
# -*- coding: utf-8 -*-
#
# @Author: Arrack
# @Date:   2020-05-27 16:02:25
# @Last modified by:   Arrack
# @Last Modified time: 2020-05-27 16:29:13
#

from faker import Faker

from app.extensions import db
from app.models import Talk


def fakeTalks(count=50):
    fake = Faker('zh_CN')
    i = 0
    with db.autoCommit():
        while i < count:
            t = Talk(
                content=fake.paragraph(nb_sentences=1),
                _createTime=fake.date_time())
            db.session.add(t)
            i += 1
    return count
