import { createComponent, ref, provide, inject, Ref, onMounted, computed } from '@vue/composition-api'

import { Plugin, PluginProperties, PluginFunctions, User, PluginMeta, PluginEnv } from '@/model'

import _, { LoDashStatic } from 'lodash'
import socket from '@/socket'
import store from '@/store'

type Component = ReturnType<typeof createComponent>

interface EventContext { event: string, args: any[] }

const SocketInjectorSymbol = Symbol()

const fromEntries = <V>(iterable: Iterable<[string, V]>): Record<string, V> =>
  [...iterable].reduce((obj, [k, v]) => ({ [k]: v, ...obj }), {})

const objectMap = <T, R>(obj: Record<string, T>, transformer: (v: T) => R): Record<string, R> => {
  return fromEntries(Object.entries(obj).map(([k, v]) => [k, transformer(v)]))
}

interface SocketInjector {
  record: Ref<Record<string, any>>
  pluginSyncFunction: (res: { record: Record<string, any> }) => void
  pluginCloneFunction: ({ roomId, instanceId, from }: {
    roomId: string
    instanceId: string
    from: string,
  }) => void
}

const socketInjector = {
  setup () {
    // plugin data
    const record = ref<Record<string, any>>({})
    const pluginSyncFunction = (res: { record: Record<string, any> }) => {
      record.value = res.record
    }
    const pluginCloneFunction = ({ roomId, instanceId, from }: {
      roomId: string, instanceId: string, from: string,
    }) => {
      console.log(`[Plugin] came clone request from ${from}`)

      socket.emit('plugin/clone', {
        roomId,
        instanceId,
        record: Object.assign({}, record.value),
        from,
      })
    }

    provide(SocketInjectorSymbol, {
      record,
      pluginSyncFunction,
      pluginCloneFunction,
    })
  },
}

export const compile = async (
  plugin: Plugin,
  properties: PluginProperties,
): Promise<Component> => {
  const components = {}
  const setup: Component['setup'] = () => {
    const meta = ref<PluginMeta>(properties.meta)
    const env = ref<PluginEnv>(properties.env)
    const events = objectMap(plugin.functions as PluginFunctions, (fn) =>
      ref<(...args: any[]) => void>((...args: any[]) => {
        fn(...args)
        // extend event
        console.log(plugin.instanceId)
        socket.emit('plugin/trigger', {
          roomId: env.value.room.id,
          instanceId: env.value.instanceId,
          data: { event, args },
          options: {},
        })
      }),
    )

    const {
      record, pluginSyncFunction, pluginCloneFunction,
    } = inject<SocketInjector>(SocketInjectorSymbol) as SocketInjector

    socket.on(`plugin/${env.value.instanceId}/sync`, pluginSyncFunction)
    socket.on(`plugin/${env.value.instanceId}/clone`, pluginCloneFunction)
    socket.on(`plugin/${env.value.instanceId}/trigger`, (res: { data: EventContext }) => {
      events[res.data.event].value(res.data.args)
    })

    // Api
    const $me = computed(() => {
      return env.value.room.members.find((m) => m.id === store.getters.userId)
    })
    const $members = computed(() => {
      return env.value.room.members
    })
    const $send = (event: string, options?: { to: string } | { broadcast: boolean }, ...args: any[]) => {
      socket.emit('plugin/trigger', {
        roomId: env.value.room.id,
        // @ts-ignore
        instanceId: env.value.instanceId,
        data: { event, args },
        options,
      })
      console.log(`${env.value.instanceId} ${event}`)
    }
    const $_ = ref<LoDashStatic>(_)

    onMounted(() => {
      console.log(`[${env.value.instanceId}] active`)

      // if someone exist, sync records
      if (1 < env.value.room.members.length) {
        socket.emit('plugin/sync', {
          roomId: env.value.room.id,
          instanceId: env.value.instanceId,
        })
        console.log(`[Plugin] send sync request`)
      } else {
        console.log('[Plugin] initialized record')
      }
    })

    return {
      ...events,
      record,
      meta,
      env,
      $me,
      $members,
      $send,
      $_,
    }
  }

  return createComponent({
    template: plugin.template,
    components,
    setup,
  })
}
