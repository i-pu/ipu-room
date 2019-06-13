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

    def test_visit(self):
        @self.sio.on('visit')
        def visit(data):
            self.data = data

        self.sio.emit('visit', {'userName': 'alis'})
        self.sio.sleep(2)
        self.assertTrue('user' in self.data)
        self.assertTrue('id' in self.data['user'])
        self.assertTrue('name' in self.data['user'])
        self.assertTrue('roomId' in self.data['user'])

    def test_lobby(self):
        @self.sio.on('lobby')
        def lobby(data):
            self.data = data

        self.sio.emit('visit', {'userName': 'lobby user'})
        self.sio.emit('lobby')
        self.sio.sleep(2)
        self.assertFalse('rooms' in self.data)
