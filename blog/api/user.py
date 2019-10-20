from flask import jsonify, request, url_for

from . import api
from ..extensions import db
from ..models import User


@api.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify({'users': [user.to_json() for user in users]}), 200


@api.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'No such user.'}), 404
    return jsonify(user.to_json()), 200


@api.route('/users', methods=['POST'])
def new_user():
    user = User.from_json(request.json)
    db.session.add(user)
    db.session.commit()

    return jsonify({'user': user.to_json()}), 201, {'Location': url_for('api.get_user', id=user.id)}


@api.route('/users/<int:id>', methods=['PUT'])
def edit_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'No such user.'}), 404
    user.username = request.json.get('username', user.username)
    user.password = request.json.get('password', user.password)
    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_json()), 200
