import sys, os

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

    def test_room_create_with_plugin(self):
        print('\n', sys._getframe().f_code.co_name)

        @self.sio.on('plugin/register')
        def plugin_register(data):
            self.data = data
            print(self.data, file=sys.stderr, flush=True)

        @self.sio.on('room/create')
        def room_create(data):
            self.data = data
            print(self.data, file=sys.stderr, flush=True)

        file_name = os.path.join(os.path.dirname(__file__), 'counter.ipl')
        with open(file_name, mode='r') as f:
            content = f.read()

        self.sio.emit('visit', {'userName': 'room_with_plugin'})
        self.sio.emit('plugin/register',
                      {'name': 'counter',
                       'description': 'counter',
                       'author': 'k',
                       'tags': 'official',
                       'content': content})

        self.sio.sleep(2)
        self.sio.emit('room/create', {'roomName': 'some_room', 'plugins': [self.data['id']]})
        self.sio.sleep(2)

        self.assertTrue('room' in self.data)
        self.assertTrue('plugins' in self.data['room'])
        self.assertTrue(len(self.data['room']['plugins']) > 0)
        self.assertTrue('plugin' in self.data['room']['plugins'][0])
        self.assertTrue('template' in self.data['room']['plugins'][0]['plugin'])
        self.assertTrue('functions' in self.data['room']['plugins'][0]['plugin'])
        # self.assertTrue(len(self.data['room']['plugins'][0]['plugin']['functions']) > 0)
        self.assertTrue('instanceId' in self.data['room']['plugins'][0]['plugin'])
        self.assertTrue('config' in self.data['room']['plugins'][0]['plugin'])
        self.assertTrue('enabled' in self.data['room']['plugins'][0]['plugin']['config'])
        self.assertTrue('meta' in self.data['room']['plugins'][0])
        self.assertTrue('id' in self.data['room']['plugins'][0]['meta'])
        self.assertTrue('name' in self.data['room']['plugins'][0]['meta'])
        self.assertTrue('description' in self.data['room']['plugins'][0]['meta'])
        self.assertTrue('author' in self.data['room']['plugins'][0]['meta'])
        self.assertTrue('tags' in self.data['room']['plugins'][0]['meta'])
        self.assertTrue('content' in self.data['room']['plugins'][0]['meta'])

    def test_room_enter_with_plugin(self):
        print('\n', sys._getframe().f_code.co_name)

        @self.sio.on('plugin/register')
        def plugin_register(data):
            self.data = data
            print(self.data, file=sys.stderr, flush=True)

        @self.sio.on('room/create')
        def room_create(data):
            self.data = data
            print(self.data, file=sys.stderr, flush=True)

        @self.sio.on('room/enter')
        def room_enter(data):
            self.data = data
            print(self.data, file=sys.stderr, flush=True)

        file_name = os.path.join(os.path.dirname(__file__), 'counter.ipl')
        with open(file_name, mode='r') as f:
            content = f.read()

        self.sio.emit('visit', {'userName': 'room_with_plugin'})
        self.sio.emit('plugin/register',
                      {'name': 'counter',
                       'description': 'counter',
                       'author': 'k',
                       'tags': 'official',
                       'content': content})
        self.sio.sleep(2)
        self.sio.emit('room/create', {'roomName': 'some_room', 'plugins': [self.data['id']]})
        self.sio.sleep(2)
        self.sio.emit('room/enter', {'roomId': self.data['room']['id']})
        self.sio.sleep(2)

        self.assertTrue('room' in self.data)
        self.assertTrue('plugins' in self.data['room'])
        self.assertTrue(len(self.data['room']['plugins']) > 0)
        self.assertTrue('plugin' in self.data['room']['plugins'][0])
        self.assertTrue('template' in self.data['room']['plugins'][0]['plugin'])
        self.assertTrue('functions' in self.data['room']['plugins'][0]['plugin'])
        # self.assertTrue(len(self.data['room']['plugins'][0]['plugin']['functions']) > 0)
        self.assertTrue('instanceId' in self.data['room']['plugins'][0]['plugin'])
        self.assertTrue('config' in self.data['room']['plugins'][0]['plugin'])
        self.assertTrue('enabled' in self.data['room']['plugins'][0]['plugin']['config'])
        self.assertTrue('meta' in self.data['room']['plugins'][0])
        self.assertTrue('id' in self.data['room']['plugins'][0]['meta'])
        self.assertTrue('name' in self.data['room']['plugins'][0]['meta'])
        self.assertTrue('description' in self.data['room']['plugins'][0]['meta'])
        self.assertTrue('author' in self.data['room']['plugins'][0]['meta'])
        self.assertTrue('tags' in self.data['room']['plugins'][0]['meta'])
        self.assertTrue('content' in self.data['room']['plugins'][0]['meta'])
