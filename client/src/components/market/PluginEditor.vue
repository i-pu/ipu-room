<template lang="pug">
  v-layout(row wrap v-if="loaded")
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
    async 'innerPluginPackage.plugin.functions' (innerPluginPackage: PluginPackage) {
      console.log('watch')
      await this.$emit('refresh', innerPluginPackage)
    },
    async 'innerPluginPackage.plugin.template' (innerPluginPackage: PluginPackage) {
      await this.$emit('refresh', innerPluginPackage)
    },
  },
})
export default class PluginEditor extends Vue {
  @Prop() public pluginPackage!: PluginPackage

  private loaded: boolean = false
  private innerPluginPackage!: PluginPackage

  private editableFunctions: string = ''
  private editableTempate: string = ''

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

  private mounted () {
    // @ts-ignore
    Function.prototype.toJSON = Function.prototype.toString
    this.innerPluginPackage = _.clone(this.pluginPackage)
    this.editableFunctions = JSON.stringify(this.pluginPackage.plugin.functions, null, '\t')
    this.editableTempate = _.clone(this.pluginPackage.plugin.template)
    this.loaded = true
  }
}
</script>

<style lang="stylus" scoped>
.editor
  height 300px
  text-align left
</style>