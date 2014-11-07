import os
import sys

from flask.ext.httpauth import HTTPBasicAuth
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
auth = HTTPBasicAuth()

# #######################
# Configure Secret Key #
# #######################


def install_secret_key(app, filename='secret_key'):
    """Configure the SECRET_KEY from a file
    in the instance directory.

    If the file does not exist, print instructions
    to create it from a shell with a random key,
    then exit.
    """
    filename = os.path.join(app.instance_path, filename)

    try:
        app.config['SECRET_KEY'] = open(filename, 'rb').read()
    except IOError:
        print('Error: No secret key. Create it with:')
        full_path = os.path.dirname(filename)
        if not os.path.isdir(full_path):
            print('mkdir -p {filename}'.format(filename=full_path))
        print('head -c 24 /dev/urandom > {filename}'.format(filename=filename))
        sys.exit(1)


if not app.config['DEBUG']:
    install_secret_key(app)

# @app.errorhandler(404)
# def not_found(error):
# return render_template('404.html'), 404

# Users module
from app.users.views import mod as users_module
app.register_blueprint(users_module)

# Products module
from app.products.views import mod as products_module

app.register_blueprint(products_module)

# Categories module
from app.categories.views import mod as categories_module

app.register_blueprint(categories_module)

# Reviews module
from app.reviews.views import mod as reviews_module

app.register_blueprint(reviews_module)

# Stickers module
from app.stickers.views import mod as stickers_module

app.register_blueprint(stickers_module)

# Comments module
from app.comments.views import mod as comments_module

app.register_blueprint(comments_module)

# Likes module
from app.likes.views import mod as likes_module

app.register_blueprint(likes_module)

# Ratings module
from app.ratings.views import mod as ratings_module

app.register_blueprint(ratings_module)

# Favorites module
from app.favorites.views import mod as favorites_module

app.register_blueprint(favorites_module)

# Subscribes module
from app.subscribes.views import mod as subscribes_module

app.register_blueprint(subscribes_module)

# Later on you'll import the other blueprints the same way:
#from app.comments.views import mod as commentsModule
#from app.posts.views import mod as postsModule
#app.register_blueprint(commentsModule)
#app.register_blueprint(postsModule)