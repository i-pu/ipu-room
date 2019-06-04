from uuid import uuid4

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)
    # db.create_all()


def uuid4_for_str():
    return str(uuid4())
