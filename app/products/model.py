from app import db


products_categories = db.Table('products_categories',
                               db.Column('product_id', db.Integer(), db.ForeignKey('products.id')),
                               db.Column('category_id', db.Integer(), db.ForeignKey('categories.id')))

products_stickers = db.Table('products_stickers',
                             db.Column('product_id', db.Integer(), db.ForeignKey('products.id')),
                             db.Column('sticker_id', db.Integer(), db.ForeignKey('stickers.id')))


class Product(db.Model):
    """
    Need to add Table Structure
    """
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(length=128), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.Text)
    creation_date = db.Column(db.DateTime)
    is_deleted = db.Column(db.Boolean, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # links
    comments = db.relationship('Comment', backref='products', lazy='dynamic')
    likes = db.relationship('Like', backref='products', lazy='dynamic')
    favorites = db.relationship('Favorite', backref='products', lazy='dynamic')
    categories = db.relationship('Category', secondary=products_categories,
                                 backref=db.backref('products', lazy='dynamic'))
    stickers = db.relationship('Sticker', secondary=products_stickers,
                               backref=db.backref('products', lazy='dynamic'))
