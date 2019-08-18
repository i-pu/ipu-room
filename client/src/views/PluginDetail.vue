<template lang="pug">
  v-container(fluid grid-list-md text-xs-center)
    v-layout(row wrap v-if="loaded")
      v-toolbar(app)
        v-btn(icon to="/market")
          v-icon arrow_back
        v-toolbar-title.headline.text-uppercase
          span.pr-3 プラグインの詳細
        v-spacer
        PluginUploadForm(:update="true" :pluginMeta="pluginMeta")

      v-flex(xs12 d-flex)
        v-carousel(hide-delimiters height="300")
          v-carousel-item(
            v-for="src, i in pluginMeta.thumbnailUrls"
            :key="i"
            :src="src"
          )
          
      v-flex(xs12 d-flex)
        v-list(two-line subheader)
          v-subheader 基本情報
          v-list-tile
            v-list-tile-content
              v-list-tile-title パッケージ名
              v-list-tile-title {{ pluginMeta.author }}/{{ pluginMeta.name }}
          v-list-tile
            v-list-tile-content
              v-list-tile-title バージョン
              v-list-tile-sub-title {{ pluginMeta.version }}
          v-list-tile
            v-list-tile-content
              v-list-tile-title タグ
              v-list-tile-sub-title
                v-chip(
                  v-for="tag in pluginMeta.tags.split(',')"
                  label
                  color="pink"
                  text-color="white"
                )
                  v-icon(left) label
                  | {{ tag }}
          v-list-tile
            v-list-tile-content
              v-list-tile-title 説明
              v-list-tile-sub-title {{ pluginMeta.description }}
        //- PluginEditor(
        //-   v-if="loaded"
        //-   :pluginPackage="room.pluginPackages[0]"
        //-   @refresh="refresh"
        //-   @toast="toast"
        //- )

        //- v-flex(d-flex xs12 sm12 md6)
        //-   v-card(white flat fluid)
        //-     v-card-title.grey--text(icon) Plugin
        //-     component(v-if="instance" :is="instance.component")
        //-     v-snackbar(
        //-       v-model="snackbar"
        //-       :timeout="2000"
        //-     ) {{ snackbarMessage }}
</template>

<script lang="ts">
import Vue from 'vue'
import { Route } from 'vue-router'
import _ from 'lodash'
import { Component, Prop } from 'vue-property-decorator'

import { boot } from '@/logic/loader'
import { Room, PluginInstance, PluginMeta, PluginPackage } from '@/model'

import PluginEditor from '@/components/market/PluginEditor.vue'
import PluginUploadForm from '@/components/market/PluginUploadForm.vue'

@Component<PluginDetail>({
  components: { PluginEditor, PluginUploadForm },
  sockets: {
    // async 'room/create' ({ room }: { room: Room }) {
    //   console.log('[2/4] made room')
    //   this.$socket.emit('room/enter', { roomId: room.id })
    // },
    // 'room/enter' ({ room }: { room: Room }) {
    //   console.log('[3/4] enter room')
    //   this.room = room
    //   this.refresh()
    // },
    // 'room/remove' () {
    //   console.log('room removed')
    // }
  },
})
export default class PluginDetail extends Vue {
  // private pluginPackage!: PluginPackage
  private pluginMeta!: PluginMeta
  private loaded: boolean = false

  // private room!: Room
  // private instance: PluginInstance | null = null

  // private snackbar: boolean = false
  // private snackbarMessage: string = ''

  public created () {
    this.loaded = false
    console.log(`pluginId: ${this.$route.params.pluginId}`)
    fetch(`${process.env.VUE_APP_API_ORIGIN}/market/plugins/${this.$route.params.pluginId}`)
      .then((res) => res.json())
      .then((meta: PluginMeta) => {
        console.log('[1/4] fetched plugin package')
        this.pluginMeta = meta
        this.loaded = true
      })

    // this.$socket.emit('room/create', {
    //   roomName: '部屋',
    //   plugins: [ this.$route.params.pluginId ],
    // })
  }

  // beforeDestroy() {
  //   console.log('leave')
  //   this.$socket.emit('room/remove', { roomId: this.room.id })
  // }

  // private async refresh () {
  //   console.log('refresh')
  //   if (!this.room) {
  //     return
  //   }
  //   try {
  //     for (const pluginPackage of this.room.pluginPackages) {
  //       this.instance = await boot(pluginPackage, { room: this.room })
  //     }
  //     this.toast('Successfully Compiled')
  //     console.log('[4/4] refresh all plugin')
  //     this.loaded = true
  //   } catch (error) {
  //     this.toast('Failed to Compile')
  //     console.log(error)
  //   }
  // }

  // private async toast (message: string) {
  //   this.snackbar = true
  //   this.snackbarMessage = message
  // }
}
</script>
