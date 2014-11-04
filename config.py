import os

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

ADMINS = frozenset(['ff.warprobot@gmail.com'])
SECRET_KEY = 'This string will be replaced with a proper key in production.'
SERVER_NAME = 'localhost:5000'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'app.db')
DATABASE_CONNECT_OPTIONS = {}

THREADS_PER_PAGE = 8  # need more tests