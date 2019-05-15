from flask import jsonify

from .config import app
from .models import Room, Plugin
from . import utils


@app.route('/room', methods=['GET'])
@utils.function_info_wrapper
def get_rooms():
    rooms = Room.query.all()
    return jsonify(
        {
            'rooms': list(map(Room.__to_dict__, rooms)),
        }
    )


@app.route('/plugin', methods=['GET'])
@utils.function_info_wrapper
def get_plugins():
    plugins = Plugin.query.all()
    return jsonify(
        {
            'plugins': list(map(Plugin.__to_dict__, plugins)),
        }
    )
