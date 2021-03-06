import Vue, { Component } from 'vue'
import { Plugin, PluginProperties, PluginComponent, PluginFunctions, User, Room } from '@/model'

import _, { LoDashStatic } from 'lodash'
// @ts-ignore
import VueP5 from 'vue-p5'
// @ts-ignore
import VuePlayingCard from 'vue-playing-card'
// TODO: global install -> local install
Vue.use(VuePlayingCard)

/**
* [TODO] Import dynamically additional components are used in a plugin.
*/
const installModules = async () => {
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
    .filter(([componentName, __]) => componentName[0] === 'V')
    .forEach(([componentName, component]) => {
      modules[componentName] = component
    })
  // vue-youtube
  // @ts-ignore
  modules.player = (await import('vue-youtube')).Youtube

  modules.VueP5 = VueP5

  // modules.VuePlayingCard = VuePlayingCard

  return modules
}

/**
* Compiles a plugin-package, and converts Vue component.
*
* ### Hook type
* - (without prefix, ex: add): send me, recieve all members in room.
* - (with '_' prefix ex: _add): call the function directly.
* - (with 'bc_' ex: bc_add): broadcast to room, recieve all members excepts me in room.
*
* @param plugin hoge
* @param properties hoge
*/
export const compile = async (
  plugin: Plugin,
  properties: PluginProperties,
): Promise<any> => {
  try {
    // addons
    const addonComponents: Record<string, Component> = await installModules()

    const hooks: Record<string, (...args: any) => void> = {}
    console.log(Object.keys(plugin.functions))
    for (const [event, fn] of Object.entries<
      ((...args: any[]) => void)
    >(plugin.functions as PluginFunctions)) {
      // console.log(` - ${event} : ${fn.toString()}`)
      /**
       *  functions that its name starts with 'event/*', '_*' are special functions.
       *
       *  # Events
       *  - event/room : fire when room updated.
       *  - event/member :
       */
      if (event.startsWith('_') || event.startsWith('event/')) {
        hooks[event] = fn
      } else {
        hooks[event] = function (this: PluginComponent, ...args: any[]) {
          // emit to server
          console.log(this.env.instanceId)
          this.$socket.emit('plugin/trigger', {
            roomId: this.env.room.id,
            instanceId: this.env.instanceId,
            data: {
              event,
              args,
            },
            options: {},
          })
        }
        hooks[`__callback__${event}`] = fn
      }
    }

    console.log(`[Compiler] compiled ${properties.env.instanceId} successfully`)

    // @ts-ignore
    return Vue.extend({
      template: plugin.template,
      components: addonComponents,
      // @ts-ignore
      sockets: {
        [`plugin/${plugin.instanceId}/sync`] (this: PluginComponent, { record }: { record: Record<string, any> }) {
          // @ts-ignore
          this.record = record
          console.log('record synced')
        },
        [`plugin/${plugin.instanceId}/clone`] ({ roomId, instanceId, from }: {
          roomId: string, instanceId: string, from: string,
        }) {
          console.log(`[Plugin] came clone request from ${from}`)

          // @ts-ignore
          this.$socket.emit('plugin/clone', {
            // @ts-ignore
            roomId: this.env.room.id,
            // @ts-ignore
            instanceId: this.env.instanceId,
            // @ts-ignore
            record: this.$cloneRecord(),
            from,
          })
        },
        [`plugin/${plugin.instanceId}/trigger`] (payload: { data: { event: string, args: [] } }) {
          // @ts-ignore
          this.callbackFromServer(payload)
        },
      },
      // watch: {
      //   record: {
      //     handler (v) {
      //       console.log(Object.assign({}, v))
      //     },
      //     deep: true
      //   }
      // },
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
            roomId: this.env.room.id,
            instanceId: this.env.instanceId,
          })
          console.log(`[Plugin] send sync request`)
        } else {
          console.log('[Plugin] initialized record')
        }
      },
      computed: {
        /**
         *  support Lodash
         */
        _ (): LoDashStatic {
          return _
        },
        /**
          *  return [User] of mine.
        */
        $me (): User {
          // @ts-ignore
          return this.env.room.members.find((m) => m.id === this.$socket.id)
        },
        /**
         *   return [User[]] members in room
         */
        $members (): User[] {
          return this.env.room.members
        },
      },
      methods: {
        $cloneRecord (): Record<string, any> {
          // @ts-ignore
          return Object.assign({}, this.record)
        },
        $send (event: string, options?: { to: string } | { broadcast: boolean }, ...args: any[]) {
        // @ts-ignore
          this.$socket.emit('plugin/trigger', {
            // @ts-ignore
            roomId: this.env.room.id,
            // @ts-ignore
            instanceId: this.env.instanceId,
            data: {
              event,
              args,
            },
            options,
          })
          // @ts-ignore
          console.log(`${this.env.instanceId} ${event}`)
        },
        ...hooks,
        // callback from server
        callbackFromServer ({ data }: { data: { event: string, args: any[] } },
        ) {
          const { event, args } = data
          // console.log(`[plugin/trigger/${this.env.instanceId}] ${event}(${args})`)
          // @ts-ignore
          this[`__callback__${event}`](...args)
        },
      },
    })
  } catch (error) {
    throw error
  }
}
