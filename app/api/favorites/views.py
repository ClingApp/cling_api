from flask import Blueprint, abort, jsonify, request, g

from app.api import db
from app.api.helpers import response_builder
from app.api.favorites.model import Favorite
from app.api.products.model import Product

mod = Blueprint('favorites', __name__, url_prefix='/api/favorites')


# {"user_id":3, "product_id":2}
@mod.route('/', methods=['POST'])
def new_favorite():
    user_id = request.json.get('user_id')
    product_id = request.json.get('product_id')
    if user_id is None or product_id is None:
        abort(400)  # missing arguments
    favorite = Favorite(user_id=user_id, product_id=product_id)
    db.session.add(favorite)
    db.session.commit()
    information = response_builder(favorite, Favorite)
    return jsonify({'status': 201, 'result': information}), 201


@mod.route('/', methods=['GET'])
def get_favorite():
    user_id = g.user.id
    favorites = Favorite.query.filter_by(user_id=user_id)
    products = []
    for favorite in favorites:
        information = response_builder(Product.query.get(favorite.product_id), Product)
        products.append(information)
    return jsonify({'status': 200, 'products': products}), 200


@mod.route('/<int:id>', methods=['DELETE'])
def delete_favorite(id):
    favorite = Favorite.query.get(id)
    if not favorite:
        abort(400)  # favorite with `id` isn't exist
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({'status': 200}), 200