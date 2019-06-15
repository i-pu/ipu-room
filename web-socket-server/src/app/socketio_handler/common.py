from logging import basicConfig, DEBUG, getLogger
from flask import request
from flask_socketio import leave_room

from ..config import socketio
from .. import utils
from .. import model

basicConfig()
mylogger = getLogger(__name__)
mylogger.setLevel(DEBUG)


@socketio.on('sample')
@utils.byte_data_to_dict
@utils.function_info_wrapper
def sample(data):
    mylogger.debug('- - socket id: {}'.format(request.sid))


@socketio.on('visit')
@utils.byte_data_to_dict
@utils.function_info_wrapper
def visit(data):
    json = model.User.create(request.sid, data['userName'])
    mylogger.info(json)
    socketio.emit('visit', data={'user': json}, room=request.sid)


@socketio.on('lobby')
@utils.byte_data_to_dict
@utils.check_user
@utils.function_info_wrapper
def lobby(data):
    json = model.Room.get()
    mylogger.info(json)
    socketio.emit('lobby', data={'rooms': json}, room=request.sid)


@socketio.on('disconnect')
@utils.byte_data_to_dict
@utils.check_user
@utils.function_info_wrapper
def disconnect(data):
    """
    データベースから削除して部屋を更新して通知する
    """
    room_id = model.User.get(request.sid, None)['roomId']
    if room_id is not None:
        leave_room(room_id)
        model.User.delete(request.sid)
        room = model.Room.get(room_id)
        active_plugins = model.ActivePlugin.get(None, room_id)
        members, plugins = model.Room.make_json_elem(room_id,
                                                     None,
                                                     active_plugins)
        socketio.emit('room/update',
                      data={'room': {**room,
                                     'members': members,
                                     'plugins': plugins}},
                      room=room_id)


@socketio.on_error()
def on_error(e):
    mylogger.error('error happen!!!')
    mylogger.error(request.event["message"])
    mylogger.error(request.event["args"])
    mylogger.error(e)
