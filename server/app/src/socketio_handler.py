import pprint
from typing import List, Any

from flask_socketio import join_room, leave_room, rooms
from flask import request, g

from .config import socketio
from .models import db, Room, Comment, User, Plugin, ActivePlugin
from . import utils
from .plugin.compiler import plugin_compiler


# todo: skip id を 使ってみる

@socketio.on('sample')
@utils.byte_data_to_dict
@utils.debug_wrapper
def sample(data):
    pprint.pprint(data)
    print('socket id:', request.sid)


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


@socketio.on('plugin/register')
@utils.byte_data_to_dict
@utils.debug_wrapper
@utils.check_user
def plugin_register(data):
    print('plugin/register', flush=True)
    print('data:', data, flush=True)
    plugin_name: str = data['plugin_name']
    plugin_file = data['plugin_file']

    html, _, python = plugin_compiler(plugin_file)

    plugin = Plugin(name=plugin_name, python=python, html=html)
    try:
        db.session.add(plugin)
        db.session.commit()
        socketio.emit('plugin/register', data={'state': True})
    except Exception as e:
        socketio.emit('plugin/register', data={'state': False})
        raise e


@socketio.on('room/create')
@utils.byte_data_to_dict
@utils.debug_wrapper
@utils.check_user
def room_crate(data):
    # todo: html と rendering はいろいろ細かいところが決まっていないのでしていない
    """
    room/create -> insert into rooms -> emit room

    Args:
        data: {'room_name': str, 'plugins': [plugin_name]}

    Emit:
        room

        htmls: []

    Returns:

    """
    room_name = data['room_name']
    plugins: List[str] = data['plugins']
    room = Room(name=room_name)

    db.session.add(room)
    db.session.commit()

    if 'plugins' not in g:
        g.plugins = {}

    htmls = []

    for plugin_id in plugins:
        print(plugin_id, flush=True)
        plugin = Plugin.query.filter_by(id=plugin_id).one_or_none()

        if plugin is None:
            raise RuntimeError('plugin_id: {} does not exist')

        active_plugin = ActivePlugin(room_id=room.id, plugin_id=plugin_id)
        db.session.add(active_plugin)
        db.session.commit()

        python = plugin.python
        exec(python)
        exec('user_plugin = UserPlugin()')

        g.plugins[room.id + plugin_id] = user_plugin
        htmls.append(g.plugins[room.id + plugin_id].constructor())

    socketio.emit('room/create', data={
        **room.__to_dict__(),
        'htmls': htmls,
    })


@socketio.on('room/enter')
@utils.byte_data_to_dict
@utils.debug_wrapper
@utils.check_user
def room_enter(data):
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

    room.users.append(user)
    db.session.commit()

    socketio.emit('room/enter',
                  data={
                      **room.__to_dict__(),
                      'html': g.plugins[room_id + 'sample_plugin'].constructor(),
                      'event': []
                  }, room=room_id)


@socketio.on('plugin/trigger')
@utils.byte_data_to_dict
@utils.debug_wrapper
@utils.check_user
def plugin_trigger(data):
    room_id = data['room_id']
    plugin_id = data['plugin_id']
    event_name = data['event_name']
    event_args: List[Any] = data['args']

    user_plugin = g.plugins[room_id + plugin_id]
    exec('event_func = user_plugin.{}'.format(event_name))
    result = event_func(event_args)
    socketio.emit('plugin/trigger', data={'html': result}, room=room_id)


@socketio.on('chat')
@utils.byte_data_to_dict
@utils.debug_wrapper
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
@utils.debug_wrapper
@utils.check_user
def exit_room(data):
    room_id = data['room_id']

    user = User.query.filter_by(id=request.sid).one()
    user.query.update({'room_id': None})
    db.session.commit()

    leave_room(room_id)
    socketio.emit('room/exit', room=room_id)


@socketio.on('disconnect')
@utils.byte_data_to_dict
@utils.debug_wrapper
@utils.check_user
def disconnect(data):
    print('disconnect', flush=True)
    print(data, flush=True)

    user = User.query.filter_by(id=request.sid).one()
    db.session.delete(user)


@socketio.on_error()
def on_error(e):
    print('---------- error happen!!! --------- ', flush=True)
    print(e, flush=True)
