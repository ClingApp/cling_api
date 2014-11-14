import logging
from logging.handlers import RotatingFileHandler
import os

import sys
from flask.ext.httpauth import HTTPBasicAuth
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy



# #######################
# Init                  #
# #######################


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

# #######################
# Views                 #
# #######################

# Users module
from app.api.users.views import mod as users_module

app.register_blueprint(users_module)

# Products module
from app.api.products.views import mod as products_module

app.register_blueprint(products_module)

# Categories module
from app.api.categories.views import mod as categories_module

app.register_blueprint(categories_module)

# Reviews module
from app.api.reviews.views import mod as reviews_module

app.register_blueprint(reviews_module)

# Stickers module
from app.api.stickers.views import mod as stickers_module

app.register_blueprint(stickers_module)

# Comments module
from app.api.comments.views import mod as comments_module

app.register_blueprint(comments_module)

# Likes module
from app.api.likes.views import mod as likes_module

app.register_blueprint(likes_module)

# Ratings module
from app.api.ratings.views import mod as ratings_module

app.register_blueprint(ratings_module)

# Favorites module
from app.api.favorites.views import mod as favorites_module

app.register_blueprint(favorites_module)

# Subscribes module
from app.api.subscribes.views import mod as subscribes_module

app.register_blueprint(subscribes_module)

# #######################
# Logs Handler          #
# #######################


formatter = logging.Formatter("%(asctime)s\t%(name)s\t%(message)s")

error_handler = RotatingFileHandler('logs/error.log', maxBytes=10000, backupCount=1)
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)
app.logger.addHandler(error_handler)

info_handler = RotatingFileHandler('logs/info.log', maxBytes=10000, backupCount=1)
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(formatter)
app.logger.addHandler(info_handler)