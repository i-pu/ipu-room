<template lang='pug'>
  div
    v-container(fluid grid-list-md text-xs-center)
      v-layout(row wrap)
        v-flex(d-flex xs12 sm12 md12)
          v-toolbar(dense)
            v-toolbar-title {{ room.room_name }} {{ room.plugins.join(',') }}
            v-spacer
            // v-btn(color="primary" @click="activate") プラグインを有効にする
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
import { Component, Mixins } from 'vue-mixin-decorator'

import Desk from '@/components/room/Desk.vue'
import Chat from '@/components/room/Chat.vue'
import Status from '@/components/room/Status.vue'
import Settings from '@/components/room/Settings.vue'

import { ROOMS_MOCK } from '@/api/mock'
import { Room } from '@/model'
import PluginApi from '@/api/plugin'

@Component({
  components: { Desk, Chat, Status, Settings }
})
export default class RoomView extends Mixins<PluginApi>(PluginApi) {
  room: Room = ROOMS_MOCK[0]

  mounted () {
    this.onEnterRoom()
    console.log(this.$route.params.roomId)
  }

  onEnterRoom () {
    this.$socket.emit('room/enter', {
      user_id: this.$socket.id,
      room_id: this.$route.params.roomId
    })
  }

  exitRoom () {
    this.$router.push('/lobby/1234')
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
