<template lang="pug">
  div
    // register(@register="register" @makeroom="makeRoom")

    v-container(fluid grid-list-md)
      v-layout(row wrap)
        v-flex(
          v-for="room in rooms"
          :key="room.roomId"
          d-flex
          xs12 sm6 md3
        )
          v-card
            v-img(:src="room.thumbnailUrl" height="200px")
            v-card-title(primary-title) {{ room.title }}
            v-card-actions
              v-btn(color="info") 入室

        // 新規作成
        v-flex(d-flex xs12 sm6 md3)
          v-card(color="green")
            v-card-title(primary-title) 新規作成
            v-card-actions
              v-btn(color="info") 作成

    v-btn(@click="$socket.emit('notice', 'a')") notice
    v-btn(@click="$socket.emit('bye', {})") bye
</template>

<script>
import Register from './../components/Register'

export default {
  name: 'Lobby',
  components: { Register },
  sockets: {
    connect () {
      console.log(`connected id: ${this.$socket.id}`)
    },
    reply (data) {
      console.log(data)
    }
  },
  data () {
    return {
      rooms: [{
        title: '雑談部屋',
        hostUserId: 'aaa',
        members: ['a', 'b', 'c'],
        roomId: 'room1',
        thumbnailUrl: 'https://cdn.vuetifyjs.com/images/cards/house.jpg'
      }],
      user: {}
    }
  },
  mounted () {
    // fetch('http://10.160.163.229/rooms')
    //   .then(response => response.json())
    //   .then(rooms => {
    //     console.log(rooms)
    //     this.rooms = rooms

    //     // E2E test
    //     // this.test()
    //   })
  },
  methods: {
    send () {
      this.$socket.emit('notice', {})
    },
    post(endpoint, object, callback) {
      return new Promise((resolve) => {
        fetch(`http://10.160.163.229/${endpoint}`, {
          body: JSON.stringify(object),
          method: 'post'
        })
        .then(res => res.json())
        .then(payload => {
          console.log(payload)
          if (callback) callback(payload)
          resolve(payload)
        })
        .catch(console.error)
      })
    },
    makeRoom () {
      return this.post('makeroom', { 
        userId: this.user.userId,
        nickName: this.user.nickName
      },
      room => {
        this.rooms.push(room)
      })
    },
    register (nickName) {
      return this.post('makeuser', {
        nickName: nickName
      },
      user => {
        this.user = user
      })
    },
    joinRoom (userId, roomId) {
      return this.post('joinroom', { 
          userId: userId,
          roomId: roomId
      })
    },

    async test () {
      console.log('A register')
      const A = await this.register('A')
      console.log('A make room')
      const room = await this.makeRoom()
      console.log('A join room')
      await this.joinRoom(A.userId, room.roomId)
      console.log('B register')
      const B = await this.register('B')
      console.log('B join room')
      const room_new = await this.joinRoom(B.userId, room.roomId)
      console.assert(room_new.members.length === 2, 'failed')
    }
  }
}
</script>