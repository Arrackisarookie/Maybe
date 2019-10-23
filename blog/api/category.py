from flask import jsonify, request, url_for

from . import api
from ..extensions import db
from ..models.article import Category


@api.route('/category', methods=['GET'])
def get_categorys():
    categorys = Category.query.all()
    return jsonify({'categorys': [category.to_json() for category in categorys]}), 200


@api.route('/category/<name>', methods=['GET'])
def get_category(name):
    category = Category.query.filter_by(name=name).first()
    if not category:
        return jsonify({'error': 'No such category.'}), 404
    return jsonify(category.to_json()), 200


@api.route('/category', methods=['POST'])
def new_category():
    category = Category.from_json(request.json)
    db.session.add(category)
    db.session.commit()

    return jsonify({'category': category.to_json()}), 201, {'Location': url_for('api.get_category', id=category.id)}


@api.route('/category/<name>', methods=['PUT'])
def edit_category(name):
    category = Category.query.filter_by(name=name).first()
    if not category:
        return jsonify({'error': 'No such category.'}), 404
    category.name = request.json.get('name', category.name)
    category.slogan = request.json.get('slogan', category.slogan)

    db.session.add(category)
    db.session.commit()

    return jsonify(category.to_json()), 200
