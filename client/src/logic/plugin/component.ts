import Vue, { VueConstructor } from 'vue'
import { SamplePlugin } from '@/logic/plugin/sample'

type Component = VueConstructor<Record<never, any> & Vue>

export class PluginManager {

  private static __getMethods (instance: any) {
    const proto = Object.getPrototypeOf (instance)
    const names = Object.getOwnPropertyNames (proto)
    return names.filter ((name) => typeof instance[name] === 'function' && name !== 'constructor')
  }
  private instance: any
  private template: string
  private properties: Record<string, any> = {}
  private methods: Record<string, Function> = {}

  constructor (plugin: SamplePlugin, template: string) {
    this.instance = plugin
    this.template = template

    PluginManager.__getMethods(plugin)
      .forEach((method) => {
        this.methods[method] = ((...args: any[]) => {
          console.log(`event: ${method} fired`)
          this.instance[method](...args)
          const payload = {
            room_id: '1234',
            plugin_id: 'counter',
            event: method,
            args,
          }
          // this.$socket.emit('plugin/trigger', payload)
        })
      })
  }

  public component (): Component {
    const that = this
    console.log(that.properties)

    return Vue.extend({
      template: this.template,
      sockets: {
        // from server
        'plugin/trigger' (data) {
          console.log(data)
        },
      },
      data () {
        return Object(that.instance)
      },
      methods: this.methods,
    })
  }
}
