import requests
import pprint
from uuid import uuid4
from logging import basicConfig, getLogger, DEBUG, INFO

from ..config import flask_app
from .user import User
from .active_plugin import ActivePlugin
from .plugin import Plugin
from ..plugin_compiler import compiler

basicConfig()
mylogger = getLogger(__name__)
if flask_app.config['ENV'] == 'dev':
    mylogger.setLevel(DEBUG)
elif flask_app.config['ENV'] == 'prd':
    mylogger.setLevel(INFO)
else:
    raise EnvironmentError("flask_app.config['ENV'] is invalid.")


class Room:
    url = 'http://' + flask_app.config['DC_URL'] + ':' + flask_app.config['DC_PORT'] + '/api/v1/rooms'

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
    def make_json_elem(cls, room_id, members=None, active_plugins=None):
        """
        Parameters
        ----------
        room_id: str
        members: list[Any]
        active_plugins: list[str]

        Returns
        -------
        tuple
        """

        if members is None:
            members = User.get(user_id=None, room_id=room_id)

        if active_plugins is None:
            active_plugins = ActivePlugin.get(active_plugin_id=None,
                                              room_id=room_id)

        plugins = []
        for ap in active_plugins:
            plugin_meta = Plugin.get(ap['pluginId'])
            # TODO: plugin_metaにthumbnailUrlsとtags(list)を追加する必要がある
            # TODO: tagsはstringで帰ってきているので一時的に空配列にする
            plugin_meta['thumbnailUrls'] = []
            plugin_meta['tags'] = []

            res = requests.post(
                f'http://{flask_app.config["BACKEND_URL"]}:{flask_app.config["BACKEND_PORT"]}/api/v1/plugin/compile',
                json=plugin_meta
            )
            res.close()
            mylogger.debug(f'{pprint.pformat(res.json())}')
            cp = res.json()
            plugins.append(cp)

        return members, plugins
