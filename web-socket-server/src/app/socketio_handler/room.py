from logging import basicConfig, DEBUG, getLogger

from flask_socketio import join_room, leave_room
from flask import request, g

from .. import config
from ..config import socketio
from .. import utils

basicConfig()
mylogger = getLogger(__name__)
mylogger.setLevel(DEBUG)


@socketio.on('room/create')
@utils.byte_data_to_dict
@utils.check_user
@utils.function_info_wrapper
def room_create(data):
    basicConfig()
    # room_name = data['room_name']
    # plugins = data['plugins']

    # room = Room(name=room_name)
    # db.session.add(room)
    # db.session.commit()

    # for plugin_id in plugins:

    #     try:
    #         plugin = Plugin.query.filter_by(id=plugin_id).one()
    #     except Exception as e:
    #         mylogger.error(e)
    #         raise e

    #     active_plugin = ActivePlugin(room_id=room.id, plugin_id=plugin_id)
    #     db.session.add(active_plugin)
    #     db.session.commit()

    #     exec(plugin.python)

    #     config.global_plugins[room.id + '-' + active_plugin.id] = eval('Plugin()')
    #     mylogger.info('--------------- plugins ---------------')
    #     mylogger.info(config.global_plugins[room.id + '-' + active_plugin.id])

    # ret = {'room': room.__to_dict__()}
    # mylogger.info('- - return')
    # mylogger.info('{}'.format(ret))
    # socketio.emit('room/create', data=ret)


@socketio.on('room/enter')
@utils.byte_data_to_dict
@utils.check_user
@utils.function_info_wrapper
def room_enter(data):
    basicConfig()
#     room_id = data['room_id']
#     room = Room.query.filter_by(id=room_id).one_or_none()
#     if room is None:
#         raise RuntimeError('room_id: {} does not exist'.format(room_id))
#
#     join_room(room_id)
#
#     user = User.query.filter_by(id=request.sid).one_or_none()
#
#     room.members.append(user)
#     db.session.commit()
#
#     ret = {'room': room.__to_dict__()}
#     mylogger.info('- - return')
#     mylogger.info('{}'.format(ret))
#     socketio.emit('room/enter', data=ret, room=room_id)


@socketio.on('room/exit')
@utils.byte_data_to_dict
@utils.check_user
@utils.function_info_wrapper
def room_exit(data):
    basicConfig()
    # user = User.query.filter_by(id=request.sid).one()
    # room_id = user.room_id
    # leave_room(room_id)

    # user.query.update({'room_id': None})
    # db.session.commit()

    # socketio.emit('room/exit')  # 抜けた人に通知

    # users = User.query.filter_by(room_id=room_id).all()

    # ret = {'members': list(map(User.__to_dict__, users))}
    # socketio.emit('room/exit_event',  # 残ってる人に通知
    #               data=ret,
    #               room=room_id)
