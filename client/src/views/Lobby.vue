<template lang="pug">
  div
    v-toolbar(app)
      v-toolbar-title.headline.text-uppercase
        span.pr-3 ipu {{ userId }}
        // span.pr-3 {{ name }} さん
      v-spacer
      plugin-create-form
      room-create-form
    room-list(:rooms="rooms" :userId="userId")
</template>

<script>
import RoomList from '@/components/lobby/RoomList'
import RoomCreateForm from '@/components/lobby/RoomCreateForm'
import PluginCreateForm from '@/components/PluginCreateForm'

import { ROOMS_MOCK } from '@/api/mock'

export default {
  name: 'Lobby',
  components: { RoomList, RoomCreateForm, PluginCreateForm },
  data () {
    return {
      rooms: ROOMS_MOCK,
      userId: '',
      name: 'ななし'
    }
  },
  sockets: {
    'room/create' (data) {
      console.log(data)
      this.rooms.push(data.room)
    },
    lobby (data) {
      console.log(data)
      // this.rooms = data.rooms
    },
    visit (data) {
      console.log(data)
      this.userId = data.user_id
      this.$socket.emit('lobby', {
        user_id: data.user_id
      })
    }
  },
  mounted() {
    console.log(this.$route.params.userId)
    this.$socket.emit('visit', {
      user_name: 'AAA'
    })
  }
}
</script>