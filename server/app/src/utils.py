import importlib
import pprint
import json
from functools import wraps
from types import FunctionType
from logging import basicConfig, getLogger, DEBUG

from flask_socketio import SocketIO
from flask import request

from .models import User

basicConfig()
mylogger = getLogger(__name__)
mylogger.setLevel(DEBUG)


def function_info_wrapper(handler: FunctionType):
    @wraps(handler)
    def wrapped(*args, **kwargs):
        mylogger.info('------- {} --------'.format(handler.__name__))

        mylogger.info('- - args: {}'.format(args))
        mylogger.info('- - kwargs: {}'.format(kwargs))

        ret = handler(*args, **kwargs)

        mylogger.info('------- {} end --------'.format(handler.__name__))

        return ret

    return wrapped


def check_user(handler: FunctionType):
    @wraps(handler)
    def already_registered(*args, **kwargs):
        mylogger.info('-------- check user -----------')

        user = User.query.filter_by(id=request.sid).one_or_none()
        if user is None:
            raise RuntimeError("user is not defined.")

        mylogger.debug('- - user is {}'.format(user))
        return handler(*args, **kwargs)

    return already_registered


def byte_data_to_dict(handler: FunctionType):
    @wraps(handler)
    def data_is_dict(*args, **kwargs):
        mylogger.info('------ byte data to dict ------')
        if len(args) == 0:
            args = (None,)

        data = args[0]

        mylogger.debug('- - data type is {}'.format(type(data)))
        if (type(data) is not dict) and (data is not None):
            mylogger.debug('- - therefor change to dict')
            data = json.loads(data)
        mylogger.debug('- - data: {}'.format(data))

        return handler(data, *args[1:], **kwargs)

    return data_is_dict


# todo: will be deprecated
def wrapping_emit(handler: FunctionType, plugin, socketio: SocketIO, plugin_name: str, room_id: str, event: str):
    @wraps(handler)
    def wrapped_event(*args, **kwargs):
        mylogger.info('wrapped event')

        handle_return = handler(plugin, *args[1:], **kwargs)
        if (handle_return is not None) and (type(handle_return) is not dict):
            mylogger.error('error:', 'type of return:', type(handle_return), flush=True)
            raise RuntimeError()

        socketio.emit(plugin_name + room_id + event, handle_return, room=room_id)

    return wrapped_event


def activate_plugin(plugin_name: str, socketio: SocketIO, room_id: str):
    # todo: Plugin オブジェクトをグローバルに保存し消せるようにしたい
    plugin = importlib.import_module(plugin_name).Plugin

    print('plugin', type(plugin()))

    for event_name, func in plugin.all().items():
        socketio.on(room_id + plugin_name + event_name) \
            (wrapping_emit(func, plugin, socketio, room_id, plugin_name, event_name))
