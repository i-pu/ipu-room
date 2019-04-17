from functools import wraps

from flask_socketio import join_room, leave_room, rooms

from .config import socketio
from .models import db, User, Room, Comment


def check_user(handler):
    @wraps(handler)
    def already_registered(*args, **kwargs):
        data = args[0]
        user_id = data['user_id']
        user = User.query.filter('id={}'.format(user_id)).one()
        if user is None:
            raise RuntimeError()
        return handler(*args, **kwargs)

    return already_registered


@socketio.on('visit')
def visit(data):
    print('visit')
    user = User(data['username'])
    db.session.add(user)
    db.session.commit()


@socketio.on('create_room')
def create_room(data):
    print(create_room)
    print(data)

    room_name = data['room_name']
    room = Room(room_name)

    db.session.add(room)
    db.session.commit()

    socketio.emit('create_room', data={
        'room_name': room.name,
        'room_id': room.id,
    })


@socketio.on('lobby')
@check_user
def lobby(data):
    print('lobby')
    print('user_id', data['user_id'])
    all_room = Room.query().all()
    socketio.emit('lobby', data={
        'rooms': all_room,
    })


@socketio.on('enter_room')
@check_user
def begin_chat(data):
    print('enter_room')
    print('data:', data)
    user = User.query().filter('id={}'.format(data['user_id'])).one()
    print('user_id', user.id)

    room_id = data['room_id']
    room = Room.query().filter('id={}'.format(room_id)).one()
    print('room:', room)

    comments = Comment.query().filter('room_id={}'.format(room_id)).all()

    join_room(room_id)
    user.room_id = room_id
    db.session.add(user)
    db.session.commit()

    users = User.query().filter('room_id={}', format(room_id)).all()

    socketio.emit('enter_room',
                  data={
                      'users': users,
                      'comments': comments,
                      'room_name': room.name,
                      'room_id': room.id,
                  })


@socketio.on('chat')
@check_user
def chat(data):
    print('chat event')
    print('data:', data)

    room_id = data['room_id']
    user_id = data['user_id']
    content = data['content']
    created_at = data['created_at']

    comment = Comment(room_id, user_id, content, created_at)
    db.session.add(comment)
    db.session.commit()

    socketio.emit('chat', data=comment.__dict__(), room=room_id)


@socketio.on('exit_room')
@check_user
def exit_chat(data):
    print('exit room')
    print(data)

    room_id = data['room_id']
    user_id = data['user_id']

    user = User.query().filter('id={}'.format(user_id)).one()
    user.query.update({'room_id': None})
    db.session.commit()

    leave_room(room_id)


@socketio.on_error()
def on_error(e):
    print('---------- error happen!!! --------- ')
    print(e)