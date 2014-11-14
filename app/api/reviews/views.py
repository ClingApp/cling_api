from flask import Blueprint, abort, jsonify, request

from app.api import db
from app.api.helpers import response_builder
from app.api.reviews.model import Review
from app.api.users.model import User

mod = Blueprint('reviews', __name__, url_prefix='/api/reviews')


# {"text":"fttyft", "user_from_id":3, "user_to_id":2}
@mod.route('/', methods=['POST'])
def new_review():
    text = request.json.get('text')
    user_from_id = request.json.get('user_from_id')
    user_to_id = request.json.get('user_to_id')
    if text is None or user_from_id is None or user_to_id is None:
        abort(400)  # missing arguments
    review = Review(text=text, user_from_id=user_from_id, user_to_id=user_to_id)
    db.session.add(review)
    db.session.commit()
    information = response_builder(review, Review)
    return jsonify({'status': 201, 'result': information}), 201


@mod.route('/<int:id>', methods=['PUT'])
def update_review(id):
    review = Review.query.get(id)
    if not review:
        abort(400)
    if request.json.get('text'):
        review.text = request.json.get('text')
    db.session.commit()
    review = Review.query.get(id)
    information = response_builder(review, Review)
    return jsonify({'status': 200, 'result': information}), 200


@mod.route('/<int:id>', methods=['GET'])
def get_reviews(id):
    reviews = []
    for review in Review.query.filter_by(user_to_id=id):
        information = {}
        information['user_from'] = response_builder(User.query.get(review.user_from_id), User, excluded=['password'])
        information['text'] = review.text
        reviews.append(information)
    return jsonify({'status': 200, 'reviews': reviews}), 200


@mod.route('/<int:id>', methods=['DELETE'])
def delete_review(id):
    review = Review.query.get(id)
    if not review:
        abort(400)  # review with `id` isn't exist
    db.session.delete(review)
    db.session.commit()
    return jsonify({'status': 200}), 200