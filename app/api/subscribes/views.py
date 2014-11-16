from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError

from app.api import db
from app.api.helpers import response_builder
from app.api.subscribes.model import Subscribe
from app.api.users.model import User


mod = Blueprint('subscribes', __name__, url_prefix='/api/subscribes')


# {"user_from_id":3, "user_to_id":2}
@mod.route('/', methods=['POST'])
def new_subscribe():
    user_from_id = request.json.get('user_from_id')
    user_to_id = request.json.get('user_to_id')
    if user_from_id is None or user_to_id is None:
        return jsonify({'error_code': 400, 'result': 'not ok'}), 200  # missing arguments
    subscribe = Subscribe(user_from_id=user_from_id, user_to_id=user_to_id)
    db.session.add(subscribe)
    try:
        db.session.commit()
    except IntegrityError:
        return jsonify({'error_code': 400, 'result': 'not ok'}), 200
    information = response_builder(subscribe, Subscribe)
    return jsonify({'error_code': 201, 'result': information}), 201


@mod.route('/from/<int:id>', methods=['GET'])
def get_subscribes_from_user(id):
    users = []
    for subscribe in Subscribe.query.filter_by(user_from_id=id):
        information = response_builder(User.query.get(subscribe.user_to_id), User, excluded=['password'])
        users.append(information)
    return jsonify({'error_code': 200, 'users': users}), 200


@mod.route('/to/<int:id>', methods=['GET'])
def get_subscribes_to_user(id):
    users = []
    for subscribe in Subscribe.query.filter_by(user_to_id=id):
        information = response_builder(User.query.get(subscribe.user_from_id), User, excluded=['password'])
        users.append(information)
    return jsonify({'error_code': 200, 'users': users}), 200


@mod.route('/<int:id>', methods=['DELETE'])
def delete_subscribe(id):
    subscribe = Subscribe.query.get(id)
    if not subscribe:
        return jsonify({'error_code': 400, 'result': 'not ok'}), 200  # rating with `id` isn't exist
    db.session.delete(subscribe)
    db.session.commit()
    return jsonify({'error_code': 200}), 200