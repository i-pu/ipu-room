import os

from flask_socketio import SocketIO
from flask import Flask
from flask_cors import CORS

from .models import init_db


class Development(object):
    DEBUG = True
    SQLITE_PATH = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'models',
        'test.db',
    )
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + SQLITE_PATH
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'dev'


class Staging(object):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{password}@{host}/{database}'.format(**{
        'user': os.getenv('POSTGRES_USER'),
        'password': os.getenv('POSTGRES_PASSWORD'),
        'host': os.getenv('POSTGRES_HOST'),
        'database': os.getenv('POSTGRES_DB'),
    })
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'stage'


app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

global_plugins = {}


def create_app(env):
    if env == 'docker-compose':
        app.config.from_object(Staging)
    else:
        app.config.from_object(Development)

    # init
    with app.app_context():
        init_db(app)

    from .socketio_handler import socketio

    return app, socketio
