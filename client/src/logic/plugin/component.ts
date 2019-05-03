import Vue, { VueConstructor } from 'vue'
import * as VuetifyComponents from 'vuetify/lib'

import { Counter } from '@/logic/plugin/counter'

export type PluginComponent = VueConstructor<Record<never, any> & Vue>

export class PPM {
  public pluginNames: string[] = [] 
  public plugins: Record<string, PluginComponent> = {}

  private async fetchPlugin (pluginName: string): Promise<PluginComponent> {
    const template = `
      <div>
          <h3> {{ count }} </h3>
          <v-btn @click="plus"> Add </v-btn>
      </div>
    `
    return new PluginManager(new Counter(), template).component()
  }

  public async installPlugins () {
    for (const pluginName of this.pluginNames) {
      this.plugins[pluginName] = await this.fetchPlugin(pluginName)
      console.log(`[ppm] ${pluginName} has been installed`)
    }
  }

  public installedPlugins (): string[] {
    return this.pluginNames
  }

  constructor (plugins: string[]) {
    this.pluginNames = plugins
  }
}

export class PluginManager {
  private static __getMethods (instance: any) {
    const proto = Object.getPrototypeOf (instance)
    const names = Object.getOwnPropertyNames (proto)
    return names.filter ((name) => typeof instance[name] === 'function' && name !== 'constructor')
  }
  private instance: any
  private template: string
  private methods: Record<string, Function> = {}

  constructor (plugin: any, template: string) {
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

  public component (): PluginComponent {
    const that = this

    // const res = Vue.compile(this.template)
    const addons: Record<string, any> = {}

    // dafault addons: Vuetify
    for (const [key, component] of Object.entries(VuetifyComponents)) {
      if (key[0] === 'V') {
        addons[key] = component
      }
    }

    return Vue.extend({
      template: this.template,
      components: addons,
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
