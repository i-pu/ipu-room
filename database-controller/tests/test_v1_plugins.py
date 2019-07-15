import sys
import unittest
import requests

import config


class TestSocketIOHandler(unittest.TestCase):

    def test_get_all_plugins(self):
        print('\n', sys._getframe().f_code.co_name, flush=True)

        res = requests.get(config.url + '/api/v1/plugins')
        self.assertTrue(res.status_code < 400)
        data = res.json()
        self.assertTrue(isinstance(data, list))
        if len(data) > 0:
            for d in data:
                self.assertTrue('id' in d)
                self.assertTrue('name' in d)
                self.assertTrue('description' in d)
                self.assertTrue('author' in d)
                self.assertTrue('tags' in d)
                self.assertTrue('content' in d)
        res.close()

    def test_get_plugin(self):
        print('\n', sys._getframe().f_code.co_name, flush=True)

        data = {'id': 'some-uuid',  # it is ignored
                'name': 'counter',
                'description': 'counter plugin',
                'author': 'python test',
                'tags': 'apple,windows',
                'content': 'long long source code'}
        res = requests.post(config.url + '/api/v1/plugins', json=data)
        self.assertTrue(res.status_code < 400)
        pre_data = res.json()
        res = requests.get(config.url + '/api/v1/plugins/' + pre_data['id'])
        data = res.json()
        self.assertTrue('id' in data)
        self.assertTrue('name' in data)
        self.assertTrue('description' in data)
        self.assertTrue('author' in data)
        self.assertTrue('tags' in data)
        self.assertTrue('content' in data)
        self.assertEqual(data['id'], pre_data['id'])
        res.close()

    def test_post_plugin(self):
        print('\n', sys._getframe().f_code.co_name, flush=True)

        data = {'id': 'some-uuid',  # it is ignored
                'name': 'counter',
                'description': 'counter plugin',
                'author': 'python test',
                'tags': 'apple,windows',
                'content': 'long long source code'}
        res = requests.post(config.url + '/api/v1/plugins', json=data)
        self.assertTrue(res.status_code < 400)
        data = res.json()
        self.assertTrue(isinstance(data, dict))
        self.assertTrue('id' in data)
        self.assertNotEqual(data['id'], 'some-uuid')
        self.assertTrue('name' in data)
        self.assertTrue('description' in data)
        self.assertTrue('author' in data)
        self.assertTrue('tags' in data)
        self.assertTrue('content' in data)
        res.close()

    def test_put_plugin(self):
        print('\n', sys._getframe().f_code.co_name, flush=True)

        data = {'id': 'some-uuid',  # it is ignored
                'name': 'counter',
                'description': 'counter plugin',
                'author': 'python test',
                'tags': 'apple,windows',
                'content': 'long long source code'}
        res = requests.post(config.url + '/api/v1/plugins', json=data)
        self.assertTrue(res.status_code < 400)
        pre_data = res.json()
        pre_data['name'] = 'counter changed'
        res = requests.put(config.url + '/api/v1/plugins/' + pre_data['id'], json=pre_data)
        self.assertTrue(res.status_code < 400)
        data = res.json()
        self.assertTrue(isinstance(data, dict))
        self.assertTrue('id' in data)
        self.assertTrue('name' in data)
        self.assertTrue('description' in data)
        self.assertTrue('author' in data)
        self.assertTrue('tags' in data)
        self.assertTrue('content' in data)
        self.assertEqual(pre_data['name'], data['name'])
        res.close()
