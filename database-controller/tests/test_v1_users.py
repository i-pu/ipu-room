import sys
import unittest
import requests

import config


class TestSocketIOHandler(unittest.TestCase):

    def test_get_all_users(self):
        print('\n', sys._getframe().f_code.co_name, flush=True)

        res = requests.get(config.url + '/api/v1/users')
        res.close()
        self.assertTrue(res.status_code < 400)
        data = res.json()
        self.assertTrue(isinstance(data, list))
        if len(data) > 0:
            for d in data:
                self.assertTrue('id' in d)
                self.assertTrue('name' in d)
                self.assertTrue('roomId' in d)

    def test_get_user(self):
        print('\n', sys._getframe().f_code.co_name, flush=True)

        json = {'id': 'some-websocketid',
                'name': 'getuser',
                'roomId': None}
        res = requests.post(config.url + '/api/v1/users', json=json)
        res.close()
        self.assertTrue(res.status_code < 400)
        pre_data = res.json()
        res = requests.get(config.url + '/api/v1/users/' + pre_data['id'])
        res.close()
        data = res.json()
        self.assertTrue('id' in data)
        self.assertTrue('name' in data)
        self.assertTrue('roomId' in data)
        self.assertEqual(data['id'], pre_data['id'])

    def test_post_user(self):
        print('\n', sys._getframe().f_code.co_name, flush=True)

        json = {'id': 'some-websocketid-post',
                'name': 'postuser',
                'roomId': None}
        res = requests.post(config.url + '/api/v1/users', json=json)
        res.close()
        self.assertTrue(res.status_code < 400)
        data = res.json()
        self.assertTrue(isinstance(data, dict))
        self.assertTrue('id' in data)
        self.assertTrue('name' in data)
        self.assertTrue('roomId' in data)

    def test_put_user(self):
        print('\n', sys._getframe().f_code.co_name, flush=True)

        user = {'id': 'some-websocketid-put',
                'name': 'putuser',
                'roomId': None}
        res = requests.post(config.url + '/api/v1/users', json=user)
        res.close()
        self.assertTrue(res.status_code < 400)
        pre_data = res.json()
        pre_data['name'] = 'ppppppppppp'
        res = requests.put(config.url + '/api/v1/users', json=pre_data)
        res.close()
        self.assertTrue(res.status_code < 400)
        data = res.json()
        self.assertTrue(isinstance(data, dict))
        self.assertTrue('id' in data)
        self.assertTrue('name' in data)
        self.assertTrue('roomId' in data)
