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
            v-btn(color="blue darken-1" flat @click="onClickCreate") 作成
</template>

<script>
export default {
  name: '',
  props: {
    userId: String
  },
  data () {
    return {
      dialog: false,
      roomNameInput: '',
      plugins: ['counter'],
      selectedPlugins: []
    }
  },
  methods: {
    onClickCreate () {
      console.log(this.roomNameInput)
      console.log(this.selectedPlugins)

      this.$socket.emit('room/create', {
        room_name: this.roomNameInput,
        plugins: this.selectedPlugins
      })
      
      this.dialog = false
      this.roomNameInput = ''
    }
  }
}
</script>