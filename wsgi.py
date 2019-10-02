from dotenv import load_dotenv
import os

from blog import create_app
from blog.extensions import db
from blog.models import Article, Category, User, Tag

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app = create_app(os.environ.get('FLASK_CONFIG') or 'default')


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Article=Article, Category=Category, User=User, Tag=Tag)


@app.cli.command()
def test():
    """ Run the unit tests. """
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
