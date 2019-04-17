<template lang="pug">
  div
    v-toolbar(app)
      v-toolbar-title.headline.text-uppercase
        span.pr-3 へやつくるやつ
        span.pr-3 {{ name }} さん
        
      v-spacer

      room-create-form

    room-list(:rooms="rooms")
</template>

<script>
import RoomList from '@/components/lobby/RoomList'
import RoomCreateForm from '@/components/lobby/RoomCreateForm'

import { ROOMS_MOCK } from '@/api/mock'

export default {
  name: 'Lobby',
  components: { RoomList, RoomCreateForm },
  data () {
    return {
      rooms: ROOMS_MOCK,
      name: 'ななし'
    }
  },
  sockets: {
    room (rooms) {
      this.rooms = rooms
    }
  },
  mounted() {
    console.log(this.$route.params.userId)

    this.$emit('room')
  }
}
</script>