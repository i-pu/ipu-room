<template lang="pug">
  div
    v-parallax(dark src="https://cdn.vuetifyjs.com/images/backgrounds/vbanner.jpg")
      v-layout(align-center column justify-center)
        h1.display-2.font-weight-thin.mb-3 Heya {{ $store.getters.localOnly ? 'Local' : '' }}
        h4.subheading Please make room

        v-spacer
        
        v-flex
          v-card(white)
            v-card-text
              v-layout(align-center)
                v-text-field(placeholder="Your name" v-model="userName")
                v-btn(color="blue-grey" class="white--text" @click="requestToLobby") Lobby
                  v-icon(right dark) arrow_right_alt
</template>

<script lang="ts">
import Vue from 'vue'
import Component from 'vue-class-component'

@Component<Top>({
  sockets: {
    visit (data: { user_id: string }) {
      this.toLobby(data)
    },
  },
})
export default class Top extends Vue {
  private userName: string = ''

  private requestToLobby () {
    if (this.$store.getters.localOnly) {
      this.toLobby({ user_id: 'random-uuid' })
    } else {
      this.$socket.emit('visit', { user_name: this.userName })
    }
  }

  private toLobby ({ user_id }: { user_id: string }) {
    this.$store.dispatch('setUserName', this.userName)
    this.$store.dispatch('setUserId', user_id)
    this.$router.push('/lobby')
  }
}
</script>