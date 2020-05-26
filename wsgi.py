#
# -*- coding: utf-8 -*-
#
# @Author: Arrack
# @Date:   2020-05-26 11:37:21
# @Last modified by:   Arrack
# @Last Modified time: 2020-05-26 17:03:33
#

import os

from dotenv import load_dotenv

from app import create_app
from app.extensions import db
from app.models import Article
from app.models import Category
from app.models import Tag
from app.models import User


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
app = create_app(os.environ.get('FLASK_CONFIG') or 'default')


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Article=Article, Category=Category, User=User, Tag=Tag)


@app.context_processor
def inject_models():
    return dict(Article=Article, Category=Category, User=User, Tag=Tag)


@app.context_processor
def inject_title():
    return dict(title=app.config['SITE_TITLE'], subtitle=app.config['SITE_SUBTITLE'])


@app.cli.command()
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
