import sys

import unittest
import socketio

from config import url


class TestSocketIOHandler(unittest.TestCase):

    def setUp(self):
        self.sio = socketio.Client()
        self.sio.connect(url)

        self.data = None
        self.expected = None
        self.actual = None

    def tearDown(self):
        self.sio.disconnect()

    def test_plugin_register(self):
        print('\n', sys._getframe().f_code.co_name)
        @self.sio.on('plugin/register')
        def plugin_register(data):
            self.data = data

        self.sio.emit('visit', {'userName': 'plugin register'})
        self.sio.emit('plugin/register',
                      {'name': 'plugin name',
                       'description': 'plugin description',
                       'author': 'plugin author',
                       'tags': 'plugin tags',
                       'content': 'plugin content'})
        self.sio.sleep(2)

        self.assertTrue(self.data['state'])
