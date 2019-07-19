from logging import basicConfig, DEBUG, getLogger
from uuid import uuid4

from flask_socketio import join_room, leave_room
from flask import request
import requests

from ..config import socketio, flask_app
from .. import utils
from .. import model

basicConfig()
mylogger = getLogger(__name__)
mylogger.setLevel(DEBUG)


@socketio.on('room/create')
@utils.byte_data_to_dict
@utils.check_user
@utils.function_info_wrapper
def room_create(data):
    room_name = data['roomName']
    plugin_ids = data['plugins']

    room = model.Room.create(str(uuid4()), room_name)

    members = []
    active_plugins = []
    for pi in plugin_ids:
        active_plugins.append(model.ActivePlugin.create(str(uuid4()),
                                                        pi,
                                                        room['id']))
    members, plugins = model.Room.make_json_elem(room['id'],
                                                 members,
                                                 active_plugins)
    socketio.emit('room/create',
                  data={'room': {**room,
                                 'members': members,
                                 'plugins': plugins}})


@socketio.on('room/enter')
@utils.byte_data_to_dict
@utils.check_user
@utils.function_info_wrapper
def room_enter(data):
    room_id = data['roomId']
    join_room(room_id)
    model.Room.enter(room_id, request.sid)
    room = model.Room.get(room_id)

    members, plugins = model.Room.make_json_elem(room_id, None, None)

    socketio.emit('room/update',
                  data={'room': {**room,
                                 'members': members,
                                 'plugins': plugins}},
                  room=room_id)
    socketio.emit('room/enter',
                  data={'room': {**room,
                                 'members': members,
                                 'plugins': plugins}},
                  room=request.sid)


@socketio.on('room/exit')
@utils.byte_data_to_dict
@utils.check_user
@utils.function_info_wrapper
def room_exit(data):
    user = model.User.get(request.sid, None)
    room_id = user['roomId']
    user = model.User.update(user['id'], user['name'], None)
    leave_room(room_id)

    room = model.Room.get(room_id)
    members, plugins = model.Room.make_json_elem(room_id, None, None)

    socketio.emit('room/exit', data=user, room=request.sid)
    socketio.emit('room/update',
                  data={'room': {**room,
                                 'members': members,
                                 'plugins': plugins}},
                  room=room_id)
