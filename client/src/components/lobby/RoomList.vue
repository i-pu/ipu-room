<template lang='pug'>
  div
    v-container(fluid grid-list-md)
      v-layout(row wrap)
        v-flex(
          v-for="room in rooms" :key="room.room_id"
          d-flex xs12 sm6 md3
        )
          v-card
            v-img(:src="room.thumbnail_url" height="200px")
            v-card-title
              h3.headline {{ room.room_name }}
            v-card-text
              template(v-for="member, i in room.members")
                v-tooltip.mr-2(top :key="i")
                  template(v-slot:activator="{ on }")
                    v-avatar(v-on="on")
                      img(:src="member.avatar_url")
                  span {{ member.name }}
            v-card-actions
              v-btn(color="info" @click="onClickJoin") 入室
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
      // this.$socket.emit('enter_room', { room_name: this.roomNameInput })
      this.$router.push('/room')
    }
  }
}
</script>