import requests

from ..config import flask_app


class Plugin:
    url = 'http://' + flask_app.config['DC_URL'] + ':' + flask_app.config['DC_PORT'] + '/api/v1/plugins'

    @classmethod
    def get(cls, plugin_id=None):
        if plugin_id is None:
            res = requests.get(cls.url)
        else:
            res = requests.get(cls.url + '/' + plugin_id)
        res.close()
        if res.status_code >= 400:
            raise Exception("status code is {}".format(res.status_code))

        return res.json()

    @classmethod
    def create(cls, name, description, author, tags, content):
        res = requests.post(cls.url, json={'name': name,
                                           'description': description,
                                           'author': author,
                                           'tags': tags,
                                           'content': content})
        res.close()
        if res.status_code >= 400:
            raise Exception("status code is {}".format(res.status_code))

        return res.json()
