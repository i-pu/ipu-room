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
  version: 'v0.0.1',
  tags: 'トランプ',
  content: `
<template lang="pug">
div
  vue-playing-card(v-for="i in 4" :signature="_random()" :width="80")
</template>
<script>
  ({
    initialize () {
      return {}
    },
    'event/members' (members) {
      console.log(members)
    },
    _random () {
      const nums = ['a', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
      const suits = ['c', 'd', 'h', 's']
      return this._.sample(nums) + this._.sample(suits)
    }
  })
</script>`
} as PluginMeta