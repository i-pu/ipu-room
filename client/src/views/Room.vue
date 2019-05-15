<template lang='pug'>
  div(v-if="room")
    v-container(fluid grid-list-md text-xs-center)
      v-layout(row wrap)
        v-flex(d-flex xs12 sm12 md12)
          v-toolbar(dense)
            v-toolbar-title {{ room.name }}
            v-spacer
            settings(:room="room" @add-plugin="addPlugin")
            v-btn(color="error" @click="requestExitRoom") 退出

    desk#desk(:room="room")

    v-container(fluid grid-list-md text-xs-center)
      v-layout(row wrap)
        v-flex(d-flex xs12 sm12 md12)
          v-card(white)
            status#status(:members="room.members")
</template>

<script lang="ts">
import Vue from 'vue'
import Component from 'vue-class-component'

import { Room, User, Plugin, PluginConfig, PluginMeta } from '@/model'

import Desk from '@/components/room/Desk.vue'
import Status from '@/components/room/Status.vue'
import Settings from '@/components/room/Settings.vue'

import { ROOMS_MOCK } from '@/api/mock'
import { compile } from '@/logic/compiler'

import Counter, { CounterServer } from '@/plugin_examples/counter'
import YoutubePlayer, { YoutubePlayerServer } from '@/plugin_examples/youtubePlayer'
import Chat, { ChatServer } from '@/plugin_examples/chat'

@Component<RoomView>({
  components: { Desk, Status, Settings },
  sockets: {
    'room/enter' (data: { room: Room }) {
      this.responseEnterRoom(data)
    },
    'room/exit' (data: {}) {
      this.responseExitRoom()
    },
    'room/exit-event' ({ members }: { members: User[] }) {
      this.room!!.members = members
    },
    'plugin/info' (packages: Array<{ instance: Plugin, meta: PluginMeta, config: PluginConfig }>) {
      this.room!!.plugins = []
      for (const { instance, meta, config } of packages) {
        this.addPlugin(instance, meta, config)
      }
    },
  },
})
export default class RoomView extends Vue {
  private room: Room | null = null

  private get roomId (): string {
    return this.$route.params.roomId
  }

  private mounted () {
    this.requestEnterRoom({ room_id: this.roomId })
  }

  private requestEnterRoom (data: { room_id: string }) {
    console.log(`[Room] request enter`)
    if (this.$store.getters.localOnly) {
      this.responseEnterRoom({ room: ROOMS_MOCK[0] })
    } else {
      this.$socket.emit('room/enter', { room_id: this.roomId })
    }
  }

  private responseEnterRoom (data: { room: Room }) {
    console.log(`[Room] entered`)
    console.log(JSON.parse(JSON.stringify(data.room.plugins)))
    this.room = data.room
    if (this.$store.getters.localOnly) {
      // this.addPluginLocal('chat')
    } else {
      this.$socket.emit('plugin/info', { room_id: this.room.id })
    }
  }

  private async addPlugin (instance: Plugin, meta: PluginMeta, config: PluginConfig, server?: any) {
    const component = await compile(instance, meta, config, server)
    this.room!!.plugins.push({ component, meta, config })
  }

  private requestExitRoom () {
    if (this.$store.getters.localOnly) {
      this.responseExitRoom()
    } else {
      this.$socket.emit('room/exit', {})
    }
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
