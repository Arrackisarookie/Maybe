from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment


bootstrap = Bootstrap()
db = SQLAlchemy()
loginmanager = LoginManager()
migrate = Migrate()
moment = Moment()
