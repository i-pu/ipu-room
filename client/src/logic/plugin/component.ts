import Vue, { Component } from 'vue'

export type Plugin = { 
  template: string, 
  events: Record<string, any>, 
  record: Record<string, any>, 
  addons: Record<string, Component> 
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
  
    const hooks: Record<string, (vm: any, ...args: any) => void> = {}
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
          console.log(`[${this.pluginName}] callback from server`)
          for (const [k, _] of Object.entries(this.$data)) {
            this.$set(this, k, data[k])
          }
        }
      },
    })
}

export const compile = ({ template, events, record, addons } : Plugin): Component => {
  // 1. generate client class
  const client = new (class Client {
    [trigger: string]: (...args: any[]) => void
  })

  // 2. define methods
  const hooks: Record<string, (vm: any, ...args: any) => void> = {}
  Object.keys(events).map(event => {
    hooks[event] = function(...args: any[]): void {
      this.$socket.emit('plugin/trigger', {})
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
      'plugin/trigger' (data: Record<string, any>) {
        this.callbackFromServer(data)
      },
    },
    data: () => Object(client),
    mounted () {
      console.log(`[${this.pluginName}] activate`)
      this.$socket.emit('plugin/info', { name: this.pluginName })
    },
    methods: {
      ...hooks,
      // callback from server
      callbackFromServer (record: Record<string, any>) {
        console.log(`[${this.pluginName}] callback from server`)
        for (const [k, v] of Object.entries(record)) {
          this.$set(this, k, v)
        }
      }
    },
  })
}
