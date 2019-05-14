import Vue, { Component } from 'vue'
import { Plugin, PluginConfig } from '@/model'

export const compileLocal = async (
  instance: Plugin,
  meta: PluginConfig,
  server: any
): Promise<Component> => {
  // addons
  const addonComponents: Record<string, Component> = {}
  // module import
  await import('vuetify/lib').then((addons: Object) => {
    Object.entries(addons)
      .filter(([key, _]) => key[0] == 'V')
      .forEach(([key, component]) => {
        addonComponents[key] = component
      })
  })

  for (const [key, path] of Object.entries(instance.addons)) {
    import(path).then(addon => {
      console.log({ key, addon })
      addonComponents[key] = addon.Youtube
    })
  }
  // single import
  // for (const [key, path] of Object.entries(plugin.addons)) {
  //   import(path).then((addon: Component) => {
  //     console.log(addon)
  //     addonComponents[key] = addon
  //   })
  // }

  // create hooks
  const methodNames = Object
    .getOwnPropertyNames(Object.getPrototypeOf(server))
    .filter ((name) => typeof server[name] === 'function' && name !== 'constructor')
  const hooks: Record<string, (...args: any[]) => void> = {}
  methodNames.map((method) => {
    hooks[method] = function (...args: any[]): void {
      // invoke function
      server[method](...args)
      const record = Object(server)
      this.callbackFromServer(record)
    }
  })

  // create dynamic component
  return Vue.extend({
    template: instance.template,
    components: addonComponents,
    data () {
      return {
        // all plugin vars is under v.[...]
        v: Object(instance.record),
        meta: meta,
        instance: instance,
      }
    },
    mounted () {
      console.log(`[${instance.id}] activate`)
    },
    methods: {
      ...hooks,
      // callback from server
      callbackFromServer (data: Record<string, any>) {
        console.log(`[${instance.id}] callback from server`)
        for (const [k, v] of Object.entries(data)) {
          // @ts-ignore
          this.$set(this.v, k, v)
        }
      },
    },
  })
}

export const compile = async (instance: Plugin, meta: PluginConfig): Promise<Component> => {
  console.log(`[Compiler] ${instance.id} try to compile`)

  // TODO : addon by dynamic imports
  // addons
  const addonComponents: Record<string, Component> = {}
  // module import
  await import('vuetify/lib').then((addons: Object) => {
    Object.entries(addons)
      .filter(([key, _]) => key[0] == 'V')
      .forEach(([key, component]) => {
        addonComponents[key] = component
      })
  })
  // for (const [key, path] of Object.entries(instance.addons)) {
  //   import(path).then(addon => {
  //     addonComponents[key] = addon
  //   })
  // }

  const hooks: Record<string, (vm: any, ...args: any) => void> = {}
  instance.events.map((event) => {
    hooks[event] = function (_: Event): void {
      const args = [].slice.call(arguments)
      console.log(`[${instance.id}] Trigger ${event} with args [${args.join(',')}]`)
      // @ts-ignore
      this.$socket.emit('plugin/trigger', {
        room_id: instance.room_id,
        instance_id: instance.id,
        event_name: event,
        args: args,
      })
    }
  })

  return Vue.extend({
    template: instance.template,
    components: addonComponents,
    sockets: {
      // from server
      'plugin/trigger' ({ vs }: { vs: Record<string, any> }) {
        // @ts-ignore
        this.callbackFromServer(vs)
      },
    },
    data (): {
      v: Record<string, any>,
      meta: PluginConfig,
      instance: Plugin
    } {
      return {
        v: Object(instance.record),
        meta: meta,
        instance: instance,
      }
    },
    mounted () {
      console.log(`[${instance.id}] active`)
    },
    methods: {
      ...hooks,
      // callback from server
      callbackFromServer (vs: Record<string, any>) {
        console.log(`[${instance.id}] callback from server ${Object.keys(vs)}`)
        for (const [k, v] of Object.entries(vs)) {
          // @ts-ignore
          this.$set(this.v, k, v)
        }
      },
    },
  })
}
