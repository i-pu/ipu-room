<template lang="pug">
  v-layout(row wrap)
    v-flex(d-flex xs12 sm12 md6
      v-for="{ component, properties } in plugins"
    )
      v-card(white fluid)
        component(:is="component" :ref="properties.env.instanceId")
</template>

<script lang="ts">
import { createComponent, ref, computed, onMounted, watch, reactive } from '@vue/composition-api'
import { Room, PluginInstance, PluginPackage, User } from '@/model'
import { boot } from '@/logic/loader'

import _ from 'lodash'

export default createComponent({
  props: {
    room: Object as () => Room,
  },
  setup (props: { room: Room }) {
    const plugins = ref<PluginInstance[]>([])
    const room = reactive(props.room)

    const pluginIds = computed(() => plugins.value.map((instance) => instance.properties.env.instanceId))

    const bootPlugins = async () => {
      for (const pluginPackage of props.room.pluginPackages) {
        try {
          const instance = await boot(pluginPackage, { room: props.room })
          // push reactively
          this.plugins.push(instance)
        } catch (error) {
          console.error(error)
        }
      }
    }

    onMounted(() => { bootPlugins() })

    watch(() => {
      console.log('[Desk] event event/room')
      invokePluginsFunction('event/room', room)
    })

    watch(() => room.members, (newMembers: User[], oldMembers: User[]) => {
      if (newMembers.length === oldMembers.length) { return }
      const isJoin: boolean = newMembers.length > oldMembers.length
      const diffs: User[] = _.differenceBy(
        isJoin ? newMembers : oldMembers,
        isJoin ? oldMembers : newMembers,
        'id',
      )
      const member: User = diffs[0]

      if (isJoin) {
        this.invokePluginsFunction('join/member', member)
      } else {
        this.invokePluginsFunction('leave/member', member)
      }
    })

    const invokePluginsFunction = (event: string, ...args: any[]) => {
      // pluginIds.value.forEach(id => invokePluginFunction(id, event, ...args))
    }

    // const invokePluginFunction = (instanceId: string, event: string, ...args: any[]) => {
    //   const instance = getInstance(instanceId) as Record<string, any>

    //   if (instance && instance[event] && typeof instance[event] === 'function') {
    //     instance[event](...args)
    //   }
    // }

    return {
      plugins,
    }
  },
})
</script>