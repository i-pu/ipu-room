from logging import basicConfig, DEBUG, getLogger
from flask import request, g

from ..config import socketio, app
from .. import utils
from .. import model

basicConfig()
mylogger = getLogger(__name__)
mylogger.setLevel(DEBUG)


# todo: 特定の人に送る

@socketio.on('sample')
@utils.byte_data_to_dict
@utils.function_info_wrapper
def sample(data):
    mylogger.debug('- - socket id: {}'.format(request.sid))


@socketio.on('visit')
@utils.byte_data_to_dict
@utils.function_info_wrapper
def visit(data):
    json = {'user': model.User.post({'name': data['userName']})}
    mylogger.info(json)

    socketio.emit('visit', data=json)


@socketio.on('lobby')
@utils.byte_data_to_dict
@utils.check_user
@utils.function_info_wrapper
def lobby(data):
    json = model.Room.get()
    mylogger.info(json)
    socketio.emit('lobby', data=json)


@socketio.on('disconnect')
@utils.byte_data_to_dict
@utils.check_user
@utils.function_info_wrapper
def disconnect(data):
    mylogger.debug('- - socket id: {}'.format(request.sid))
    # mylogger.debug('- - data: {}'.format(data))

    # user = User.query.filter_by(id=request.sid).one()
    # db.session.delete(user)
    # db.session.commit()


@socketio.on_error()
def on_error(e):
    mylogger.error('---------- error happen!!! --------- ')
    mylogger.error(e)
