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
    plugins = data['plugins']

    json = model.Room.create(str(uuid4()), room_name, plugins)

    members = []
    plugins = []
    socketio.emit('room/create',
                  data={'room': {**json,
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
    print("ok enter", flush=True)
    json = model.Room.get(room_id)
    print("ok get", flush=True)
    members = []
    plugins = []
    # todo: maybe room_update
    socketio.emit('room/enter',
                  data={'room': {**json,
                                 'members': members,
                                 'plugins': plugins}},
                  room=room_id)


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
