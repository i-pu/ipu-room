import os
import sys
import unittest

import socketio

from config import url, socketio_path


def test_plugin_register():
    client = socketio.Client()
    client.connect(url, socketio_path=socketio_path)

    @client.on('plugin/register')
    def plugin_register(res):
        client.response = res

    client.emit('visit', {'userName': 'plugin register'})
    client.sleep(0.3)
    client.emit('plugin/register',
                {'name': 'plugin name',
                 'description': 'plugin description',
                 'thumbnailUrls': [],
                 'author': 'plugin author',
                 'tags': ['test'],
                 'content': 'plugin content'})
    client.sleep(0.3)
    client.disconnect()

    assert 'state' in client.response
    assert client.response['state']


def test_plugin_trigger():
    client = socketio.Client()
    client.connect(url, socketio_path=socketio_path)

    @client.on('plugin/register')
    def plugin_register(res):
        client.response = res

    @client.on('room/create')
    def room_create(res):
        client.response = res

    @client.on('plugin/trigger')
    def plugin_trigger(res):
        client.response = res

    client.emit('visit', data={'userName': 'plugin/trigger'})
    file_name = os.path.join(os.path.dirname(__file__), 'counter.ipl')
    with open(file_name, mode='r') as f:
        content = f.read()

    client.emit('plugin/register',
                {'name': 'counter',
                 'description': 'counter',
                 'thumbnailUrls': [],
                 'author': 'k',
                 'tags': ['test'],
                 'content': content})

    client.sleep(0.3)
    client.emit('room/create', {'roomName': 'some_room', 'plugins': [client.response['id']]})
    client.sleep(0.3)
    client.emit('room/enter',
                {'roomId': client.response['room']['id']})
    client.sleep(0.3)
    client.emit('plugin/trigger',
                {'roomId': client.response['room']['id'],
                 'instanceId': client.response['room']['plugins'][0]['plugin']['instanceId'],
                 'data': {'event': 'nums', 'args': [1, 2, 3]}})
    client.sleep(0.3)
    client.disconnect()

    assert 'data' in client.response
    assert 'event' in client.response['data']
    assert 'args' in client.response['data']


def test_plugin_clone():
    client = socketio.Client()
    client.connect(url, socketio_path=socketio_path)
    client2 = socketio.Client()
    client2.connect(url, socketio_path=socketio_path)

    @client.on('plugin/register')
    def plugin_register(res):
        client.response = res

    @client.on('room/create')
    def room_enter(res):
        client.response = res

    @client.on('plugin/clone')
    def plugin_clone(res):
        client.response = res
        # clone が呼ばれているか
        client.emit(
            'plugin/clone',
            {'roomId': res['roomId'],
             'instanceId': res['instanceId'],
             'record': {'obj': 'string obj'},
             'from': res['from']}
        )

    @client2.on('plugin/sync')
    def plugin_sync(res):
        client2.response = res

    client.emit('visit', {'userName': 'plugin/clone'})
    client.sleep(0.3)

    file_name = os.path.join(os.path.dirname(__file__), 'counter.ipl')
    with open(file_name, mode='r') as f:
        content = f.read()
    client.emit(
        'plugin/register',
        {'name': 'counter',
         'description': 'counter',
         'thumbnailUrls': [],
         'author': 'k',
         'tags': ['test'],
         'content': content}
    )
    client.sleep(0.3)
    client.emit('room/create', {'roomName': 'plugin/clone', 'plugins': [client.response['id']]})
    client.sleep(0.3)
    client.emit('room/enter', {'roomId': client.response['room']['id']})
    client.sleep(0.3)

    client2.emit('visit', {'userName': 'plugin/clone2'})
    client2.sleep(0.3)
    client2.emit('room/enter', {'roomId': client.response['room']['id']})
    client2.sleep(0.3)
    client2.emit(
        'plugin/sync',
        {'roomId': client.response['room']['id'],
         'instanceId': client.response['room']['plugins'][0]['plugin']['instanceId']}
    )
    client2.sleep(0.3)
    client.sleep(0.3)

    client.disconnect()
    client2.disconnect()

    assert 'roomId' in client.response
    assert 'instanceId' in client.response
    assert 'from' in client.response

    assert 'record' in client2.response
