from app import db


class Rating(db.Model):
    """
    Need to add Table Structure
    """
    __tablename__ = "rating"

    id = db.Column(db.Integer, primary_key=True)
    vote = db.Column(db.Boolean, default=1)
    creation_date = db.Column(db.DateTime)
    is_deleted = db.Column(db.Boolean, default=0)
    user_from_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_to_id = db.Column(db.Integer, db.ForeignKey('users.id'))