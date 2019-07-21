import os
import sys

import socketio

from config import url, socketio_path


def test_room_create_no_plugin():
    client = socketio.Client()
    client.connect(url, socketio_path=socketio_path)

    @client.on('room/create')
    def room_create(res):
        client.response = res

    client.emit('visit', {'userName': 'room/create'})
    client.sleep(0.3)
    client.emit('lobby')
    client.sleep(0.3)
    client.emit('room/create', {'roomName': 'room/create', 'plugins': []})
    client.sleep(0.3)
    client.disconnect()
    client.sleep(0.3)

    assert 'room' in client.response
    assert 'id' in client.response['room']
    assert 'name' in client.response['room']
    assert 'members' in client.response['room']
    assert 'plugins' in client.response['room']


def test_room_enter_no_plugin():
    client = socketio.Client()
    client.connect(url, socketio_path=socketio_path)

    @client.on('room/create')
    def room_create(res):
        client.response = res['room']['id']

    @client.on('room/enter')
    def room_enter(res):
        client.response = res

    client.emit('visit', {'userName': 'room/enter user'})
    client.sleep(0.3)
    client.emit('room/create', {'roomName': 'room/enter room', 'plugins': []})
    client.sleep(0.3)
    client.emit('room/enter', {'roomId': client.response})
    client.sleep(0.3)

    assert 'room' in client.response
    assert 'id' in client.response['room']
    assert 'name' in client.response['room']
    assert 'members' in client.response['room']
    assert 'plugins' in client.response['room']

    client.disconnect()


def test_room_create_with_plugin():
    client = socketio.Client()
    client.connect(url, socketio_path=socketio_path)

    @client.on('plugin/register')
    def plugin_register(res):
        client.response = res

    @client.on('room/create')
    def room_create(res):
        client.response = res

    file_name = os.path.join(os.path.dirname(__file__), 'counter.ipl')
    with open(file_name, mode='r') as f:
        content = f.read()

    client.emit('visit', {'userName': 'room_with_plugin'})
    client.sleep(0.3)
    client.emit('plugin/register',
                {'name': 'counter',
                 'description': 'counter',
                 'thumbnailUrls': [],
                 'author': 'integration test',
                 'tags': ['test'],
                 'content': content})
    client.sleep(0.3)
    client.emit('room/create', {'roomName': 'some_room', 'plugins': [client.response['id']]})
    client.sleep(0.3)

    assert 'room' in client.response
    assert 'plugins' in client.response['room']
    assert len(client.response['room']['plugins']) > 0
    assert 'plugin' in client.response['room']['plugins'][0]
    assert 'template' in client.response['room']['plugins'][0]['plugin']
    assert 'functions' in client.response['room']['plugins'][0]['plugin']
    assert len(client.response['room']['plugins'][0]['plugin']['functions']) > 0
    assert 'instanceId' in client.response['room']['plugins'][0]['plugin']
    assert 'config' in client.response['room']['plugins'][0]['plugin']
    assert 'enabled' in client.response['room']['plugins'][0]['plugin']['config']
    assert 'meta' in client.response['room']['plugins'][0]
    assert 'id' in client.response['room']['plugins'][0]['meta']
    assert 'name' in client.response['room']['plugins'][0]['meta']
    assert 'description' in client.response['room']['plugins'][0]['meta']
    assert 'thumbnailUrls' in client.response['room']['plugins'][0]['meta']
    assert 'author' in client.response['room']['plugins'][0]['meta']
    assert 'tags' in client.response['room']['plugins'][0]['meta']
    assert 'content' in client.response['room']['plugins'][0]['meta']

    client.disconnect()
