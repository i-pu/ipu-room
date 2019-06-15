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

    def test_room_create_no_plugin(self):
        print('\n', sys._getframe().f_code.co_name)
        @self.sio.on('room/create')
        def room_create(data):
            self.data = data
            print(self.data, file=sys.stderr, flush=True)

        self.sio.emit('visit', {'userName': 'room/create user'})
        self.sio.emit('lobby')
        self.sio.emit('room/create', {'roomName': 'some room', 'plugins': []})
        self.sio.sleep(2)

        self.assertTrue('room' in self.data)
        self.assertTrue('id' in self.data['room'])
        self.assertTrue('name' in self.data['room'])
        self.assertTrue('members' in self.data['room'])
        self.assertTrue('plugins' in self.data['room'])

    def test_room_enter_no_plugin(self):
        print('\n', sys._getframe().f_code.co_name)
        @self.sio.on('room/create')
        def room_create(data):
            self.data = data['room']['id']

        @self.sio.on('room/enter')
        def room_enter(data):
            self.data = data
            print(self.data, file=sys.stderr, flush=True)

        self.sio.emit('visit', {'userName': 'room/enter user'})
        self.sio.emit('room/create', {'roomName': 'room/enter room', 'plugins': []})
        self.sio.sleep(2)
        self.sio.emit('room/enter', {'roomId': self.data})
        self.sio.sleep(2)

        self.assertTrue('room' in self.data)
        self.assertTrue('id' in self.data['room'])
        self.assertTrue('name' in self.data['room'])
        self.assertTrue('members' in self.data['room'])
        self.assertTrue('plugins' in self.data['room'])

    # def test_room_create_with_plugin(self):
        #print('\n', sys._getframe().f_code.co_name)
    #     @self.sio.on('room/create')
    #     def room_create(data):
    #         self.assertFalse('room' in data.values())
    #         self.expected = [{'config': {'name': 'counter', 'enabled': True}}]
    #         self.actual = data['room']['plugins']

    #     self.sio.emit('visit', {'user_name': 'room/create user'})
    #     self.sio.emit('room/create', {'room_name': 'some_room', 'plugins': ['counter']})
    #     self.sio.sleep(1)
    #     self.assertEqual(self.expected, self.actual)
