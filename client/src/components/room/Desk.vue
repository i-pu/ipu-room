
<template lang="pug">
  #desk
    v-container(fluid grid-list-md text-xs-center)
      v-layout(row wrap v-if="plugins")
        v-flex(
          d-flex xs12 sm12 md9
          v-for="{ component, properties } in plugins"
        )
          v-card(white fluid)
            component(:is="component")
</template>

<script lang="ts">
import Vue from 'vue'
import Component from 'vue-class-component'
import { Prop } from 'vue-property-decorator'
import { Room } from '@/model'

@Component
export default class Desk extends Vue {
  @Prop() public plugins!: Room['plugins']
}
</script>