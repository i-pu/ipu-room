import os

from flask_socketio import SocketIO
from flask import Flask
from flask_cors import CORS

from .models import init_db


class Development(object):
    DEBUG = True
    SECRET_KEY = 'dev'


class Staging(object):
    DEBUG = True
    SECRET_KEY = 'stage'


app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)


def create_app(env):
    if env == 'docker-compose':
        app.config.from_object(Staging)
    else:
        app.config.from_object(Development)

    # init
    # with app.app_context():
    #     init_db(app)

    from . import socketio_handler
    from . import handler

    return app, socketio
