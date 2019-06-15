from logging import basicConfig, DEBUG, getLogger
from uuid import uuid4

from flask import request

from ..config import socketio
from .. import utils
from .. import model

basicConfig()
mylogger = getLogger(__name__)
mylogger.setLevel(DEBUG)


@socketio.on('plugin/register')
@utils.byte_data_to_dict
@utils.check_user
@utils.function_info_wrapper
def plugin_register(data):
    json = model.Plugin.create(str(uuid4()),
                               data['name'],
                               data['description'],
                               data['author'],
                               data['tags'],
                               data['content'])
    print(json, flush=True)
    if 'id' in json:
        socketio.emit('plugin/register',
                      data={'state': True, **json},
                      room='user' + request.sid)
    else:
        socketio.emit('plugin/register',
                      data={'state': False},
                      room='user' + request.sid)


@socketio.on('plugin/trigger')
@utils.byte_data_to_dict
@utils.check_user
@utils.function_info_wrapper
def plugin_trigger(data):
    basicConfig()
    # room_id = data['room_id']
    # instance_id = data['instance_id']
    # event_name = data['event_name']
    # event_args: List[Any] = data['args']

    # mylogger.info('- - return')
    # socketio.emit('plugin/trigger', data=result, room=room_id)


@socketio.on('plugin/sync')
@utils.byte_data_to_dict
@utils.check_user
@utils.function_info_wrapper
def plugin_clone(data):
    # todo: 今いる部屋にいるユーザをランダムに一人選びクローンする
    # todo: tokenを利用して，有効な相手からクローンが来たかドウかを確認するのもいいかも
    # todo: clone がsyncのとき以外からアクセスできるようになってしまっているのか
    socketio.emit('plugin/sync')


@socketio.on('plugin/sync')
@utils.byte_data_to_dict
@utils.check_user
@utils.function_info_wrapper
def plugin_sync(data):
    basicConfig()
    # sync要求が
    # @socketio.on('plugin/clone')
    # @utils.byte_data_to_dict
    # @utils.check_user
    # @utils.function_info_wrapper
    # def plugin_clone(data):

    # socketio.emit('plugin/clone')
