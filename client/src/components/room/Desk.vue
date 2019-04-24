
<template lang="pug">
  #desk
    v-btn(@click="fire") 発動
    div(v-html="customHTML")
</template>

<script>

export default {
  name: 'Desk',
  props: {
    room: Object
  },
  data () {
    return {
      customHTML: '<p>Hello, Plugin</p>',
      socketPrefix: this.room.room_id + this.room.plugins[0]
    }
  },
  mounted() {
    console.log(this.socketPrefix)

    this.sockets.subscribe(this.socketPrefix + 'my_event', (data) => {
      console.log(data)
    })

    this.sockets.subscribe(this.socketPrefix + 'f', (data) => {
      console.log(data)
    })
  },
  methods: {
    fire () {
      // this.$socket.emit(this.socketPrefix + 'my_event', {
      //   hoge: 1
      // })

      this.$socket.emit(this.socketPrefix + 'f', {
        aaa: 'hoge'
      })
    }
  },
}
</script>