#
#
# def test_room_enter_with_plugin():
#     client = socketio.Client()
#     client.connect(url, socketio_path=socketio_path)
#
#     @client.on('plugin/register')
#     def plugin_register(res):
#         client.response = res
#
#     @client.on('room/create')
#     def room_create(res):
#         client.response = res
#
#     @client.on('room/enter')
#     def room_enter(res):
#         client.response = res
#
#     file_name = os.path.join(os.path.dirname(__file__), 'counter.ipl')
#     with open(file_name, mode='r') as f:
#         content = f.read()
#
#     client.sleep(0.3)
#     client.emit('visit', {'userName': 'room_with_plugin'})
#     client.sleep(0.3)
#     client.emit('plugin/register',
#                 {'name': 'counter',
#                  'description': 'counter',
#                  'thumbnailUrls': [],
#                  'author': 'k',
#                  'tags': ['test'],
#                  'content': content})
#     client.sleep(0.3)
#     client.emit('room/create', {'roomName': 'some_room', 'plugins': [client.response['id']]})
#     client.sleep(0.3)
#     client.emit('room/enter', {'roomId': client.response['room']['id']})
#     client.sleep(0.3)
#
#     assert 'room' in client.response
#     assert 'plugins' in client.response['room']
#     assert len(client.response['room']['plugins']) > 0
#     assert 'plugin' in client.response['room']['plugins'][0]
#     assert 'template' in client.response['room']['plugins'][0]['plugin']
#     assert 'functions' in client.response['room']['plugins'][0]['plugin']
#     assert len(client.response['room']['plugins'][0]['plugin']['functions']) > 0
#     assert 'instanceId' in client.response['room']['plugins'][0]['plugin']
#     assert 'config' in client.response['room']['plugins'][0]['plugin']
#     assert 'enabled' in client.response['room']['plugins'][0]['plugin']['config']
#     assert 'meta' in client.response['room']['plugins'][0]
#     assert 'id' in client.response['room']['plugins'][0]['meta']
#     assert 'name' in client.response['room']['plugins'][0]['meta']
#     assert 'description' in client.response['room']['plugins'][0]['meta']
#     assert 'thumbnailUrls' in client.response['room']['plugins'][0]['meta']
#     assert 'author' in client.response['room']['plugins'][0]['meta']
#     assert 'tags' in client.response['room']['plugins'][0]['meta']
#     assert 'content' in client.response['room']['plugins'][0]['meta']
#
#     client.disconnect()
#
#
# def test_room_enter_update_detection():
#     client = socketio.Client()
#     client.connect(url, socketio_path=socketio_path)
#     client2 = socketio.Client()
#     client2.connect(url, socketio_path=socketio_path)
#
#     @client.on('room/create')
#     def room_enter(res):
#         client.response = res
#
#     @client.on('room/update')
#     def room_update(res):
#         client.response = res
#
#     client.emit('visit', {'userName': 'update_detection'})
#     client.sleep(0.3)
#     client.emit('room/create', {'roomName': 'some room', 'plugins': []})
#     client.sleep(0.3)
#     client.emit('room/enter', {'roomId': client.response['room']['id']})
#     client.sleep(0.3)
#
#     client2.emit('visit', {'userName': 'update_detection2'})
#     client.sleep(0.3)
#     client2.emit('room/enter', {'roomId': client.response['room']['id']})
#     client2.sleep(0.3)
#
#     assert 'room' in client.response
#     assert 'id' in client.response['room']
#     assert 'name' in client.response['room']
#     assert 'members' in client.response['room']
#     assert 'plugins' in client.response['room']
#
#     client.disconnect()
#     client2.disconnect()
#
#
# def test_room_exit_update_detection():
#     client = socketio.Client()
#     client.connect(url, socketio_path=socketio_path)
#     client2 = socketio.Client()
#     client2.connect(url, socketio_path=socketio_path)
#
#     @client.on('room/create')
#     def room_enter(res):
#         client.response = res
#
#     @client.on('room/update')
#     def room_update(res):
#         client.response = res
#
#     @client2.on('room/exit')
#     def room_exit(res):
#         client2.response = res
#
#     client.emit('visit', {'userName': 'exit_detection'})
#     client.sleep(0.3)
#     client.emit('room/create', {'roomName': 'some room', 'plugins': []})
#     client.sleep(0.3)
#     client.emit('room/enter', {'roomId': client.response['room']['id']})
#     client.sleep(0.3)
#
#     client2.emit('visit', {'userName': 'exit_detection2'})
#     client2.sleep(0.3)
#     client2.emit('room/enter', {'roomId': client.response['room']['id']})
#     client2.sleep(0.3)
#     client2.emit('room/exit')
#     client2.sleep(0.3)
#
#     assert 'room' in client.response
#     assert 'id' in client.response['room']
#     assert 'name' in client.response['room']
#     assert 'members' in client.response['room']
#     assert len(client.response['room']['members']) == 1
#     assert 'plugins' in client.response['room']
#     assert client2.response is not None
#
#     client.disconnect()
#     client2.disconnect()
