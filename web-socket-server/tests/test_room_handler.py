import sys, os

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

    def test_room_create_no_plugin(self):
        print('\n', sys._getframe().f_code.co_name)

        @self.client.on('room/create')
        def room_create(data):
            self.data = data
            print(self.data, file=sys.stderr, flush=True)

        self.client.emit('visit', {'userName': 'room/create user'})
        self.client.emit('lobby')
        self.client.emit('room/create', {'roomName': 'some room', 'plugins': []})
        self.client.sleep(2)

        self.assertTrue('room' in self.data)
        self.assertTrue('id' in self.data['room'])
        self.assertTrue('name' in self.data['room'])
        self.assertTrue('members' in self.data['room'])
        self.assertTrue('plugins' in self.data['room'])

    def test_room_enter_no_plugin(self):
        print('\n', sys._getframe().f_code.co_name)

        @self.client.on('room/create')
        def room_create(data):
            self.data = data['room']['id']

        @self.client.on('room/enter')
        def room_enter(data):
            self.data = data
            print(self.data, file=sys.stderr, flush=True)

        self.client.emit('visit', {'userName': 'room/enter user'})
        self.client.emit('room/create', {'roomName': 'room/enter room', 'plugins': []})
        self.client.sleep(2)
        self.client.emit('room/enter', {'roomId': self.data})
        self.client.sleep(2)

        self.assertTrue('room' in self.data)
        self.assertTrue('id' in self.data['room'])
        self.assertTrue('name' in self.data['room'])
        self.assertTrue('members' in self.data['room'])
        self.assertTrue('plugins' in self.data['room'])

    def test_room_create_with_plugin(self):
        print('\n', sys._getframe().f_code.co_name)

        @self.client.on('plugin/register')
        def plugin_register(data):
            self.data = data
            print(self.data, file=sys.stderr, flush=True)

        @self.client.on('room/create')
        def room_create(data):
            self.data = data
            print(self.data, file=sys.stderr, flush=True)

        file_name = os.path.join(os.path.dirname(__file__), 'counter.ipl')
        with open(file_name, mode='r') as f:
            content = f.read()

        self.client.emit('visit', {'userName': 'room_with_plugin'})
        self.client.emit('plugin/register',
                      {'name': 'counter',
                       'description': 'counter',
                       'author': 'k',
                       'tags': 'official',
                       'content': content})

        self.client.sleep(2)
        self.client.emit('room/create', {'roomName': 'some_room', 'plugins': [self.data['id']]})
        self.client.sleep(2)

        self.assertTrue('room' in self.data)
        self.assertTrue('plugins' in self.data['room'])
        self.assertTrue(len(self.data['room']['plugins']) > 0)
        self.assertTrue('plugin' in self.data['room']['plugins'][0])
        self.assertTrue('template' in self.data['room']['plugins'][0]['plugin'])
        self.assertTrue('functions' in self.data['room']['plugins'][0]['plugin'])
        self.assertTrue(len(self.data['room']['plugins'][0]['plugin']['functions']) > 0)
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

        @self.client.on('plugin/register')
        def plugin_register(data):
            self.data = data
            print(self.data, file=sys.stderr, flush=True)

        @self.client.on('room/create')
        def room_create(data):
            self.data = data
            print(self.data, file=sys.stderr, flush=True)

        @self.client.on('room/enter')
        def room_enter(data):
            self.data = data
            print(self.data, file=sys.stderr, flush=True)

        file_name = os.path.join(os.path.dirname(__file__), 'counter.ipl')
        with open(file_name, mode='r') as f:
            content = f.read()

        self.client.emit('visit', {'userName': 'room_with_plugin'})
        self.client.emit('plugin/register',
                      {'name': 'counter',
                       'description': 'counter',
                       'author': 'k',
                       'tags': 'official',
                       'content': content})
        self.client.sleep(2)
        self.client.emit('room/create', {'roomName': 'some_room', 'plugins': [self.data['id']]})
        self.client.sleep(2)
        self.client.emit('room/enter', {'roomId': self.data['room']['id']})
        self.client.sleep(2)

        self.assertTrue('room' in self.data)
        self.assertTrue('plugins' in self.data['room'])
        self.assertTrue(len(self.data['room']['plugins']) > 0)
        self.assertTrue('plugin' in self.data['room']['plugins'][0])
        self.assertTrue('template' in self.data['room']['plugins'][0]['plugin'])
        self.assertTrue('functions' in self.data['room']['plugins'][0]['plugin'])
        self.assertTrue(len(self.data['room']['plugins'][0]['plugin']['functions']) > 0)
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
