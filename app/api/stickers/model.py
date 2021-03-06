from datetime import datetime

from app.api import db


class Sticker(db.Model):
    """
    Need to add Table Structure
    """
    __tablename__ = "stickers"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    image = db.Column(db.Text)
    is_deleted = db.Column(db.Boolean, default=0)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow())
