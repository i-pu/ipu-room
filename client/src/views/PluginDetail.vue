<template lang="pug">
  div
    v-container(fluid grid-list-md text-xs-center)
      v-layout(row wrap)
        v-flex(d-flex xs12 sm12 md9)
          PluginEditor(:pluginPackage="pluginPackage")
</template>

<script lang="ts">
import Vue from 'vue'
import _ from 'lodash'
import Component from 'vue-class-component'
import { Prop } from 'vue-property-decorator'
import PluginEditor from '@/components/store/PluginEditor.vue'
import { PluginPackage } from '../model'
const Counter = require('@/plugin_examples/counter')

@Component({
  components: { PluginEditor }
})
export default class PluginDetail extends Vue {
  private pluginPackage: PluginPackage = _.clone(Counter)
}
</script>
