import Vue, { Component } from 'vue'
import { Plugin, PluginProperties } from '@/model'

const fetchPreinstalledModules = async () => {
  // addons
  const modules: Record<string, Component> = {}

  // custom install
  // for (const [key, path] of Object.entries(addons)) {
  //   const [library, comp] = path.split('/')
  //   console.log([library, comp])
  //   if (comp) {
  //     const addon = await import(library)
  //     console.log(addon[comp])
  //     modules[key] = addon[comp]
  //   } else {
  //     const addon = await import(path)
  //     console.log(addon)
  //     modules[key] = addon
  //   }
  // }
  
  // vuetify
  const vuetifyAddons: Record<string, any> = await import('vuetify/lib')
  Object.entries(vuetifyAddons)
    .filter(([componentName, _]) => componentName[0] === 'V')
    .forEach(([componentName, component]) => {
      modules[componentName] = component
    })
  // vue-youtube
  modules['player'] = (await import('vue-youtube'))['Youtube']

  return modules
}

export const compile = async (
  plugin: Plugin, 
  properties: PluginProperties,
  isLocal: boolean = true
): Promise<Component> => {
  if (isLocal) {
    console.log(`[Compiler] ${properties.env.instanceId} try to compile with local mode`)
  } else {
    console.log(`[Compiler] ${properties.env.instanceId} try to compile`)
  }

  // addons
  const addonComponents: Record<string, Component> = await fetchPreinstalledModules()

  // const localInterface = (event: string) => {
  //   return function (this: Vue & { callbackFromServer: (functionName: string, args: any[]) => void, $env: PluginProperties['env'] }, _: Event): void {
  //     const args = [].slice.call(arguments).splice(1)
  //     console.log(`[local:${this.$env.instanceId}] Trigger ${event} with args [${args.join(',')}]`)
  //     this.callbackFromServer(event, args)
  //   }
  // }

  const hooks: Record<string, (...args: any) => void> = {}
  Object.entries(plugin.functions).forEach(([event, fn]) => {
    console.log(`[Compiler] ${properties.env.instanceId} register ${event}`)
    hooks[event] = function(this: Vue & { callbackFromServer: (functionName: string, args: any[]) => void, env: PluginProperties['env'] }, e: Event, ...args: any[]) {
      // emit to server
      // this.$socket.emit('plugin/trigger', {
      //   room_id: this.$env.room.id,
      //   instance_id: this.$env.instanceId,
      //   event_name: event,
      //   args,
      // })
      console.log(`${this.env.instanceId} ${event} clicked`)
      this.callbackFromServer(event, args)
    }
    hooks[`__callback__${event}`] = new Function(...fn) as (...args: any[]) => void
  })

  console.log(properties.env)

  console.log(`[Compiler] compiled ${properties.env.instanceId} successfully`)

  return Vue.extend({
    template: plugin.template,
    components: addonComponents,
    sockets: {
      // from server
      'plugin/trigger' ({ record }: { record: Record<string, any> }) {
        // @ts-ignore
        this.callbackFromServer(record)
      },
    },
    data (): {
      record: Record<string, any>,
      meta: PluginProperties['meta'],
      env: PluginProperties['env']
    } {
      return {
        record: Object.assign({}, properties.record),
        meta: properties.meta,
        env: properties.env,
      }
    },
    mounted () {
      console.log(`[${this.env.instanceId}] active`)
    },
    methods: {
      clone (this: Vue & { record: Record<string, any> }): { plugin: Plugin, properties: PluginProperties } {
        const currentRecord: Record<string, any> = Object.assign({}, this.record)
        return { 
          plugin,
          properties: {
          ...properties,
          record: currentRecord
          }
        }
      },
      '$log' (message: any) {
        console.log(message)
      },
      ...hooks,
      // callback from server
      callbackFromServer (this: Vue & Record<string, (...args: any[]) => void>, event: string, args: any[]) {
        console.log(`[plugin/trigger/${this.env.instanceId}] ${event}(${args})`)
        this[`__callback__${event}`](...args)
      },
    },
  })
}
