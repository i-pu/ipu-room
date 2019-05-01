from config import sio
import visit
import lobby
import room.create
import plugin.register

sio.connect('http://localhost:8000')

print('visit')
visit.test()

print('lobby')
lobby.test()

print('room.create')
room.create.test()

print('plugin.register')
plugin.register.test()

sio.disconnect()
