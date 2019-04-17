<template lang='pug'>
  div
    v-container(fluid grid-list-md text-xs-center)
      v-layout(row wrap)
        v-flex(xs12 sm12 md12)
          v-toolbar(dense floating)
            v-toolbar-title {{ room.name }}
            v-spacer
            v-toolbar-title お絵かき
        v-flex(d-flex xs12 sm12 md9)
          v-responsive(:aspect-ratio="16/9")
            v-card(height="100%" white)
              desk#desk
        v-flex(d-flex xs12 sm12 md3)
          v-card(white)
            chat#chat
        v-flex(d-flex xs12 sm12 md12)
          v-card(white)
            status#status
</template>

<script>
import Desk from '@/components/room/Desk'
import Chat from '@/components/room/Chat'
import Status from '@/components/room/Status'

export default {
  name: 'Room',
  components: { Desk, Chat, Status },
  data () {
    return {
      room: {
        name: 'テスト部屋'
      }
    }
  },
  methods: { }
}
</script>

<style scoped>
#desk {
  height: 100%;
}

#status {
  height: 300px;
}

v-card {
  height: 100%;
}
</style>
