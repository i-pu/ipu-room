<template lang="pug">
  v-container(fluid grid-list-md ma-0 pa-0 text-xs-center)
    v-layout(row wrap)
      top-toolbar

      v-flex(d-flex xs12 sm12 md12)
        v-layout(align-center column justify-center)
          v-parallax(src="https://i.imgur.com/A9c6blU.jpg")
            h1.display-3.font-weight-thin.mb-4.mt-4 ipu-room
            v-card(white)
              v-card-text
                v-layout(align-center)
                  v-text-field(placeholder="ニックネーム" v-model="userName")
                  v-btn(color="blue-grey" class="white--text" :disabled="userName === ''" @click="requestToLobby") ロビーへ
                    v-icon(right dark) arrow_right_alt
</template>

<script lang="ts">
import Vue from 'vue'
import Component from 'vue-class-component'
import TopToolbar from '@/components/TopToolbar.vue'

@Component<Top>({
  components: { TopToolbar },
  sockets: {
    /**
    *  response visit event
    *  @param userId: string
    */
    visit (data: { userId: string }) {
      this.toLobby(data)
    },
  },
})
export default class Top extends Vue {
  private userName: string = ''

  private mounted () {
    console.log(process.env)
  }

  private requestToLobby () {
    /**
     *  request visit event
     *  @param userName: string
     */
    this.$socket.emit('visit', { userName: this.userName })
  }

  private toLobby ({ userId }: { userId: string }) {
    this.$store.dispatch('setUserName', this.userName)
    this.$store.dispatch('setUserId', userId)
    this.$router.push('/lobby')
  }
}
</script>

<style lang="stylus" scoped>
.v-image__image
  height: 100vh
  width auto

</style>
