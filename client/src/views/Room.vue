<template lang='pug'>
  div(v-if="room")
    v-container(fluid grid-list-md text-xs-center)
      v-layout(row wrap)
        v-flex(d-flex xs12 sm12 md12)
          v-toolbar(dense)
            v-toolbar-title {{ room.room_name }}
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

import Desk from '@/components/room/Desk.vue'
import Status from '@/components/room/Status.vue'
import Settings from '@/components/room/Settings.vue'

import { ROOMS_MOCK } from '@/api/mock'
import { Room } from '@/model'
import { compile, compileLocal, Plugin, PluginConfig } from '@/logic/plugin/component'

// =================
//  Example Plugins
// =================
import Counter, { CounterServer } from '@/logic/plugin/counter'
import YoutubePlayer, { YoutubePlayerServer } from '@/logic/plugin/youtubePlayer'
import Chat, { ChatServer } from '@/logic/plugin/chat'
import { PluginConfig, PluginConfig } from '../logic/plugin/component';

@Component<RoomView>({
  components: { Desk, Status, Settings },
  sockets: {
    'room/enter' (data: { room: Room }) {
      this.responseEnterRoom(data)
    },
    'room/exit' (data: {}) {
      this.responseExitRoom()
    },
    'plugin/info' (plugin: Plugin) {
      // Repair data from server
      // << VBtn
      plugin.addons = Counter.addons
      const config: PluginConfig = {
        room_id: this.roomId,
        name: 'counter',
        plugin_name: 'counter',
        enabled: true,
      }

      this.addPlugin(config, plugin)
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
      const config: PluginConfig = {
        room_id: this.roomId,
        plugin_id: 'counter',
        name: 'counter',
        enabled: true,
      }
      const plugin = {
        template: Counter.template,
        events: ['plus'],
        addons: Counter.addons,
        record: { count: 0 },
      }
      this.addPlugin(config, plugin)
    } else {
      this.$socket.emit('plugin/info', { room_id: this.room.id })
    }
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

  private addPlugin (config: PluginConfig, plugin?: Plugin) {
    if (!plugin) {
      // counter
      if (config.name === 'counter') {
        this.room!!.plugins.push({
          component: compileLocal({
            template: Counter.template,
            addons: Counter.addons,
            server: new CounterServer(),
          }),
          config,
        })
      } else if (config.name === 'chat') {
        // this.room!!.plugins.push({
        //   component: compileLocal({ ...Chat, server: new ChatServer() }),
        //   config
        // })
      } else {
        console.warn(`[Room] plugin ${config.name} not found`)
      }
    } else {
      console.log(plugin)
      this.room!!.plugins.push({
        component: compile({ ...plugin!! }, config),
        config,
      })
    }
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
