# url = 'http://localhost:8000'
# url = 'http://35.187.206.173:31420'
import socketio

url = 'http://192.168.99.114:30000/'
socketio_path = 'web-socket-server/socket.io'
client = socketio.Client()
client.connect(url, socketio_path=socketio_path)
client.disconnect()
