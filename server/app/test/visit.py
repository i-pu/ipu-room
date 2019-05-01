from config import sio


def test():
    @sio.on('visit')
    def visit(data):
        print(data, flush=True)

    sio.emit('visit', {'user_name': 'alis'})
    sio.sleep(1)
