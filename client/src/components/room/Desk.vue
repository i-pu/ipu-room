
<template lang="pug">
  #desk
    v-btn(color="info" :disabled="pluginLoaded" @click="onEnterRoomTest") ACTIVATE
    // v-btn(color="primary" @click="trigger") トリガー

    div(v-html="pluginHtml")
</template>

<script>
// test in local
class Plugin {
  constructor () {
    this.count = 0
  }

  plus (data) {
    this.count += parseInt(data)
    return { changed: 'count' }
  }
}

export default {
  name: 'Desk',
  props: {
    room: Object
  },
  data () {
    return {
      testInLocal: true,
      plugin: null,
      pluginHtml: '',
      pluginElements: [],
      pluginLoaded: false
    }
  },
  computed: {
    eventElements () {
      return this.pluginElements.filter(element => element.type === 'event')
    },
    viewElements () {
      return this.pluginElements.filter(element => element.type === 'view')
    }
  },
  sockets: {
    // from server
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
    // test methods in local
    trigger ({ event, args }) {
      // invoke plugin function
      const { changed } = this.plugin[event](args)
      // reflact changes
      this.pluginElements.filter(element => element.type === 'view' && element.bind === changed).forEach(element => {
        this.updateElement(element)
      })
    },
    attachEvent (element) {
      document.getElementById(element.id).addEventListener('click', () => {
        console.log(`event: ${element.event} fired`)
        const payload = {
          event: element.event,
          plugin_id: 'counter',
          room_id: this.room.room_id,
          args: [1]
        }
        if (this.testInLocal) {
          this.trigger(payload)
        } else {
          this.$socket.emit('plugin/trigger', payload)
        }
      })
    },
    updateElement (element) {
      const target = document.getElementById(element.id)
      const [all, variable] = element.template.match(/\{\{(.*)\}\}/)
      target.innerText = element.template.replace(all, this.plugin[variable])
    },
    onEnterRoomTest () {
      const html = `
        <p id="_1"></p>
        <button id="_2"> add </button>
      `
      const elements = [
        { id: '_1', type: 'view', bind: 'count', template: '{{count}}' },
        { id: '_2', type: 'event', event: 'plus' }
      ]
      this.activatePlugin({ html, elements })
    },

    activatePlugin ({ html, elements }) {
      this.pluginHtml = html
      this.pluginElements = elements
      this.plugin = new Plugin()

      this.$nextTick(() => {
        // register event
        this.eventElements.forEach(element => {
          this.attachEvent(element)
        })
        // render view elements
        this.viewElements.forEach(element => {
          this.updateElement(element)
        })
        this.pluginLoaded = true
      })
    }
  },
}
</script>