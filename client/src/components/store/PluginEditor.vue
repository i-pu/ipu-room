<template lang="pug">
  div
    v-container(fluid grid-list-md text-xs-center)
      v-layout(row wrap v-if="innerPluginPackage")
        v-flex(d-flex xs12 sm12 md6)
          code.blockquote.editor(@input="syncTemplate" v-text="editableTempate" contenteditable="true")
        v-flex(d-flex xs12 sm12 md6)
          code.blockquote.editor(@input="syncFunctions" v-text="editableFunctions" contenteditable="true")
      v-layout(row wrap)
        v-flex(d-flex xs12 sm12 md6 v-if="instance")
          v-card(white fluid)
            component(:is="instance.component")
</template>

<script lang="ts">
import Vue from 'vue'
import _ from 'lodash'

import Component from 'vue-class-component'
import { Prop, Watch } from 'vue-property-decorator'
import { PluginPackage, PluginComponent, Room, PluginInstance } from '@/model'
import { boot } from '@/logic/loader'

@Component<PluginEditor>({
  sockets: {
    async 'room/make' ({ room }: { room: Room }) {
      this.room = room
      this.instance = await boot(this.room.pluginPackages[0], { room: this.room })
      this.$socket.emit('room/enter', { room_id: this.room.id })
    }
  }
})
export default class PluginEditor extends Vue {
  @Prop() public pluginPackage!: PluginPackage
  private room!: Room
  private innerPluginPackage: PluginPackage | null = null
  private instance: PluginInstance | null = null

  private editableFunctions: string = ''
  private editableTempate: string = ''

  async mounted () {
    this.innerPluginPackage = _.clone(this.pluginPackage)

    this.editableTempate = _.clone(this.innerPluginPackage.plugin.template)
    this.editableFunctions = this.prettifiedFunctions

    this.$socket.emit('room/make', { name: '部屋', pluginPackages: [ this.innerPluginPackage ] }) 
  }

  private get prettifiedFunctions (): string {
    return JSON.stringify(this.innerPluginPackage!!.plugin.functions, null, "\t")
  }

  private syncFunctions (e: Event) {
    try {
      this.innerPluginPackage!!.plugin.functions = JSON.parse((e.target as HTMLInputElement).innerHTML)
    } catch (e) {
      console.log('Systax Error')
    }
  }

  private syncTemplate (e: Event) {
    this.innerPluginPackage!!.plugin.template = (e.target as HTMLInputElement).innerText
  }

  @Watch('innerPluginPackage', { deep: true })
  private reloadPlugin () {
    if (!this.room) {
      return
    }
    _.debounce(async () => {
      try {
        this.instance = await boot(this.innerPluginPackage!!, { room: this.room })
        console.log('Refreshed')
      } catch (e) {
        console.error('Some compile error occured!!')
      }
    }, 1000)()
  }
}
</script>

<style lang="stylus" scoped>
.editor
  height 300px
  text-align left
</style>