import Vue, { Component } from 'vue'
import { Plugin, PluginProperties, PluginMeta } from '@/model'

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
  meta: PluginMeta, 
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

  const socketInterface = (event: string) => {
    return function (this: Vue & { $env: PluginProperties['env'] }, _: Event): void {
      const args = [].slice.call(arguments)
      console.log(`[${this.$env.instanceId}] Trigger ${event} with args [${args.join(',')}]`)
      this.$socket.emit('plugin/trigger', {
        room_id: this.$env.room.id,
        instance_id: this.$env.instanceId,
        event_name: event,
        args,
      })
    }
  }

  const localInterface = (event: string) => {
    return function (this: Vue & { callbackFromServer: (functionName: string, args: any[]) => void, $env: PluginProperties['env'] }, _: Event): void {
      const args = [].slice.call(arguments).splice(1)
      console.log(`[local:${this.$env.instanceId}] Trigger ${event} with args [${args.join(',')}]`)
      this.callbackFromServer(event, args)
    }
  }

  const hooks: Record<string, (vm: any, ...args: any) => void> = {}
  Object.keys(plugin.functions).map((event: string) => {
    if (isLocal) {
      hooks[event] = localInterface(event)
    } else {
      hooks[event] = socketInterface(event)
    }
  })

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
      $meta: PluginMeta,
      $env: PluginProperties['env']
    } {
      return {
        record: Object.assign({}, properties.record),
        $meta: Object.assign({}, properties.meta),
        $env: Object.assign({}, properties.env)
      }
    },
    mounted () {
      console.log(`[${this.$env.instanceId}] active`)
    },
    methods: {
      '$log' (message: any) {
        console.log(message)
      },
      ...hooks,
      // callback from server
      callbackFromServer (this: Vue & Record<string, (...args: any[]) => void>, event: string, passArgs: any[]) {
        console.log(`[plugin/trigger/${this.$env.instanceId}] ${event}(${passArgs})`)
        this[event](...passArgs)
      },
    },
  })
}
