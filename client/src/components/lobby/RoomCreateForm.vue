<template lang='pug'>
  div
    v-layout(row justify-center)
      v-dialog(v-model="dialog" max-width="600px")
        template(v-slot:activator="{ on }")
          v-btn(color="success" @click="fetchPluginData" v-on="on") 部屋を作成
        v-card
          v-card-title
            span.headline 部屋を作成
          v-card-text
            v-container(grid-list-md)
              v-layout(wrap)
                v-flex(xs12 sm12)
                  v-text-field(label="部屋名" required v-model="roomNameInput")
                v-flex(xs12 sm12)
                  v-select(
                    v-model="selectedPlugins"
                    :items="pluginIds"
                    label="プラグイン"
                    multiple
                  )
                    template(v-slot:selection="{ item, index }")
                      v-chip(v-if="index === 0")
                        span {{ item }}
          v-card-actions
            v-spacer
            v-btn(color="blue darken-1" flat @click="requestCreateRoom") 作成
</template>

<script lang="ts">
import Vue from 'vue'
import Component from 'vue-class-component'
import { Prop } from 'vue-property-decorator'
import { Room } from '@/model'

@Component<RoomCreateForm>({
  sockets: {
    'room/make' (data: { room: Room }) {
      this.$emit('add', data)
    },
  },
})
export default class RoomCreateForm extends Vue {
  @Prop() public userId!: string

  private dialog: boolean = false
  private roomNameInput: string = ''
  private pluginIds: string[] = []
  private selectedPlugins: string[] = []

  private fetchPluginData () {
    this.pluginIds = [
      'counter-0123-abcdef-4567',
      'paint-xxxx-12345678'
    ]
    // TODO
    // fetch(`${process.env.VUE_APP_API_ORIGIN}/plugin`)
    //   .then((res) => res.json())
    //   .then(({ plugins }: { plugins: Array<{ id: string }>}) => {
    //     this.plugins = plugins.map((plugin) => plugin.id)
    //   })
  }

  private requestCreateRoom () {
    this.$socket.emit('room/make', {
      roomName: this.roomNameInput,
      pluginIds: this.selectedPlugins,
    })

    this.dialog = false
    this.roomNameInput = ''
  }
}
</script>