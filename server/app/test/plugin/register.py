import os

from config import sio


def test():
    @sio.on('plugin/register')
    def plugin_register(data):
        print(data)

    with open(os.path.join(os.path.dirname(__file__), 'sample_plugin.py.txt'), mode='r') as f:
        file = f.read()

    sio.emit('plugin/register', {'plugin_name': 'sample_plugin', 'plugin_file': file})
    sio.sleep(1)
