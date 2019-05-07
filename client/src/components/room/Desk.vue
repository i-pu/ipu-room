
<template lang="pug">
  #desk
    v-container(fluid grid-list-md text-xs-center)
      v-layout(row wrap)
        v-flex(d-flex xs12 sm12 md9 v-for="(plugin, index) in plugins")
          v-card(white fluid)
            component(:is="plugin")
</template>

<script lang="ts">
import Vue, { VueConstructor } from 'vue'
import { Route } from 'vue-router'
import Component from 'vue-class-component'
import { Prop } from 'vue-property-decorator'
import store from '@/store'

import { Room } from '@/model'
import { Plugin, PluginComponent } from '@/logic/plugin/component'
import { ROOMS_MOCK } from '@/api/mock'

import { Counter, counterTemplate } from '@/logic/plugin/counter'
import { Chat, chatTemplate } from '@/logic/plugin/chat'
import * as VuetifyComponents from 'vuetify/lib'

// Vue.config.warnHandler = (err, vm, info) => {
//   console.log({ err, vm, info })
// }

@Component
export default class Desk extends Vue {
  @Prop() room!: Room
  private plugins: Array<PluginComponent> = []

  mounted () {
    const addons: Record<string, any> = {}
    for (const [name, comp] of Object.entries(VuetifyComponents)) {
      if (name[0] === 'V') addons[name] = comp
    }
    this.plugins.push(Plugin.compile({ instance: new Counter(), template: counterTemplate, addons }))
    this.plugins.push(Plugin.compile({ instance: new Chat(), template: chatTemplate, addons }))
  }
}
</script>