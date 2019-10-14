from dotenv import load_dotenv
import os

from blog import create_app
from blog.extensions import db
from blog.models import About, Article, Category, User, Tag, Talk, Top

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app = create_app(os.environ.get('FLASK_CONFIG') or 'default')


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, About=About, Article=Article, Category=Category, User=User, Tag=Tag, Talk=Talk, Top=Top)


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
