import importlib
import pprint
import json
from functools import wraps
from types import FunctionType

from flask_socketio import SocketIO
from flask import request

from .models import User


def debug_wrapper(handler: FunctionType):
    @wraps(handler)
    def debug_wrapped(*args, **kwargs):
        print('------- debug --------')

        print(handler.__name__, flush=True)
        print('args', end='', flush=True)
        pprint.pprint(args)
        print('kwargs', end='', flush=True)
        pprint.pprint(kwargs)

        ret = handler(*args, **kwargs)

        print('------- debug end --------')
        return ret

    return debug_wrapped


def check_user(handler: FunctionType):
    @wraps(handler)
    def already_registered(*args, **kwargs):
        print('check_user', flush=True)

        user = User.query.filter_by(id=request.sid).one_or_none()
        if user is None:
            raise RuntimeError("user is not defined.")

        print('user is', user, flush=True)
        return handler(*args, **kwargs)

    return already_registered


def byte_data_to_dict(handler: FunctionType):
    @wraps(handler)
    def data_is_dict(*args, **kwargs):
        print('byte data to dict', flush=True)

        data = args[0]
        print('data type is {}'.format(type(data)), flush=True)
        if (type(data) is not dict) and (data is not None):
            print('therefor change to dict', flush=True)
            data = json.loads(data)
        print('data:', data, flush=True)
        return handler(data, *args[1:], **kwargs)

    return data_is_dict


def wrapping_emit(handler: FunctionType, plugin, socketio: SocketIO, plugin_name: str, room_id: str, event: str):
    @wraps(handler)
    def wrapped_event(*args, **kwargs):
        print('wrapped event', flush=True)

        handle_return = handler(plugin, *args[1:], **kwargs)
        if (handle_return is not None) and (type(handle_return) is not dict):
            print('error:', 'type of return:', type(handle_return), flush=True)
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


class PluginWrapper(object):
    plugin = None


# def activate_plugin(plugin_name: str, room_id: str):
#     plugin = importlib.import_module(plugin_name).Plugin
    
