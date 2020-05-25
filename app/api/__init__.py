from flask import Blueprint

api = Blueprint('api', __name__)

from . import authentication, article, category, tag, user, talktalk, errors
