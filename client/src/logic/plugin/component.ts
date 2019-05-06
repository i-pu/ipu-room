import Vue, { VueConstructor } from 'vue'
import { BasePlugin } from '../baseplugin'
export type PluginComponent = VueConstructor<Record<never, any> & Vue>

export const compile = <Plugin extends BasePlugin> (
  { instance, template, addons }: { instance: Plugin, template: string, addons: Record<string, any> },
): PluginComponent => {
  const methods: Record<string, (...args: any[]) => any> = {}
  const methodNames = Object
    .getOwnPropertyNames(Object.getPrototypeOf(instance))
    .filter ((name) => typeof instance[name] === 'function' && name !== 'constructor')
  const hook = (method: string) => ((...args: any[]): any => {
    console.log(`event: ${method} fired`)
    const res = instance[method](...args)
    // const payload = {
    //   room_id: '1234',
    //   plugin_id: 'counter',
    //   event: method,
    //   args,
    // }
    // this.$socket.emit('plugin/trigger', payload)
    return res
  })

  console.log('[Plugin compiler] register hooks')
  methodNames.forEach((method) => { methods[method] = hook(method) })

  console.log('[Plugin compiler] componentize')
  return Vue.extend({
    template,
    components: addons,
    // sockets: {
    //   // from server
    //   'plugin/trigger' (data) {
    //     console.log(data)
    //   },
    // },
    data: () => Object(instance),
    methods,
  })
}
