import os

from flask_socketio import SocketIO
from flask import Flask
from flask_cors import CORS


class Dev(object):
    DEBUG = True
    SECRET_KEY = 'dev'
    DC_PORT = os.getenv('DC_PORT')
    DC_URL = os.getenv('DC_URL')


class Prd(object):
    DEBUG = False
    SECRET_KEY = 'prd'
    DC_PORT = os.getenv('DC_PORT')
    DC_URL = os.getenv('DC_URL')


app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)


def create_app(env):
    if env == 'prd':
        app.config.from_object(Prd)
    elif env == 'dev':
        app.config.from_object(Dev)
    else:
        raise Exception("env must be set!")

    # init
    # with app.app_context():
    #     init_db(app)

    from . import socketio_handler
    from . import handler

    return app, socketio
