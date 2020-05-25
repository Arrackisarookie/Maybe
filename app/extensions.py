from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment


db = SQLAlchemy()
loginmanager = LoginManager()
moment = Moment()
