from datetime import datetime

from app.api import db


class Favorite(db.Model):
    """
    Need to add Table Structure
    """
    __tablename__ = "favorites"

    id = db.Column(db.Integer, primary_key=True)
    is_deleted = db.Column(db.Boolean, default=0)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
