from flask import jsonify

from .config import app
from .models import Room


@app.route('/room', methods=['GET'])
def get_rooms():
    rooms = Room.query().all()
    return jsonify(
        {
            rooms: rooms
        }
    )
