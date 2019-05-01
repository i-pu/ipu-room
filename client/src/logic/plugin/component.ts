import Vue, { VueConstructor } from 'vue'
import { Element, Event, View } from './index'
import { SamplePlugin } from '@/logic/plugin/sample'

export class PluginManager {
  private instance?: SamplePlugin
  private elements: Element[] = []

  get eventElements (): Event[] {
    return this.elements
      .filter(((element) => element.type === 'event') as (element: Element) => element is Event)
  }

  get viewElements (): View[] {
    return this.elements
      .filter(((element) => element.type === 'view') as (element: Element) => element is View)
  }

  public component (
    template: string,
    elements: Element[],
  ): VueConstructor<Record<never, any> & Vue> {
    this.instance = new SamplePlugin()
    this.elements = elements

    const triggers = []
    this.eventElements.forEach((event) => {
      // TODO
    })
    return Vue.extend({
      template,
      sockets: {
        // from server
        'plugin/trigger' (data) {
          console.log(data)
        },
      },
      data () {
        return {
          count: 0,
        }
      },
      methods: {
        plus () {
          console.log(`event: plus fired`)
          this.count++
          const payload = {
            room_id: '1234',
            plugin_id: 'counter',
            event: 'plus',
            args: [1],
          }
          // this.$socket.emit('plugin/trigger', payload)
        },
      },
    })
  }
}
