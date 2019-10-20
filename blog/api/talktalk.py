from flask import jsonify, request, url_for

from . import api
from ..extensions import db
from ..models import Talk


@api.route('/talktalk', methods=['GET'])
def get_talks():
    talks = Talk.query.all()
    return jsonify({'talks': [talk.to_json() for talk in talks]}), 200


@api.route('/talktalk/<int:id>', methods=['GET'])
def get_talk(id):
    talk = Talk.query.get(id)
    if not talk:
        return jsonify({'error': 'No such talk.'}), 404
    return jsonify(talk.to_json()), 200


@api.route('/talktalk', methods=['POST'])
def new_talk():
    talk = Talk.from_json(request.json)
    db.session.add(talk)
    db.session.commit()

    return jsonify({'talk': talk.to_json()}), 201, {'Location': url_for('api.get_talk', id=talk.id)}


@api.route('/talktalk/<int:id>', methods=['PUT'])
def edit_talk(name):
    talk = Talk.query.get(id)
    if not talk:
        return jsonify({'error': 'No such talk.'}), 404
    talk.name = request.json.get('content', talk.content)
    talk.private = request.json.get('private', talk.private)

    db.session.add(talk)
    db.session.commit()

    return jsonify(talk.to_json()), 200
