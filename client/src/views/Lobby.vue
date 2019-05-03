<template lang="pug">
  div
    v-toolbar(app)
      v-toolbar-title.headline.text-uppercase
        span.pr-3 ipu-room
      v-spacer
      plugin-create-form
      room-create-form(@create="responseCreateRoom")
    room-list(:rooms="rooms")
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
    visit () {
      this.responseVisit()
    },
    lobby (data) {
      this.responseLobby(data)
    },
  },
})

export default class Lobby extends Vue {
  public rooms: Room[] = []

  private get userId () {
    return this.$store.getters.userId
  }

  private mounted () {
    if (this.$store.getters.localOnly) {
      this.responseVisit()
    } else {
      this.$socket.emit('visit', {
        user_name: 'AAA',
      })
    }
  }

  private responseVisit () {
    if (this.$store.getters.localOnly) {
      this.responseLobby({ rooms: ROOMS_MOCK })
    } else {
      this.$socket.emit('lobby', {
        user_id: this.$store.getters.userId,
      })
    }
  }

  private responseLobby (data: { rooms: Room[] }) {
    this.rooms = data.rooms
  }

  private responseCreateRoom (data: { room: Room }) {
    this.rooms.push(data.room)
  }
}
</script>