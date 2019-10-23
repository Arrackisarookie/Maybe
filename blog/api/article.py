from flask import jsonify, request, url_for

from . import api
from ..extensions import db
from ..models.article import Article


@api.route('/article', methods=['GET'])
def get_articles():
    articles = Article.query.all()
    return jsonify({'articles': [article.to_json() for article in articles]}), 200


@api.route('/article/<int:id>', methods=['GET'])
def get_article(id):
    article = Article.query.get(id)
    if not article:
        return jsonify({'error': 'No such article.'}), 404
    return jsonify(article.to_json()), 200


@api.route('/article', methods=['POST'])
def new_article():
    article = Article.from_json(request.json)
    db.session.add(article)
    db.session.commit()

    return jsonify({'article': article.to_json()}), 201, {'Location': url_for('api.get_article', id=article.id)}


@api.route('/article/<int:id>', methods=['PUT'])
def edit_article(id):
    article = Article.query.get(id)
    if not article:
        return jsonify({'error': 'No such article.'}), 404
    article.title = request.json.get('title', article.title)
    article.body = request.json.get('body', article.body)
    article.url = request.json.get('url', article.url)
    # ?
    article.cate_id = request.json.get('cate_id', article.cate_id)

    db.session.add(article)
    db.session.commit()

    return jsonify(article.to_json()), 200
