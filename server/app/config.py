from flask_socketio import SocketIO
from flask import Flask

from .models import init_db


class Development(object):
    # Flask
    DEBUG = True

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # session
    SECRET_KEY = 'dev'


class Staging(object):
    # todo: create staging config
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'posgre'


Config = Development


class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        block_start_string='(%',
        block_end_string='%)',
        variable_start_string='((',
        variable_end_string='))',
        comment_start_string='(#',
        comment_end_string='#)',
    ))


app = CustomFlask(__name__)
socketio = SocketIO(app)


def create_app():
    app.config.from_object(Config)
    with app.app_context():
        init_db(app)
    from .chat import socketio

    return app, socketio
