<template lang="pug">
  v-container(fluid grid-list-md text-xs-center)
    v-layout(row wrap)
      v-toolbar(app)
        v-toolbar-title.headline.text-uppercase
          span.pr-3 {{ userName }} さん
        v-spacer
        v-btn(color="blue white--text" @click="toMarket") ストアへ
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
            v-btn(color="info" @click="toRoom(room.id)") 入室
            v-btn(color="red white--text" @click="removeRoom(room.id)") 削除
</template>

<script lang="ts">
import { Room } from '@/model'
import RoomCreateForm from '@/components/lobby/RoomCreateForm.vue'
import { createComponent, SetupContext, ref, computed, onMounted } from '@vue/composition-api'
import store from '@/store'
import socket from '@/socket'
import router from '@/router'

const rooms = ref<Room[]>([])
const userId = computed<string>(() => store.getters.userId)
const userName = computed<string>(() => store.getters.userName)

const requestFetchRooms = () => {
  socket.emit('lobby', { userId: userId.value })
}

const responseLobby = (data: { rooms: Room[] }) => {
  rooms.value = data.rooms
}

socket.on('lobby', (data: { rooms: Room[] }) => {
  responseLobby(data)
})

socket.on('room/remove', () => {
  requestFetchRooms()
})

export default createComponent({
  components: { RoomCreateForm },
  setup () {
    const responseCreateRoom = (data: { room: Room }) => {
      rooms.value.push(data.room)
    }

    const removeRoom = (roomId: string) => {
      socket.emit('room/remove', { roomId })
    }

    const toMarket = () => {
      router.push('/market')
    }

    const toRoom = (roomId: string) => {
      router.push(`/room/${roomId}`)
    }

    onMounted(() => {
      requestFetchRooms()
    })

    return {
      rooms,
      userId,
      userName,
      requestFetchRooms,
      responseLobby,
      responseCreateRoom,
      removeRoom,
      toMarket,
      toRoom,
    }
  },
})
</script>
