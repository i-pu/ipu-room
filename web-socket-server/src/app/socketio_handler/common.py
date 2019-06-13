from logging import basicConfig, DEBUG, getLogger
from flask import request, g
import requests

from ..config import socketio, app
from .. import utils

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

    mylogger.debug('- - socket id: {}'.format(request.sid))
    res = requests.post(
        'http://'
        + app.config['DC_URL'] + ':' + app.config['DC_PORT']
        + '/api/v1/users',
        json={'name': data['user_name']})
    res.close()

    if res.status_code >= 400:
        raise Exception("status code is {}".format(res.status_code))

    mylogger.info(res.json())
    socketio.emit('visit', data=res.json())


@socketio.on('lobby')
@utils.byte_data_to_dict
@utils.check_user
@utils.function_info_wrapper
def lobby(data):

    mylogger.debug('- - socket id: {}'.format(request.sid))
    # all_room = Room.query.all()

    # ret = {'rooms': list(map(Room.__to_dict__, all_room))}
    # mylogger.info('- - return')
    # mylogger.info('{}'.format(ret))
    # socketio.emit('lobby', data=ret)


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
