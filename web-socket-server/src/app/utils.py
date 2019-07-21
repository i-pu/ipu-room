import json
from functools import wraps
from logging import basicConfig, getLogger, DEBUG, INFO

from flask import request

from .model import User
from .config import flask_app

basicConfig()
mylogger = getLogger(__name__)
if flask_app.config['ENV'] == 'dev':
    mylogger.setLevel(DEBUG)
elif flask_app.config['ENV'] == 'prd':
    mylogger.setLevel(INFO)
else:
    raise EnvironmentError("flask_app.config['ENV'] is invalid.")


def function_info_wrapper(handler):
    @wraps(handler)
    def wrapped(*args, **kwargs):
        mylogger.debug('{}'.format(handler.__name__))
        mylogger.debug('args: {}'.format(args))
        mylogger.debug('kwargs: {}'.format(kwargs))
        ret = handler(*args, **kwargs)
        mylogger.debug('end {}'.format(handler.__name__))
        return ret

    return wrapped


def check_user(handler):
    @wraps(handler)
    def wrapped(*args, **kwargs):
        mylogger.debug('check user')
        mylogger.debug(f'{request.sid}')
        mylogger.debug(request.sid)
        user = User.get(request.sid, None)
        if user is None:
            raise RuntimeError("user.id: {} is not defined.".format(request.sid))
        else:
            mylogger.info('user: {}'.format(request.sid))

        return handler(*args, **kwargs)

    return wrapped


def byte_data_to_dict(handler):
    @wraps(handler)
    def wrapped(*args, **kwargs):
        mylogger.debug('byte data to dict')
        if len(args) == 0:
            args = (None,)

        data = args[0]

        mylogger.debug('data type is {}'.format(type(data)))
        if (type(data) is not dict) and (data is not None):
            mylogger.error('why ? therefor change to dict')
            data = json.loads(data)

        mylogger.debug('data: {}'.format(data))
        return handler(data, *args[1:], **kwargs)

    return wrapped
