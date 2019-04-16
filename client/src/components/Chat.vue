<template lang='pug'>
  div
    v-list#chat(two-line height="50%")
      v-subheader チャット
      template(v-for="comment, i in comments")
        v-list-tile(
          :key="comment.id"
          avatar
        )
          v-list-tile-avatar
            img(:src="comment.avatar")
          v-list-tile-content
            v-list-tile-title {{ comment.content }}
            v-list-tile-sub-title {{ comment.name }}

    v-form
      v-container
        v-layout
          v-flex(xs8 md8)
            v-text-field(
              v-model="chatInput"
              label="コメント"
            )
          v-flex(xs4 md4)
            v-btn(color="info" @click="0") 送信
</template>

<script>
export default {
  name: 'Chat',
  data () {
    return {
      chatInput: '',
      comments: [...new Array(5)].map((_, i) => {
        return { 
          avatar: `https://cdn.vuetifyjs.com/images/lists/${i + 1}.jpg`,
          name: 'John',
          content: `コメント${i}`,
          id: i
        }
      })
    }
  },
  created () {},
  methods: { }
}
</script>

<style scoped>
</style>