from flask import g
from flask_httpauth import HTTPBasicAuth

from blog.models import User
from blog.api import api
from blog.api.errors import unauthorized, forbidden


auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    if username == '':
        return False
    user = User.query.filter_by(username=username).first()
    if not user:
        return False
    g.current_user = user
    return user.verify_password(password)


@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials.')


@api.before_request
@auth.login_required
def before_request():
    if not g.current_user:
        return forbidden('Unconfirmed account.')
