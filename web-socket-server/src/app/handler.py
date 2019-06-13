from flask import jsonify

from .config import app
from .models import Room, Plugin
from . import utils


@app.route('/healthz')
def hello():
    return 'healthz'
