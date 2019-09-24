import os

from dotenv import load_dotenv

from blog import create_app
from blog.generate import Generate

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app = create_app()
