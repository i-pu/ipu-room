import requests

from ..config import flask_app


class User:
    url = 'http://' + flask_app.config['DC_URL'] + ':' + flask_app.config['DC_PORT'] + '/api/v1/users'

    @classmethod
    def get(cls, user_id=None, room_id=None, **kwargs):
        res = None
        if user_id is not None and room_id is not None:
            raise Exception('user_id and room_id cant be set at once'
                            'user_id: {}, room_id: {}'.format(user_id, room_id))

        if user_id is not None:
            res = requests.get(cls.url + '/' + user_id)
        elif room_id is not None:
            res = requests.get(cls.url + '?roomId={}'.format(room_id))
        else:
            res = requests.get(cls.url)
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
        json = cls.get(user_id)
        json['roomId'] = room_id
        json = cls.update(json['id'], json['name'], json['roomId'])
        return json

    @classmethod
    def delete(cls, user_id):
        res = requests.delete(cls.url + '/' + user_id)
        res.close()
        if not res.json()['state']:
            raise Exception('delete user: {} is not success'.format(user_id))
