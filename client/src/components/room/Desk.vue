
<template lang="pug">
  #desk
    v-btn(color="info" @click="onEnterRoom") EnterRoom
    // v-btn(color="primary" @click="trigger") トリガー

    div(v-html="pluginHtml")
</template>

<script lang="ts">
import Vue from 'vue'
import Component from 'vue-class-component'
import { Prop } from 'vue-property-decorator'

import { Room } from '@/model'
import { ROOMS_MOCK } from '@/api/mock'

@Component<Desk>({
  sockets: {
    'plugin/trigger' ({ html }) {
      this.pluginHtml = html
    },
    'room/enter' (data) {
      this.loadPlugin(data)
    }
  }
})

export default class Desk extends Vue {
  constructor () {
    super()
    this.room = ROOMS_MOCK[0]
  }

  @Prop()
  room: Room

  private pluginHtml: string = ''

  mounted() {}

  loadPlugin ({ html }: { html: string }) {
    console.log(html)
    this.pluginHtml = html
    const events = [
      { id: 'a', name: 'plus' }
    ]
    this.$nextTick(() => {
      for (let emitEvent of events) {
        const target = document.getElementById(emitEvent.id)
        if (!target) continue
        target.addEventListener('click', () => {
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
}
</script>