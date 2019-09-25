from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_uploads import UploadSet
from flask_sqlalchemy import SQLAlchemy


bootstrap = Bootstrap()
db = SQLAlchemy()
loginmanager = LoginManager()
markdowns = UploadSet('markdown', ('md'))


@loginmanager.user_loader
def load_user(username):
    from blog.views.admin import query_user, User
    if query_user(username) is not None:
        cur_user = User
        cur_user.id = username
        return cur_user
    return None


loginmanager.login_view = 'admin.login'
loginmanager.login_message = '你特娘的请登录啊，管理员'
