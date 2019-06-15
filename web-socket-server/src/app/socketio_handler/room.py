from logging import basicConfig, DEBUG, getLogger
from uuid import uuid4

from flask_socketio import join_room, leave_room
from flask import request

from ..config import socketio
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

    active_plugins = model.ActivePlugin.get(active_plugin_id=None,
                                            room_id=room_id)
    members, plugins = model.Room.make_json_elem(room_id, None, active_plugins)

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
    basicConfig()
    # user = User.query.filter_by(id=request.sid).one()
    # room_id = user.room_id
    # leave_room(room_id)

    # user.query.update({'room_id': None})
    # db.session.commit()

    # socketio.emit('room/exit')  # 抜けた人に通知

    # users = User.query.filter_by(room_id=room_id).all()

    # ret = {'members': list(map(User.__to_dict__, users))}
    # socketio.emit('room/exit_event',  # 残ってる人に通知
    #               data=ret,
    #               room=room_id)
