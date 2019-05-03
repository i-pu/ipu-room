
<template lang="pug">
  #desk
    .plugin
      component(v-for="name in $store.getters.plugins" :is="name")
</template>

<script lang="ts">
import Vue, { VueConstructor } from 'vue'
import { Route } from 'vue-router'
import Component from 'vue-class-component'
import { Prop } from 'vue-property-decorator'
import store from '@/store'

import { Room } from '@/model'
import { PluginManager, PluginComponent, PPM } from '@/logic/plugin/component'
import { ROOMS_MOCK } from '@/api/mock'
import { mount } from '@vue/test-utils'

// Vue.config.warnHandler = (err, vm, info) => {
//   console.log({ err, vm, info })
// }

@Component<Desk>({
  components: store.getters.plugins,
})
export default class Desk extends Vue {
  @Prop() public room!: Room

  async beforeEnter (to: Route, from: Route, next: Function) {
    console.log('before enter')
    next()
  }
}
</script>