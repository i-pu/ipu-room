<template lang="pug">
  v-container(fluid grid-list-md text-xs-center)
    v-layout(row wrap)
      v-toolbar(app)
        v-toolbar-title.headline.text-uppercase
          span.pr-3 {{ $store.getters.userName }} さん
        v-spacer
        v-btn(color="blue white--text" @click="$router.push('/market')") ストアへ
        room-create-form(@add="responseCreateRoom")

      v-flex(d-flex xs12 sm12 md12)
        v-btn(@click="requestFetchRooms") 更新
        
      v-flex(
        v-for="room in rooms" :key="room.id"
        d-flex xs12 sm6 md3
      )
        v-card
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
            v-btn(color="red white--text" @click="removeRoom(room.id)") 削除
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
      console.log(data)
      this.responseLobby(data)
    },
    'room/remove' () {
      this.requestFetchRooms()
    }
  },
})
export default class Lobby extends Vue {
  public rooms: Room[] = []

  private get userId () {
    return this.$store.getters.userId
  }

  private mounted () {
    this.requestFetchRooms()
  }

  private requestFetchRooms() {
    this.$socket.emit('lobby', {
      userId: this.$store.getters.userId,
    })
  }

  private responseLobby (data: { rooms: Room[] }) {
    this.rooms = data.rooms
  }

  private responseCreateRoom (data: { room: Room }) {
    console.log(data)
    this.rooms.push(data.room)
  }

  private removeRoom(roomId: string) {
    this.$socket.emit('room/remove', { roomId })
  }
}
</script>