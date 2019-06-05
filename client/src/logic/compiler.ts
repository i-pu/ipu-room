import Vue, { Component } from 'vue'
import { Plugin, PluginProperties } from '@/model'

// @ts-ignore
import VueP5 from 'vue-p5'

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
  // @ts-ignore
  modules.player = (await import('vue-youtube')).Youtube

  modules['VueP5'] = VueP5

  return modules
}

export const compile = async (
  plugin: Plugin,
  properties: PluginProperties,
): Promise<Component> => {
  // console.log(`[Compiler] ${properties.env.instanceId} try to compile`)

  // addons
  const addonComponents: Record<string, Component> = await fetchPreinstalledModules()

  const hooks: Record<string, (...args: any) => void> = {}
  for (const [event, fn] of Object.entries(plugin.functions)) {
    if (event[0] === '_') {
      // direct
      // console.log(`[Compiler] ${properties.env.instanceId} directry ${event}`)
      hooks[event] = new Function(...fn) as (...args: any[]) => void
    } else {
      // console.log(`[Compiler] ${properties.env.instanceId} register hooks ${event}`)
      hooks[event] = function (this: Vue & {
        callbackFromServer: (functionName: string, args: any[]) => void,
        env: PluginProperties['env'],
      },
      ...args: any[]) {
        // emit to server
        this.$socket.emit('plugin/trigger', {
          room_id: this.env.room.id,
          instance_id: this.env.instanceId,
          event_name: event,
          args: args,
        })
        console.log(`${this.env.instanceId} ${event}`)
        // his.callbackFromServer(event, args)
      }

      hooks[`__callback__${event}`] = new Function(...fn) as (...args: any[]) => void
    }
  }

  console.log(`[Compiler] compiled ${properties.env.instanceId} successfully`)

  return Vue.extend({
    template: plugin.template,
    components: addonComponents,
    sockets: {
      // from server
      [`plugin/${plugin.instanceId}/sync`] (this: Vue, { record }: { record: Record<string, any> }) {
        // @ts-ignore
        this.record = record
        console.log('record synced')
      },
      [`plugin/${plugin.instanceId}/clone`] (this: Vue, { room_id, instance_id, from }: { room_id: string, instance_id: string, from: string }) {
        console.log(`[Plugin] came clone request from ${from}`)
        this.$socket.emit('plugin/clone', {
          // @ts-ignore
          room_id: this.env.room.id,
          // @ts-ignore
          instance_id: this.env.instanceId,
          // @ts-ignore
          record: this.$cloneRecord(),
          from: from
        })
      },
      [`plugin/${plugin.instanceId}/trigger`] (payload: { event: string, args: [] }) {
        // @ts-ignore
        this.callbackFromServer(payload)
      },
    },
    data (): {
      record: Record<string, any>,
      meta: PluginProperties['meta'],
      env: PluginProperties['env'],
    } {
      return {
        record: Object.assign({}, properties.record),
        meta: properties.meta,
        env: properties.env,
      }
    },

    mounted () {
      console.log(`[${this.env.instanceId}] active`)

      // if someone exist, sync records
      if (1 < this.env.room.members.length) {
        this.$socket.emit('plugin/sync', {
          room_id: this.env.room.id,
          instance_id: this.env.instanceId
        })
        console.log(`[Plugin] send sync request`)
      } else {
        console.log('[Plugin] initialized record')
      }
    },
    methods: {
      $cloneRecord (this: Vue & { record: Record<string, any> }): Record<string, any> {
        return Object.assign({}, this.record)
      },
      $log (message: any) {
        console.log(message)
      },
      $send (event: string, ...args: any[]) {
        this.$socket.emit('plugin/trigger', {
          room_id: this.env.room.id,
          instance_id: this.env.instanceId,
          event_name: event,
          args: args,
        })
        console.log(`${this.env.instanceId} ${event}`)
      },
      ...hooks,
      // callback from server
      callbackFromServer (this: Vue 
        & Record<string, (...args: any[]) => void> 
        & { env: { instanceId: string } }
        , { event, args }: { event: string, args: any[] }
      ) {
        // console.log(`[plugin/trigger/${this.env.instanceId}] ${event}(${args})`)
        this[`__callback__${event}`](...args)
      },
    }
  })
}
