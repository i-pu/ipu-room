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

import { compile, compileLocal, Plugin } from '@/logic/plugin/component'
// import YoutubePlugin from '@/logic/plugin/youtubePlayer'
import { CounterServer, counter } from '@/logic/plugin/counter'
import Chat, { ChatServer } from '@/logic/plugin/chat'

@Component<RoomView>({
  components: { Desk, Status, Settings },
  sockets: {
    'room/enter' (data: { room: Room }) {
      this.responseEnterRoom(data)
    },
    'plugin/add' (data: Plugin) {
      this.addPlugin({ name: 'counter', enabled: true }, data)
    }
  },
})
export default class RoomView extends Vue {
  private room: Room | null = null

  private get roomId () {
    return this.$route.params.roomId
  }

  private mounted () {
    this.requestEnterRoom({ room_id: this.roomId })
  }

  private requestEnterRoom (data: { room_id: string }) {
    if (this.$store.getters.localOnly) {
      this.responseEnterRoom({ room: ROOMS_MOCK[0] })
    } else {
      this.$socket.emit('room/enter', { room_id: this.roomId })
    }
  }

  private responseEnterRoom (data: { room: Room }) {
    this.room = data.room
    this.room.plugins = []
    this.addPlugin({ name: 'counter', enabled: true }, {
      template: counter.template,
      events: { plus: {} },
      addons: counter.addons,
      record: { count: 0 }
    })
  }

  private exitRoom () {
    this.$router.push('/lobby')
  }

  private addPlugin (
    config: { name: string, enabled: boolean }, 
    plugin?: Plugin
  ) {
    if (!plugin) {
      // counter
      if (config.name === 'Counter') {
        this.room!!.plugins.push({
          component: compileLocal({ 
            template: counter.template,
            addons: counter.addons,
            server: new CounterServer()
          }),
          config
        })
      } else if (config.name === 'Chat') {
        // this.room!!.plugins.push({
        //   component: compileLocal({ ...Chat, server: new ChatServer() }),
        //   config
        // })
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
