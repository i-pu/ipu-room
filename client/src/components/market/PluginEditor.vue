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
    v-flex(d-flex xs12 sm12 md6)
      v-card(white flat fluid)
        v-card-title.grey--text(icon) Plugin
        component(v-if="instance" :is="instance.component")
        v-snackbar(
          v-model="snackbar"
          :timeout="2000"
        ) {{ snackbarMessage }}
</template>

<script lang="ts">
import Vue from 'vue'
import _ from 'lodash'

import Component from 'vue-class-component'
import { Prop, Watch } from 'vue-property-decorator'
import { PluginPackage, PluginComponent, Room, PluginInstance, Plugin } from '@/model'
import { boot } from '@/logic/loader'

@Component<PluginEditor>({
  sockets: {
    async 'room/make' ({ room }: { room: Room }) {
      this.room = room
      await this.refresh()
      this.$socket.emit('room/enter', { roomId: this.room.id })
    }
  },
  watch: {
    async 'innerPluginPackage.plugin.functions' () {
      await this.refresh()
    },
    async 'innerPluginPackage.plugin.template' () {
      await this.refresh()
    }
  }
})
export default class PluginEditor extends Vue {
  @Prop() public pluginPackage!: PluginPackage
  private snackbar: boolean = false
  private snackbarMessage: string = ''

  private room!: Room
  private innerPluginPackage: PluginPackage = _.clone(this.pluginPackage)
  private instance: PluginInstance | null = null

  private editableFunctions: string = this.prettifiedFunctions
  private editableTempate: string = _.clone(this.innerPluginPackage.plugin.template)

  async mounted () {
    this.$socket.emit('room/make', { roomName: '部屋', pluginIds: [ this.innerPluginPackage.meta.id ] }) 
  }

  private get prettifiedFunctions (): string {
    return JSON.stringify(this.innerPluginPackage.plugin.functions, null, "\t")
  }

  private syncFunctions = _.debounce(async (e: Event) => {
    try {
      const functions = JSON.parse((e.target as HTMLInputElement).innerHTML)
      this.innerPluginPackage.plugin.functions = functions
    } catch (e) {
      this.toast('Syntax error')
    }
  }, 1000)

  private syncTemplate = _.debounce(async (e: Event) => {
    this.innerPluginPackage.plugin.template = (e.target as HTMLInputElement).innerText
  }, 1000)

  private async refresh () {
    try {
      this.instance = await boot(this.innerPluginPackage, { room: this.room })
      this.toast('Successfully Compiled')
    } catch (error) {
      this.toast('Failed to Compile')
    }
  }

  private async toast (message: string) {
    this.snackbar = true
    this.snackbarMessage = message
  }
}
</script>

<style lang="stylus" scoped>
.editor
  height 300px
  text-align left
</style>