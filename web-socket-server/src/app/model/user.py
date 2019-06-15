import requests
from uuid import uuid4

from ..config import app


class User:
    url = 'http://' + app.config['DC_URL'] + ':' + app.config['DC_PORT'] + '/api/v1/users'

    @classmethod
    def get(cls, user_id=None, **kwargs):
        res = None
        if user_id is None:
            res = requests.get(cls.url)
        else:
            res = requests.get(cls.url + '/' + user_id)
        res.close()

        if res.status_code >= 400:
            raise Exception("status code is {}".format(res.status_code))

        return res.json()

    @classmethod
    def create(cls, user_id, name):
        res = requests.post(cls.url, json={'id': user_id, 'name': name})
        res.close()

        if res.status_code >= 400:
            raise Exception("status code is {}".format(res.status_code))

        return res.json()

    @classmethod
    def update(cls, user_id, name, room_id=None):
        json = {'id': user_id, 'name': name, 'roomId': room_id}
        res = requests.put(cls.url, json=json)
        res.close()
        if res.status_code >= 400:
            raise Exception("{0}{1}".format('status code is {}. '.format(res.status_code),
                                            'json={}'.format(json)))

        return res.json()

    @classmethod
    def enter(cls, room_id, user_id):
        import sys
        print(room_id, user_id, file=sys.stderr, flush=True)
        json = cls.get(user_id)
        print(json, file=sys.stderr, flush=True)
        json['roomId'] = room_id
        json = cls.update(json['id'], json['name'], json['roomId'])
        return json
