<template lang='pug'>
  div
    v-container(fluid grid-list-md text-xs-center)
      v-layout(row wrap)
        v-flex(d-flex xs12 sm12 md12)
          v-toolbar(dense)
            v-toolbar-title {{ room.room_name }} {{ room.plugins.join(',') }}
            v-spacer
            v-btn(color="primary" @click="activate") プラグインを有効にする
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

<script>
import Desk from '@/components/room/Desk'
import Chat from '@/components/room/Chat'
import Status from '@/components/room/Status'
import Settings from '@/components/room/Settings'

import { ROOMS_MOCK } from '@/api/mock'
import PluginApi from '@/api/plugin'

export default {
  name: 'Room',
  mixins: [ PluginApi ],
  components: { Desk, Chat, Status, Settings },
  data () {
    return {
      room: ROOMS_MOCK[0]
    }
  },
  methods: {
    exitRoom () {
      this.$router.push('/lobby/1234')
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
