<template lang='pug'>
  div
    v-container(fluid grid-list-md)
      v-layout(row wrap)
        v-flex(
          v-for="room in rooms" :key="room.roomId"
          d-flex xs12 sm6 md3
        )
          v-card
            v-img(:src="room.thumbnailUrl" height="200px")
            v-card-title(primary-title) {{ room.title }}
            v-card-actions
              v-btn(color="info" @click="onClickJoin") 入室

        // 新規作成
        v-flex(d-flex xs12 sm6 md3)
          v-card(color="light-green lighten-4")
            v-card-title(primary-title) 新規作成
            v-card-actions
              v-text-field(
                v-model="roomNameInput"
                label="部屋名"
              )
              v-btn(color="info" @click="onClickCreate") 作成
</template>

<script>
export default {
  name: '',
  props: {
    rooms: Array
  },
  data () {
    return {
      roomNameInput: ''
    }
  },
  methods: {
    onClickJoin () {
      this.$socket.emit('enter_room', { room_name: this.roomNameInput })
      this.roomNameInput = ''
    },
    onClickCreate () {
      this.$emit('create', { roomName: this.roomNameInput })
      this.roomNameInput = ''
    }
  }
}
</script>