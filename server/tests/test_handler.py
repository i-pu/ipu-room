import unittest

import requests

from config import url


class TestHandler(unittest.TestCase):

    def test_room(self):
        res = requests.get(url + '/room')
        self.assertEqual(200, res.status_code)
        self.assertEqual(type(res.json()['rooms']), list)

    def test_plugin(self):
        res = requests.get(url + '/plugin')
        self.assertEqual(200, res.status_code)
        self.assertEqual(type(res.json()['plugins']), list)
