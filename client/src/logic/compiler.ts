import Vue, { Component } from 'vue'
import { Plugin, PluginConfig, PluginMeta } from '@/model'

const fetchPreinstalledModules = async (addons: Record<string, string>) => {
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
  instance: Plugin, 
  meta: PluginMeta, 
  config: PluginConfig,
  server?: any
): Promise<Component> => {
  const isLocalOnly = !!server

  if (isLocalOnly) {
    console.log(`[Compiler] ${config.id} try to compile with local mode`)
  } else {
    console.log(`[Compiler] ${config.id} try to compile`)
  }

  // addons
  const addonComponents: Record<string, Component> = await fetchPreinstalledModules(instance.addons)

  const socketInterface = (event: string) => {
    return function (this: Vue, _: Event): void {
      const args = [].slice.call(arguments)
      console.log(`[${config.id}] Trigger ${event} with args [${args.join(',')}]`)
      this.$socket.emit('plugin/trigger', {
        room_id: config.room_id,
        instance_id: config.id,
        event_name: event,
        args,
      })
    }
  }

  const localInterface = (event: string) => {
    return function (this: Vue & { callbackFromServer: (record: Record<string, any>) => void }, _: Event): void {
      const args = [].slice.call(arguments).splice(1)
      console.log(`[local:${config.id}] Trigger ${event} with args [${args.join(',')}]`)
      // invoke function
      server[event](...args)
      const record = Object(server)
      this.callbackFromServer(record)
    }
  }

  const hooks: Record<string, (vm: any, ...args: any) => void> = {}
  instance.events.map((event: string) => {
    if (isLocalOnly) {
      hooks[event] = localInterface(event)
    } else {
      hooks[event] = socketInterface(event)
    }
  })

  return Vue.extend({
    template: instance.template,
    components: addonComponents,
    sockets: {
      // from server
      'plugin/trigger' ({ record }: { record: Record<string, any> }) {
        // @ts-ignore
        this.callbackFromServer(record)
      },
    },
    data (): {
      v: Record<string, any>
    } {
      return {
        v: Object.assign({}, instance.record)
      }
    },
    mounted () {
      console.log(`[${config.id}] active`)
    },
    methods: {
      '$log' (message: any) {
        console.log(message)
      },
      ...hooks,
      // callback from server
      callbackFromServer (vs: Record<string, any>) {
        console.log(`[${config.id}] callback from server ${Object.keys(vs)}`)
        for (const [k, v] of Object.entries(vs)) {
          // @ts-ignore
          this.$set(this.v, k, v)
        }
      },
    },
  })
}
