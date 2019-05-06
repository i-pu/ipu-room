<template lang='pug'>
  div(v-if="room")
    v-container(fluid grid-list-md text-xs-center)
      v-layout(row wrap)
        v-flex(d-flex xs12 sm12 md12)
          v-toolbar(dense)
            v-toolbar-title {{ room.room_name }}
            v-spacer
            settings(:room="room")
            v-btn(color="error" @click="exitRoom") 退出

    // v-responsive(:aspect-ratio="16/9")
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

import { Plugin, PluginComponent } from '@/logic/plugin/component'
import YoutubePlugin from '@/logic/plugin/youtubePlayer'
import Counter from '@/logic/plugin/counter'
import Chat from '@/logic/plugin/chat'

@Component<RoomView>({
  components: { Desk, Status, Settings },
  sockets: {
    'room/enter' (data: { room: Room }) {
      this.responseEnterRoom(data)
    },
    // unused
    'activate' (roomId: string, plugins: string[]) {
      this.$socket.emit('plugin/activate', {
        plugins, // id
        room_id: roomId,
      })
    },
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
      this.$socket.emit('room/enter', {
        user_id: this.$store.getters.userId,
        room_id: this.roomId,
      })
    }
  }

  private responseEnterRoom (data: { room: Room }) {
    this.room = data.room
    this.room.plugins = []
    // counter
    this.room.plugins.push({
      instance: Counter.instance,
      component: Plugin.compile(Counter)
    })
    // chat
    this.room.plugins.push({
      instance: Chat.instance,
      component: Plugin.compile(Chat)
    })

  }

  private exitRoom () {
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
