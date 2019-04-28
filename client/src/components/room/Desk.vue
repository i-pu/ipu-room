
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
    // test methods in local
    trigger ({ event, args }) {
      const { changed } = this.plugin[event](args)
      this.pluginElements.filter(element => element.type === 'view' && element.bind === changed).forEach(element => {
        const target = document.getElementById(element.id)
        target.innerText = this.replacer(element)
      })
    },

    replacer (element) {
      const [all, variable] = element.template.match(/\{\{(.*)\}\}/)
      return element.template.replace(all, this.plugin[variable])
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
      this.pluginElements = elements

      const _attachEvent = (eventElement) => {
        document.getElementById(eventElement.id).addEventListener('click', () => {
          console.log(`event: ${eventElement.event} fired`)
          const payload = {
            event: eventElement.event,
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
      }

      this.plugin = new Plugin()
      this.pluginHtml = html
      this.$nextTick(() => {
        // register event
        elements.filter(element => element.type === 'event').forEach(element => {
          _attachEvent(element)
        })
        // render view elements
        elements.filter(element => element.type === 'view').forEach(element => {
          const target = document.getElementById(element.id)
          target.innerText = this.replacer(element)
        })
      })
      this.pluginLoaded = true
    }
  },
}
</script>