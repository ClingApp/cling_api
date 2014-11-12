from app import db


class Review(db.Model):
    """
    Need to add Table Structure
    """
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    creation_date = db.Column(db.DateTime)
    is_deleted = db.Column(db.Boolean, default=0)
    user_from_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_to_id = db.Column(db.Integer, db.ForeignKey('users.id'))
