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
    """
    テスト用に残しておく
    Parameters
    ----------
    data

    Returns
    -------

    """
    json = model.Plugin.create(data['name'],
                               data['description'],
                               data['author'],
                               '',
                               # todo: tagsはリストで受け取っているがから文字列に一時的に変更する
                               # data['tags'],
                               data['content'])
    mylogger.debug(json)

    if 'id' in json:
        res_data = {'state': True, **json}
    else:
        res_data = {'state': False},

    socketio.emit('plugin/register',
                  data=res_data,
                  room=request.sid)


@socketio.on('plugin/trigger')
@utils.byte_data_to_dict
@utils.check_user
@utils.function_info_wrapper
def plugin_trigger(data):
    room_id = data['roomId']
    instance_id = data['instanceId']
    data = data['data']

    socketio.emit('plugin/trigger',
                  data={'data': data, 'instanceId': instance_id},
                  room=room_id)


@socketio.on('plugin/clone')
@utils.byte_data_to_dict
@utils.check_user
@utils.function_info_wrapper
def plugin_clone(data):
    room_id = data['roomId']
    instance_id = data['instanceId']
    record = data['record']
    sync_id = data['from']
    socketio.emit('plugin/sync',
                  data={'record': record},
                  room=sync_id)


@socketio.on('plugin/sync')
@utils.byte_data_to_dict
@utils.check_user
@utils.function_info_wrapper
def plugin_sync(data):
    room_id = data['roomId']
    instance_id = data['instanceId']
    clone_id = model.User.get(None, room_id)[0]['id']

    socketio.emit('plugin/clone',
                  data={'roomId': room_id,
                        'instanceId': instance_id,
                        'from': request.sid},
                  room=clone_id)
