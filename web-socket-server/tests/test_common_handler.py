import sys

import unittest
import socketio

from config import url, socketio_path


def test_visit():
    client = socketio.Client()
    client.connect(url, socketio_path=socketio_path)

    @client.on('visit')
    def visit(res):
        client.response = res
        pass

    client.emit('visit', {'userName': 'alis'})
    client.sleep(0.3)

    client.disconnect()

    assert 'user' in client.response
    assert 'id' in client.response['user']
    assert 'name' in client.response['user']
    assert 'roomId' in client.response['user']


def test_lobby():
    client = socketio.Client()
    client.connect(url, socketio_path=socketio_path)

    @client.on('lobby')
    def lobby(res):
        client.response = res

    client.emit('visit', {'userName': 'lobby user'})
    client.sleep(0.3)
    client.emit('lobby')
    client.sleep(0.3)

    client.disconnect()

    assert 'rooms' in client.response
