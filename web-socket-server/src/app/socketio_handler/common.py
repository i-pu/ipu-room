from logging import basicConfig, DEBUG, getLogger

from flask import request, g

from ..config import socketio
from ..models import db, User, Room
from .. import utils

basicConfig()
mylogger = getLogger(__name__)
mylogger.setLevel(DEBUG)


@socketio.on('sample')
@utils.byte_data_to_dict
@utils.function_info_wrapper
def sample(data):

    mylogger.debug('- - socket id: {}'.format(request.sid))
    mylogger.debug('- - global plugins: {}'.format(config.global_plugins))


@socketio.on('visit')
@utils.byte_data_to_dict
@utils.function_info_wrapper
def visit(data):

    user = User(name=data['user_name'], id=request.sid)
    db.session.add(user)
    db.session.commit()

    mylogger.debug('- - user: {}'.format(user))

    ret = {'user': user.__to_dict__()}
    mylogger.info('- - return')
    mylogger.info('{}'.format(ret))
    socketio.emit('visit', data=ret)


@socketio.on('lobby')
@utils.byte_data_to_dict
@utils.check_user
@utils.function_info_wrapper
def lobby(data):

    all_room = Room.query.all()

    ret = {'rooms': list(map(Room.__to_dict__, all_room))}
    mylogger.info('- - return')
    mylogger.info('{}'.format(ret))
    socketio.emit('lobby', data=ret)


@socketio.on('disconnect')
@utils.byte_data_to_dict
@utils.check_user
@utils.function_info_wrapper
def disconnect(data):
    mylogger.debug('- - data: {}'.format(data))

    user = User.query.filter_by(id=request.sid).one()
    db.session.delete(user)
    db.session.commit()


@socketio.on_error()
def on_error(e):
    mylogger.error('---------- error happen!!! --------- ')
    mylogger.error(e)
