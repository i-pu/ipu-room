from flask import jsonify

from .config import app
from .models import Room, Plugin


@app.route('/room', methods=['GET'])
def get_rooms():
    rooms = Room.query.all()
    return jsonify(
        {
            'rooms': list(map(Room.__to_dict__, rooms)),
        }
    )


@app.route('/plugin', methods=['GET'])
def get_plugins():
    plugins = Plugin.query.all()
    return jsonify(
        {
            'plugins': list(map(Plugin.__to_dict__, plugins)),
        }
    )
