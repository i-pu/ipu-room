
<template lang="pug">
  #desk
    v-container(fluid grid-list-md text-xs-center)
      v-layout(row wrap)
        v-flex(
          d-flex xs12 sm12 md9
          v-for="{ component, config } in room.plugins"
          v-if="config.enabled"
        )
          v-card(white fluid)
            component(:is="component")
</template>

<script lang="ts">
import Vue from 'vue'
import Component from 'vue-class-component'
import { Prop } from 'vue-property-decorator'

import { Room } from '@/model'

// Vue.config.warnHandler = (err, vm, info) => {
//   console.log({ err, vm, info })
// }

@Component
export default class Desk extends Vue {
  @Prop() public room!: Room
}
</script>