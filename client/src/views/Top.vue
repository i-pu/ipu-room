<template lang="pug">
  v-container(fluid grid-list-md ma-0 pa-0 text-xs-center)
    v-layout(row wrap)
      top-toolbar

      v-flex(d-flex xs12 sm12 md12)
        v-layout(align-center column justify-center)
          h1.display-3.font-weight-thin.mb-4.mt-4 ipu-room
          v-card(white)
            v-card-text
              v-layout(align-center)
                v-text-field(placeholder="ニックネーム" v-model="userName")
                v-btn(color="blue-grey" class="white--text" :disabled="userName === ''" @click="requestToLobby") ロビーへ
                  v-icon(right dark) arrow_right_alt
</template>

<script lang="ts">
import { createComponent, ref } from '@vue/composition-api'
import TopToolbar from '@/components/TopToolbar.vue'
import router from '@/router'
import store, { Session } from '@/store'
import socket from '@/socket'

const userName = ref<string>('')

socket.on('visit', ({ userId }: { userId: string }) => {
  store.dispatch('setUserId', userId)
  store.dispatch('setUserName', userName.value)
  router.push('/lobby')
})

export default createComponent({
  components: { TopToolbar },
  setup () {
    const requestToLobby = () => {
      socket.emit('visit', { userName })
    }

    return {
      userName,
      requestToLobby,
    }
  },
})
</script>

<style lang="stylus" scoped>
.v-image__image
  height: 100vh
  width auto

</style>
