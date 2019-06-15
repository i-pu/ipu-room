import sys

import unittest
import socketio

from config import url


class TestSocketIOHandler(unittest.TestCase):

    def setUp(self):
        self.client = socketio.Client()
        self.client2 = socketio.Client()
        self.client.connect(url)

        self.data = None
        self.expected = None
        self.actual = None

    def tearDown(self):
        self.client.disconnect()

    def test_plugin_register(self):
        print('\n', sys._getframe().f_code.co_name)
        @self.client.on('plugin/register')
        def plugin_register(data):
            self.data = data

        self.client.emit('visit', {'userName': 'plugin register'})
        self.client.emit('plugin/register',
                      {'name': 'plugin name',
                       'description': 'plugin description',
                       'author': 'plugin author',
                       'tags': 'plugin tags',
                       'content': 'plugin content'})
        self.client.sleep(2)

        self.assertTrue(self.data['state'])
