import Vue, { VueConstructor } from 'vue'
import { SamplePlugin } from '@/logic/plugin/sample'

export class PluginManager {
  private instance?: SamplePlugin

  public component (
    template: string
  ): VueConstructor<Record<never, any> & Vue> {
    this.instance = new SamplePlugin()
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
