<template lang="pug">
  v-container(fluid grid-list-md text-xs-center)
    v-layout(row wrap)
      v-toolbar(app)
        v-toolbar-title.headline.text-uppercase
          span.pr-3 {{ $store.getters.userName }} さん
        v-spacer
        v-btn(color="blue" @click="$router.push('/market')") ストアへ
        room-create-form(@add="responseCreateRoom")
        
      v-flex(
        v-for="room in rooms" :key="room.id"
        d-flex xs12 sm6 md3
      )
        v-cardc
          v-card-title
            h3.headline {{ room.name }} [{{ room.members.length }} / 6]
          v-card-text
            template(v-for="member, i in room.members")
              v-tooltip.mr-2(top :key="i")
                template(v-slot:activator="{ on }")
                  v-avatar(v-on="on" size="60")
                    img(:src="member.avatarUrl")
                span {{ member.name }}
          v-card-actions
            v-btn(color="info" @click="$router.push(`/room/${room.id}`)") 入室
</template>

<script lang="ts">
import Vue from 'vue'
import Component from 'vue-class-component'
import { Room } from '@/model'
import RoomCreateForm from '@/components/lobby/RoomCreateForm.vue'

@Component<Lobby>({
  components: { RoomCreateForm },
  sockets: {
    lobby (data: { rooms: Room[] }) {
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
    /**
    *  request lobby event
    *  @event lobby
    *  @param userId: string
    */
    this.$socket.emit('lobby', {
      userId: this.$store.getters.userId,
    })
  }

  private responseLobby (data: { rooms: Room[] }) {
    this.rooms = data.rooms
  }

  private responseCreateRoom (data: { room: Room }) {
    this.rooms.push(data.room)
  }
}
</script>