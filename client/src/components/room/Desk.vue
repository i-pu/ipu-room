
<template lang="pug">
  #desk
    v-btn(@click="emitTest") 発動
    div(v-html="pluginHtml" ref="plugin")
</template>

<script>
export default {
  name: 'Desk',
  props: {
    room: Object
  },
  data () {
    return {
      pluginHtml: '',
      socketPrefix: this.room.room_id + this.room.plugins[0]
    }
  },
  mounted() {
    console.log(this.socketPrefix)

    // test
    const pluginHtml = `<button event="plus('hoge')">1</button>`
    const compiledHtml = `<button id="_plugin_btn_1_">1</button>`
    this.pluginHtml = compiledHtml
    // emit events from client
    const emitEvents = [ 
      { id: '_plugin_btn_1_', name: 'plus', args: ['hoge'] }
    ]
    // on events from server
    const onEvents = [
      { name: 'f', action: ['data', 'console.log(data.aaa)'] }
    ]

    this.$nextTick(() => {
      for (let emitEvent of emitEvents) {
        document.getElementById(emitEvent.id).addEventListener('click', () => {
          // this.pluginActionHander(emitEvent.name, emitEvent.args)
          console.log(`event: ${emitEvent.name} args: ${emitEvent.args}`)
        })
      }

      for (let onEvent of onEvents) {
        this.$socket.on(this.socketPrefix + onEvent.name, Function(onEvent.action).bind(this))
      }
    })
  },
  methods: {
    emitTest () {
      this.pluginActionHander('my_event', { hoge: 1 })
    },
    pluginActionHander (event, args) {
      this.$socket.emit(this.socketPrefix + event, args)
    }
  },
}
</script>