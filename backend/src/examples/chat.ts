import { PluginMeta } from '@client/model'

export default {
  id: 'chat-0123-abcdef-4567',
  name: 'チャット',
  thumbnailUrls: [
    'https://cdn3.iconfinder.com/data/icons/social-messaging-ui-color-line/254000/01-512.png',
    'https://cdn.vuetifyjs.com/images/carousel/squirrel.jpg',
    'https://cdn.vuetifyjs.com/images/carousel/sky.jpg',
    'https://cdn.vuetifyjs.com/images/carousel/bird.jpg',
  ],
  description: 'これはプラグインですこれはプラグインですこれはプラグインです',
  author: 'wakame-tech',
  version: 'v0.0.1',
  tags: 'コミュニケーション',
  content: `
<template>
<div>
      <v-list id="chat" two-line="two-line" height="50%">
        <v-subheader>チャット</v-subheader>
        <template v-for="comment, i in record.comments">
          <v-list-tile v-if="comment.type === 'comment'" :key="comment.commentId" avatar="avatar">
            <v-list-tile-avatar>
              <img :src="comment.avatar"/>
            </v-list-tile-avatar>
            <v-list-tile-content>
              <v-list-tile-title>{{ comment.text }}</v-list-tile-title>
              <v-list-tile-sub-title>{{ comment.userName }}</v-list-tile-sub-title>
            </v-list-tile-content>
          </v-list-tile>
        </template>
      </v-list>

      <v-container fluid="fluid" grid-list-md="grid-list-md" text-xs-center="text-xs-center">
        <v-layout row="row" wrap="wrap">
          <v-flex d-flex="d-flex" xs8="xs8" sm8="sm8" md8="md8">
            <v-text-field v-model="record.chatInput" label="コメント"></v-text-field>
          </v-flex>
          <v-flex d-flex="d-flex" xs4="xs4" sm4="sm4" md4="md4">
            <v-btn color="info" @click="comment(record.chatInput); record.chatInput = ''">送信</v-btn>
          </v-flex>
        </v-layout>
      </v-container>
    </div>
</template>
<script>
  ({
    initialize () {
      return {
        comments: [],
        chatInput: ''
      }
    },
    comment (text) {
      this.record.comments.push({
        type: 'comment',
        avatar: this.$me.avatarUrl,
        commentId: Math.random().toString(),
        userName: this.$me.name,
        userId: this.$me.id,
        text: text
      })
    }
  })
</script>`
} as PluginMeta
