from config import sio


def test():
    @sio.on('visit')
    def visit(data):
        print(data)

    @sio.on('lobby')
    def lobby(data):
        print(data)

    @sio.on('room/create')
    def room_create(data):
        print(data)

    sio.emit('room/create', {'room_name': 'some_room', 'plugins': []})
    sio.sleep(1)
