from .config import app
import requests


class User:
    url = 'http://' + app.config['DC_URL'] + ':' + app.config['DC_PORT'] + '/api/v1/users'

    @classmethod
    def get(cls, **kwargs):
        res = requests.get(cls.url)
        res.close()

        if res.status_code >= 400:
            raise Exception("status code is {}".format(res.status_code))

        return res.json()

    @classmethod
    def post(cls, json):
        res = requests.post(cls.url, json=json)
        res.close()

        if res.status_code >= 400:
            raise Exception("status code is {}".format(res.status_code))

        return res.json()


class Room:
    url = 'http://' + app.config['DC_URL'] + ':' + app.config['DC_PORT'] + '/api/v1/rooms'

    @classmethod
    def get(cls, **kwargs):
        res = requests.get(cls.url)
        res.close()

        if res.status_code >= 400:
            raise Exception("status code is {}".format(res.status_code))

        return res.json()

    @classmethod
    def post(cls, json):
        res = requests.get(cls.url, json=json)
        res.close()

        if res.status_code >= 400:
            raise Exception("status code is {}".format(res.status_code))

        return res.json()
