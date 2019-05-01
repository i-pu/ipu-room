<template lang="pug">
  div
    v-parallax(dark src="https://cdn.vuetifyjs.com/images/backgrounds/vbanner.jpg")
      v-layout(align-center column justify-center)
        h1.display-2.font-weight-thin.mb-3 Heya
        h4.subheading Please make room

        v-spacer
        
        v-flex
          v-card(white)
            v-card-text
              v-layout(align-center)
                v-text-field(placeholder="Your name" v-model="userName")
                v-btn(color="blue-grey" class="white--text" @click="toLobby") Lobby
                  v-icon(right dark) arrow_right_alt
</template>

<script lang="ts">
import Vue from 'vue'
import Component from 'vue-class-component'

@Component<Top>({
  props: {
  },
  sockets: {
    visit (data) {
      console.log(data)
      // TODO Vuex
      this.$router.push({
        path: `/lobby/${data.user_id}`,
        params: {
          userId: data.user_id
        }
      })
    }
  }
})
export default class Top extends Vue {
  private userName: string = ''

  toLobby () {
    this.$socket.emit('visit', { user_name: this.userName })
  }
}
</script>