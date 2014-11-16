from flask import Blueprint, jsonify, request

from app.api import db
from app.api.helpers import response_builder
from app.api.comments.model import Comment

mod = Blueprint('comments', __name__, url_prefix='/api/comments')


# {"text":"good^^", "user_id":3, "product_id":2}
@mod.route('/', methods=['POST'])
def new_comment():
    text = request.json.get('text')
    user_id = request.json.get('user_id')
    product_id = request.json.get('product_id')
    if text is None or user_id is None or product_id is None:
        return jsonify({'error_code': 400, 'result': 'not ok'}), 200  # missing arguments
    comment = Comment(text=text, user_id=user_id, product_id=product_id)
    db.session.add(comment)
    db.session.commit()
    information = response_builder(comment, Comment)
    return jsonify({'error_code': 201, 'result': information}), 201


@mod.route('/<int:id>', methods=['PUT'])
def update_comment(id):
    comment = Comment.query.get(id)
    if not comment:
        return jsonify({'error_code': 400, 'result': 'not ok'}), 200
    if request.json.get('text'):
        comment.text = request.json.get('text')
    db.session.commit()
    comment = Comment.query.get(id)
    information = response_builder(comment, Comment)
    return jsonify({'error_code': 200, 'result': information}), 200


@mod.route('/<int:id>', methods=['GET'])
def get_comment(id):
    comment = Comment.query.get(id)
    if not comment:
        return jsonify({'error_code': 400, 'result': 'not ok'}), 200  # comment with `id` isn't exist
    information = response_builder(comment, Comment)
    return jsonify({'error_code': 200, 'result': information}), 200


@mod.route('/', methods=['GET'])
def get_all_comments():
    comments = []
    for comment in Comment.query.filter_by(is_deleted=0):
        information = response_builder(comment, Comment)
        comments.append(information)
    return jsonify({'error_code': 200, 'result': comments}), 200


@mod.route('/<int:id>', methods=['DELETE'])
def delete_comment(id):
    comment = Comment.query.get(id)
    if not comment:
        return jsonify({'error_code': 400, 'result': 'not ok'}), 200  # comment with `id` isn't exist
    db.session.delete(comment)
    db.session.commit()
    return jsonify({'error_code': 200}), 200