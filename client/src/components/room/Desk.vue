<template lang="pug">
  v-layout(row wrap)
    v-flex(d-flex xs12 sm12 md6
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

import _ from 'lodash'

@Component
export default class Desk extends Vue {

  private get pluginIds (): string[] {
    return this.plugins.map((instance) => instance.properties.env.instanceId)
  }
  @Prop() private room!: Room
  private plugins: PluginInstance[] = []

  public mounted () {
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
  private onUpdateMember (newMembers: User[], oldMembers: User[]) {
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
  }

  private invokePluginsFunction (event: string, ...args: any[]) {
    this.pluginIds.forEach((id) => this.invokePluginFunction(id, event, ...args))
  }

  private invokePluginFunction (instanceId: string, event: string, ...args: any[]) {
    const instance = this.getInstance(instanceId) as Record<string, any>

    if (instance && instance[event] && typeof instance[event] === 'function') {
      instance[event](...args)
    }
  }
}
</script>