from config import sio


def test():
    @sio.on('visit')
    def visit(data):
        print(data, flush=True)

    @sio.on('lobby')
    def lobby(data):
        print(data, flush=True)

    sio.emit('visit', {'user_name': 'alis'})
    sio.sleep(1)
    sio.emit('lobby')
    sio.sleep(1)

