from flask import Blueprint

from app import db

from app.stickers.model import Sticker


mod = Blueprint('stickers', __name__, url_prefix='/api/stickers')


@mod.route('/', methods=['POST', 'GET'])
def create_stickers():
    """
    Create a sticker with name, taken from sent filename
    """
    # if request.method == 'POST':
    # file
    sticker = Sticker(title="test")
    db.session.add(sticker)
    db.session.commit()