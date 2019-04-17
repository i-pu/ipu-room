from flask_socketio import join_room, leave_room, rooms
from .config import socketio


@socketio.on('enter_room')
def begin_chat(data):
    print('begin_chat')
    print(data)
    join_room('chat_room')
    socketio.emit('enter_room',
                  data={
                      'comments': ['hoge comment', 'hoge2 comment'],
                      'users': ['user1', 'user2'],
                      'room': {'room_name': 'hoge room name'},
                  })


@socketio.on('chat')
def chat(data):
    # data is json
    print('chat event')
    print('data:', data)
    print('rooms:', rooms())
    data['comment_id'] = '10000000'
    socketio.emit('chat', data=data, room='chat_room')


@socketio.on('exit_room')
def exit_chat(data):
    print('exit room')
    print(data)
    leave_room('chat_room')


@socketio.on_error()
def on_error():
    print('wtf')
