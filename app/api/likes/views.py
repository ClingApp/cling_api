from flask import Blueprint, abort, jsonify, request

from app.api import db
from app.api.helpers import response_builder
from app.api.likes.model import Like
from app.api.users.model import User


mod = Blueprint('likes', __name__, url_prefix='/api/likes')


# {"user_id":3, "product_id":2}
@mod.route('/', methods=['POST'])
def new_like():
    user_id = request.json.get('user_id')
    product_id = request.json.get('product_id')
    if user_id is None or product_id is None:
        abort(400)  # missing arguments
    like = Like(user_id=user_id, product_id=product_id)
    db.session.add(like)
    db.session.commit()
    information = response_builder(like, Like)
    return jsonify({'status': 201, 'result': information}), 201


@mod.route('/<int:id>', methods=['GET'])
def get_likes(id):
    liked_users = []
    amount = Like.query.filter_by(product_id=id).count()
    for like in Like.query.filter_by(product_id=id):
        information = response_builder(User.query.get(like.user_id), User, excluded=['password'])
        liked_users.append(information)
    return jsonify({'status': 200, 'amount': amount, 'users': liked_users}), 200


@mod.route('/<int:id>', methods=['DELETE'])
def delete_like(id):
    like = Like.query.get(id)
    if not like:
        abort(400)  # like with `id` isn't exist
    db.session.delete(like)
    db.session.commit()
    return jsonify({'status': 200}), 200