<template lang='pug'>
  div
    v-list#chat(two-line height="50%")
      v-subheader チャット
      template(v-for="comment, i in comments")
        v-list-tile(:key="comment.comment_id" avatar)
          v-list-tile-avatar
            img(:src="comment.avatar")
          v-list-tile-content
            v-list-tile-title {{ comment.text }}
            v-list-tile-sub-title {{ comment.user_name }}

    v-form
      v-container
        v-layout
          v-flex(xs8 md8)
            v-text-field(
              v-model="chatInput"
              label="コメント"
            )
          v-flex(xs4 md4)
            v-btn(color="info" @click="comment") 送信
</template>

<script>
export default {
  name: 'Chat',
  data () {
    return {
      chatInput: '',
      comments: []
    }
  },
  sockets: {
    chat (comment) {
      this.comments.push(comment)
    }
  },
  mounted () {
    this.$socket.emit('enter_room', {
      roomId: 'chat_room'
    })
  },
  methods: {
    comment () {
      const comment = {
        avatar: `https://cdn.vuetifyjs.com/images/lists/${1}.jpg`,
        comment_id: Math.random().toString(36),
        user_name: 'John',
        user_id: 'xxxx',
        text: this.chatInput,
        commented_at: new Date()
      }

      // fook
      const cancelled = !this.beforeComment(comment)

      this.chatInput = ''

      if (cancelled) {
        return
      }

      // Local
      this.comments.push(comment)
      // this.$socket.emit('chat', comment)
    },

    beforeComment (comment) {
      console.log(comment)
      return true
    }
  }
}
</script>