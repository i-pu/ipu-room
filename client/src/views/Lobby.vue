<template lang="pug">
  div
    v-toolbar(app)
      v-toolbar-title.headline.text-uppercase
        span へやつくるやつ
        
      v-spacer

      v-btn(
        color="error"
        href="#"
        target="_blank"
      ) 退出

    room-list(:rooms="rooms")
</template>

<script>
import RoomList from '@/components/lobby/RoomList'

import { ROOMS_MOCK } from '@/api/mock'

export default {
  name: 'Lobby',
  components: { RoomList },
  data () {
    return {
      rooms: ROOMS_MOCK
    }
  }
}
</script>