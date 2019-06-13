from logging import basicConfig, DEBUG, getLogger

from .. import config
from ..config import socketio
from .. import utils


basicConfig()
mylogger = getLogger(__name__)
mylogger.setLevel(DEBUG)


@socketio.on('plugin/info')
@utils.byte_data_to_dict
@utils.check_user
@utils.function_info_wrapper
def plugin_info(data):
    basicConfig()
    # active_plugins = ActivePlugin.query.filter_by(room_id=data['room_id']).all()
    # mylogger.debug('active_plugins: {}'.format(active_plugins))

    # configs = []
    # for ap in active_plugins:
    #     plugin_obj = config.global_plugins[data['room_id'] + '-' + ap.id]
    #     plugin = Plugin.query.filter_by(id=ap.plugin_id).one()
    #     try:
    #         configs.append(
    #             {'instance': {'template': plugin.template,
    #                           'events': plugin_obj.events,
    #                           'record': plugin_obj.constructor(),
    #                           'addons': [],
    #                           **ap.__to_dict__(),
    #                           },
    #              'meta': plugin.__to_dict__(),
    #              }
    #         )
    #     except Exception as e:
    #         import traceback
    #         mylogger.error(e)
    #         traceback.print_exc()
    #         raise e

    # mylogger.info('- - return')
    # mylogger.info('{}'.format(configs))
    # socketio.emit('plugin/info', data=configs)


@socketio.on('plugin/trigger')
@utils.byte_data_to_dict
@utils.check_user
@utils.function_info_wrapper
def plugin_trigger(data):
    basicConfig()
    # room_id = data['room_id']
    # instance_id = data['instance_id']
    # event_name = data['event_name']
    # event_args: List[Any] = data['args']

    # mylogger.info('- - return')
    # socketio.emit('plugin/trigger', data=result, room=room_id)


@socketio.on('plugin/sync')
@utils.byte_data_to_dict
@utils.check_user
@utils.function_info_wrapper
def plugin_sync(data):
    basicConfig()
    # sync要求が
    # @socketio.on('plugin/clone')
    # @utils.byte_data_to_dict
    # @utils.check_user
    # @utils.function_info_wrapper
    # def plugin_clone(data):
    #     # todo: 今いる部屋にいるユーザをランダムに一人選びクローンする
    #     # todo: tokenを利用して，有効な相手からクローンが来たかドウかを確認するのもいいかも
    #     # todo: clone がsyncのとき以外からアクセスできるようになってしまっているのか
    #     socketio.emit('plugin/sync')

    # socketio.emit('plugin/clone')
