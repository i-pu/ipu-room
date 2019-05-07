import Vue, { Component } from 'vue'

// typeof plugin
export type Plugin = {
  // html template
  template: string,
  // trigger methods' name
  events: string[], 
  // variables in plugin
  record: Record<string, any>,
  // custom component that be used in
  addons: Record<string, Component> 
}

// typeof plugin config
export type PluginConfig = {
  // 
  room_id: string,
  // 
  plugin_id: string,
  // plugin name
  name: string,
  // plugin enabled
  enabled: boolean
}

export const compileLocal = ({
  template, addons, server
} : {
  template: string,
  addons: Record<string, Component>,
  server: any
}): Component => {
    // 1. generate client class
    const client = new (class Client {
      [trigger: string]: (...args: any[]) => void
    })
  
    // 2. define methods
    let methodNames = Object
      .getOwnPropertyNames(Object.getPrototypeOf(server))
      .filter ((name) => typeof server[name] === 'function' && name !== 'constructor')
  
    const hooks: Record<string, (...args: any[]) => void> = {}
    methodNames.map(method => {
      hooks[method] = function(...args: any[]): void {
        server[method](...args)
        const record = Object(server)
        this.callbackFromServer(record)
      }
    })
  
    // 3. define members
    for (const key of Object.keys(Object(server))) {
      client[key] = server[key]
    }
  
    // 4. create dynamic component
    return Vue.extend({
      template,
      components: addons,
      sockets: {
        // from server
        'plugin/trigger' (data: Record<string, any>) {
          // @ts-ignore
          this.callbackFromServer(data)
        },
      },
      data: () => Object(client),
      mounted () {
        console.log(`[${this.pluginName}] activate`)
      },
      methods: {
        ...hooks,
        // callback from server
        callbackFromServer (data: Record<string, any>) {
          // @ts-ignore
          console.log(`[${this.pluginName}] callback from server`)
          for (const [k, _] of Object.entries(this.$data)) {
            this.$set(this, k, data[k])
          }
        }
      },
    })
}

export const compile = ({ template, events, record, addons } : Plugin, config: PluginConfig): Component => {
  // 1. generate client class
  const client = new (class Client {
    [trigger: string]: (...args: any[]) => void
  })

  // 2. define methods
  const hooks: Record<string, (vm: any, ...args: any) => void> = {}
  events.map(event => {
    hooks[event] = function(eventObject: any, ...args: any[]): void {
      console.log(`[${config.name}] Trigger ${event} with args ${args.toString()}`)
      // @ts-ignore
      this.$socket.emit('plugin/trigger', {
        room_id: config.room_id,
        plugin_id: config.name,
        event_name: event,
        args: args
      })
    }
  })

  // 3. define members
  for (const [k, v] of Object.entries(record)) {
    client[k] = v
  }

  // 4. create dynamic component
  return Vue.extend({
    template,
    components: addons,
    sockets: {
      // from server
      'plugin/trigger' ({ record }: { record: Record<string, any> }) {
        console.log(`[${config.name}] Response ${Object.keys(record)}`)
        // @ts-ignore
        this.callbackFromServer(record)
      },
    },
    data (): {
      v: Record<string, any>
    } { 
      return {
        v: Object(client)
      }
    },
    mounted () {
      console.log(`[${config.name}] active`)
    },
    methods: {
      ...hooks,
      // callback from server
      callbackFromServer (record: Record<string, any>) {
        console.log(`[${config.name}] callback from server ${Object.keys(record)}`)
        for (const [k, v] of Object.entries(record)) {
          // @ts-ignore
          this.$set(this.v, k, v)
        }
      }
    },
  })
}
