<template lang="pug">
  v-container(fluid grid-list-md text-xs-center)
    v-layout(row wrap v-if="room")
      v-flex(d-flex xs12 sm12 md12)
        v-toolbar(dense)
          v-toolbar-title {{ room.name }}
          v-spacer
          settings(:room="room")
          v-btn(color="error" @click="requestExitRoom") 退出

      desk#desk(:room="room")
</template>

<script lang="ts">
import { createComponent, ref, computed, SetupContext, onMounted } from '@vue/composition-api'
import { Room, User } from '@/model'
import socket from '@/socket'
import router from '@/router'

import Desk from '@/components/room/Desk.vue'
import Settings from '@/components/room/Settings.vue'

const room = ref<Room | null>(null)

socket.on('room/enter', (res: { room: Room }) => {
  console.log(`[Room] entered`)
  room.value = res.room
})

socket.on('room/update', (res: { room: Room }) => {
  if (!room.value) { return }
  room.value.members = res.room.members
})

socket.on('room/exit', () => {
  router.push('/lobby')
})

export default createComponent({
  components: { Desk, Settings },
  setup (props: {}, { root }: SetupContext) {
    const roomId = computed(() => root.$route.params.roomId)

    onMounted(() => {
      console.log(`[Room] request enter`)
      socket.emit('room/enter', { roomId: roomId.value })
    })

    const requestExitRoom = () => {
      socket.emit('room/exit', { roomId: roomId.value })
    }

    return {
      roomId,
      requestExitRoom,
      room,
    }
  },
})
</script>

