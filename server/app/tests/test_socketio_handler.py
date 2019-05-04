import os
import unittest

import socketio


class TestSocketIOHandlers(unittest.TestCase):
    sio = None
    expected = None
    actual = None

    def setUp(self):
        self.sio = socketio.Client()
        self.sio.connect('http://localhost:8000')
        self.expected = None
        self.actual = None

    def tearDown(self):
        self.sio.disconnect()

    def test_visit(self):
        @self.sio.on('visit')
        def visit(data):
            self.expected = 'alis'
            self.actual = data['user']['name']

        self.sio.emit('visit', {'user_name': 'alis'})
        self.sio.sleep(1)
        self.assertIsNotNone(self.expected)
        self.assertIsNotNone(self.actual)
        self.assertEqual(self.expected, self.actual, 'expect alis')

    def test_lobby(self):
        @self.sio.on('lobby')
        def lobby(data):
            self.expected = 0
            self.actual = data['rooms']

        self.sio.emit('visit', {'user_name': 'lobby user'})
        self.sio.emit('lobby')
        self.sio.sleep(1)
        self.assertIsNotNone(self.expected)
        self.assertIsNotNone(self.actual)
        self.assertTrue(self.expected == len(self.actual))

    def test_room_create(self):
        @self.sio.on('room/create')
        def room_create(data):
            self.expected = {'room_name': data['room']['name'], 'htmls': data['htmls']}
            self.actual = {'room_name': 'some_room', 'htmls': []}

        self.sio.emit('visit', {'user_name': 'room/create user'})
        self.sio.emit('room/create', {'room_name': 'some_room', 'plugins': []})
        self.sio.sleep(1)
        self.assertIsNotNone(self.expected)
        self.assertIsNotNone(self.actual)
        self.assertEqual(self.expected, self.actual)

    def test_plugin_register(self):
        @self.sio.on('plugin/register')
        def plugin_register(data):
            self.expected = True
            self.actual = data['state']

        plugin_name = 'test_plugin_name'
        with open(os.path.join(os.path.dirname(__file__), 'sample_plugin.py.txt'), mode='r') as f:
            plugin_file = f.read()
        self.sio.emit('visit', {'user_name': 'plugin_register user'})
        self.sio.emit('plugin/register', {'plugin_name': plugin_name, 'plugin_file': plugin_file})
        self.sio.sleep(1)
        self.assertEqual(self.expected, self.actual)
