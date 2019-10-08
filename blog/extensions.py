from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment


db = SQLAlchemy()
loginmanager = LoginManager()
migrate = Migrate()
moment = Moment()
