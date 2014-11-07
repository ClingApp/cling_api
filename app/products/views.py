from flask import Blueprint, abort, jsonify, request, url_for

from app import db
from app.products.model import Product
from app.users.model import User


mod = Blueprint('products', __name__, url_prefix='/api/products')


@mod.route('/', methods=['POST'])
def new_product():
    title = request.json.get('title')
    price = request.json.get('price')
    description = request.json.get('description')
    user = request.json.get('user')
    if title is None or price is None:
        abort(400)  # missing arguments
    user_instance = User.query.get(user)
    product = Product(title=title, price=price, description=description, user_id=user_instance.id)
    db.session.add(product)
    db.session.commit()
    return (jsonify({'username': user_instance.username, 'title': product.title}), 201,
            {'Location': url_for('.get_product', id=product.id, _external=True)})


@mod.route('/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    if not product:
        abort(400)  # product with `id` isn't exist
    return jsonify(product)