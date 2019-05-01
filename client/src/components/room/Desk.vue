
<template lang="pug">
  #desk
    .plugin
      plugin
</template>

<script lang="ts">
import Vue, { VueConstructor } from 'vue'
import Component from 'vue-class-component'
import { Prop } from 'vue-property-decorator'

import { Room } from '@/model'
import { PluginManager } from '@/logic/plugin/component'
import { ROOMS_MOCK } from '@/api/mock'

const template = `
  <div>
    <p> {{ count }} </p>
    <input type="button" value="add" @click="plus()"> </input>
  </div>
`

const plugins: { [pluginName: string]: VueConstructor<Record<never, any> & Vue> } = {
  plugin: new PluginManager().component(template),
}

Vue.config.warnHandler = (err, vm, info) => {
  console.log({ err, vm, info })
}

@Component<Desk>({
  components: plugins,
  sockets: {
    'room/enter' (data) {
      // this.loadPlugin(data)
    },
  },
})
export default class Desk extends Vue {
  @Prop() public room!: Room
}
</script>