from flask import Blueprint, abort, jsonify, request

from app import db
from app.helpers import response_builder
from app.ratings.model import Rating
from app.users.model import User

mod = Blueprint('ratings', __name__, url_prefix='/api/ratings')


# {"vote":1, "user_from_id":3, "user_to_id":2}
@mod.route('/', methods=['POST'])
def new_rating():
    vote = request.json.get('vote')
    user_from_id = request.json.get('user_from_id')
    user_to_id = request.json.get('user_to_id')
    if vote is None or user_from_id is None or user_to_id is None:
        abort(400)  # missing arguments
    rating = Rating(vote=vote, user_from_id=user_from_id, user_to_id=user_to_id)
    db.session.add(rating)
    db.session.commit()
    information = response_builder(rating, Rating)
    return jsonify({'status': 201, 'result': information}), 201


@mod.route('/<int:id>', methods=['GET'])
def get_rating(id):
    users = []
    amount = Rating.query.filter_by(user_to_id=id, vote=1).count() - \
             Rating.query.filter_by(user_to_id=id, vote=0).count()
    for rating in Rating.query.filter_by(user_to_id=id):
        information = response_builder(User.query.get(rating.user_from_id), User, excluded=['password'])
        users.append(information)
    return jsonify({'status': 200, 'amount': amount, 'users': users}), 200


@mod.route('/<int:id>', methods=['DELETE'])
def delete_rating(id):
    rating = Rating.query.get(id)
    if not rating:
        abort(400)  # rating with `id` isn't exist
    db.session.delete(rating)
    db.session.commit()
    return jsonify({'status': 200}), 200