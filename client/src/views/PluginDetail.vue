<template lang="pug">
  v-layout(row wrap v-if="loaded")
    v-toolbar(app)
      v-btn(icon to="/market")
        v-icon arrow_back
      v-toolbar-title.headline.text-uppercase
        span.pr-3 {{ pluginMeta.name }} の詳細
      v-spacer
    v-flex(xs12 d-flex)
      v-carousel(hide-delimiters height="300")
        v-carousel-item(
          v-for="src, i in pluginMeta.thumbnailUrls"
          :key="i"
          :src="src"
        )
    v-list(two-line subheader)
      v-subheader 基本情報
      v-list-tile(
        v-for="value, key in pluginMeta"
      )
        v-list-tile-content
          v-list-tile-title {{ key }}
          v-list-tile-sub-title(v-if="key !== 'tags'") {{ value }}
          v-list-tile-sub-title(v-else)
            v-chip(
              v-for="tag in value.split(',')"
              label
              color="pink"
              text-color="white"
            )
              v-icon(left) label
              | {{ tag }}

    //- PluginEditor(
    //-   :pluginPackage="pluginPackage"
    //-   @refresh="refresh"
    //-   @toast="toast"
    //- )

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
import { Prop } from 'vue-property-decorator'
import PluginEditor from '@/components/market/PluginEditor.vue'
import { Room, PluginInstance, PluginMeta, PluginPackage } from '../model'
import { boot } from '@/logic/loader'

@Component<PluginDetail>({
  components: { PluginEditor },
  sockets: {
    async 'room/make' ({ room }: { room: Room }) {
      console.log('[2/4] made room')
      this.$socket.emit('room/enter', { roomId: room.id })
    },
    'room/enter' ({ room }: { room: Room }) {
      console.log('[3/4] enter room')
      this.room = room
      this.refresh()
    }
  },
})
export default class PluginDetail extends Vue {
  // private pluginPackage!: PluginPackage
  private pluginMeta!: PluginMeta
  private loaded: boolean = false

  private room!: Room
  private instance: PluginInstance | null = null

  private snackbar: boolean = false
  private snackbarMessage: string = ''

  created () {
    fetch(`http://localhost:8080/api/v1/market/plugins/counter`)
      .then(res => res.json())
      .then((meta: PluginMeta) => {
        console.log('[1/4] fetched plugin package')
        this.pluginMeta = meta
        this.loaded = true
      })

    this.makeSandbox()
  }

  makeSandbox () {
    this.$socket.emit('room/make', { 
      roomName: '部屋', 
      pluginIds: [ 'counter' ] 
    })
  }

  private async refresh () {
    if (!this.room) {
      return
    }
    try {
      for (const pluginPackage of this.room.pluginPackages) {
        this.instance = await boot(pluginPackage, { room: this.room })
      }
      this.toast('Successfully Compiled')
    } catch (error) {
      this.toast('Failed to Compile')
      console.log(error)
    }
  }

  private async toast (message: string) {
    this.snackbar = true
    this.snackbarMessage = message
  }
}
</script>
