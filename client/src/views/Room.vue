<template lang='pug'>
  div
    v-container(fluid grid-list-md text-xs-center v-if="room")
      v-layout(row wrap)
        v-flex(d-flex xs12 sm12 md12)
          v-toolbar(dense)
            v-toolbar-title {{ room.room_name }} {{ room.plugins.join(',') }}
            v-spacer
            settings
            v-btn(color="error" @click="exitRoom") 退出
        v-flex(d-flex xs12 sm12 md9)
          // v-responsive(:aspect-ratio="16/9")
          v-card(white)
            desk#desk(:room="room")
        v-flex(d-flex xs12 sm12 md3)
          v-card(white)
            chat#chat
        v-flex(d-flex xs12 sm12 md12)
          v-card(white)
            status#status(:members="room.members")
</template>

<script lang="ts">
import Vue from 'vue'
import Component from 'vue-class-component'

import Desk from '@/components/room/Desk.vue'
import Chat from '@/components/room/Chat.vue'
import Status from '@/components/room/Status.vue'
import Settings from '@/components/room/Settings.vue'

import { ROOMS_MOCK } from '@/api/mock'
import { Room } from '@/model'

@Component<RoomView>({
  components: { Desk, Chat, Status, Settings },
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
