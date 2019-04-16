<template lang="pug">
  div
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