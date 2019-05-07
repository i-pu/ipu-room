<template lang='pug'>
  div(v-if="room")
    v-container(fluid grid-list-md text-xs-center)
      v-layout(row wrap)
        v-flex(d-flex xs12 sm12 md12)
          v-toolbar(dense)
            v-toolbar-title {{ room.room_name }}
            v-spacer
            settings(:room="room" @add-plugin="addPlugin")
            v-btn(color="error" @click="exitRoom") 退出

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
import { CounterServer, counter } from '@/logic/plugin/counter'
// import YoutubePlugin from '@/logic/plugin/youtubePlayer'
// import Chat, { ChatServer } from '@/logic/plugin/chat'

@Component<RoomView>({
  components: { Desk, Status, Settings },
  sockets: {
    'room/enter' (data: { room: Room }) {
      this.responseEnterRoom(data)
    },
    'plugin/info' (data: Plugin) {
      // << VBtn
      data.addons = counter.addons
      this.addPlugin({ name: 'counter', enabled: true }, data)
    }
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
    this.room = data.room
    if (this.$store.getters.localOnly) {
      this.addPlugin({ name: 'counter', enabled: true }, {
        template: counter.template,
        events: { plus: {} },
        addons: counter.addons,
        record: { count: 0 }
      })
    } else {
      this.$emit('plugin/info', { room_id: this.room.id })
    }
  }

  private exitRoom () {
    this.$router.push('/lobby')
  }

  private addPlugin (config: PluginConfig, plugin?: Plugin) {
    if (!plugin) {
      // counter
      if (config.name === 'counter') {
        this.room!!.plugins.push({
          component: compileLocal({ 
            template: counter.template,
            addons: counter.addons,
            server: new CounterServer()
          }),
          config
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
      this.room!!.plugins.push({
        component: compile({ ...plugin!! }),
        config
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
