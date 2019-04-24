import importlib
import json
from functools import wraps

from flask_socketio import SocketIO

from .models import User


def check_user(handler):
    @wraps(handler)
    def already_registered(*args, **kwargs):
        print('check_user', flush=True)
        data = args[0]
        user_id = data['user_id']
        user = User.query.filter_by(id=user_id).one()
        if user is None:
            raise RuntimeError
        else:
            print('user:', user, flush=True)
        return handler(*args, **kwargs)

    return already_registered


def byte_data_to_dict(handler):
    @wraps(handler)
    def data_is_dict(*args, **kwargs):
        print('byte data to dict', flush=True)
        data = args[0]
        print('datatype', type(data), flush=True)
        if type(data) is not dict:
            data = json.load(data)
        print('data:', data, flush=True)
        return handler(data, *args[1:], **kwargs)

    return data_is_dict


def wrapping_emit(handler, plugin, socketio: SocketIO, plugin_name: str, room_id: str, event: str):
    @wraps(handler)
    def wrapped_event(*args, **kwargs):
        print('---------', flush=True)
        print(*args, flush=True)
        print(**kwargs, flush=True)
        print('---------', flush=True)
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
