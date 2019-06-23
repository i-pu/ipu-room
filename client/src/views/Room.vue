<template lang="pug">
  v-container(fluid grid-list-md text-xs-center)
    v-layout(row wrap v-if="room")
      v-flex(d-flex xs12 sm12 md12)
        v-toolbar(dense)
          v-toolbar-title {{ room.name }}
          v-spacer
          settings(:room="room")
          v-btn(color="error" @click="requestExitRoom") 退出

      desk#desk(:room="room")
</template>

<script lang="ts">
import Vue, { ComponentOptions, VueConstructor } from 'vue'
import Component from 'vue-class-component'
import { Room, User } from '@/model'

import Desk from '@/components/room/Desk.vue'
import Settings from '@/components/room/Settings.vue'
import { Watch } from 'vue-property-decorator';

@Component<RoomView>({
  components: { Desk, Settings },
  sockets: {
    'room/enter' ({ room }: { room: Room }) {
      console.log(`[Room] entered`)
      this.room = room
    },
    'room/update' ({ room }: { room: Room }) {
      if (!this.room) { return }
      this.room.members = room.members
    },
    'room/exit' (data: {}) {
      this.$router.push('/lobby')
    },
  },
})
export default class RoomView extends Vue {
  private room: Room | null = null

  private get roomId (): string {
    return this.$route.params.roomId
  }

  private mounted () {
    console.log(`[Room] request enter`)
    this.$socket.emit('room/enter', { roomId: this.roomId })
  }

  private requestExitRoom () {
    this.$socket.emit('room/exit', { roomId: this.roomId })
  }
}
</script>

