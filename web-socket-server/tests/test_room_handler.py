import sys, os

import unittest
import socketio

from config import url, socketio_path


class TestSocketIOHandler(unittest.TestCase):

    def setUp(self):
        self.client = socketio.Client()
        self.client.connect(url, socketio_path=socketio_path)

        self.data = None
        self.expected = None
        self.actual = None

    def tearDown(self):
        self.client.disconnect()

    def test_room_create_no_plugin(self):
        print('\n', sys._getframe().f_code.co_name, flush=True)

        @self.client.on('room/create')
        def room_create(data):
            self.data = data

        self.client.emit('visit', {'userName': 'room/create user'})
        self.client.sleep(0.3)
        self.client.emit('lobby')
        self.client.sleep(0.3)
        self.client.emit('room/create', {'roomName': 'some room', 'plugins': []})
        self.client.sleep(0.3)

        self.assertTrue('room' in self.data)
        self.assertTrue('id' in self.data['room'])
        self.assertTrue('name' in self.data['room'])
        self.assertTrue('members' in self.data['room'])
        self.assertTrue('plugins' in self.data['room'])

    def test_room_enter_no_plugin(self):
        print('\n', sys._getframe().f_code.co_name, flush=True)

        @self.client.on('room/create')
        def room_create(data):
            self.data = data['room']['id']

        @self.client.on('room/enter')
        def room_enter(data):
            self.data = data

        self.client.emit('visit', {'userName': 'room/enter user'})
        self.client.sleep(0.3)
        self.client.emit('room/create', {'roomName': 'room/enter room', 'plugins': []})
        self.client.sleep(0.3)
        self.client.emit('room/enter', {'roomId': self.data})
        self.client.sleep(0.3)

        self.assertTrue('room' in self.data)
        self.assertTrue('id' in self.data['room'])
        self.assertTrue('name' in self.data['room'])
        self.assertTrue('members' in self.data['room'])
        self.assertTrue('plugins' in self.data['room'])

    def test_room_create_with_plugin(self):
        print('\n', sys._getframe().f_code.co_name, flush=True)

        @self.client.on('plugin/register')
        def plugin_register(data):
            self.data = data

        @self.client.on('room/create')
        def room_create(data):
            self.data = data

        file_name = os.path.join(os.path.dirname(__file__), 'counter.ipl')
        with open(file_name, mode='r') as f:
            content = f.read()

        self.client.emit('visit', {'userName': 'room_with_plugin'})
        self.client.sleep(0.3)
        self.client.emit('plugin/register',
                         {'name': 'counter',
                          'description': 'counter',
                          'author': 'k',
                          'tags': 'official',
                          'content': content})

        self.client.sleep(0.3)
        self.client.emit('room/create', {'roomName': 'some_room', 'plugins': [self.data['id']]})
        self.client.sleep(0.3)

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
        print('\n', sys._getframe().f_code.co_name, flush=True)

        @self.client.on('plugin/register')
        def plugin_register(data):
            self.data = data

        @self.client.on('room/create')
        def room_create(data):
            self.data = data

        @self.client.on('room/enter')
        def room_enter(data):
            self.data = data

        file_name = os.path.join(os.path.dirname(__file__), 'counter.ipl')
        with open(file_name, mode='r') as f:
            content = f.read()

        self.client.sleep(0.3)
        self.client.emit('visit', {'userName': 'room_with_plugin'})
        self.client.sleep(0.3)
        self.client.emit('plugin/register',
                         {'name': 'counter',
                          'description': 'counter',
                          'author': 'k',
                          'tags': 'official',
                          'content': content})
        self.client.sleep(0.3)
        self.client.emit('room/create', {'roomName': 'some_room', 'plugins': [self.data['id']]})
        self.client.sleep(0.3)
        self.client.emit('room/enter', {'roomId': self.data['room']['id']})
        self.client.sleep(0.3)

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

    def test_room_enter_update_detection(self):
        print('\n', sys._getframe().f_code.co_name, flush=True)
        self.client2 = socketio.Client()
        self.client2.connect(url, socketio_path=socketio_path)

        @self.client.on('room/create')
        def room_enter(data):
            self.data = data

        @self.client.on('room/update')
        def room_update(data):
            self.data = data

        self.client.emit('visit', {'userName': 'update_detection'})
        self.client.sleep(0.3)
        self.client.emit('room/create', {'roomName': 'some room', 'plugins': []})
        self.client.sleep(0.3)
        self.client.emit('room/enter', {'roomId': self.data['room']['id']})
        self.client.sleep(0.3)

        self.client2.emit('visit', {'userName': 'update_detection2'})
        self.client.sleep(0.3)
        self.client2.emit('room/enter', {'roomId': self.data['room']['id']})
        self.client2.sleep(0.3)

        self.assertTrue('room' in self.data)
        self.assertTrue('id' in self.data['room'])
        self.assertTrue('name' in self.data['room'])
        self.assertTrue('members' in self.data['room'])
        self.assertTrue('plugins' in self.data['room'])

        self.client2.disconnect()

    def test_room_exit_update_detection(self):
        print('\n', sys._getframe().f_code.co_name, flush=True)

        self.client2 = socketio.Client()
        self.client2.connect(url, socketio_path=socketio_path)

        @self.client.on('room/create')
        def room_enter(data):
            self.data = data

        @self.client.on('room/update')
        def room_update(data):
            self.data = data

        @self.client2.on('room/exit')
        def room_exit(data):
            print('\ncalled exit\n', flush=True)

        self.client.emit('visit', {'userName': 'exit_detection'})
        self.client.sleep(0.3)
        self.client.emit('room/create', {'roomName': 'some room', 'plugins': []})
        self.client.sleep(0.3)
        self.client.emit('room/enter', {'roomId': self.data['room']['id']})
        self.client.sleep(0.3)

        self.client2.emit('visit', {'userName': 'exit_detection2'})
        self.client2.sleep(0.3)
        self.client2.emit('room/enter', {'roomId': self.data['room']['id']})
        self.client2.sleep(0.3)
        self.client2.emit('room/exit')
        self.client2.sleep(0.3)

        self.assertTrue('room' in self.data)
        self.assertTrue('id' in self.data['room'])
        self.assertTrue('name' in self.data['room'])
        self.assertTrue('members' in self.data['room'])
        self.assertEqual(len(self.data['room']['members']), 1)
        self.assertTrue('plugins' in self.data['room'])

        self.client2.disconnect()
