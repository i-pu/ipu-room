<template lang="pug">
  div
    register(@register="register" @makeroom="makeRoom")

    b-container
      b-row
        b-col(v-for="room in rooms" :key="room.roomId" class="col-4 mb-4")
          b-card(:title="room.hostUserId.toString()")
            h4(slot="header") {{ room.roomId }}
            p {{ room.members }}
            b-button(@click="joinRoom(user.userId, room.roomId)" variant="primary") 入室

    b-button(@click="send") 送信

    b-button(@click="$socket.emit('bye')") Bye
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
      rooms: [],
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