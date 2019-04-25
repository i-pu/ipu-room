
<template lang="pug">
  #desk
    v-btn(color="info" @click="onEnterRoom") EnterRoom
    // v-btn(color="primary" @click="trigger") トリガー

    div(v-html="pluginHtml")
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
    }
  },
  sockets: {
    'plugin/trigger' ({ html }) {
      this.pluginHtml = html
    },
    'room/enter' (data) {
      this.loadPlugin(data)
    }
  },
  mounted() {
  },
  methods: {
    loadPlugin ({ html }) {
      console.log(html)
      this.pluginHtml = html
      const events = [
        { id: 'a', name: 'plus' }
      ]
      this.$nextTick(() => {
        for (let emitEvent of events) {
          document.getElementById(emitEvent.id).addEventListener('click', () => {
            console.log(`event: ${emitEvent.name} fired`)
            this.$socket.emit('plugin/trigger', {
              event: emitEvent.name,
              plugin_id: 'counter',
              room_id: this.room.room_id,
              args: [1]
            })
          })
        }
      })
    }
  },
}
</script>