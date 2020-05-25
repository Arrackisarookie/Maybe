from flask import jsonify, request, url_for

from . import api
from ..extensions import db
from ..models.article import Tag


@api.route('/tag', methods=['GET'])
def get_tags():
    tags = Tag.query.all()
    return jsonify({'tags': [tag.to_json() for tag in tags]}), 200


@api.route('/tag/<name>', methods=['GET'])
def get_tag(name):
    tag = Tag.query.filter_by(name=name).first()
    if not tag:
        return jsonify({'error': 'No such tag.'}), 404
    return jsonify(tag.to_json()), 200


@api.route('/tag', methods=['POST'])
def new_tag():
    tag = Tag.from_json(request.json)
    db.session.add(tag)
    db.session.commit()

    return jsonify({'tag': tag.to_json()}), 201, {'Location': url_for('api.get_tag', id=tag.id)}


@api.route('/tag/<name>', methods=['PUT'])
def edit_tag(name):
    tag = Tag.query.filter_by(name=name).first()
    if not tag:
        return jsonify({'error': 'No such tag.'}), 404
    tag.name = request.json.get('name', tag.name)
    tag.slogan = request.json.get('slogan', tag.slogan)

    db.session.add(tag)
    db.session.commit()

    return jsonify(tag.to_json()), 200
