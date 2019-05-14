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
      addonComponents[key] = addon
    })
  }

  // 1. generate client class
  // tslint:disable-next-line
  const client = new (class Client {
    [trigger: string]: (...args: any[]) => void
  })

  // 2. define methods
  const hooks: Record<string, (vm: any, ...args: any) => void> = {}
  instance.events.map((event) => {
    hooks[event] = function (eventObject: any, ...args: any[]): void {
      console.log(`[${instance.id}] Trigger ${event} with args ${args.toString()}`)
      // @ts-ignore
      this.$socket.emit('plugin/trigger', {
        room_id: meta.room_id,
        plugin_id: meta.name,
        event_name: event,
        args: args
      })
    }
  })

  // 3. define members
  for (const [k, v] of Object.entries(instance.record)) {
    client[k] = v
  }

  // 4. create dynamic component
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
    } {
      return {
        v: Object(client),
        meta: meta,
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
