<template lang='pug'>
  div
    v-layout(row justify-center)
      v-dialog(v-model="dialog" max-width="600px")
        template(v-slot:activator="{ on }")
          v-btn(color="success" v-on="on") 設定
        v-card
          v-card-title
            span.headline 設定
          v-card-text
            v-form
              v-container(grid-list-md)
                v-layout(wrap)
                  v-flex(xs12)
                    h3 一般

                    v-text-field(
                      v-model="roomName"
                      :counter="12"
                      :rules="[v => !!v || '必須項目です']",
                      label="部屋名"
                      required
                    )

                    v-checkbox(
                      v-model="setting1"
                      label="設定1"
                    )

                    h3 プラグイン

                    template(v-for="{ config } in room.plugins")
                      v-switch(
                        v-model="config.enabled"
                        :label="config.name"
                        @change="onChangePluginSettings(config.name)"
                      )

                  v-flex(xs6 sm6)
                    v-select(
                      v-model="selectedPlugin"
                      :items="['counter', 'chat', 'player']"
                      label="プラグイン"
                    )
                  v-flex(xs6 sm6)
                    v-btn(color="success" block @click="addPlugin") を追加
          v-card-actions
</template>

<script lang="ts">
import Vue from 'vue'
import Component from 'vue-class-component'
import { Prop } from 'vue-property-decorator'
import { Room } from '@/model'
import { Plugin, PluginConfig } from '@/model'

import Counter, { CounterServer } from '@/plugin_examples/counter'
import YoutubePlayer, { YoutubePlayerServer } from '@/plugin_examples/youtubePlayer'
import Chat, { ChatServer } from '@/plugin_examples/chat'

@Component
export default class Settings extends Vue {
  @Prop() public room!: Room

  private dialog: boolean = false
  private roomName: string = 'ほげ'
  private setting1: boolean = false
  private addPluginDialog: boolean = false
  private selectedPlugin: string = ''

  public mounted () {
    console.log(this.room.plugins)
  }

  private addPlugin () {
    if (this.selectedPlugin === 'counter') {
      const config: PluginConfig = {
        room_id: this.room.roomId,
        plugin_id: 'counter--1',
        name: 'counter',
        enabled: true,
      }
      this.$emit('add-plugin', config, Counter)
    } else if (this.selectedPlugin === 'chat') {
      const config: PluginConfig = {
        room_id: this.room.roomId,
        plugin_id: 'chat001',
        name: 'chat',
        enabled: true,
      }
      this.$emit('add-plugin', config, Chat)
    } else {
      const config: PluginConfig = {
        room_id: this.room.roomId,
        plugin_id: 'player001',
        name: 'player',
        enabled: true,
      }
      this.$emit('add-plugin', config, YoutubePlayer)
    }
  }

  private onChangePluginSettings (pluginName: string) {
    return {}
  }
}
</script>
