from flask_socketio import join_room, leave_room, rooms

from .config import socketio
from .models import db, Room, Comment
from .utils import *


@socketio.on('register_plugin')
@byte_data_to_dict
def register_plugin_handler(data):
    print('register_plugin_handler', flush=True)
    print('data:', data, flush=True)
    plugin_name = data['plugin_name']
    plugin_python_file = data['python_file']

    with open(plugin_name + '.py', mode='w') as f:
        f.write(plugin_python_file)


@socketio.on('activate_plugin')
@byte_data_to_dict
def activate_plugin_handler(data):
    print('activate_plugin_handler', flush=True)
    print(data)
    room_id = str(data['room_id'])
    plugin_name = data['plugin_name']

    activate_plugin(plugin_name, socketio, room_id)


@socketio.on('visit')
@byte_data_to_dict
def visit(data):
    print('visit', flush=True)
    print('data:', data, flush=True)

    user = User(name=data['user_name'])
    db.session.add(user)
    db.session.commit()

    print('user:', user, flush=True)
    socketio.emit('visit', data=user.__to_dict__())


@socketio.on('create_room')
@byte_data_to_dict
@check_user
def create_room(data):
    print('create_room', flush=True)
    print(data, flush=True)

    room_name = data['room_name']
    room = Room()
    room.name = room_name

    db.session.add(room)
    db.session.commit()

    socketio.emit('create_room', data=room.__to_dict__())


@socketio.on('lobby')
@byte_data_to_dict
@check_user
def lobby(data):
    print('lobby', flush=True)
    print('user_id', data['user_id'], flush=True)
    all_room = Room.query.all()

    socketio.emit('lobby',
                  data={
                      'rooms': list(map(__dict__, all_room)),
                  })


@socketio.on('enter_room')
@byte_data_to_dict
@check_user
def begin_chat(data):
    print('enter_room', flush=True)
    print('data:', data, flush=True)
    user = User.query.filter_by(id=data['user_id']).one()
    print('user_id', user.id, flush=True)

    room_id = data['room_id']
    room = Room.query.filter_by(id=room_id).one()
    print('room:', room, flush=True)

    comments = Comment.query.filter_by(room_id=room_id).all()

    join_room(room_id)
    user.room_id = room_id
    db.session.add(user)
    db.session.commit()

    users = User.query.filter_by(room_id=room_id).all()

    socketio.emit('enter_room',
                  data={
                      'users': users,
                      'comments': comments,
                      'room_name': room.name,
                      'room_id': room.id,
                  })


@socketio.on('chat')
@byte_data_to_dict
@check_user
def chat(data):
    print('chat event', flush=True)
    print('data:', data, flush=True)

    room_id = data['room_id']
    user_id = data['user_id']
    content = data['content']
    created_at = data['created_at']

    comment = Comment(room_id, user_id, content, created_at)
    db.session.add(comment)
    db.session.commit()

    socketio.emit('chat', data=comment.__to_dict(), room=room_id)


@socketio.on('exit_room')
@byte_data_to_dict
@check_user
def exit_chat(data):
    print('exit room', flush=True)
    print(data, flush=True)

    room_id = data['room_id']
    user_id = data['user_id']

    user = User.query.filter_by(id=user_id).one()
    user.query.update({'room_id': None})
    db.session.commit()

    leave_room(room_id)


@socketio.on_error()
def on_error(e):
    print('---------- error happen!!! --------- ', flush=True)
    print(e, flush=True)
