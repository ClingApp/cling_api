from flask import Blueprint, abort, jsonify, request

from app import db
from app.helpers import get_info
from app.categories.model import Category

mod = Blueprint('categories', __name__, url_prefix='/api/categories')


# {"title":"good"}
@mod.route('/', methods=['POST'])
def new_category():
    title = request.json.get('title')
    if title is None:
        abort(400)  # missing arguments
    category = Category(title=title)
    db.session.add(category)
    db.session.commit()
    information = get_info(category, Category, [])
    return jsonify({'status': 201, 'result': information}), 201


@mod.route('/<int:id>', methods=['PUT'])
def update_category(id):
    category = Category.query.get(id)
    if not category:
        abort(400)
    if request.json.get('title'):
        category.title = request.json.get('title')
    db.session.commit()
    category = Category.query.get(id)
    information = get_info(category, Category, [])
    return jsonify({'status': 200, 'result': information}), 200


@mod.route('/<int:id>', methods=['GET'])
def get_category(id):
    category = Category.query.get(id)
    if not category:
        abort(400)  # category with `id` isn't exist
    information = get_info(category, Category, [])
    return jsonify({'status': 200, 'result': information}), 200


@mod.route('/', methods=['GET'])
def get_all_categories():
    categories = []
    for category in Category.query.filter_by(is_deleted=0):
        information = get_info(category, Category, not_used='password')
        categories.append(information)
    return jsonify({'status': 200, 'result': categories}), 200


@mod.route('/<int:id>', methods=['DELETE'])
def delete_category(id):
    category = Category.query.get(id)
    if not category:
        abort(400)  # category with `id` isn't exist
    db.session.delete(category)
    db.session.commit()
    return jsonify({'status': 200}), 200