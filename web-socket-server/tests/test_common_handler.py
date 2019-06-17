import sys

import unittest
import socketio

from config import url


class TestSocketIOHandler(unittest.TestCase):

    def setUp(self):
        self.client = socketio.Client()
        self.client.connect(url)

        self.data = None
        self.expected = None
        self.actual = None

    def tearDown(self):
        self.client.disconnect()

    def test_visit(self):
        print('\n', sys._getframe().f_code.co_name, flush=True)
        @self.client.on('visit')
        def visit(data):
            self.data = data

        self.client.emit('visit', {'userName': 'alis'})
        self.client.sleep(1)

        self.assertTrue('user' in self.data)
        self.assertTrue('id' in self.data['user'])
        self.assertTrue('name' in self.data['user'])
        self.assertTrue('roomId' in self.data['user'])

    def test_lobby(self):
        print('\n', sys._getframe().f_code.co_name, flush=True)
        @self.client.on('lobby')
        def lobby(data):
            self.data = data
            print(self.data, file=sys.stderr, flush=True)

        self.client.emit('visit', {'userName': 'lobby user'})
        self.client.emit('lobby')
        self.client.sleep(1)

        self.assertTrue('rooms' in self.data)
