<template lang="pug">
  div
    v-container(fluid grid-list-md)
      v-layout(row wrap)
        v-flex(d-flex xs12 sm12 md12)
          v-parallax(src="https://www.pakutaso.com/shared/img/thumb/YM_DSC8677_TP_V.jpg" height="200")
            v-layout(align-center column justify-center)
              h1.display-2.font-weight-thin.mb-3 Heya {{ $store.getters.localOnly ? 'Local' : '' }}
              h4.subheading Please make room

        v-flex(d-flex xs12 sm4 md4)
          v-card.elevation-0(white)
            v-card-media.mt-4.text-xs-center(height="45px")
              v-icon.brown--text(x-large) people
            v-card-title(primary-title)
              .headline(text-xs-center) 交流
            v-card-text この文章はテストです。この文章はテストですこの文章はテストですこの文章はテストですこの文章はテストですこの文章はテストですこの文章はテストです
        v-flex(d-flex xs12 sm4 md4)
          v-card.elevation-0(white)
            v-card-media.mt-4.text-xs-center(height="45px")
              v-icon.brown--text(x-large) flash_on
            v-card-title(primary-title)
              .headline(text-xs-center) リアルタイム
            v-card-text この文章はテストです。この文章はテストですこの文章はテストですこの文章はテストですこの文章はテストですこの文章はテストですこの文章はテストです
        v-flex(d-flex xs12 sm4 md4)
          v-card.elevation-0(white)
            v-card-media.mt-4.text-xs-center(height="45px")
              v-icon.brown--text(x-large) widgets
            v-card-title(primary-title)
              .headline(text-xs-center) プラグイン
            v-card-text この文章はテストです。この文章はテストですこの文章はテストですこの文章はテストですこの文章はテストですこの文章はテストですこの文章はテストです

        v-flex(d-flex xs12 sm12 md12)
          v-parallax(src="https://st2.depositphotos.com/1875497/11620/i/950/depositphotos_116200084-stock-photo-abstract-blur-sport-room.jpg" height="200")
            v-layout(align-center column justify-center)
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

<style scoped>
</style>
