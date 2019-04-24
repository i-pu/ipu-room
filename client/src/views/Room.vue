<template lang='pug'>
  div
    v-container(fluid grid-list-md text-xs-center)
      v-layout(row wrap)
        v-flex(d-flex xs12 sm12 md12)
          v-toolbar(dense)
            v-toolbar-title {{ room.room_name }} {{ room.plugins.join(',') }}
            v-spacer
            v-btn(color="success") 設定
            v-btn(color="error") 退出
        v-flex(d-flex xs12 sm12 md9)
          // v-responsive(:aspect-ratio="16/9")
          v-card(white)
            desk#desk
        v-flex(d-flex xs12 sm12 md3)
          v-card(white)
            chat#chat
        v-flex(d-flex xs12 sm12 md12)
          v-card(white)
            status#status(:members="room.members")
</template>

<script>
import Desk from '@/components/room/Desk'
import Chat from '@/components/room/Chat'
import Status from '@/components/room/Status'

import { ROOMS_MOCK } from '@/api/mock'

export default {
  name: 'Room',
  components: { Desk, Chat, Status },
  data () {
    return {
      room: ROOMS_MOCK[0]
    }
  },
  methods: { }
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
