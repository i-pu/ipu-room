<template lang='pug'>
  div
    v-list#chat(two-line height="50%")
      v-subheader チャット
      template(v-for="comment, i in comments")
        v-list-tile(v-if="comment.type === 'comment'" :key="comment.comment_id" avatar)
          v-list-tile-avatar
            img(:src="comment.avatar")
          v-list-tile-content
            v-list-tile-title {{ comment.text }}
            v-list-tile-sub-title {{ comment.user_name }}

    v-container(fluid grid-list-md text-xs-center)
      v-layout(row wrap)
        v-flex(d-flex xs8 sm8 md8)
          v-text-field(
            v-model="chatInput"
            label="コメント"
          )
        v-flex(d-flex xs4 sm4 md4)  
          v-btn(color="info" @click="comment") 送信
</template>

<script lang="ts">
import Vue from 'vue'
import Component from 'vue-class-component'

import { Comment } from '@/model'

@Component<Chat>({
  sockets: {
    chat (comment: Comment) {
      this.comments.push(comment)
    },
  },
})

export default class Chat extends Vue {
  private comments: Comment[] = []
  private chatInput: string = ''

  public comment () {
    // mock
    const comment: Comment = {
      type: 'comment',
      avatar: `https://cdn.vuetifyjs.com/images/lists/${1}.jpg`,
      comment_id: Math.random().toString(36),
      user_name: 'John',
      user_id: 'xxxx',
      text: this.chatInput,
      commented_at: new Date(),
    }

    // fook
    const cancelled = !this.beforeComment(comment)

    this.chatInput = ''

    if (cancelled) {
      return
    }

    if (this.$store.getters.localOnly) {
      this.comments.push(comment)
    } else {
      this.$socket.emit('chat', comment)
    }
  }

  public beforeComment (comment: Comment): boolean {
    console.log(comment)
    return true
  }
}
</script>