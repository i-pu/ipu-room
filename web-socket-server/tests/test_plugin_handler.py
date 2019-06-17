import sys, os

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
        print('\n', sys._getframe().f_code.co_name, flush=True)

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
        self.client.sleep(1)

        self.assertTrue(self.data['state'])

    def test_plugin_trigger(self):
        print('\n', sys._getframe().f_code.co_name, flush=True)

        @self.client.on('plugin/register')
        def plugin_register(data):
            self.data = data

        @self.client.on('room/create')
        def room_create(data):
            self.data = data

        @self.client.on('plugin/trigger')
        def plugin_trigger(data):
            self.data = data

        self.client.emit('visit', data={'userName': 'plugin/trigger'})
        import os
        file_name = os.path.join(os.path.dirname(__file__), 'counter.ipl')
        with open(file_name, mode='r') as f:
            content = f.read()
        self.client.emit('plugin/register',
                         {'name': 'counter',
                          'description': 'counter',
                          'author': 'k',
                          'tags': 'official',
                          'content': content})

        self.client.sleep(1)
        self.client.emit('room/create',
                         data={'roomName': 'some_room', 'plugins': [self.data['id']]})
        self.client.sleep(1)
        self.client.emit('room/enter',
                         data={'roomId': self.data['room']['id']})
        self.client.sleep(1)
        # client compile at local
        self.client.emit('plugin/trigger',
                         data={'roomId': self.data['room']['id'],
                               'instanceId': self.data['room']['plugins'][0]['plugin']['instanceId'],
                               'data': {'event': 'nums',
                                        'args': [1, 2, 3]}})

        self.client.sleep(1)

        self.assertTrue('data' in self.data)
        self.assertTrue('event' in self.data['data'])
        self.assertTrue('args' in self.data['data'])

    def test_plugin_clone(self):
        print('\n', sys._getframe().f_code.co_name, flush=True)
        self.client2 = socketio.Client()
        self.client2.connect(url)

        @self.client.on('plugin/register')
        def plugin_register(data):
            self.data = data

        @self.client.on('room/create')
        def room_enter(data):
            self.data = data

        @self.client.on('plugin/clone')
        def plugin_clone(data):
            print('\n', sys._getframe().f_code.co_name, flush=True)
            self.data = data
            # clone が呼ばれているか
            self.assertTrue('roomId' in self.data)
            self.assertTrue('instanceId' in self.data)
            self.assertTrue('from' in self.data)
            self.client.emit('plugin/clone',
                             data={
                                 'roomId': data['roomId'],
                                 'instanceId': data['instanceId'],
                                 'record': {'obj': 'string obj'},
                                 'from': data['from']})

        @self.client2.on('plugin/sync')
        def plugin_sync(data):
            self.data = data

        self.client.emit('visit', {'userName': 'plugin/clone'})
        self.client.sleep(1)

        file_name = os.path.join(os.path.dirname(__file__), 'counter.ipl')
        with open(file_name, mode='r') as f:
            content = f.read()
        self.client.emit('plugin/register',
                         {'name': 'counter',
                          'description': 'counter',
                          'author': 'k',
                          'tags': 'official',
                          'content': content})
        self.client.sleep(1)
        self.client.emit('room/create', {'roomName': 'plugin/clone', 'plugins': [self.data['id']]})
        self.client.sleep(1)
        self.client.emit('room/enter', {'roomId': self.data['room']['id']})
        self.client.sleep(1)

        self.client2.emit('visit', {'userName': 'plugin/clone2'})
        self.client.sleep(1)
        self.client2.emit('room/enter', {'roomId': self.data['room']['id']})
        self.client.sleep(1)
        self.client2.emit('plugin/sync',
                          {'roomId': self.data['room']['id'],
                           'instanceId': self.data['room']['plugins'][0]['plugin']['instanceId']})
        self.client.sleep(1)

        print(self.data, file=sys.stderr, flush=True)
        self.assertTrue('record' in self.data)

        self.client2.disconnect()
