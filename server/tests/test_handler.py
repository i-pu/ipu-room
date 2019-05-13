import unittest

import requests


class TestHandler(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # cls.url = 'http://localhost'
        cls.url = 'http://35.187.206.173'
        cls.port = ':31420'

    def test_room(self):
        res = requests.get(self.url + self.port + '/room')
        self.assertEqual(200, res.status_code)
        self.assertEqual(type(res.json()['rooms']), list)

    def test_plugin(self):
        res = requests.get(self.url + self.port + '/plugin')
        self.assertEqual(200, res.status_code)
        self.assertEqual(type(res.json()['plugins']), list)