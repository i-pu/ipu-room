// ==========================
//  playing card plugin
// ========================
import { PluginMeta } from '@/model'

export default {
  id: 'playingcard-0123-abcdef-4567',
  name: 'playingcard',
  thumbnailUrls: [
    'https://www.silhouette-illust.com/wp-content/uploads/2017/03/game_cards_26725-300x300.jpg',
    'https://cdn.vuetifyjs.com/images/carousel/squirrel.jpg',
    'https://cdn.vuetifyjs.com/images/carousel/sky.jpg',
    'https://cdn.vuetifyjs.com/images/carousel/bird.jpg',
  ],
  description: 'これはプラグインですこれはプラグインですこれはプラグインです',
  author: 'wakame-tech',
  version: '0.0.1',
  tags: 'トランプ',
  content: `
<template lang="pug">
div
  vue-playing-card(v-for="sig in record.sigs" :signature="sig" :width="80")
</template>
<script>
  ({
    initialize () {
      return {
        sigs: []
      }
    },
    'join/member' (member) {
      console.log('+' + member.name)
    },
    'leave/member' (member) {
      console.log('-' + member.name)
    },
    mounted () {
      const nums = ['a', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
      const suits = ['c', 'd', 'h', 's']
      for (let i = 0; i < 4; i++) {
        this.record.sigs.push(this._.sample(nums) + this._.sample(suits))
      }
    },
  })
</script>`
} as PluginMeta