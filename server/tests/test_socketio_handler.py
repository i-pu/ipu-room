import os
import unittest

import socketio

from config import url


class TestSocketIOHandler(unittest.TestCase):
    sio = None
    expected = None
    actual = None

    def setUp(self):
        self.sio = socketio.Client()
        self.sio.connect(url)

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
        self.sio.sleep(2)
        self.assertIsNotNone(self.expected)
        self.assertIsNotNone(self.actual)
        self.assertEqual(self.expected, self.actual, 'expect alis')

    def test_lobby(self):
        @self.sio.on('lobby')
        def lobby(data):
            self.assertFalse('rooms' in data.values())

        self.sio.emit('visit', {'user_name': 'lobby user'})
        self.sio.emit('lobby')
        self.sio.sleep(2)

    def test_room_create(self):
        @self.sio.on('room/create')
        def room_create(data):
            self.assertFalse('room' in data.values())
            self.expected = {'room_name': data['room']['name']}
            self.actual = {'room_name': 'some_room'}

        self.sio.emit('visit', {'user_name': 'room/create user'})
        self.sio.emit('room/create', {'room_name': 'some_room', 'plugins': []})
        self.sio.sleep(1)
        self.assertEqual(self.expected, self.actual)

    def test_room_create_with_plugin(self):
        @self.sio.on('room/create')
        def room_create(data):
            self.assertFalse('room' in data.values())
            self.expected = [{'config': {'name': 'counter', 'enabled': True}}]
            self.actual = data['room']['plugins']

        self.sio.emit('visit', {'user_name': 'room/create user'})
        self.sio.emit('room/create', {'room_name': 'some_room', 'plugins': ['counter']})
        self.sio.sleep(1)
        self.assertEqual(self.expected, self.actual)

    def test_room_enter(self):
        @self.sio.on('room/create')
        def room_create(data):
            self.assertFalse('room' in data.values())
            room_id = data['room']['id']
            self.sio.emit('room/enter', {'room_id': room_id})

        @self.sio.on('room/enter')
        def room_enter(data):
            self.assertFalse('room' in data.values())

        self.sio.emit('visit', {'user_name': 'room/enter user'})
        self.sio.sleep(1)

    # 最後に実行したいので zzz をつけている
    def test_zzz_sample(self):
        @self.sio.on('sample')
        def sample(data):
            print(data, flush=True)

        self.sio.emit('sample')
        self.sio.sleep(1)
