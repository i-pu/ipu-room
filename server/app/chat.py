import pprint

from flask_socketio import join_room, leave_room, rooms
from flask import request, g

from .config import socketio
from .models import db, Room, Comment, User, Plugin
from . import utils
from .io import WriteFile


# todo: data['user_id'] -> request.sid


@socketio.on('plugin/register')
@utils.byte_data_to_dict
@utils.debug_wrapper
def register_plugin_handler(data):
    print('plugin/register', flush=True)
    print('data:', data, flush=True)
    plugin_name: str = data['plugin_name']
    plugin_python_file = data['python_file']
    with open(plugin_name, mode='w') as f:
        f.write(plugin_python_file)

    # todo: 実験のため 一時コメント化
    # WriteFile(plugin_name + '.py', plugin_python_file)


@socketio.on('plugin/activate')
@utils.byte_data_to_dict
@utils.debug_wrapper
def activate_plugin_handler(data):
    print('plugin/activate', flush=True)
    print(data)
    room_id = str(data['room_id'])
    plugin_name = data['plugin_name']

    utils.activate_plugin(plugin_name, socketio, room_id)


# todo: plugin は pluginイベントを定義してその中でevent_nameとマッチした関数を呼び出すようにしたい


@socketio.on('plugin/trigger')
@utils.byte_data_to_dict
@utils.check_user
@utils.debug_wrapper
def plugin_trigger(data):
    # event name
    # plugin name
    room_id = data['room_id']
    plugin_args = data['args']
    invoked = g.plugins[room_id + 'sample_plugin'].plus(*plugin_args)
    socketio.emit('plugin/trigger', data={'html': invoked}, room=room_id)


def html_compiler():
    # TODO
    return '<button type="button" id="_plugin_btn_1_"> Add </button>'


def plugin_compiler(plugin):
    # TODO
    html = html_compiler()
    python = 'hoge'
    '''
    class Plugin():
      count = 0
  
      @classmethod
      def on_plus(cls, data):
        cls.count += data
        return { 'count': cls.count }
  
      @classmethod
      def all(cls) -> dict:
        return {
          'plus': cls.on_plus
        }
    '''
    return html, python


@socketio.on('visit')
@utils.byte_data_to_dict
@utils.debug_wrapper
def visit(data):
    """
    login procedure
    create user -> insert into users -> emit user

    Args:
        data: { 'user_name': str }

    Emit:
        user

    Returns:

    """

    user = User(name=data['user_name'], id=request.sid)
    db.session.add(user)
    db.session.commit()

    print('user:', user, flush=True)
    socketio.emit('visit', data=user.__to_dict__())


@socketio.on('room/create')
@utils.byte_data_to_dict
@utils.check_user
@utils.debug_wrapper
def room_crate(data):
    """
    create room -> insert into rooms -> emit room

    Args:
        data: {'room_name': str, 'plugins': [plugin_name]}

    Emit:
        room

    Returns:

    """
    from typing import List
    room_name = data['room_name']
    plugins: List[str] = data['plugins']
    room = Room(name=room_name)

    db.session.add(room)
    db.session.commit()
    for plugin_id in plugins:
        print('plugins', flush=True)
        print(plugin_id, flush=True)
    room_id: str = room.id
    print('room:', room)

    class Plugin():
        a = 0

        @classmethod
        def plus(cls, data):
            cls.a += data.num
            return '<p id="a"> num: {} </p>'.format(cls.a)

        def constructor(cls):
            return '<p id="a"> init {} </p>'.format(cls.a)

    get_plugin = Plugin()
    if 'plugins' not in g:
        g.plugins = {}
    g.plugins[room_id + 'sample_plugin'] = get_plugin

    socketio.emit('room/create', data=room.__to_dict__())


@socketio.on('lobby')
@utils.byte_data_to_dict
@utils.debug_wrapper
@utils.check_user
def lobby(data):
    all_room = Room.query.all()
    pprint.pprint(rooms(request.sid))

    socketio.emit('lobby',
                  data={
                      'rooms': list(map(Room.__to_dict__, all_room)),
                  })


@socketio.on('room/enter')
@utils.byte_data_to_dict
@utils.debug_wrapper
@utils.check_user
def room_enter(data):
    # todo: 部屋に入っているかどうかもこちらで判断する
    user = User.query.filter_by(id=request.sid).one_or_none()
    if user is None:
        raise RuntimeError('user_id: {} does not exist'.format(request.sid))
    print('user', user, flush=True)

    room_id = data['room_id']
    room = Room.query.filter_by(id=room_id).one_or_none()
    if room is None:
        raise RuntimeError('room_id: {} does not exist'.format(room_id))
    print('room:', room, flush=True)

    join_room(room_id)
    user.room_id = room_id
    db.session.add(user)
    db.session.commit()

    users = User.query.filter_by(room_id=room_id).all()
    comments = Comment.query.filter_by(room_id=room_id).all()
    socketio.emit('room/enter',
                  data={
                      'users': users,
                      'comments': comments,
                      'room_name': room.name,
                      'room_id': room.id,
                      'html': g.plugins[room_id+'sample_plugin'].constructor(),
                      'event': []
                  }, room=room_id)


@socketio.on('chat')
@utils.byte_data_to_dict
@utils.check_user
def chat(data):
    room_id = data['room_id']
    user_id = request.sid
    content = data['content']
    created_at = data['created_at']

    comment = Comment(room_id, user_id, content, created_at)
    db.session.add(comment)
    db.session.commit()

    socketio.emit('chat', data=comment.__to_dict(), room=room_id)


@socketio.on('room/exit')
@utils.byte_data_to_dict
@utils.check_user
def exit_room(data):
    room_id = data['room_id']
    user_id = data['user_id']

    user = User.query.filter_by(id=user_id).one()
    user.query.update({'room_id': None})
    db.session.commit()

    leave_room(room_id)
    socketio.emit('room/exit', room=room_id)


@socketio.on('disconnect')
@utils.byte_data_to_dict
@utils.check_user
def delete_user(data):
    print('disconnect', flush=True)
    print(data, flush=True)
    # todo: delete user from database


@socketio.on('sample')
@utils.byte_data_to_dict
def sample(data):
    print('socket id:', request.sid)


@socketio.on_error()
def on_error(e):
    print('---------- error happen!!! --------- ', flush=True)
    print(e, flush=True)
