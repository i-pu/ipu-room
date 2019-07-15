import requests

from ..config import flask_app


class ActivePlugin:
    url = 'http://' + flask_app.config['DC_URL'] + ':' + flask_app.config['DC_PORT'] + '/api/v1/active_plugins'

    @classmethod
    def get(cls, active_plugin_id=None, room_id=None, **kwargs):
        if active_plugin_id is not None and room_id is not None:
            raise Exception('active_plugin_id and room_id cant be set at once'
                            'active_plugin_id: {}, room_id: {}'.format(active_plugin_id, room_id))

        if active_plugin_id is not None:
            res = requests.get(cls.url + '/' + active_plugin_id)
        elif room_id is not None:
            res = requests.get(cls.url + '?roomId={}'.format(room_id))
        else:
            res = requests.get(cls.url)
        res.close()

        if res.status_code >= 400:
            raise Exception("status code is {}".format(res.status_code))

        return res.json()

    @classmethod
    def create(cls, active_plugin_id, plugin_id, room_id):
        res = requests.post(cls.url, json={'id': active_plugin_id,
                                           'roomId': room_id,
                                           'pluginId': plugin_id,
                                           'enabled': True})
        res.close()

        if res.status_code >= 400:
            raise Exception("status code is {}".format(res.status_code))

        return res.json()

    @classmethod
    def update(cls, active_plugin_id, name, room_id=None):
        json = {'id': active_plugin_id, 'name': name, 'roomId': room_id}
        res = requests.put(cls.url, json=json)
        res.close()
        if res.status_code >= 400:
            raise Exception("{0}{1}".format('status code is {}. '.format(res.status_code),
                                            'json={}'.format(json)))

        return res.json()
