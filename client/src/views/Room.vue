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

import { Room } from '@/model'
import { Plugin, PluginConfig } from '@/model'

import Desk from '@/components/room/Desk.vue'
import Status from '@/components/room/Status.vue'
import Settings from '@/components/room/Settings.vue'

import { ROOMS_MOCK } from '@/api/mock'
import { compile, compileLocal } from '@/logic/compiler'

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
    'plugin/info' (packages: Array<{ instance: Plugin, meta: PluginConfig }>) {
      for (const { instance, meta } of packages) {
        this.addPlugin(instance, meta)
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
    this.room.plugins = []
    if (this.$store.getters.localOnly) {
      this.addPluginLocal('chat')
    } else {
      this.$socket.emit('plugin/info', { room_id: this.room.id })
    }
  }

  private async addPluginLocal (name: string) {
    if (!this.room) {
      return
    }
    const meta: PluginConfig = {
      room_id: this.roomId,
      plugin_id: '${name}001',
      name: name,
      enabled: true,
    }
    // counter
    if (meta.name === 'counter') {
      this.room.plugins.push({
        component: await compileLocal(Counter, meta, new CounterServer()),
        config: meta,
      })
    } else if (meta.name === 'chat') {
      this.room.plugins.push({
        component: await compileLocal(Chat, meta, new ChatServer()),
        config: meta,
      })
    } else if (meta.name === 'player') {
      this.room.plugins.push({
        component: await compileLocal(YoutubePlayer, meta, new YoutubePlayerServer()),
        config: meta,
      })
    } else {
      console.warn(`[Room] plugin ${meta.name} not found`)
    }
  }

  private async addPlugin (instance: Plugin, meta: PluginConfig) {
    this.room!!.plugins.push({
      component: await compile(instance, meta),
      config: meta,
    })
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
