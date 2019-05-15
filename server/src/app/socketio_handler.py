import pprint
from logging import basicConfig, DEBUG, getLogger
from typing import List, Any

from flask_socketio import join_room, leave_room, rooms
from flask import request, g

from . import config
from .config import socketio
from .models import db, Room, Comment, User, Plugin, ActivePlugin
from . import utils
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

    ret = {'user': user.__to_dict__()}
    mylogger.info('- - return')
    mylogger.info('{}'.format(ret))
    socketio.emit('visit', data=ret)


@socketio.on('lobby')
@utils.byte_data_to_dict
@utils.check_user
@utils.function_info_wrapper
def lobby(data):
    all_room = Room.query.all()

    ret = {'rooms': list(map(Room.__to_dict__, all_room))}
    mylogger.info('- - return')
    mylogger.info('{}'.format(ret))
    socketio.emit('lobby', data=ret)


@socketio.on('plugin/register')
@utils.byte_data_to_dict
@utils.check_user
@utils.function_info_wrapper
def plugin_register(data):
    mylogger.debug('- - data: {}'.format(data))
    plugin_name: str = data['name']
    plugin_content = data['content']
    plugin_description = data['description']
    # name: string,
    # description: string,
    # author: string,
    # tags: string,
    # content: string,

    try:
        template, events, records, python, addons = plugin_compiler(plugin_content)
        # todo: compiler error
        template = \
            '''
      <div>
        <h3> {{ v.count }} </h3>
        <v-btn @click="plus(1)"> Add </v-btn>
      </div>
    '''
    except Exception as e:
        mylogger.error(e)
        raise e

    plugin = Plugin(name=plugin_name,
                    python=python,
                    template=template,
                    description=plugin_description)
    try:
        db.session.add(plugin)
        db.session.commit()
        ret = {'state': True}
    except Exception as e:
        mylogger.error(e)
        ret = {'state': False}

    mylogger.info('- - return')
    mylogger.info('{}'.format(ret))
    socketio.emit('plugin/register', data=ret)


@socketio.on('room/create')
@utils.byte_data_to_dict
@utils.check_user
@utils.function_info_wrapper
def room_create(data):
    """
    新しく部屋を作り，
    plugin を作成して
    部屋の情報を作成し返す．

    Args:
        data: {'room_name': str, 'plugins': [plugin_id]}

    Emit:
        room

    Returns:

    """
    room_name = data['room_name']
    room = Room(name=room_name)
    db.session.add(room)
    db.session.commit()

    plugins = data['plugins']

    for plugin_id in plugins:

        try:
            plugin = Plugin.query.filter_by(id=plugin_id).one()
        except Exception as e:
            mylogger.error(e)
            raise e

        active_plugin = ActivePlugin(room_id=room.id, plugin_id=plugin_id)
        db.session.add(active_plugin)
        db.session.commit()

        exec(plugin.python)

        config.global_plugins[room.id + '-' + active_plugin.id] = eval('Plugin()')
        mylogger.info('--------------- plugins ---------------')
        mylogger.info(config.global_plugins[room.id + '-' + active_plugin.id])

    ret = {'room': room.__to_dict__()}
    mylogger.info('- - return')
    mylogger.info('{}'.format(ret))
    socketio.emit('room/create', data=ret)


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

    ret = {'room': room.__to_dict__()}
    mylogger.info('- - return')
    mylogger.info('{}'.format(ret))
    socketio.emit('room/enter', data=ret, room=room_id)


@socketio.on('plugin/info')
@utils.byte_data_to_dict
@utils.check_user
@utils.function_info_wrapper
def plugin_info(data):
    active_plugins = ActivePlugin.query.filter_by(room_id=data['room_id']).all()
    mylogger.debug('active_plugins: {}'.format(active_plugins))

    configs = []
    for ap in active_plugins:
        plugin_obj = config.global_plugins[data['room_id'] + '-' + ap.id]
        plugin = Plugin.query.filter_by(id=ap.plugin_id).one()
        try:
            configs.append(
                {'instance': {'template': plugin.template,
                              'events': plugin_obj.events,
                              'record': plugin_obj.constructor(),
                              'addons': [],
                              **ap.__to_dict__(),
                              },
                 'meta': plugin.__to_dict__(),
                 }
            )
        except Exception as e:
            import traceback
            mylogger.error(e)
            traceback.print_exc()
            raise e

    mylogger.info('- - return')
    mylogger.info('{}'.format(configs))
    socketio.emit('plugin/info', data=configs)


# todo: trigger するときにはroom.idとactive_plugin.idがほしい
@socketio.on('plugin/trigger')
@utils.byte_data_to_dict
@utils.check_user
@utils.function_info_wrapper
def plugin_trigger(data):
    room_id = data['room_id']
    instance_id = data['instance_id']
    event_name = data['event_name']
    event_args: List[Any] = data['args']

    user_plugin = config.global_plugins[room_id + '-' + instance_id]
    event_func = eval('user_plugin.{}'.format(event_name))
    result = {'record': event_func(*event_args)}

    mylogger.info('- - return')
    mylogger.info('{}'.format(result))
    socketio.emit('plugin/trigger', data=result, room=room_id)


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

    socketio.emit('chat', data={'comment': comment.__to_dict()}, room=room_id)


@socketio.on('room/exit')
@utils.byte_data_to_dict
@utils.check_user
@utils.function_info_wrapper
def room_exit(data):
    user = User.query.filter_by(id=request.sid).one()
    room_id = user.room_id
    leave_room(room_id)

    user.query.update({'room_id': None})
    db.session.commit()

    socketio.emit('room/exit')  # 抜けた人に通知

    users = User.query.filter_by(room_id=room_id).all()

    ret = {'members': list(map(User.__to_dict__, users))}
    socketio.emit('room/exit_event',  # 残ってる人に通知
                  data=ret,
                  room=room_id)


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
