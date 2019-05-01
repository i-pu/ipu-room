
<template lang="pug">
  #desk
    v-btn(color="info" :disabled="pluginLoaded" @click="onEnterRoomTest") ACTIVATE
    // v-btn(color="primary" @click="trigger") トリガー

    div(v-html="pluginHtml")
</template>

<script lang="ts">
import Vue from 'vue'
import Component from 'vue-class-component'
import { Prop } from 'vue-property-decorator'

import { Room } from '@/model'
import { SamplePlugin } from '@/logic/plugin/sample'
import { ROOMS_MOCK } from '@/api/mock'

interface PluginElement { id: string, type: string }
interface PluginViewelement extends PluginElement { id: string, type: 'view', bind: string, template: string }
interface PluginEventElement extends PluginElement { id: string, type: 'event', event: string }

@Component<Desk>({
  sockets: {
    // from server
    'plugin/trigger' ({ html }) {
      this.pluginHtml = html
    },
    'room/enter' (data) {
      this.loadPlugin(data)
    },
  },
})
export default class Desk extends Vue {
  @Prop() public room!: Room

  private testInLocal: boolean = true
  private plugin: SamplePlugin | null = null
  private pluginHtml: string = ''
  private pluginElements: PluginElement[] = []
  private pluginLoaded: boolean = false

  get eventElements (): PluginEventElement[] {
    return this.pluginElements
      .filter(((element) => element.type === 'event') as (element: PluginElement) => element is PluginEventElement)
  }

  get viewElements (): PluginViewelement[] {
    return this.pluginElements
      .filter(((element) => element.type === 'view') as (element: PluginElement) => element is PluginViewelement)
  }

  public loadPlugin ({ html }: { html: string }) {
    console.log(html)
    this.pluginHtml = html
    const events = [
      { id: 'a', name: 'plus' },
    ]
    this.$nextTick(() => {
      for (const emitEvent of events) {
        const target = document.getElementById(emitEvent.id)
        if (!target) { continue }
        target.addEventListener('click', () => {
          console.log(`event: ${emitEvent.name} fired`)
          this.$socket.emit('plugin/trigger', {
            event: emitEvent.name,
            plugin_id: 'counter',
            room_id: this.room.room_id,
            args: [1],
          })
        })
      }
    })
  }

  // test methods in local
  public trigger ({ event, args }: { event: string, args: any[] }) {
    if (!this.plugin) {
      return
    }
    // invoke plugin function
    const { changed } = (this.plugin as any)[event](args)
    // reflact changes
    this.viewElements.filter((e) => e.bind === changed).forEach((element) => {
      this.updateElement(element)
    })
  }

  public attachEvent (element: PluginEventElement) {
    const target = document.getElementById(element.id)
    if (!target) {
      return
    }
    target.addEventListener('click', () => {
      console.log(`event: ${element.event} fired`)
      const payload = {
        event: element.event,
        plugin_id: 'counter',
        room_id: this.room.room_id,
        args: [1],
      }
      if (this.testInLocal) {
        this.trigger(payload)
      } else {
        this.$socket.emit('plugin/trigger', payload)
      }
    })
  }

  public updateElement (element: PluginViewelement) {
    const target = document.getElementById(element.id)
    if (!target) {
      return
    }
    const [all, variable] = element.template.match(/\{\{(.*)\}\}/)!!
    target.innerText = element.template.replace(all, (this.plugin as any)[variable])
  }

  public onEnterRoomTest () {
    const html = `
      <p id="_1"></p>
      <button id="_2"> add </button>
    `
    const elements = [
      { id: '_1', type: 'view', bind: 'count', template: '{{count}}' },
      { id: '_2', type: 'event', event: 'plus' },
    ]
    this.activatePlugin({ html, elements })
  }

  public activatePlugin ({ html, elements }: { html: string, elements: PluginElement[] }) {
    this.pluginHtml = html
    this.pluginElements = elements
    this.plugin = new SamplePlugin()

    this.$nextTick(() => {
      // register event
      this.eventElements.forEach((element) => {
        this.attachEvent(element)
      })
      // render view elements
      this.viewElements.forEach((element) => {
        this.updateElement(element)
      })
      this.pluginLoaded = true
    })
  }
}
</script>