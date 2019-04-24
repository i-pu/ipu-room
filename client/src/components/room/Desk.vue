
<template lang="pug">
  #desk
    v-btn(@click="emitTest") 発動
    div(v-html="customHTML")
</template>

<script>
const pluginHander = {
  methods: {
    fire () {
      console.log('out')
    }
  }
}

export default {
  name: 'Desk',
  mixins: [ pluginHander ],
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

    const handlers = [
      { event: 'connect', script: ['console.log(this)'] },
      { event: 'my_event', script: ['data', 'console.log(data)'] },
      { event: 'f', script: ['data', 'console.log(data)'] }
    ]

    for (const hander of handlers) {
      this.$socket.on(this.socketPrefix + hander.event, Function(hander.script).bind(this))
    }
  },
  methods: {
    emitTest () {
      this.pluginActionHander('my_event', { hoge: 1 })
    },
    pluginActionHander (event, ...args) {
      this.$socket.emit(this.socketPrefix + event, args)
    }
  },
}
</script>