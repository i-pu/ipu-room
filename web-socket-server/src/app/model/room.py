import requests
from uuid import uuid4

from ..config import app
from .user import User
from .active_plugin import ActivePlugin
from .plugin import Plugin
from ..plugin_compiler import compiler


class Room:
    url = 'http://' + app.config['DC_URL'] + ':' + app.config['DC_PORT'] + '/api/v1/rooms'

    @classmethod
    def get(cls, room_id=None, **kwargs):
        res = None
        if room_id is None:
            res = requests.get(cls.url)
        else:
            res = requests.get(cls.url + '/' + room_id)
        res.close()

        if res.status_code >= 400:
            raise Exception("status code is {}".format(res.status_code))

        return res.json()

    @classmethod
    def create(cls, room_id, name):
        room_res = requests.post(cls.url, json={'id': room_id, 'name': name})
        room_res.close()
        if room_res.status_code >= 400:
            raise Exception("{0}{1}" \
                            .format("status code is {}. ".format(room_res.status_code),
                                    'request: {}.'.format({'name': name})))

        return room_res.json()

    @classmethod
    def enter(cls, room_id, sid):
        User.enter(room_id, sid)

    @classmethod
    def make_json_elem(cls, room_id, members, active_plugins):
        if members is None:
            members = User.get(user_id=None, room_id=room_id)

        if active_plugins is None:
            active_plugins = []

        plugins = []
        for ap in active_plugins:
            plugin_meta = Plugin.get(ap['pluginId'])
            template, functions = compiler(plugin_meta['content'])
            plugins.append({'plugin': {'template': template,
                                       'functions': functions,
                                       'instanceId': ap['id'],
                                       'config': {'enabled': ap['enabled']}
                                       },
                            'meta': {**plugin_meta}})

        return members, plugins
