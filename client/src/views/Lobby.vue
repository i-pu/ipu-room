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

<script lang="ts">
import Vue from 'vue'
import Component from 'vue-class-component'

import { Room } from '@/model'

import RoomList from '@/components/lobby/RoomList.vue'
import RoomCreateForm from '@/components/lobby/RoomCreateForm.vue'
import PluginCreateForm from '@/components/PluginCreateForm.vue'

import { ROOMS_MOCK } from '@/api/mock'

@Component<Lobby>({
  components: { RoomList, RoomCreateForm, PluginCreateForm },
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
  }
})

export default class Lobby extends Vue {
  rooms: Room[] = ROOMS_MOCK
  userId: string = ''
  name: string = 'ななし'

  mounted () {
    console.log(this.$route.params.userId)
    this.$socket.emit('visit', {
      user_name: 'AAA'
    })
  }
}
</script>