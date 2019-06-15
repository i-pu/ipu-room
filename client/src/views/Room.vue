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
import { Room, User } from '@/model'
import { boot } from '@/logic/loader'

import Desk from '@/components/room/Desk.vue'
import Status from '@/components/room/Status.vue'
import Settings from '@/components/room/Settings.vue'

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
    /**
    *  request room/enter event
    *  @event room/enter
    *  @param roomId: string
    */
    this.$socket.emit('room/enter', { roomId: this.roomId })
  }

  /**
  * Room
  */
  private async responseEnterRoom ({ room }: { room: Room }) {
    console.log(`[Room] entered`)
    this.room = room
    this.room.plugins = []

    for (const pluginPackage of this.room.pluginPackages) {
      const instance = await boot(pluginPackage, { room: this.room })
        .catch(error => {
          console.error(error)
        })
        .then(instance => {
          // push reactively
          this.$set(this.room!!, 'plugins', [...this.room!!.plugins, instance])
        })
    }
  }

  /**
  * Room
  */
  private requestExitRoom () {
    /**
    *  request room/exit event
    *  @event room/exit
    *  @param roomId: string
    */
    this.$socket.emit('room/exit', { roomId: this.roomId})
  }

  /**
  * Room
  */
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
