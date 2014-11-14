from flask import Blueprint, abort, jsonify, request

from app.api import db
from app.api.helpers import response_builder
from app.api.stickers.model import Sticker

mod = Blueprint('stickers', __name__, url_prefix='/api/stickers')


# {"title":"good", "image":"rtrt"}
@mod.route('/', methods=['POST'])
def new_sticker():
    title = request.json.get('title')
    image = request.json.get('image')
    if title is None or image is None:
        abort(400)  # missing arguments
    sticker = Sticker(title=title)
    db.session.add(sticker)
    db.session.commit()
    information = response_builder(sticker, Sticker)
    return jsonify({'status': 201, 'result': information}), 201


@mod.route('/<int:id>', methods=['PUT'])
def update_sticker(id):
    sticker = Sticker.query.get(id)
    if not sticker:
        abort(400)
    if request.json.get('title'):
        sticker.title = request.json.get('title')
    if request.json.get('image'):
        sticker.image = request.json.get('image')
    db.session.commit()
    sticker = Sticker.query.get(id)
    information = response_builder(sticker, Sticker)
    return jsonify({'status': 200, 'result': information}), 200


@mod.route('/<int:id>', methods=['GET'])
def get_sticker(id):
    sticker = Sticker.query.get(id)
    if not sticker:
        abort(400)  # sticker with `id` isn't exist
    information = response_builder(sticker, Sticker)
    return jsonify({'status': 200, 'result': information}), 200


@mod.route('/', methods=['GET'])
def get_all_stickers():
    stickers = []
    for sticker in Sticker.query.filter_by(is_deleted=0):
        information = response_builder(sticker, Sticker)
        stickers.append(information)
    return jsonify({'status': 200, 'result': stickers}), 200


@mod.route('/<int:id>', methods=['DELETE'])
def delete_sticker(id):
    sticker = Sticker.query.get(id)
    if not sticker:
        abort(400)  # sticker with `id` isn't exist
    db.session.delete(sticker)
    db.session.commit()
    return jsonify({'status': 200}), 200
