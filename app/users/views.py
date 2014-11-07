from flask import abort, request, jsonify, g, url_for, Blueprint

from app import db, auth
from app.users.model import User


mod = Blueprint('users', __name__, url_prefix='/api')


@auth.verify_password
def verify_password(email_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(email_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(email=email_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@mod.route('/users', methods=['POST'])
def new_user():
    email = request.json.get('email')
    password = request.json.get('password')
    if email is None or password is None:
        abort(400)  # missing arguments
    if User.query.filter_by(email=email).first() is not None:
        abort(400)  # existing user
    user = User(email=email)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return (jsonify({'email': user.email}), 201,
            {'Location': url_for('.get_user', id=user.id, _external=True)})


@mod.route('/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'email': user.email})


@mod.route('/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})


@mod.route('/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.email})