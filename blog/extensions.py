from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_uploads import UploadSet
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


bootstrap = Bootstrap()
db = SQLAlchemy()
loginmanager = LoginManager()
markdowns = UploadSet('markdown', ('md'))
migrate = Migrate()
