import os

from flask_socketio import SocketIO
from flask import Flask

from .models import init_db


class Development(object):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
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


def create_app(env=None):
    if env == 'docker-compose':
        app.config.from_object(Staging)
    else:
        app.config.from_object(Development)
    with app.app_context():
        init_db(app)
    from .chat import socketio

    return app, socketio
