<template lang='pug'>
  div(v-if="room")
    v-container(fluid grid-list-md text-xs-center)
      v-layout(row wrap)
        v-flex(d-flex xs12 sm12 md12)
          v-toolbar(dense)
            v-toolbar-title {{ room.name }}
            v-spacer
            settings(:room="room")
            v-btn(color="error" @click="requestExitRoom") 退出

    desk#desk(:plugins="room.plugins")

    v-container(fluid grid-list-md text-xs-center)
      v-layout(row wrap)
        v-flex(d-flex xs12 sm12 md12)
          v-card(white)
            status#status(:members="room.members")
</template>

<script lang="ts">
import Vue from 'vue'
import Component from 'vue-class-component'

import { Room, User, Plugin, PluginProperties, PluginMeta } from '@/model'

import Desk from '@/components/room/Desk.vue'
import Status from '@/components/room/Status.vue'
import Settings from '@/components/room/Settings.vue'

import { ROOMS_MOCK } from '@/api/mock'
import { compile } from '@/logic/compiler'

import * as Package from '@/plugin_examples/counter'
// import * as Package from '@/plugin_examples/chat'
// import * as Package from '@/plugin_examples/paint'

@Component<RoomView>({
  components: { Desk, Status, Settings },
  sockets: {
    'room/enter' (data: { room: Room }) {
      this.responseEnterRoom(data)
    },
    'room/update' (data: { room: Room }) {
      this.room!!.members = data.room.members
    },
    'room/exit' (data: {}) {
      this.responseExitRoom()
    },
    'room/exit-event' ({ members }: { members: User[] }) {
      this.room!!.members = members
    }
  },
})
export default class RoomView extends Vue {
  private room: Room | null = null

  private get roomId (): string {
    return this.$route.params.roomId
  }

  private mounted () {
    console.log(`[Room] request enter`)
    this.$socket.emit('room/enter', { room_id: this.roomId })
  }

  private async responseEnterRoom ({ room }: { room: Room }) {
    console.log(`[Room] entered`)
    this.room = room
    this.room.plugins = []

    for (const { plugin, meta } of this.room.pluginPackages) {
      const initializer = new Function(...plugin.functions['initialize'])
      const properties: PluginProperties = {
        record: initializer(),
        env: { instanceId: plugin.instanceId, room: this.room },
        meta: meta,
      }
      const component = await compile(plugin, properties)
      // reactively
      this.room.plugins.push({ component, properties })
    }
  }

  private requestExitRoom () {
    this.$socket.emit('room/exit', { room_id: this.roomId})
  }

  private responseExitRoom () {
    this.$router.push('/lobby')
  }
}
</script>

<style scoped>
#desk {
  height: 100%;
}

#status {
  height: 300px;
}

v-card {
  height: 100%;
}
</style>
