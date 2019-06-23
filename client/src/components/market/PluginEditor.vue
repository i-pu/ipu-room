<template lang="pug">
  v-layout(row wrap v-if="innerPluginPackage")
    // template editor
    v-flex(d-flex xs12 sm12 md6)
      v-card(white flat)
        v-card-title.grey--text Template
        .editor.px-4(@input="syncTemplate" v-text="editableTempate" contenteditable="true")
    // functions editor
    v-flex(d-flex xs12 sm12 md6)
      v-card(white flat)
        v-card-title.grey--text Functions
        .editor.px-4(@input="syncFunctions" v-text="editableFunctions" contenteditable="true")
</template>

<script lang="ts">
import Vue from 'vue'
import _ from 'lodash'

import Component from 'vue-class-component'
import { Prop, Watch } from 'vue-property-decorator'
import { PluginPackage, PluginComponent, Room, PluginInstance, Plugin } from '@/model'

@Component<PluginEditor>({
  watch: {
    async 'innerPluginPackage.plugin.functions' () {
      await this.$emit('refresh', this.innerPluginPackage)
    },
    async 'innerPluginPackage.plugin.template' () {
      await this.$emit('refresh', this.innerPluginPackage)
    },
  },
})
export default class PluginEditor extends Vue {

  private get prettifiedFunctions (): string {
    return JSON.stringify(this.innerPluginPackage.plugin.functions, null, '\t')
  }
  @Prop() public pluginPackage!: PluginPackage

  private innerPluginPackage: PluginPackage = _.clone(this.pluginPackage)

  private editableFunctions: string = this.prettifiedFunctions
  private editableTempate: string = _.clone(this.innerPluginPackage.plugin.template)

  private syncFunctions = _.debounce(async (e: Event) => {
    try {
      const functions = JSON.parse((e.target as HTMLInputElement).innerHTML)
      this.innerPluginPackage.plugin.functions = functions
    } catch (e) {
      this.$emit('toast', 'Syntax error')
    }
  }, 1000)

  private syncTemplate = _.debounce(async (e: Event) => {
    this.innerPluginPackage.plugin.template = (e.target as HTMLInputElement).innerText
  }, 1000)
}
</script>

<style lang="stylus" scoped>
.editor
  height 300px
  text-align left
</style>