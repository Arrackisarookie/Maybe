from flask import g, jsonify
from flask_httpauth import HTTPBasicAuth

from blog.models.user import User
from blog.api import api
from blog.api.errors import unauthorized


auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # Try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.current_user = user
    return True


@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials.')


@api.before_request
@auth.login_required
def before_request():
    pass


@api.route('/token', methods=['POST'])
def get_auth_token():
    token = g.current_user.generate_auth_token(expiration=600)
    return jsonify({'token': token.decode('ascii'), 'expiration': 600})
