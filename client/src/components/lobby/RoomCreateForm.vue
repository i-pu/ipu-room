<template lang='pug'>
  div
    v-layout(row justify-center)
      v-dialog(v-model="dialog" max-width="600px")
        template(v-slot:activator="{ on }")
          v-btn(color="success" v-on="on") 部屋を作成
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
                    
                    :items="plugins"
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
    'room/create' (data: { room: Room }) {
      this.$emit('create', data)
    },
  },
})
export default class RoomCreateForm extends Vue {
  @Prop() public userId!: string

  private dialog: boolean = false
  private roomNameInput: string = ''
  private plugins: string[] = ['counter']
  private selectedPlugins: string[] = []

  private requestCreateRoom () {
    if (this.$store.getters.localOnly) {
      this.$emit('create', {
        room: {
          room_name: this.roomNameInput,
          room_id: Math.random().toString(32),
          // tslint:disable:max-line-length
          thumbnail_url: 'https://public.potaufeu.asahi.com/686b-p/picture/12463073/5c4a362cea9cb2f5d90b60e2f2a6c85f.jpg',
          members: [],
          plugins: [],
        },
      })
    } else {
      this.$socket.emit('room/create', {
        room_name: this.roomNameInput,
        plugins: this.selectedPlugins,
      })
    }

    this.dialog = false
    this.roomNameInput = ''
  }
}
</script>