import Vue, { VueConstructor } from 'vue'
import { BasePlugin } from '../baseplugin'
export type PluginComponent = VueConstructor<Record<never, any> & Vue>

export const compile = (
  { server, template, addons }: { server: any, template: string, addons: Record<string, any> },
): PluginComponent => {
  const sockets: Record<string, (...args: any[]) => any> = {}

  // 1. generate client class
  const client = new (class Client {
    [trigger: string]: (...args: any[]) => void
  })

  // 2. define methods
  const methodNames = Object
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

  console.log(`[Plugin compiler] componentize ${client.pluginName}`)

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
