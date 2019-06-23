<template lang="pug">
  v-layout(row wrap)
    v-flex(d-flex xs12 sm12 md9
      v-for="{ component, properties } in plugins"
    )
      v-card(white fluid)
        component(:is="component" :ref="properties.env.instanceId")
</template>

<script lang="ts">
import Vue from 'vue'
import Component from 'vue-class-component'
import { Prop, Watch } from 'vue-property-decorator'
import { Room, PluginInstance, PluginPackage, User } from '@/model'
import { boot } from '@/logic/loader'

@Component
export default class Desk extends Vue {
  @Prop() private room!: Room
  private plugins: PluginInstance[] = []

  private get pluginIds (): string[] {
    return this.plugins.map(instance => instance.properties.env.instanceId)
  }

  private getInstance (instanceId: string): Vue | null {
    const components = this.$refs[instanceId]
    if (components && (components as Vue[]).length === 1) {
      return (components as Vue[])[0]
    } else {
      return null
    }
  }

  @Watch('room', { deep: true })
  private onUpdateRoom (room: Room) {
    console.log('[Desk] event event/room')
    this.invokePluginsFunction('event/room', room)
  }

  @Watch('room.members')
  private onUpdateMembers (members: User[]) {
    console.log('[Desk] event event/members')
    this.invokePluginsFunction('event/members', members)
  }

  mounted() {
    this.bootPlugins()
  }

  public async bootPlugins () {
    for (const pluginPackage of this.room.pluginPackages) {
      try {
        const instance = await boot(pluginPackage, { room: this.room })
        // push reactively
        this.plugins.push(instance)
      } catch (error) {
        console.error(error)
      }
    }
  }

  private invokePluginsFunction (event: string, ...args: any[]) {
    this.pluginIds.forEach(id => this.invokePluginFunction(id, event, ...args))
  }

  private invokePluginFunction (instanceId: string, event: string, ...args: any[]) {
    const instance = this.getInstance(instanceId) as Record<string, any>
    if (instance && instance[event] && typeof instance[event] === 'function') {
      instance[event](...args)
    } else {
      console.warn(`[Desk] ${instanceId} ${event} did not successed.`)
    }
  }
}
</script>