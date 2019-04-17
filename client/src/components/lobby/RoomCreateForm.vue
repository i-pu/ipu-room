<template lang='pug'>
  div
    v-layout(row justify-center)
      v-dialog(v-model="dialog" persistent max-width="600px")
        template(v-slot:activator="{ on }")
          v-btn(color="success" v-on="on") 部屋を作成
        v-card
          v-card-title
            span.headline 部屋を作成
          v-card-text
            v-container(grid-list-md)
              v-layout(wrap)
                v-flex(xs12 sm6 md4)
                  v-text-field(label="部屋名" required v-model="roomNameInput")
          v-card-actions
            v-spacer
            v-btn(color="blue darken-1" flat @click="onClickCreate") 作成
</template>

<script>
export default {
  name: '',
  data () {
    return {
      dialog: false,
      roomNameInput: ''
    }
  },
  methods: {
    onClickCreate () {
      console.log(this.roomNameInput)
      // this.$emit('create', { roomName: this.roomNameInput })
      this.dialog = false
      this.roomNameInput = ''
    }
  }
}
</script>