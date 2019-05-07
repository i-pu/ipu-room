import pprint
from logging import basicConfig, DEBUG, getLogger
from typing import List, Any

from flask_socketio import join_room, leave_room, rooms
from flask import request, g

from src import config
from src.config import socketio
from src.models import db, Room, Comment, User, Plugin, ActivePlugin
from src import utils
from .plugin.compiler import plugin_compiler

# todo: skip id を 使ってみる

basicConfig()
mylogger = getLogger(__name__)
mylogger.setLevel(DEBUG)


@socketio.on('sample')
@utils.byte_data_to_dict
@utils.function_info_wrapper
def sample(data):
    mylogger.debug('- - socket id: {}'.format(request.sid))
    mylogger.debug('- - global plugins: {}'.format(config.global_plugins))


@socketio.on('visit')
@utils.byte_data_to_dict
@utils.function_info_wrapper
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

    mylogger.debug('- - user: {}'.format(user))
    socketio.emit('visit', data=user.__to_dict__())


@socketio.on('lobby')
@utils.byte_data_to_dict
@utils.check_user
@utils.function_info_wrapper
def lobby(data):
    all_room = Room.query.all()

    socketio.emit('lobby',
                  data={
                      'rooms': list(map(Room.__to_dict__, all_room)),
                  })


@socketio.on('plugin/register')
@utils.byte_data_to_dict
@utils.check_user
@utils.function_info_wrapper
def plugin_register(data):
    mylogger.debug('- - data: {}'.format(data))
    plugin_name: str = data['plugin_name']
    plugin_file = data['plugin_file']

    # html, _, python = plugin_compiler(plugin_file)

    plugin = Plugin(name=plugin_name, python=plugin_file)
    try:
        db.session.add(plugin)
        db.session.commit()
        socketio.emit('plugin/register', data={'state': True})
    except Exception as e:
        socketio.emit('plugin/register', data={'state': False})
        raise e


@socketio.on('room/create')
@utils.byte_data_to_dict
@utils.check_user
@utils.function_info_wrapper
def room_crate(data):
    """
    新しく部屋を作り，
    plugin を作成して
    部屋の情報を作成し返す．

    Args:
        data: {'room_name': str, 'plugins': [plugin_name]}

    Emit:
        room

    Returns:

    """
    room_name = data['room_name']
    room = Room(name=room_name)
    db.session.add(room)
    db.session.commit()

    plugin_names = data['plugins']

    if config.global_plugins is None:
        mylogger.error('----------- plugins error --------')
        mylogger.error('config global is None!!!!!!!')
        raise Exception('config global is None')

    for plugin_name in plugin_names:

        plugin = Plugin.query.filter_by(name=plugin_name).one_or_none()
        if plugin is None:
            raise RuntimeError('plugin: {} does not exist'.format(plugin_name))

        active_plugin = ActivePlugin(room_id=room.id, name=plugin_name)
        db.session.add(active_plugin)
        db.session.commit()

        exec(plugin.python)

        config.global_plugins[room.id + '-' + plugin_name] = eval('UserPlugin()')
        mylogger.info('--------------- plugins ---------------')
        mylogger.info(config.global_plugins[room.id + '-' + plugin_name])

    socketio.emit('room/create', data={
        **room.__to_dict__(),
    })


@socketio.on('room/enter')
@utils.byte_data_to_dict
@utils.check_user
@utils.function_info_wrapper
def room_enter(data):
    room_id = data['room_id']
    room = Room.query.filter_by(id=room_id).one_or_none()
    if room is None:
        raise RuntimeError('room_id: {} does not exist'.format(room_id))

    join_room(room_id)

    user = User.query.filter_by(id=request.sid).one_or_none()

    room.members.append(user)
    db.session.commit()
    mylogger.debug('- - room: {}'.format(room))

    socketio.emit('room/enter',
                  data={
                      **room.__to_dict__(),
                  }, room=room_id)


@socketio.on('plugin/info')
@utils.byte_data_to_dict
@utils.check_user
@utils.function_info_wrapper
def plugin_info(data):
    # room_id から plugin を呼び出す．
    active_plugin = ActivePlugin.query.filter_by(room_id=data['room_id']).all()

    mylogger.debug('active_plugins: {}'.format(active_plugin))

    # todo: 固定になっているので 動的に生成する
    socketio.emit('plugin/info',
                  data={
                      'template': '<div><h3> {{ count }} </h3><v-btn @click="plus"> Add </v-btn></div>',
                      'events': {'plus': []},
                      'record': {'count': 0},
                  })


@socketio.on('plugin/trigger')
@utils.byte_data_to_dict
@utils.check_user
@utils.function_info_wrapper
def plugin_trigger(data):
    room_id = data['room_id']
    plugin_id = data['plugin_id']
    event_name = data['event_name']
    event_args: List[Any] = data['args']

    user_plugin = config.global_plugins[room_id + '-' + plugin_id]
    event_func = eval('user_plugin.{}'.format(event_name))
    result = event_func(event_args)
    socketio.emit('plugin/trigger', data={'html': result}, room=room_id)


@socketio.on('chat')
@utils.byte_data_to_dict
@utils.check_user
@utils.function_info_wrapper
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
@utils.function_info_wrapper
def exit_room(data):
    room_id = data['room_id']

    user = User.query.filter_by(id=request.sid).one()
    user.query.update({'room_id': None})
    db.session.commit()

    leave_room(room_id)
    socketio.emit('room/exit', room=room_id)


@socketio.on('disconnect')
@utils.byte_data_to_dict
@utils.check_user
@utils.function_info_wrapper
def disconnect(data):
    mylogger.debug('- - data: {}'.format(data))

    user = User.query.filter_by(id=request.sid).one()
    db.session.delete(user)
    db.session.commit()


@socketio.on_error()
def on_error(e):
    mylogger.error('---------- error happen!!! --------- ')
    mylogger.error(e)
