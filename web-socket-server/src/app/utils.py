import json
from functools import wraps
from types import FunctionType
from logging import basicConfig, getLogger, DEBUG

from flask import request

from .model import User

basicConfig()
mylogger = getLogger(__name__)
mylogger.setLevel(DEBUG)


def function_info_wrapper(handler: FunctionType):
    @wraps(handler)
    def wrapped(*args, **kwargs):
        mylogger.info('{}'.format(handler.__name__))

        mylogger.info('args: {}'.format(args))
        mylogger.info('kwargs: {}'.format(kwargs))

        ret = handler(*args, **kwargs)

        mylogger.info('end {}'.format(handler.__name__))

        return ret

    return wrapped


def check_user(handler: FunctionType):
    @wraps(handler)
    def already_registered(*args, **kwargs):
        mylogger.info('check user')
        user = User.get(request.sid, None)

        if user is None:
            raise RuntimeError("user.id: {} is not defined.".format(request.sid))
        else:
            mylogger.info('user: {}'.format(request.sid))
        return handler(*args, **kwargs)

    return already_registered


def byte_data_to_dict(handler: FunctionType):
    @wraps(handler)
    def data_is_dict(*args, **kwargs):
        mylogger.info('byte data to dict')
        if len(args) == 0:
            args = (None,)

        data = args[0]

        mylogger.debug('data type is {}'.format(type(data)))
        if (type(data) is not dict) and (data is not None):
            mylogger.debug('therefor change to dict')
            data = json.loads(data)
        mylogger.debug('data: {}'.format(data))

        return handler(data, *args[1:], **kwargs)

    return data_is_dict
