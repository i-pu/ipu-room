<template lang="pug">
  div
    v-toolbar(app)
      v-toolbar-title.headline.text-uppercase
        span.pr-3 ipu
        // span.pr-3 {{ name }} さん
      v-spacer
      v-btn(@click="test") テスト
      plugin-create-form
      room-create-form
    room-list(:rooms="rooms" :userId="userId")
</template>

<script>
import RoomList from '@/components/lobby/RoomList'
import RoomCreateForm from '@/components/lobby/RoomCreateForm'
import PluginCreateForm from '@/components/PluginCreateForm'

import { ROOMS_MOCK } from '@/api/mock'

export default {
  name: 'Lobby',
  components: { RoomList, RoomCreateForm, PluginCreateForm },
  data () {
    return {
      rooms: ROOMS_MOCK,
      userId: -1,
      name: 'ななし'
    }
  },
  sockets: {
    room (data) {
      console.log(data)
      this.rooms.push(data.room)
    },
    lobby (data) {
      console.log(data.rooms)
      this.rooms = data.rooms
    },
    visit (data) {
      console.log(data)
      this.userId = data.user_id
      this.$socket.emit('lobby', { user_id: data.user_id })
    }
  },
  mounted() {
    console.log(this.$route.params.userId)
    this.$socket.emit('visit', { user_name: 'AAA' })
  },
  methods: {
    test () {
      this.$socket.emit('register_plugin', {
        plugin_name: 'counter',
        python_file: "class Plugin():\n  count = 0\n\n  @classmethod\n  def on_connect(cls):\n    print('connected', flush=True)\n\n  @classmethod\n  def on_disconnect(cls):\n      print('disconnected', flush=True)\n\n  @classmethod\n  def on_my_event(cls, data=None):\n    cls.count += 1\n    print('on_my_event')\n    return {'count': cls.count}\n\n  @classmethod\n  def all(cls) -> dict:\n    return {\n      # todo: event 名の最初になんかの prefix を付ける必要がある\n      'my_connect': cls.on_connect,\n      'my_disconnect': cls.on_disconnect,\n      'my_event': cls.on_my_event\n    }"
      })
    }
  },
}
</script>