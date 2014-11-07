from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

from app import db, app


class User(db.Model):
    """
    Need to add Table Structure
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(length=250), unique=True, nullable=False, index=True)
    password = db.Column(db.String(length=64))  # hashed string with salt - SECRET_KEY
    first_name = db.Column(db.String(length=128), nullable=True)
    last_name = db.Column(db.String(length=128), nullable=True)
    phone = db.Column(db.String(length=20), nullable=True)
    city = db.Column(db.String(length=50), nullable=True)
    active = db.Column(db.Boolean, default=1)
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)
    registered_on = db.Column(db.DateTime)

    # links
    products = db.relationship('Product', backref='users', lazy='dynamic')
    reviews_to_user = db.relationship('Review', backref='users', lazy='dynamic')
    reviews_from_user = db.relationship('Review', backref='users', lazy='dynamic')
    comments = db.relationship('Comment', backref='users', lazy='dynamic')
    likes = db.relationship('Like', backref='users', lazy='dynamic')
    favorites = db.relationship('Favorite', backref='users', lazy='dynamic')
    ratings_to_user = db.relationship('Rating', backref='users', lazy='dynamic')
    ratings_from_user = db.relationship('Rating', backref='users', lazy='dynamic')
    subscribes_to_user = db.relationship('Subscribe', backref='users', lazy='dynamic')
    subscribes_from_user = db.relationship('Subscribe', backref='users', lazy='dynamic')

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    # TODO return status code
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user