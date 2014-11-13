from flask import Blueprint, abort, jsonify, request, url_for

from app import db
from app.helpers import get_info
from app.products.model import Product
from app.users.model import User


mod = Blueprint('products', __name__, url_prefix='/api/products')

# {"title":"smth","price":"3000","description":"","user":"3"}
@mod.route('/', methods=['POST'])
def new_product():
    title = request.json.get('title')
    price = request.json.get('price')
    description = request.json.get('description')
    user = request.json.get('user')
    image = request.json.get('image')
    if title is None or price is None:
        abort(400)  # missing arguments
    user_instance = User.query.get(user)
    product = Product(title=title, price=price, description=description, image=image, user_id=user_instance.id)
    db.session.add(product)
    db.session.commit()
    return (jsonify({'email': user_instance.email, 'title': product.title}), 201,
            {'Location': url_for('.get_product', id=product.id, _external=True)})


@mod.route('/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)
    if not product:
        abort(400)
    if request.json.get('title'):
        product.title = request.json.get('title')
    if request.json.get('price'):
        product.price = request.json.get('price')
    if request.json.get('description'):
        product.description = request.json.get('description')
    if request.json.get('image'):
        product.image = request.json.get('image')
    db.session.commit()
    product = Product.query.get(id)
    information = get_info(product, Product, [])
    return jsonify({'status': 200, 'result': information}), 200


@mod.route('/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    if not product:
        abort(400)  # product with `id` isn't exist
    information = get_info(product, Product, [])
    return jsonify({'status': 200, 'result': information}), 200


@mod.route('/', methods=['GET'])
def get_all_products():
    products = []
    for product in Product.query.filter_by(is_deleted=0):
        information = get_info(product, Product, not_used='password')
        products.append(information)
    return jsonify({'status': 200, 'result': products}), 200


@mod.route('/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        abort(400)  # product with `id` isn't exist
    db.session.delete(product)
    db.session.commit()
    return jsonify({'status': 200}), 200