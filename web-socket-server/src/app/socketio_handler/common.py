from logging import basicConfig, DEBUG, getLogger
from uuid import uuid4
from flask import request
from flask_socketio import join_room, leave_room

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
    join_room('user' + request.sid)
    socketio.emit('visit', data={'user': json}, room='user' + request.sid)


@socketio.on('lobby')
@utils.byte_data_to_dict
@utils.check_user
@utils.function_info_wrapper
def lobby(data):
    json = model.Room.get()
    mylogger.info(json)
    socketio.emit('lobby', data={'rooms': json}, room='user' + request.sid)


@socketio.on('disconnect')
@utils.byte_data_to_dict
@utils.check_user
@utils.function_info_wrapper
def disconnect(data):
    mylogger.debug('- - socket id: {}'.format(request.sid))
    leave_room('user' + request.sid)
    # todo: delete from database
    # mylogger.debug('- - data: {}'.format(data))

    # user = User.query.filter_by(id=request.sid).one()
    # db.session.delete(user)
    # db.session.commit()


@socketio.on_error()
def on_error(e):
    mylogger.error('---------- error happen!!! --------- ')
    mylogger.error(e)
