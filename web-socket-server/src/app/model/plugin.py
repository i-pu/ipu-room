import requests

from ..config import app


class Plugin:
    url = 'http://' + app.config['DC_URL'] + ':' + app.config['DC_PORT'] + '/api/v1/plugins'

    @classmethod
    def get(cls, plugin_id=None):
        res = None
        if plugin_id is None:
            res = requests.get(cls.url)
        else:
            res = requests.get(cls.url + '/' + plugin_id)
        res.close()
        if res.status_code >= 400:
            raise Exception("status code is {}".format(res.status_code))

        return res.json()

    @classmethod
    def create(cls, plugin_id, name, description, author, tags, content):
        res = requests.post(cls.url, json={'id': plugin_id,
                                           'name': name,
                                           'description': description,
                                           'author': author,
                                           'tags': tags,
                                           'content': content})
        res.close()
        if res.status_code >= 400:
            raise Exception("status code is {}".format(res.status_code))

        return res.json()
